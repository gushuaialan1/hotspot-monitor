from dataclasses import dataclass
from typing import Optional


@dataclass
class HotspotItem:
    title: str
    url: str
    source: str
    hot_value: Optional[str] = None
    excerpt: Optional[str] = None


@dataclass
class SelectedItem:
    title: str
    url: str
    source: str
    reason: str
    score: int
    account_type: str
