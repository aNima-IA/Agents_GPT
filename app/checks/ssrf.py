from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check

PARAMS = ["url", "image", "feed", "callback", "fetch"]


class Check(Check):
    id = "ssrf"
    title = "Server Side Request Forgery"
    severity = "MEDIUM"
    cwe = "CWE-918"
    owasp = "A10:2021"
    references = ["https://owasp.org/www-community/attacks/Server_Side_Request_Forgery"]

    def __init__(self, allow_probe: bool = False):
        self.allow_probe = allow_probe

    async def run(self, target: str, client: httpx.AsyncClient):
        if not self.allow_probe:
            return []
        findings = []
        for p in PARAMS:
            url = f"{target}?{p}=http://127.0.0.1"
            resp = await client.get(url)
            if "127.0.0.1" in resp.text or resp.status_code in (500, 400):
                findings.append(
                    Finding(
                        id=self.id,
                        title=self.title,
                        severity=self.severity,
                        cwe=self.cwe,
                        owasp=self.owasp,
                        target=url,
                        evidence={"request": url, "status": resp.status_code},
                        repro_steps=[f"1. Solicitar {url}", "2. Revisar respuesta del servidor"],
                        confidence=0.5,
                        status="suspicious",
                        references=self.references,
                    )
                )
        return findings
