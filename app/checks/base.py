from __future__ import annotations

from typing import List

import httpx

from ..models import Finding


class Check:
    id = "base"
    title = "Base Check"
    severity = "MEDIUM"
    cwe = ""
    owasp = ""
    references: list[str] = []

    async def run(self, target: str, client: httpx.AsyncClient) -> List[Finding]:
        raise NotImplementedError
