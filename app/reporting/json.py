from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..models import Finding


def write(findings: List[Finding], path: Path) -> None:
    data = [f.__dict__ for f in findings]
    path.write_text(json.dumps(data, indent=2))
