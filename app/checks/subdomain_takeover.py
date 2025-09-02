from __future__ import annotations

import aiodns
from urllib.parse import urlparse

from ..models import Finding
from .base import Check

KNOWN = ["github.io", "amazonaws.com", "azurewebsites.net"]


class Check(Check):
    id = "subdomain-takeover"
    title = "Subdomain Takeover"
    severity = "MEDIUM"
    cwe = "CWE-770"
    owasp = "A05:2021"
    references = ["https://owasp.org/www-community/vulnerabilities/Unused_subdomain_takeover"]

    async def run(self, target: str, client):
        host = urlparse(target).hostname or ""
        resolver = aiodns.DNSResolver()
        try:
            ans = await resolver.query(host, "CNAME")
            cname = ans.cname.rstrip(".")
            if any(cname.endswith(k) for k in KNOWN):
                try:
                    await resolver.query(cname, "A")
                except aiodns.error.DNSError:
                    return [
                        Finding(
                            id=self.id,
                            title=self.title,
                            severity=self.severity,
                            cwe=self.cwe,
                            owasp=self.owasp,
                            target=host,
                            evidence={"cname": cname},
                            repro_steps=["1. Resolver CNAME", "2. Comprobar ausencia de registro"],
                            confidence=0.8,
                            status="suspicious",
                            references=self.references,
                        )
                    ]
        except aiodns.error.DNSError:
            return []
        return []
