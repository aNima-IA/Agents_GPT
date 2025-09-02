from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

import structlog
import typer

from . import config
from .checks import ALL_CHECKS, SSRFCheck, GraphQLCheck
from .http import build_client
from .models import Finding
from .reporting import json as json_report, markdown, sarif as sarif_report
from .scope import Scope

app = typer.Typer()
log = structlog.get_logger()


@app.command()
def run(
    in_scope: Path = typer.Option(..., help="CSV con objetivos"),
    burp: Path = typer.Option(..., help="Burp project JSON"),
    out: Path = typer.Option(Path("out")),
    concurrency: int = 20,
    timeout: int = 8,
    severity_min: str = "MEDIUM",
    dry_run: bool = False,
    include: str = "",
    exclude: str = "",
    sarif: bool = False,
    allow_ssrf_probe: bool = False,
    allow_graphql_introspection: bool = False,
    proxy: str | None = None,
):
    """Run scan"""

    targets = config.load_csv(in_scope)
    burp_cfg = config.load_burp(burp, Path("schemas/burp_project.schema.json"))
    scope = Scope(targets, include.split(",") if include else [], exclude.split(",") if exclude else [])

    for check in ALL_CHECKS:
        if isinstance(check, SSRFCheck):
            check.allow_probe = allow_ssrf_probe
        if isinstance(check, GraphQLCheck):
            check.allow_introspection = allow_graphql_introspection

    async def _run():
        out.mkdir(parents=True, exist_ok=True)
        client = build_client(burp_cfg, proxy_override=proxy)
        findings: List[Finding] = []
        async with client:
            for t in scope.targets:
                base = t.base_url
                for check in ALL_CHECKS:
                    if dry_run:
                        continue
                    try:
                        res = await check.run(base, client)
                        findings.extend(res)
                    except Exception as exc:  # pragma: no cover
                        log.error("check_error", check=check.id, error=str(exc))
        json_report.write(findings, out / "findings.json")
        markdown.write(findings, out / "REPORT.md")
        if sarif:
            sarif_report.write(findings, out / "findings.sarif")

    asyncio.run(_run())


if __name__ == "__main__":
    app()
