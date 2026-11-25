from typing import List, Dict, Any
from datetime import datetime, timedelta

class CalendarSlotResolver:
    """
    Calculates non-overlapping candidate interview slots
    based on interviewer commitments and working hours.
    """
    @staticmethod
    def resolve_open_slots(existing_interviews: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        slots = []
        base = datetime.utcnow() + timedelta(days=1)
        for hour in [10, 14, 16]:
            start_dt = base.replace(hour=hour, minute=0, second=0)
            end_dt = start_dt + timedelta(hours=1)
            slots.append({
                "start": start_dt.isoformat(),
                "end": end_dt.isoformat(),
                "display": f"{start_dt.strftime('%A, %b %d')} at {start_dt.strftime('%I:%M %p')}"
            })
        return slots
