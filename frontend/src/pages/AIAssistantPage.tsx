import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  Send, 
  Sparkles, 
  User, 
  CheckCircle, 
  ArrowRight,
  ShieldAlert,
  Briefcase,
  FileCheck,
  Users,
  Calendar,
  Mail,
  Check
} from 'lucide-react';
import api from '../services/api';
import { ChatMessage } from '../types';

export const AIAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! I am **HirePilot**, your AI recruitment co-pilot. I coordinate specialized agents for Job Creation, Resume Screening, Candidate Management, Interview Scheduling, and Email Communications.\n\nClick any quick scenario below or type an instruction.',
      agent_name: 'Supervisor Orchestrator',
      created_at: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [approvedActionId, setApprovedActionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendPromptText = async (textToSend: string) => {
    if (!textToSend.trim() || loading) return;

    const newMessages: ChatMessage[] = [
      ...messages,
      { role: 'user', content: textToSend, created_at: new Date().toISOString() }
    ];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/assistant/chat', {
        session_id: sessionId,
        message: textToSend
      });
      setSessionId(res.data.session_id);

      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: res.data.reply,
          agent_name: res.data.agent_used,
          action_required: res.data.action_required,
          created_at: new Date().toISOString()
        }
      ]);
    } catch (err) {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'An error occurred while contacting the recruitment agents. Please verify backend connectivity.',
          agent_name: 'Error Handler',
          created_at: new Date().toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    sendPromptText(input);
  };

  const handleApprove = async (approvalId: string) => {
    try {
      await api.post(`/approvals/${approvalId}/approve`);
      setApprovedActionId(approvalId);
      // Append confirmation
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: '✓ **Action Approved & Executed Successfully!** The database record and external provider have been updated.',
          agent_name: 'Approval Supervisor',
          created_at: new Date().toISOString()
        }
      ]);
    } catch (err) {
      alert('Failed to process approval.');
    }
  };

  // 5 Scenarios mapped directly to Part 3 requirements
  const workflowScenarios = [
    {
      title: "1. Create Job",
      icon: Briefcase,
      color: "border-indigo-500/40 text-indigo-300 bg-indigo-500/10 hover:bg-indigo-500/20",
      prompt: "Create a job opening for a Backend Developer with 2 years of experience and skills in Python, FastAPI and PostgreSQL."
    },
    {
      title: "2. Resume Screening",
      icon: FileCheck,
      color: "border-emerald-500/40 text-emerald-300 bg-emerald-500/10 hover:bg-emerald-500/20",
      prompt: "Find the best candidates for the Backend Developer position."
    },
    {
      title: "3. Shortlisted Candidates",
      icon: Users,
      color: "border-sky-500/40 text-sky-300 bg-sky-500/10 hover:bg-sky-500/20",
      prompt: "Show all shortlisted candidates."
    },
    {
      title: "4. Schedule Interviews",
      icon: Calendar,
      color: "border-amber-500/40 text-amber-300 bg-amber-500/10 hover:bg-amber-500/20",
      prompt: "Prepare interviews for the top three candidates."
    },
    {
      title: "5. Email Invites",
      icon: Mail,
      color: "border-rose-500/40 text-rose-300 bg-rose-500/10 hover:bg-rose-500/20",
      prompt: "Draft interview invitations for the shortlisted candidates."
    }
  ];

  return (
    <div className="h-[calc(100vh-6rem)] flex flex-col bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
      {/* Header */}
      <div className="h-16 px-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/80 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-600/30">
            <Bot className="w-5 h-5 text-indigo-100" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white">LangGraph Multi-Agent Recruiter</h2>
            <p className="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              6 Specialized Agents Connected to FastMCP Client
            </p>
          </div>
        </div>
      </div>

      {/* Scenario Quick-Bar */}
      <div className="p-3 bg-slate-950/70 border-b border-slate-800 flex items-center gap-2 overflow-x-auto">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider pl-2 shrink-0">Quick Workflows:</span>
        {workflowScenarios.map((sc, idx) => (
          <button
            key={idx}
            onClick={() => sendPromptText(sc.prompt)}
            className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition-all flex items-center gap-1.5 shrink-0 ${sc.color}`}
          >
            <sc.icon className="w-3.5 h-3.5" />
            <span>{sc.title}</span>
          </button>
        ))}
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role !== 'user' && (
              <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400">
                <Sparkles className="w-4 h-4" />
              </div>
            )}

            <div className={`max-w-2xl rounded-2xl px-5 py-4 text-sm leading-relaxed ${
              msg.role === 'user'
                ? 'bg-indigo-600 text-white rounded-br-none shadow-md shadow-indigo-600/20'
                : 'bg-slate-950/80 border border-slate-800 text-slate-200 rounded-bl-none shadow-md'
            }`}>
              {msg.agent_name && (
                <div className="flex items-center gap-2 mb-2 pb-1.5 border-b border-slate-800">
                  <span className="text-[11px] font-semibold tracking-wide uppercase text-indigo-400">
                    {msg.agent_name}
                  </span>
                </div>
              )}

              <div className="whitespace-pre-wrap">{msg.content}</div>

              {/* Action Approval Card */}
              {msg.action_required && (
                <div className="mt-4 p-4 rounded-xl bg-slate-900 border border-amber-500/30">
                  <div className="flex items-center gap-2 text-amber-400 text-xs font-semibold mb-1.5">
                    <ShieldAlert className="w-4 h-4" />
                    <span>Human Approval Required Before Execution</span>
                  </div>
                  <p className="text-xs text-slate-300 mb-3">{msg.action_required.description}</p>
                  
                  {approvedActionId === msg.action_required.approval_id ? (
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20">
                      <Check className="w-3.5 h-3.5" />
                      <span>Approved & Executed</span>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleApprove(msg.action_required!.approval_id)}
                      className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all flex items-center gap-1.5 shadow-md shadow-emerald-600/20"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Review & Approve Action</span>
                    </button>
                  )}
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 text-slate-300">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400">
              <Sparkles className="w-4 h-4" />
            </div>
            <div className="bg-slate-950/80 border border-slate-800 rounded-2xl rounded-bl-none px-5 py-3 text-sm text-slate-400 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:0.4s]" />
              <span className="text-xs font-medium text-slate-500 ml-1">Supervisor invoking agent & MCP tools...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <form onSubmit={handleSend} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your recruitment instruction or click one of the quick workflows above..."
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium transition-all shadow-lg shadow-indigo-600/25 disabled:opacity-50 flex items-center gap-2"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
