from collections import defaultdict
import time
from fastapi import Request, HTTPException, status
from app.core.redis import redis_client

class RateLimiter:
    """
    In-memory and Redis-backed sliding window rate limiter
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(list)

    async def check(self, identifier: str) -> bool:
        now = time.time()
        # Clean older entries
        self._requests[identifier] = [
            t for t in self._requests[identifier] if now - t < self.window_seconds
        ]
        if len(self._requests[identifier]) >= self.max_requests:
            return False
        self._requests[identifier].append(now)
        return True

rate_limiter = RateLimiter()
