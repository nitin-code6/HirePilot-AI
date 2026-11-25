import React, { useEffect, useState } from 'react';
import { Search, Mail, Phone, MapPin, Tag, Briefcase, Plus, UserPlus } from 'lucide-react';
import api from '../services/api';
import { Candidate } from '../types';

export const CandidatesPage: React.FC = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const res = await api.get(`/candidates?search=${encodeURIComponent(search)}`);
        setCandidates(res.data);
      } catch (err) {
        console.error('Failed to fetch candidates', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCandidates();
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Talent Pool</h1>
          <p className="text-sm text-slate-400 mt-1">Screened candidate profiles, skills inventories, and recruitment records</p>
        </div>
      </div>

      <div className="relative">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search candidates by name, email, or skill keywords..."
          className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {loading ? (
          <div className="col-span-3 text-center py-8 text-slate-500 text-sm">Loading talent pool...</div>
        ) : candidates.length === 0 ? (
          <div className="col-span-3 text-center py-8 text-slate-500 text-sm">No candidate profiles found.</div>
        ) : (
          candidates.map((cand) => (
            <div key={cand.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 hover:border-slate-700 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-base font-semibold text-white">{cand.full_name}</h3>
                  <p className="text-xs text-indigo-400 font-medium mt-0.5">{cand.current_title || 'Software Engineer'}</p>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {cand.experience_years} yrs exp
                </span>
              </div>

              <div className="space-y-1.5 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <Mail className="w-3.5 h-3.5 text-slate-500" />
                  <span className="truncate">{cand.email}</span>
                </div>
                {cand.phone && (
                  <div className="flex items-center gap-2">
                    <Phone className="w-3.5 h-3.5 text-slate-500" />
                    <span>{cand.phone}</span>
                  </div>
                )}
                {cand.location && (
                  <div className="flex items-center gap-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-500" />
                    <span>{cand.location}</span>
                  </div>
                )}
              </div>

              <div>
                <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Identified Skills</p>
                <div className="flex flex-wrap gap-1.5">
                  {(cand.skills || []).map((skill, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-slate-950 text-slate-300 text-[11px] font-medium border border-slate-800">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
