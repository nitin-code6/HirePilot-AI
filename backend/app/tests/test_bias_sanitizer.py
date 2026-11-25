import unittest
from app.services.bias_mitigation import BiasMitigationService

class TestBiasSanitizer(unittest.TestCase):
    def test_pronoun_anonymization(self):
        text = "She managed the team while he led the technical roadmap."
        cleaned = BiasMitigationService.sanitize_resume_text(text)
        self.assertNotIn("She", cleaned)
        self.assertNotIn(" he ", cleaned)
        self.assertIn("[CANDIDATE]", cleaned)

if __name__ == "__main__":
    unittest.main()
