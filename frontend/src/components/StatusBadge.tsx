import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const s = status.toLowerCase();
  let colorStyles = 'bg-slate-800 text-slate-300 border-slate-700';

  if (s === 'published' || s === 'approved' || s === 'hired') {
    colorStyles = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
  } else if (s === 'pending' || s === 'pending_approval' || s === 'screened') {
    colorStyles = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  } else if (s === 'rejected' || s === 'closed' || s === 'failed') {
    colorStyles = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
  } else if (s === 'shortlisted' || s === 'interview_scheduled') {
    colorStyles = 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
  }

  return (
    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${colorStyles}`}>
      {status.replace('_', ' ')}
    </span>
  );
};
