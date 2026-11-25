import os
import hashlib
import re
from typing import Dict, Any, List
import pypdf

class ResumeParserService:
    @staticmethod
    def calculate_sha256(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            try:
                reader = pypdf.PdfReader(file_path)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            except Exception as e:
                text = f"Error reading PDF: {str(e)}"
        elif ext in [".docx", ".doc"]:
            try:
                import docx
                doc = docx.Document(file_path)
                for p in doc.paragraphs:
                    text += p.text + "\n"
            except Exception:
                # Fallback to binary text extraction
                with open(file_path, "rb") as f:
                    content = f.read()
                    text = content.decode("utf-8", errors="ignore")
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        return text.strip()

    @staticmethod
    def parse_information(raw_text: str) -> Dict[str, Any]:
        """
        Extract email, phone, candidate name, skills, and experience indicators.
        """
        # Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
        email = email_match.group(0).lower() if email_match else None

        # Phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)
        phone = phone_match.group(0) if phone_match else None

        # Experience years
        exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience', raw_text, re.IGNORECASE)
        experience_years = float(exp_match.group(1)) if exp_match else 2.0

        # Skill dictionary for deterministic identification
        skill_catalog = [
            "Python", "FastAPI", "Django", "Flask", "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "React", "TypeScript", "JavaScript",
            "Node.js", "GraphQL", "REST", "Git", "CI/CD", "Linux", "SQLAlchemy", "LangChain",
            "LangGraph", "Machine Learning", "PyTorch", "TensorFlow", "Tailwind CSS", "Microservices"
        ]

        found_skills = []
        for skill in skill_catalog:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, raw_text, re.IGNORECASE):
                found_skills.append(skill)

        # First line or header heuristics for candidate name
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        candidate_name = lines[0] if lines else "Applicant"
        if len(candidate_name) > 60 or "@" in candidate_name:
            candidate_name = "Candidate"

        return {
            "full_name": candidate_name,
            "email": email or "candidate@example.com",
            "phone": phone or "N/A",
            "experience_years": experience_years,
            "skills": found_skills
        }
