from __future__ import annotations

from urllib.parse import urlencode, urlparse

import httpx

from ..models import Finding
from .base import Check


PARAMS = ["next", "redirect", "url", "dest", "destination", "return"]


class Check(Check):
    id = "open-redirect"
    title = "Open Redirect"
    severity = "MEDIUM"
    cwe = "CWE-601"
    owasp = "A01:2021"
    references = ["https://owasp.org/www-community/attacks/URL_Redirector_Abuse"]

    async def run(self, target: str, client: httpx.AsyncClient):
        findings = []
        parsed = urlparse(target)
        for p in PARAMS:
            url = f"{target}?{urlencode({p: 'https://example.com'})}"
            resp = await client.get(url, allow_redirects=False)
            loc = resp.headers.get("Location", "")
            if resp.status_code in (301, 302, 303, 307, 308) and "example.com" in loc:
                findings.append(
                    Finding(
                        id=self.id,
                        title=self.title,
                        severity=self.severity,
                        cwe=self.cwe,
                        owasp=self.owasp,
                        target=url,
                        evidence={"request": f"GET {url}", "response_headers": dict(resp.headers)},
                        repro_steps=[
                            f"1. Navegar a {url}",
                            "2. Observar redirección a https://example.com",
                        ],
                        confidence=0.8,
                        status="confirmed",
                        references=self.references,
                    )
                )
        return findings
