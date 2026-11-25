import React, { useEffect, useState } from 'react';
import { Calendar as CalendarIcon, Clock, Video, User, CheckCircle2 } from 'lucide-react';
import api from '../services/api';
import { Interview } from '../types';

export const CalendarPage: React.FC = () => {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const res = await api.get('/interviews');
        setInterviews(res.data);
      } catch (err) {
        console.error('Failed to load interviews', err);
      } finally {
        setLoading(false);
      }
    };
    fetchInterviews();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Interview Calendar</h1>
        <p className="text-sm text-slate-400 mt-1">Upcoming candidate interviews, video meeting links, and feedback logs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {loading ? (
          <div className="col-span-3 text-center py-8 text-slate-500 text-sm">Loading interviews...</div>
        ) : interviews.length === 0 ? (
          <div className="col-span-3 text-center py-8 text-slate-500 text-sm">No scheduled interviews found.</div>
        ) : (
          interviews.map((iv) => (
            <div key={iv.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
              <div className="flex items-start justify-between">
                <h3 className="text-base font-semibold text-white leading-snug">{iv.title}</h3>
                <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  {iv.status}
                </span>
              </div>

              <div className="space-y-2 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <CalendarIcon className="w-3.5 h-3.5 text-slate-500" />
                  <span>{new Date(iv.scheduled_start).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  <span>{new Date(iv.scheduled_start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                {iv.meeting_link && (
                  <div className="flex items-center gap-2 text-indigo-400 font-mono">
                    <Video className="w-3.5 h-3.5 text-indigo-400" />
                    <a href={iv.meeting_link} target="_blank" rel="noreferrer" className="hover:underline truncate">
                      {iv.meeting_link}
                    </a>
                  </div>
                )}
              </div>

              {iv.notes && (
                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-300">
                  {iv.notes}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
