from typing import Dict, Any

class EmailTemplates:
    @staticmethod
    def get_interview_invite_html(candidate_name: str, job_title: str, meeting_link: str) -> str:
        return f"""
        <div style="font-family: sans-serif; color: #1e293b; padding: 20px;">
            <h2>Interview Invitation: {job_title}</h2>
            <p>Dear {candidate_name},</p>
            <p>We are delighted to invite you for a technical discussion regarding the {job_title} role at HirePilot.</p>
            <p><a href="{meeting_link}" style="background-color: #4f46e5; color: white; padding: 10px 16px; text-decoration: none; border-radius: 6px;">Join Video Meeting</a></p>
            <p>Best regards,<br>Talent Acquisition Team</p>
        </div>
        """
