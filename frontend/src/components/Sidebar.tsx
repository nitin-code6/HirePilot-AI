import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Bot, 
  Briefcase, 
  Users, 
  FileCheck2, 
  Calendar, 
  CheckSquare, 
  BarChart3, 
  LogOut,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'AI Assistant', path: '/assistant', icon: Bot, badge: 'Copilot' },
    { name: 'Jobs', path: '/jobs', icon: Briefcase },
    { name: 'Candidates', path: '/candidates', icon: Users },
    { name: 'Resume Screening', path: '/screening', icon: FileCheck2 },
    { name: 'Interview Calendar', path: '/calendar', icon: Calendar },
    { name: 'Approvals', path: '/approvals', icon: CheckSquare },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between h-screen fixed left-0 top-0 text-slate-300 z-30">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 gap-3 border-b border-slate-800">
          <div className="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold shadow-lg shadow-indigo-500/30">
            <Sparkles className="w-5 h-5 text-indigo-200" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">HirePilot AI</h1>
            <p className="text-[10px] text-indigo-400 font-medium uppercase tracking-wider">Enterprise Copilot</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <item.icon className="w-4 h-4" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {item.badge}
                </span>
              )}
            </NavLink>
          ))}
        </nav>
      </div>

      {/* User Card & Logout */}
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center gap-3 mb-3 px-2">
          <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-slate-300 text-xs">
            {user?.full_name?.substring(0, 2).toUpperCase() || 'HR'}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-medium text-white truncate">{user?.full_name || 'HR Recruiter'}</p>
            <p className="text-xs text-slate-500 capitalize">{user?.role || 'Recruiter'}</p>
          </div>
        </div>
        <button
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-semibold text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors border border-rose-500/20"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};
