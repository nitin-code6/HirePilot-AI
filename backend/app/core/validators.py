import re
from typing import Optional

def validate_job_title(title: str) -> bool:
    if not title or len(title.strip()) < 3 or len(title) > 255:
        return False
    return True

def parse_salary_range(salary_str: Optional[str]):
    if not salary_str:
        return None, None
    matches = re.findall(r'\$?(\d[\d,]*)', salary_str)
    if len(matches) >= 2:
        try:
            low = int(matches[0].replace(',', ''))
            high = int(matches[1].replace(',', ''))
            return low, high
        except ValueError:
            pass
    return None, None
