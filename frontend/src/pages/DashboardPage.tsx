import React, { useEffect, useState } from 'react';
import { 
  Briefcase, 
  Users, 
  UserCheck, 
  Calendar, 
  Clock, 
  TrendingUp, 
  ArrowUpRight, 
  CheckCircle2, 
  Plus
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import api from '../services/api';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<any>({
    active_jobs: 0,
    total_candidates: 0,
    total_applications: 0,
    interviews_scheduled: 0,
  });
  const [funnel, setFunnel] = useState<any[]>([]);
  const [recentJobs, setRecentJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [overviewRes, funnelRes, jobsRes] = await Promise.all([
          api.get('/analytics/overview'),
          api.get('/analytics/funnel'),
          api.get('/jobs?limit=5')
        ]);
        setStats(overviewRes.data);
        setFunnel(funnelRes.data);
        setRecentJobs(jobsRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  const statCards = [
    { title: 'Active Jobs', value: stats.active_jobs, icon: Briefcase, color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
    { title: 'Total Talent Pool', value: stats.total_candidates, icon: Users, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    { title: 'Applications Screened', value: stats.total_applications, icon: UserCheck, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    { title: 'Interviews Scheduled', value: stats.interviews_scheduled, icon: Calendar, color: 'text-sky-400', bg: 'bg-sky-500/10' },
  ];

  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Recruitment Operations</h1>
          <p className="text-sm text-slate-400 mt-1">Real-time candidate pipeline, agent metrics and pending requisitions</p>
        </div>
        <div className="flex gap-3">
          <Link
            to="/assistant"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium rounded-lg border border-slate-700 transition-colors flex items-center gap-2"
          >
            <span>Ask AI Assistant</span>
          </Link>
          <Link
            to="/jobs/new"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg shadow-lg shadow-indigo-600/25 transition-all flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            <span>Create Requisition</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {statCards.map((card, idx) => (
          <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg shadow-black/20">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{card.title}</span>
              <div className={`p-2 rounded-lg ${card.bg}`}>
                <card.icon className={`w-4 h-4 ${card.color}`} />
              </div>
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold text-white">{card.value}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Analytics & Pipeline Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recruitment Funnel Chart */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-base font-semibold text-white">Recruitment Funnel Conversion</h2>
              <p className="text-xs text-slate-400 mt-0.5">Stage drop-off and progression metrics</p>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-full border border-indigo-500/20">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Real-time Funnel</span>
            </div>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnel}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="stage" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Priority Requisitions */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-semibold text-white">Active Requisitions</h2>
              <Link to="/jobs" className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
                <span>View all</span>
                <ArrowUpRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="space-y-3">
              {recentJobs.length === 0 ? (
                <p className="text-xs text-slate-500">No requisitions created yet.</p>
              ) : (
                recentJobs.map((job) => (
                  <div key={job.id} className="p-3 bg-slate-950/60 rounded-lg border border-slate-800/80">
                    <p className="text-sm font-medium text-slate-200 truncate">{job.title}</p>
                    <div className="flex items-center justify-between mt-2 text-xs text-slate-400">
                      <span>{job.department || 'Engineering'}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] uppercase font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                        {job.status}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="mt-6 p-3 rounded-lg bg-indigo-950/30 border border-indigo-500/20 flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-indigo-400 shrink-0" />
            <p className="text-xs text-indigo-200 leading-relaxed">
              LangGraph Multi-Agent Supervisor is actively tracking applicant pipelines and evaluating criteria.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
