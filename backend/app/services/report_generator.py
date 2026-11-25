from typing import Dict, Any, List

class ScreeningReportGenerator:
    @staticmethod
    def generate_html_summary(report_data: Dict[str, Any], candidate_name: str, job_title: str) -> str:
        skills = "".join([f"<li>✓ {s}</li>" for s in report_data.get("matching_skills", [])])
        missing = "".join([f"<li>✗ {s}</li>" for s in report_data.get("missing_skills", [])])
        return f"""
        <div class="screening-report">
            <h2>Screening Evaluation: {candidate_name}</h2>
            <p><strong>Position:</strong> {job_title}</p>
            <p><strong>Overall Score:</strong> {report_data.get('overall_score')}%</p>
            <h3>Matching Qualifications</h3>
            <ul>{skills}</ul>
            <h3>Identified Skill Gaps</h3>
            <ul>{missing}</ul>
            <p><strong>Assessment:</strong> {report_data.get('explanation')}</p>
        </div>
        """
