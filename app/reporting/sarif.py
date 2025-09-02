from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..models import Finding


def write(findings: List[Finding], path: Path) -> None:
    runs = []
    results = []
    for f in findings:
        results.append(
            {
                "ruleId": f.id,
                "level": f.severity.lower(),
                "message": {"text": f.title},
                "locations": [
                    {
                        "physicalLocation": {"artifactLocation": {"uri": f.target}}
                    }
                ],
            }
        )
    runs.append({"results": results})
    data = {"version": "2.1.0", "runs": runs}
    path.write_text(json.dumps(data, indent=2))
