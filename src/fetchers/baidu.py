import json
import logging
import re
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class BaiduHotFetcher(BaseFetcher):
    source_name = "baidu"

    def fetch(self) -> List[HotspotItem]:
        url = "https://top.baidu.com/board?tab=realtime"
        resp = self._get(url, headers={"Referer": "https://top.baidu.com/"})
        resp.raise_for_status()
        text = resp.text

        match = re.search(r"<!--s-data:(.*?)-->", text, re.DOTALL)
        if not match:
            logger.warning("Could not find s-data in Baidu response")
            return []

        raw_json = match.group(1)
        data = json.loads(raw_json)
        cards = data.get("data", {}).get("cards", [])
        if not cards:
            return []

        contents = cards[0].get("content", [])
        items = []
        for entry in contents:
            word = entry.get("word", "")
            if not word:
                continue
            raw_url = entry.get("rawUrl", "")
            hot_value = entry.get("hotScore", "")
            items.append(
                HotspotItem(
                    title=word,
                    url=raw_url or f"https://www.baidu.com/s?wd={word}",
                    source="baidu",
                    hot_value=str(hot_value) if hot_value else None,
                )
            )
        return items
