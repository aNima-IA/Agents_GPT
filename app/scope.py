from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Iterable, List

from .models import Target


@dataclass
class Scope:
    targets: List[Target]
    include: Iterable[str] = ()
    exclude: Iterable[str] = ()

    def hosts(self) -> List[str]:
        hosts = {t.host for t in self.targets}
        hosts.update(self.include)
        hosts.difference_update(self.exclude)
        return list(hosts)

    def in_scope(self, url: str) -> bool:
        host = urlparse(url).hostname or ""
        if host in self.exclude:
            return False
        return host in self.hosts()
