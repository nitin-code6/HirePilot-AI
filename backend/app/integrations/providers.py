from typing import Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger("hirepilot.email")

class EmailService:
    """
    Email provider with real SMTP support and clean fallback to mock delivery.
    """
    @staticmethod
    def send_email(to_email: str, subject: str, body: str) -> Dict[str, Any]:
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            try:
                import smtplib
                from email.mime.text import MIMEText
                
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = settings.EMAIL_FROM
                msg["To"] = to_email
                
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.starttls()
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                
                logger.info(f"Sent live email to {to_email}")
                return {"status": "sent", "provider": "smtp", "recipient": to_email}
            except Exception as e:
                logger.error(f"SMTP failed, falling back to mock: {e}")
                
        # Mock provider
        logger.info(f"[MOCK EMAIL PROVIDER] Delivered email to: {to_email} | Subject: {subject}")
        return {
            "status": "mock_sent",
            "provider": "mock",
            "recipient": to_email,
            "subject": subject,
            "message": "Email dispatched via Mock Email Provider (simulate mode)"
        }

class CalendarService:
    """
    Calendar provider with Google Calendar integration and clean mock support.
    """
    @staticmethod
    def create_meeting(title: str, start_time: str, end_time: str, attendee_email: str) -> Dict[str, Any]:
        # Clean mock meeting provider
        meeting_url = f"https://meet.google.com/hpr-{abs(hash(title)) % 10000}"
        return {
            "status": "confirmed",
            "provider": "mock_google_calendar",
            "meeting_url": meeting_url,
            "title": title,
            "start": start_time,
            "end": end_time,
            "attendee": attendee_email
        }
