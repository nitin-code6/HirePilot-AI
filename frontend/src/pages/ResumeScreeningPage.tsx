import React, { useState, useEffect } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, ArrowRight, Sparkles } from 'lucide-react';
import api from '../services/api';
import { Job, ScreeningReport } from '../types';

export const ResumeScreeningPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [report, setReport] = useState<ScreeningReport | null>(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await api.get('/jobs');
        setJobs(res.data);
        if (res.data.length > 0) {
          setSelectedJobId(res.data[0].id);
        }
      } catch (err) {
        console.error('Failed to load jobs', err);
      }
    };
    fetchJobs();
  }, []);

  const handleUploadAndScreen = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !selectedJobId) return;

    setUploading(true);
    setReport(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_id', selectedJobId);

    try {
      const res = await api.post('/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      // Fetch resulting screening report
      const reportRes = await api.get(`/resumes/${res.data.id}/report`);
      setReport(reportRes.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Resume upload and screening failed.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Autonomous Resume Screening</h1>
        <p className="text-sm text-slate-400 mt-1">
          Upload PDF/DOCX resumes for deterministic requirement matching and explainable skill gap scoring
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h2 className="text-base font-semibold text-white">Upload & Screen Candidate</h2>

          <form onSubmit={handleUploadAndScreen} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Target Job Requisition
              </label>
              <select
                value={selectedJobId}
                onChange={(e) => setSelectedJobId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                {jobs.map((j) => (
                  <option key={j.id} value={j.id}>
                    {j.title} ({j.department})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Resume File (PDF / DOCX)
              </label>
              <div className="border-2 border-dashed border-slate-800 hover:border-slate-700 rounded-xl p-8 text-center transition-colors">
                <UploadCloud className="w-10 h-10 text-slate-500 mx-auto mb-2" />
                <p className="text-xs text-slate-400 mb-2">Drag and drop or select candidate resume document</p>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  required
                  onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                  className="text-xs text-slate-400 file:mr-4 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={uploading || !file}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-600/25 disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4" />
              <span>{uploading ? 'Extracting & Screening...' : 'Run Autonomous Screening'}</span>
            </button>
          </form>
        </div>

        {/* Screening Results Report Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h2 className="text-base font-semibold text-white mb-4">Qualification Matching Report</h2>

          {!report ? (
            <div className="h-64 flex flex-col items-center justify-center text-center p-6 border border-slate-800/80 rounded-xl bg-slate-950/40">
              <FileText className="w-8 h-8 text-slate-600 mb-2" />
              <p className="text-xs text-slate-500">Upload a resume to generate explainable qualification scoring.</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-slate-950 rounded-xl border border-slate-800">
                <div>
                  <span className="text-xs text-slate-400">Deterministic Match Score</span>
                  <div className="text-3xl font-extrabold text-indigo-400 mt-0.5">{report.overall_score}%</div>
                </div>
                <div className="text-right text-xs space-y-1 text-slate-400">
                  <div>Skills Match: <strong className="text-slate-200">{report.skills_score}%</strong></div>
                  <div>Experience: <strong className="text-slate-200">{report.experience_score}%</strong></div>
                  <div>Education: <strong className="text-slate-200">{report.education_score}%</strong></div>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Matching Core Skills</p>
                <div className="flex flex-wrap gap-1.5">
                  {report.matching_skills.map((s, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-medium">
                      ✓ {s}
                    </span>
                  ))}
                </div>
              </div>

              {report.missing_skills.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">Missing Requirements</p>
                  <div className="flex flex-wrap gap-1.5">
                    {report.missing_skills.map((s, i) => (
                      <span key={i} className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-medium">
                        ✗ {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-300 leading-relaxed">
                <strong className="text-indigo-400 block mb-1">Explainable AI Summary:</strong>
                {report.explanation}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
