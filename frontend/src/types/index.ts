export type UserRole = 'admin' | 'hr_manager' | 'recruiter' | 'interviewer';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  company_id?: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export type JobStatus = 'draft' | 'pending_approval' | 'published' | 'closed';
export type JobType = 'full_time' | 'part_time' | 'contract' | 'internship';

export interface Job {
  id: string;
  title: string;
  department?: string;
  location: string;
  type: JobType;
  status: JobStatus;
  description: string;
  requirements: string[];
  preferred_skills: string[];
  min_experience_years: number;
  salary_range?: string;
  created_at: string;
  updated_at: string;
  applications_count?: number;
}

export interface Candidate {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  location?: string;
  current_title?: string;
  experience_years: number;
  skills: string[];
  linkedin_url?: string;
  github_url?: string;
  notes?: string;
  created_at: string;
}

export type ApplicationStage = 'applied' | 'screened' | 'shortlisted' | 'interview_scheduled' | 'offer_extended' | 'hired' | 'rejected';

export interface Application {
  id: string;
  job_id: string;
  candidate_id: string;
  stage: ApplicationStage;
  match_score?: number;
  created_at: string;
  candidate?: Candidate;
  job?: Job;
}

export interface ScreeningReport {
  id: string;
  resume_id: string;
  job_id: string;
  overall_score: number;
  skills_score: number;
  experience_score: number;
  education_score: number;
  matching_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  explanation: string;
  created_at: string;
}

export type ApprovalStatus = 'pending' | 'approved' | 'rejected' | 'failed';
export type ApprovalActionType = 'publish_job' | 'send_email' | 'schedule_interview' | 'cancel_interview' | 'stage_change';

export interface ApprovalRequest {
  id: string;
  action_type: ApprovalActionType;
  status: ApprovalStatus;
  requester_id?: string;
  reviewer_id?: string;
  title: string;
  description: string;
  payload: Record<string, any>;
  result_log?: Record<string, any>;
  rejection_reason?: string;
  created_at: string;
  updated_at: string;
}

export interface Interview {
  id: string;
  application_id: string;
  interviewer_id?: string;
  title: string;
  scheduled_start: string;
  scheduled_end: string;
  meeting_link?: string;
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled';
  notes?: string;
  created_at: string;
}

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  agent_name?: string;
  action_required?: {
    approval_id: string;
    title: string;
    description: string;
    status: string;
  };
  created_at?: string;
}
