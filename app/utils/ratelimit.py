from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Dict


class RateLimiter:
    def __init__(self, limit: int = 5):
        self.limit = limit
        self.locks: Dict[str, asyncio.Semaphore] = defaultdict(lambda: asyncio.Semaphore(limit))

    async def acquire(self, host: str):
        await self.locks[host].acquire()

    def release(self, host: str):
        self.locks[host].release()
