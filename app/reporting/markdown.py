from __future__ import annotations

from pathlib import Path
from typing import List

from ..models import Finding

HEADER = """# BBScan Report

> Escaneo realizado con consentimiento explícito. Utilizar únicamente en entornos autorizados.

| ID | Target | Severidad | Título |
|----|--------|-----------|--------|
"""


def write(findings: List[Finding], path: Path) -> None:
    lines = [HEADER]
    for f in findings:
        lines.append(f"| {f.id} | {f.target} | {f.severity} | {f.title} |")
    path.write_text("\n".join(lines))
