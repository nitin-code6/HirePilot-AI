import React, { useEffect, useState } from 'react';
import { Plus, Search, MapPin, Briefcase, ChevronRight, CheckCircle2, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Job } from '../types';

export const JobsPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await api.get(`/jobs?search=${encodeURIComponent(search)}`);
        setJobs(res.data);
      } catch (err) {
        console.error('Failed to fetch jobs', err);
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, [search]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Job Requisitions</h1>
          <p className="text-sm text-slate-400 mt-1">Manage active openings, requirements, and candidate applications</p>
        </div>
        <Link
          to="/jobs/new"
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg shadow-lg shadow-indigo-600/25 transition-all flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          <span>New Requisition</span>
        </Link>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex gap-4 items-center">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search requisitions by title or requirements..."
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Jobs List */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800">
        {loading ? (
          <div className="p-8 text-center text-sm text-slate-500">Loading requisitions...</div>
        ) : jobs.length === 0 ? (
          <div className="p-8 text-center text-sm text-slate-500">No job requisitions found matching criteria.</div>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="p-5 hover:bg-slate-800/40 transition-colors flex items-center justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center gap-3">
                  <h3 className="text-base font-semibold text-white">{job.title}</h3>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                    job.status === 'published'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                  }`}>
                    {job.status}
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <Briefcase className="w-3.5 h-3.5" />
                    {job.department || 'General'}
                  </span>
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5" />
                    {job.location}
                  </span>
                  <span>{job.applications_count || 0} Applicants</span>
                </div>
                <div className="flex gap-1.5 pt-2">
                  {(job.requirements || []).slice(0, 4).map((req, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[11px] font-medium border border-slate-700">
                      {req}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-sm font-semibold text-slate-300">{job.salary_range || 'Competitive'}</span>
                <ChevronRight className="w-5 h-5 text-slate-600" />
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
