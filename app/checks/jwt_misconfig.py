from __future__ import annotations

import base64
import json

import httpx

from ..models import Finding
from .base import Check


def _is_jwt(token: str) -> bool:
    return token.count(".") == 2


class Check(Check):
    id = "jwt-misconfig"
    title = "JWT misconfiguration"
    severity = "MEDIUM"
    cwe = "CWE-287"
    owasp = "A07:2021"
    references = ["https://owasp.org/www-community/vulnerabilities/JSON_Web_Token"]

    async def run(self, target: str, client: httpx.AsyncClient):
        resp = await client.get(target)
        findings = []
        tokens = []
        for cookie in resp.cookies.jar:
            if _is_jwt(cookie.value):
                tokens.append(cookie.value)
        auth = resp.headers.get("Authorization")
        if auth and _is_jwt(auth.split()[-1]):
            tokens.append(auth.split()[-1])
        for t in tokens:
            header = json.loads(base64.urlsafe_b64decode(t.split(".")[0] + "==").decode())
            alg = header.get("alg")
            if alg in ("none", "HS256"):
                findings.append(
                    Finding(
                        id=self.id,
                        title=self.title,
                        severity=self.severity,
                        cwe=self.cwe,
                        owasp=self.owasp,
                        target=target,
                        evidence={"jwt": t, "header": header},
                        repro_steps=["1. Capturar JWT", f"2. Verificar alg={alg}"],
                        confidence=0.7,
                        status="suspicious",
                        references=self.references,
                    )
                )
        return findings
