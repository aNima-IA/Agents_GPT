from __future__ import annotations

import httpx
import structlog

from .http import fetch
from .utils import wordlists

log = structlog.get_logger()


async def fingerprint(client: httpx.AsyncClient, base_url: str) -> dict:
    resp = await fetch(client, base_url)
    headers = dict(resp.headers)
    return {"status": resp.status_code, "headers": headers}


async def discover(client: httpx.AsyncClient, base_url: str) -> list[str]:
    found = []
    for path in wordlists.COMMON_PATHS:
        url = base_url.rstrip("/") + "/" + path
        try:
            resp = await fetch(client, url, method="HEAD")
            if resp.status_code < 400:
                found.append(url)
        except httpx.HTTPError:
            continue
    return found
