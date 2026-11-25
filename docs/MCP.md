# Model Context Protocol (MCP) Server

HirePilot AI exposes its core domain actions as standard MCP tools via the official Python MCP SDK:
- `job_tools`: create_job, list_jobs, get_job_details, update_job, close_job
- `candidate_tools`: create_candidate, list_candidates, get_candidate_details, update_candidate, update_application_status
- `resume_tools`: upload_resume, parse_resume, screen_candidate, get_screening_report
- `interview_tools`: get_available_slots, schedule_interview, get_interviews, cancel_interview
- `communication_tools`: draft_email, send_email, get_communication_history
- `analytics_tools`: get_hiring_statistics, get_job_analytics, get_recruitment_funnel
