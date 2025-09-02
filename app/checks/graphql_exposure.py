from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check

ENDPOINTS = ["/graphql", "/v3/api-docs", "/swagger.json", "/swagger-ui/"]


class Check(Check):
    id = "graphql-exposure"
    title = "GraphQL/OpenAPI Exposure"
    severity = "MEDIUM"
    cwe = "CWE-200"
    owasp = "A05:2021"
    references = ["https://graphql.org/learn/introspection/"]

    def __init__(self, allow_introspection: bool = False):
        self.allow_introspection = allow_introspection

    async def run(self, target: str, client: httpx.AsyncClient):
        base = target.rstrip("/")
        findings = []
        for ep in ENDPOINTS:
            url = base + ep
            resp = await client.get(url)
            if resp.status_code == 200:
                findings.append(
                    Finding(
                        id=self.id,
                        title=self.title,
                        severity=self.severity,
                        cwe=self.cwe,
                        owasp=self.owasp,
                        target=url,
                        evidence={"request": url, "status": resp.status_code},
                        repro_steps=[f"1. Acceder a {url}", "2. Observar esquema"],
                        confidence=0.8,
                        status="confirmed",
                        references=self.references,
                    )
                )
        return findings
