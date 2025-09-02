from __future__ import annotations

import asyncio
from typing import Any, Dict

import httpx
import structlog


log = structlog.get_logger()


def build_client(burp: Any, proxy_override: str | None = None) -> httpx.AsyncClient:
    proxies = proxy_override or (burp.proxies if burp else None)
    headers: Dict[str, str] = {}
    if burp and burp.headers:
        headers.update(burp.headers)
    if burp and burp.user_agent:
        headers["User-Agent"] = burp.user_agent
    timeout = burp.timeout if burp and burp.timeout else 10.0
    verify = burp.tls_verify if burp else True
    return httpx.AsyncClient(proxies=proxies, headers=headers, timeout=timeout, verify=verify, http2=True)


async def fetch(client: httpx.AsyncClient, url: str, method: str = "GET", **kwargs: Any) -> httpx.Response:
    log.debug("fetch", method=method, url=url)
    resp = await client.request(method, url, **kwargs)
    return resp
