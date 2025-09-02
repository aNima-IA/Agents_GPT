from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check
from ..utils.wordlists import COMMON_PATHS


class Check(Check):
    id = "sensitive-files"
    title = "Sensitive Files Exposure"
    severity = "MEDIUM"
    cwe = "CWE-200"
    owasp = "A01:2021"
    references = ["https://owasp.org/www-community/Vulnerabilities/Information_exposure"]

    async def run(self, target: str, client: httpx.AsyncClient):
        findings = []
        base = target.rstrip("/") + "/"
        for path in [p for p in COMMON_PATHS if p not in ("robots.txt", "sitemap.xml")]:
            url = base + path
            resp = await client.get(url)
            if resp.status_code == 200 and len(resp.text) > 0:
                findings.append(
                    Finding(
                        id=self.id,
                        title=self.title,
                        severity=self.severity,
                        cwe=self.cwe,
                        owasp=self.owasp,
                        target=url,
                        evidence={"request": f"GET {url}", "hash": hash(resp.text)},
                        repro_steps=[f"1. Visitar {url}", "2. Ver contenido sensible"],
                        confidence=0.9,
                        status="confirmed",
                        references=self.references,
                    )
                )
        return findings
