import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { AppLayout } from './layouts/AppLayout';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { AIAssistantPage } from './pages/AIAssistantPage';
import { JobsPage } from './pages/JobsPage';
import { CreateJobPage } from './pages/CreateJobPage';
import { CandidatesPage } from './pages/CandidatesPage';
import { ResumeScreeningPage } from './pages/ResumeScreeningPage';
import { ApprovalsPage } from './pages/ApprovalsPage';
import { CalendarPage } from './pages/CalendarPage';
import { AnalyticsPage } from './pages/AnalyticsPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) {
    return <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">Loading HirePilot...</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="assistant" element={<AIAssistantPage />} />
            <Route path="jobs" element={<JobsPage />} />
            <Route path="jobs/new" element={<CreateJobPage />} />
            <Route path="candidates" element={<CandidatesPage />} />
            <Route path="screening" element={<ResumeScreeningPage />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="approvals" element={<ApprovalsPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
