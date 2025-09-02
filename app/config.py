from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
from jsonschema import Draft7Validator

from .models import Target


@dataclass
class BurpConfig:
    proxies: Dict[str, str] | None
    include: List[str]
    exclude: List[str]
    headers: Dict[str, str]
    user_agent: str | None
    timeout: float | None
    tls_verify: bool | None


def load_csv(path: Path) -> List[Target]:
    df = pd.read_csv(path)
    targets = [Target(row["host"], row["base_url"], row.get("scope_note")) for _, row in df.iterrows()]
    return targets


def load_burp(path: Path, schema_path: Path) -> BurpConfig:
    data = json.loads(Path(path).read_text())
    schema = json.loads(Path(schema_path).read_text())
    Draft7Validator(schema).validate(data)
    proxy = None
    if data.get("proxy"):
        proxy = data["proxy"].get("http")
    include = data.get("scope", {}).get("include", [])
    exclude = data.get("scope", {}).get("exclude", [])
    headers = {h["name"]: h["value"] for h in data.get("headers", [])}
    ua = data.get("user_agent")
    timeout = data.get("timeout")
    tls_verify = data.get("tls", {}).get("verify", True)
    return BurpConfig(proxy, include, exclude, headers, ua, timeout, tls_verify)
