import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';

export const AppLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex">
      <Sidebar />
      <main className="ml-64 flex-1 p-8 bg-slate-950 min-h-screen overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
};
