from typing import List, Dict, Any
from app.models.models import Job, Resume

class ScreeningEngine:
    """
    Deterministic qualification matcher with explainable score components.
    Never relies on protected demographic criteria.
    """
    @staticmethod
    def match_resume_to_job(resume: Resume, job: Job) -> Dict[str, Any]:
        parsed = resume.parsed_data or {}
        candidate_skills = [s.lower() for s in parsed.get("skills", [])]
        candidate_exp = float(parsed.get("experience_years", 0.0))

        job_req_skills = [s.lower() for s in (job.requirements or [])]
        job_pref_skills = [s.lower() for s in (job.preferred_skills or [])]

        # 1. Skills Matching Score (50%)
        matching_skills = []
        missing_skills = []

        for req in job_req_skills:
            if any(req in s or s in req for s in candidate_skills):
                matching_skills.append(req)
            else:
                missing_skills.append(req)

        if job_req_skills:
            skills_score = (len(matching_skills) / len(job_req_skills)) * 100.0
        else:
            skills_score = 80.0

        # Preferred skills bonus (up to 10 points)
        pref_matches = [p for p in job_pref_skills if any(p in s for s in candidate_skills)]
        if job_pref_skills:
            skills_score = min(100.0, skills_score + (len(pref_matches) / len(job_pref_skills)) * 10.0)

        # 2. Experience Score (35%)
        required_exp = float(job.min_experience_years or 0)
        if required_exp <= 0:
            exp_score = 100.0
        elif candidate_exp >= required_exp:
            exp_score = 100.0
        else:
            exp_score = max(20.0, (candidate_exp / required_exp) * 100.0)

        # 3. Education / Heuristic Score (15%)
        raw_text = (resume.raw_text or "").lower()
        if "master" in raw_text or "phd" in raw_text or "bachelor" in raw_text or "degree" in raw_text:
            edu_score = 90.0
        else:
            edu_score = 75.0

        overall_score = round(
            (skills_score * 0.50) + (exp_score * 0.35) + (edu_score * 0.15), 1
        )

        strengths = [f"Possesses {s.title()}" for s in matching_skills]
        if candidate_exp >= required_exp:
            strengths.append(f"Meets experience criteria ({candidate_exp} yrs vs {required_exp} required)")

        weaknesses = [f"Missing required skill: {s.title()}" for s in missing_skills]
        if candidate_exp < required_exp:
            weaknesses.append(f"Experience below requested: {candidate_exp} yrs vs {required_exp} required")

        explanation = (
            f"Candidate achieved an overall matching score of {overall_score}%. "
            f"Skills coverage: {round(skills_score, 1)}% ({len(matching_skills)}/{len(job_req_skills)} required skills matched). "
            f"Experience suitability: {round(exp_score, 1)}%."
        )

        return {
            "overall_score": overall_score,
            "skills_score": round(skills_score, 1),
            "experience_score": round(exp_score, 1),
            "education_score": round(edu_score, 1),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "explanation": explanation
        }
