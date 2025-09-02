from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "cache-poison"
    title = "Cache Poisoning Primitives"
    severity = "MEDIUM"
    cwe = "CWE-444"
    owasp = "A05:2021"
    references = ["https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn"]

    async def run(self, target: str, client: httpx.AsyncClient):
        base = await client.get(target)
        altered = await client.get(target, headers={"X-Forwarded-Host": "evil.com"})
        if base.text != altered.text:
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"diff": True},
                    repro_steps=["1. Enviar cabecera X-Forwarded-Host", "2. Comparar respuestas"],
                    confidence=0.5,
                    status="suspicious",
                    references=self.references,
                )
            ]
        return []
