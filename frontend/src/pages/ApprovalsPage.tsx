import React, { useEffect, useState } from 'react';
import { CheckSquare, ShieldCheck, XCircle, CheckCircle2, Clock, AlertTriangle } from 'lucide-react';
import api from '../services/api';
import { ApprovalRequest } from '../types';

export const ApprovalsPage: React.FC = () => {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchApprovals = async () => {
    try {
      const res = await api.get('/approvals');
      setApprovals(res.data);
    } catch (err) {
      console.error('Failed to fetch approvals', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  const handleApprove = async (id: string) => {
    try {
      await api.post(`/approvals/${id}/approve`);
      fetchApprovals();
    } catch (err) {
      alert('Failed to approve request.');
    }
  };

  const handleReject = async (id: string) => {
    const reason = prompt('Please provide reason for rejection:');
    if (!reason) return;
    try {
      await api.post(`/approvals/${id}/reject`, { reason });
      fetchApprovals();
    } catch (err) {
      alert('Failed to reject request.');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Human Approval Workflows</h1>
        <p className="text-sm text-slate-400 mt-1">
          Review, approve, or reject high-impact agent actions (Job publishing, candidate emails, interview invitations)
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800">
        {loading ? (
          <div className="p-8 text-center text-sm text-slate-500">Loading pending requests...</div>
        ) : approvals.length === 0 ? (
          <div className="p-8 text-center text-sm text-slate-500">No pending approval requests.</div>
        ) : (
          approvals.map((req) => (
            <div key={req.id} className="p-6 space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2.5">
                    <h3 className="text-base font-semibold text-white">{req.title}</h3>
                    <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${
                      req.status === 'approved'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : req.status === 'rejected'
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                    }`}>
                      {req.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{req.description}</p>
                </div>

                {req.status === 'pending' && (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleReject(req.id)}
                      className="px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs font-semibold border border-rose-500/30 transition-colors"
                    >
                      Reject
                    </button>
                    <button
                      onClick={() => handleApprove(req.id)}
                      className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/20 transition-all flex items-center gap-1.5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Approve & Execute</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Action Payload Preview */}
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs font-mono text-slate-400 overflow-x-auto">
                {JSON.stringify(req.payload, null, 2)}
              </div>

              {req.result_log && (
                <div className="p-2.5 bg-emerald-950/20 border border-emerald-500/20 rounded-lg text-xs text-emerald-300">
                  <strong>Execution Result:</strong> {JSON.stringify(req.result_log)}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
