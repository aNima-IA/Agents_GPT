from __future__ import annotations

import asyncio

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "rate-limit-missing"
    title = "Missing Rate Limiting"
    severity = "MEDIUM"
    cwe = "CWE-770"
    owasp = "A10:2021"
    references = ["https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks"]

    async def run(self, target: str, client: httpx.AsyncClient):
        responses = []
        for _ in range(5):
            responses.append(await client.get(target))
            await asyncio.sleep(0)
        if all(r.status_code == 200 for r in responses):
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"responses": len(responses)},
                    repro_steps=["1. Enviar varias peticiones rápidas", "2. Observar ausencia de rate limit"],
                    confidence=0.5,
                    status="suspicious",
                    references=self.references,
                )
            ]
        return []
