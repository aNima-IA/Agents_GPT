from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "dir-listing"
    title = "Directory Listing"
    severity = "MEDIUM"
    cwe = "CWE-548"
    owasp = "A05:2021"
    references = ["https://owasp.org/www-community/attacks/Directory_Listing"]

    async def run(self, target: str, client: httpx.AsyncClient):
        resp = await client.get(target)
        if "Index of /" in resp.text:
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=target,
                    evidence={"request": f"GET {target}", "snippet": resp.text[:200]},
                    repro_steps=["1. Visitar la URL", "2. Observar listado de archivos"],
                    confidence=0.9,
                    status="confirmed",
                    references=self.references,
                )
            ]
        return []
