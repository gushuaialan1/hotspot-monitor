import logging
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class WeiboHotFetcher(BaseFetcher):
    source_name = "weibo"

    def fetch(self) -> List[HotspotItem]:
        url = "https://weibo.com/ajax/side/hotSearch"
        resp = self._get(url, headers={"Referer": "https://weibo.com/"})
        resp.raise_for_status()
        data = resp.json()
        realtime = data.get("data", {}).get("realtime", [])

        items = []
        for entry in realtime:
            word = entry.get("word", "")
            if not word:
                continue
            hot_value = entry.get("raw_hot", "")
            items.append(
                HotspotItem(
                    title=word,
                    url=f"https://s.weibo.com/weibo?q={word}",
                    source="weibo",
                    hot_value=str(hot_value) if hot_value else None,
                )
            )
        return items
