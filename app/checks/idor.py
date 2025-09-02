from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "idor"
    title = "IDOR/BOLA"
    severity = "MEDIUM"
    cwe = "CWE-639"
    owasp = "A01:2021"
    references = ["https://owasp.org/Top10/A01_2021-Broken_Access_Control/"]

    async def run(self, target: str, client: httpx.AsyncClient):
        url1 = f"{target}?id=1"
        url2 = f"{target}?id=2"
        r1 = await client.get(url1)
        r2 = await client.get(url2)
        if r1.status_code == 200 and r2.status_code == 200 and r1.text != r2.text:
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"request": url2, "response_snippet": r2.text[:200]},
                    repro_steps=[
                        f"1. Solicitar {url1}",
                        f"2. Solicitar {url2} y observar datos de otro usuario",
                    ],
                    confidence=0.6,
                    status="suspicious",
                    references=self.references,
                )
            ]
        return []
