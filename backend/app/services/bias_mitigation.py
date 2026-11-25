import re

class BiasMitigationService:
    """
    Strips demographic indicators (e.g., age, gendered pronouns, graduation years)
    prior to screening to ensure unbiased candidate qualification scoring.
    """
    @staticmethod
    def sanitize_resume_text(raw_text: str) -> str:
        # Mask graduation years older than 5 years to reduce age proxy bias
        cleaned = re.sub(r'\b(19\d{2}|20[0-1]\d)\b', '[YEAR]', raw_text)
        # Normalize gender pronouns to neutral candidate reference
        cleaned = re.sub(r'\b(he|she|him|her|his|hers)\b', '[CANDIDATE]', cleaned, flags=re.IGNORECASE)
        return cleaned
