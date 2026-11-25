import unittest
from app.services.resume_parser import ResumeParserService

class TestResumeDedup(unittest.TestCase):
    def test_sha256_reproducibility(self):
        data = b"Sample candidate resume content"
        hash1 = ResumeParserService.calculate_sha256(data)
        hash2 = ResumeParserService.calculate_sha256(data)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

if __name__ == "__main__":
    unittest.main()
