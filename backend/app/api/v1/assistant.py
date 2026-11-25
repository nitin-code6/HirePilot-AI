from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import (
    ConversationSession, ConversationMessage, User, ApprovalRequest
)
from app.models.enums import ApprovalActionType, ApprovalStatus
from app.schemas.recruitment import ChatRequest, ChatResponse
from app.graph.supervisor import SupervisorOrchestrator
from app.core.deps import get_current_user

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session_id = req.session_id
    if not session_id:
        sess = ConversationSession(user_id=current_user.id, title=req.message[:50])
        db.add(sess)
        db.commit()
        db.refresh(sess)
        session_id = sess.id

    # Record User Message
    user_msg = ConversationMessage(
        session_id=session_id,
        role="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()

    # Route through LangGraph Multi-Agent Supervisor
    agent_result = SupervisorOrchestrator.execute(req.message)

    action_required = None
    if agent_result.get("requires_approval") and agent_result.get("approval_payload"):
        ap = agent_result["approval_payload"]
        approval = ApprovalRequest(
            action_type=ApprovalActionType(ap["action_type"]),
            title=ap["title"],
            description=ap["description"],
            payload=ap["payload"],
            requester_id=current_user.id,
            status=ApprovalStatus.PENDING
        )
        db.add(approval)
        db.commit()
        db.refresh(approval)
        action_required = {
            "approval_id": approval.id,
            "title": approval.title,
            "description": approval.description,
            "status": "pending"
        }

    # Record Assistant Message
    assistant_msg = ConversationMessage(
        session_id=session_id,
        role="assistant",
        content=agent_result["reply"],
        agent_name=agent_result["agent_used"],
        metadata_json=action_required
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(
        session_id=session_id,
        reply=agent_result["reply"],
        agent_used=agent_result["agent_used"],
        action_required=action_required
    )

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ConversationSession).filter(ConversationSession.user_id == current_user.id).order_by(ConversationSession.updated_at.desc()).all()

@router.get("/conversations/{conversation_id}")
def get_conversation_history(conversation_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sess = db.query(ConversationSession).filter(ConversationSession.id == conversation_id).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = db.query(ConversationMessage).filter(ConversationMessage.session_id == conversation_id).order_by(ConversationMessage.created_at.asc()).all()
    return {
        "id": sess.id,
        "title": sess.title,
        "created_at": sess.created_at,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "agent_name": m.agent_name,
                "metadata": m.metadata_json,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }
