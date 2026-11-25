import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  Send, 
  Sparkles, 
  User, 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  ArrowRight,
  ShieldAlert
} from 'lucide-react';
import api from '../services/api';
import { ChatMessage } from '../types';

export const AIAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! I am **HirePilot**, your AI recruitment co-pilot. I coordinate specialized agents for Job Creation, Resume Screening, Interview Scheduling, and HR Communications. What requisition or candidate action would you like to execute today?',
      agent_name: 'Supervisor Orchestrator',
      created_at: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');

    const newMessages: ChatMessage[] = [
      ...messages,
      { role: 'user', content: userText, created_at: new Date().toISOString() }
    ];
    setMessages(newMessages);
    setLoading(true);

    try {
      const res = await api.post('/assistant/chat', {
        session_id: sessionId,
        message: userText
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
          content: 'An error occurred while contacting the recruitment agents. Please verify connectivity.',
          agent_name: 'Error Handler',
          created_at: new Date().toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (approvalId: string) => {
    try {
      await api.post(`/approvals/${approvalId}/approve`);
      alert('Action approved and executed successfully via Human-in-the-Loop workflow.');
    } catch (err) {
      alert('Failed to process approval.');
    }
  };

  const samplePrompts = [
    "Create a Backend Developer job requisition",
    "Screen uploaded resumes for engineering qualifications",
    "Find available interview slots for next round",
    "Draft an interview invitation email",
    "Show monthly recruitment analytics overview"
  ];

  return (
    <div className="h-[calc(100vh-6rem)] flex flex-col bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
      {/* Assistant Header */}
      <div className="h-16 px-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/60 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-600/30">
            <Bot className="w-5 h-5 text-indigo-100" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white">LangGraph Multi-Agent Assistant</h2>
            <p className="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              6 Specialized Agents & FastMCP Active
            </p>
          </div>
        </div>
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
                  <div className="flex items-center gap-2 text-amber-400 text-xs font-semibold mb-2">
                    <ShieldAlert className="w-4 h-4" />
                    <span>Human Approval Required Before Execution</span>
                  </div>
                  <p className="text-xs text-slate-300 mb-3">{msg.action_required.description}</p>
                  <button
                    onClick={() => handleApprove(msg.action_required!.approval_id)}
                    className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-md shadow-emerald-600/20"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>Review & Approve Action</span>
                  </button>
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
              <span className="text-xs font-medium text-slate-500 ml-1">Supervisor routing intent...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Prompts */}
      <div className="px-6 py-2 bg-slate-900/40 border-t border-slate-800/60 overflow-x-auto flex gap-2">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => {
              setInput(p);
            }}
            className="text-[11px] whitespace-nowrap bg-slate-950 hover:bg-slate-800 text-slate-300 px-3 py-1.5 rounded-full border border-slate-800 transition-colors"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <form onSubmit={handleSend} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Instruct the recruitment supervisor (e.g. 'Create a Backend Developer job' or 'Find available slots')..."
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
