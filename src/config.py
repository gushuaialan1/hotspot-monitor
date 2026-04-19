import os
from pathlib import Path
from typing import Dict, Any

import yaml


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}

    @property
    def accounts(self) -> Dict[str, Dict[str, str]]:
        return self._data.get("accounts", {})

    @property
    def sources(self) -> Dict[str, bool]:
        return self._data.get("sources", {})

    @property
    def llm(self) -> Dict[str, Any]:
        return self._data.get("llm", {})

    def is_source_enabled(self, name: str) -> bool:
        return self.sources.get(name, False)

    @property
    def kimi_api_key(self) -> str:
        key = os.environ.get("KIMI_API_KEY", "")
        if not key:
            raise ValueError("KIMI_API_KEY environment variable not set")
        return key
