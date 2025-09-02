from __future__ import annotations

import httpx

from ..models import Finding
from .base import Check


class Check(Check):
    id = "cors-misconfig"
    title = "CORS allows credentials with reflected origin"
    severity = "MEDIUM"
    cwe = "CWE-942"
    owasp = "A05:2021"
    references = ["https://owasp.org/www-project-top-ten/2021/A05-"]

    async def run(self, target: str, client: httpx.AsyncClient):
        headers = {"Origin": "https://attacker.test"}
        resp = await client.get(target, headers=headers)
        aco = resp.headers.get("Access-Control-Allow-Origin")
        acc = resp.headers.get("Access-Control-Allow-Credentials")
        if aco in ("https://attacker.test", "*") and acc == "true":
            finding = Finding(
                id=self.id,
                title=self.title,
                severity=self.severity,
                cwe=self.cwe,
                owasp=self.owasp,
                target=target,
                evidence={"request": f"GET {target}", "headers": dict(resp.headers)},
                repro_steps=[
                    "1. Enviar petición con Origin https://attacker.test",
                    "2. Observar ACAO reflejado y ACA-Credentials: true",
                ],
                confidence=0.9,
                status="confirmed",
                references=self.references,
            )
            return [finding]
        return []
