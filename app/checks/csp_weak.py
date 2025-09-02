from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "csp-weak"
    title = "Content Security Policy missing or weak"
    severity = "MEDIUM"
    cwe = "CWE-693"
    owasp = "A05:2021"
    references = ["https://owasp.org/www-project-top-ten/2017/A5-Security_Misconfiguration"]

    async def run(self, target: str, client: httpx.AsyncClient):
        resp = await client.get(target)
        csp = resp.headers.get("Content-Security-Policy")
        if not csp or "*" in csp or "unsafe-inline" in csp:
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"csp": csp},
                    repro_steps=["1. Solicitar la página", "2. Revisar encabezado CSP"],
                    confidence=0.8,
                    status="confirmed" if not csp else "suspicious",
                    references=self.references,
                )
            ]
        return []
