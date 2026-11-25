import unittest
from app.services.skill_normalizer import SkillNormalizer

class TestSynonyms(unittest.TestCase):
    def test_synonym_mappings(self):
        self.assertEqual(SkillNormalizer.normalize("golang"), "Go")
        self.assertEqual(SkillNormalizer.normalize("postgres"), "PostgreSQL")
        self.assertEqual(SkillNormalizer.normalize("fast api"), "FastAPI")

if __name__ == "__main__":
    unittest.main()
