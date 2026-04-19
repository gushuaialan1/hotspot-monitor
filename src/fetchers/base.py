import logging
from abc import ABC, abstractmethod
from typing import List

import requests

from src.models import HotspotItem

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


class BaseFetcher(ABC):
    source_name: str = ""
    timeout: int = 15

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    @abstractmethod
    def fetch(self) -> List[HotspotItem]:
        pass

    def _get(self, url: str, headers: dict = None, **kwargs) -> requests.Response:
        merged_headers = dict(DEFAULT_HEADERS)
        if headers:
            merged_headers.update(headers)
        return self.session.get(
            url, headers=merged_headers, timeout=self.timeout, **kwargs
        )

    def safe_fetch(self) -> List[HotspotItem]:
        try:
            logger.info("Fetching %s", self.source_name)
            items = self.fetch()
            logger.info("Fetched %d items from %s", len(items), self.source_name)
            return items
        except Exception as e:
            logger.error("Fetcher %s failed: %s", self.source_name, e)
            return []
