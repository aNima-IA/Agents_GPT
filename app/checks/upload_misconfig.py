from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "upload-misconfig"
    title = "Upload misconfiguration"
    severity = "MEDIUM"
    cwe = "CWE-434"
    owasp = "A08:2021"
    references = ["https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload"]

    async def run(self, target: str, client: httpx.AsyncClient):
        url = target.rstrip("/") + "/upload"
        resp = await client.options(url)
        if resp.status_code < 400 and "POST" in resp.headers.get("Allow", ""):
            return [
                Finding(
                    id=self.id,
                    title=self.title,
                    severity=self.severity,
                    cwe=self.cwe,
                    owasp=self.owasp,
                    target=url,
                    evidence={"allow": resp.headers.get("Allow")},
                    repro_steps=["1. OPTIONS", "2. Confirmar métodos permitidos"],
                    confidence=0.4,
                    status="suspicious",
                    references=self.references,
                )
            ]
        return []
