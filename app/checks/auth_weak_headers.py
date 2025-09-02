from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "auth-weak-headers"
    title = "Auth cookies missing security flags"
    severity = "MEDIUM"
    cwe = "CWE-614"
    owasp = "A05:2021"
    references = ["https://owasp.org/www-community/controls/SecureFlag"]

    async def run(self, target: str, client: httpx.AsyncClient):
        resp = await client.get(target)
        findings = []
        for c in resp.headers.get_list("set-cookie"):
            name = c.split("=")[0]
            if "session" in name.lower():
                if "httponly" not in c.lower() or "secure" not in c.lower():
                    findings.append(
                        Finding(
                            id=self.id,
                            title=self.title,
                            severity=self.severity,
                            cwe=self.cwe,
                            owasp=self.owasp,
                            target=target,
                            evidence={"cookie": c},
                            repro_steps=["1. Revisar Set-Cookie", "2. Ver flags"],
                            confidence=0.8,
                            status="confirmed",
                            references=self.references,
                        )
                    )
        return findings
