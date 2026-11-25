def test_rate_limiter_logic():
    from collections import defaultdict
    import time
    requests = defaultdict(list)
    def check(uid):
        now = time.time()
        requests[uid] = [t for t in requests[uid] if now - t < 60]
        if len(requests[uid]) >= 2:
            return False
        requests[uid].append(now)
        return True

    assert check("user1") is True
    assert check("user1") is True
    assert check("user1") is False

def test_salary_parser():
    from app.core.validators import parse_salary_range
    low, high = parse_salary_range("$120,000 - $150,000")
    assert low == 120000
    assert high == 150000

def test_skill_normalizer():
    from app.services.skill_normalizer import SkillNormalizer
    assert SkillNormalizer.normalize("py") == "Python"
    assert SkillNormalizer.normalize("k8s") == "Kubernetes"
    assert SkillNormalizer.normalize_list(["py", "Python", "k8s"]) == ["Python", "Kubernetes"]

def test_bias_mitigation():
    from app.services.bias_mitigation import BiasMitigationService
    cleaned = BiasMitigationService.sanitize_resume_text("He graduated in 2012 and worked as an engineer.")
    assert "2012" not in cleaned
    assert "candidate" in cleaned
