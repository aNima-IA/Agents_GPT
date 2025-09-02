from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Target:
    host: str
    base_url: str
    scope_note: str | None = None


@dataclass
class Finding:
    id: str
    title: str
    severity: str
    cwe: str
    owasp: str
    target: str
    evidence: Dict[str, Any]
    repro_steps: List[str]
    confidence: float
    status: str
    references: List[str] = field(default_factory=list)
