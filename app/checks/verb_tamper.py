from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "verb-tamper"
    title = "HTTP Verb Tampering"
    severity = "MEDIUM"
    cwe = "CWE-749"
    owasp = "A05:2021"
    references = ["https://portswigger.net/web-security/methods"]

    async def run(self, target: str, client: httpx.AsyncClient):
        resp = await client.options(target)
        allow = resp.headers.get("Allow", "")
        if any(m in allow for m in ["PUT", "DELETE", "TRACE"]):
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"allow": allow},
                    repro_steps=["1. OPTIONS", "2. Revisar métodos permitidos"],
                    confidence=0.7,
                    status="confirmed",
                    references=self.references,
                )
            ]
        return []
