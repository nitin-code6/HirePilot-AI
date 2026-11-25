from typing import List, Set

class SkillNormalizer:
    SYNONYM_MAP = {
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "golang": "Go",
        "postgres": "PostgreSQL",
        "k8s": "Kubernetes",
        "reactjs": "React",
        "react.js": "React",
        "fast api": "FastAPI",
        "node": "Node.js",
        "aws cloud": "AWS"
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        s_clean = skill.strip().lower()
        return cls.SYNONYM_MAP.get(s_clean, skill.strip())

    @classmethod
    def normalize_list(cls, skills: List[str]) -> List[str]:
        seen = set()
        result = []
        for s in skills:
            norm = cls.normalize(s)
            if norm.lower() not in seen:
                seen.add(norm.lower())
                result.append(norm)
        return result
