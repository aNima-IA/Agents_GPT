from __future__ import annotations

from typing import Dict, Tuple


class HTTPCache:
    def __init__(self):
        self.storage: Dict[str, Tuple[str | None, str | None]] = {}

    def get_headers(self, url: str):
        etag, modified = self.storage.get(url, (None, None))
        headers = {}
        if etag:
            headers["If-None-Match"] = etag
        if modified:
            headers["If-Modified-Since"] = modified
        return headers

    def update(self, url: str, headers):
        etag = headers.get("ETag")
        modified = headers.get("Last-Modified")
        if etag or modified:
            self.storage[url] = (etag, modified)
