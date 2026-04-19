import logging
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class NeteaseNewsFetcher(BaseFetcher):
    source_name = "netease"

    def fetch(self) -> List[HotspotItem]:
        url = "https://gw.m.163.com/nc-main/api/v1/hqc/no-repeat-hot-list"
        resp = self._get(url, headers={"Referer": "https://news.163.com/"})
        resp.raise_for_status()
        data = resp.json()
        entries = data.get("data", {}).get("items", [])

        items = []
        for entry in entries:
            title = entry.get("title", "")
            if not title:
                continue
            hot_value = entry.get("hotValue", "")
            comment_count = entry.get("commentCount", "")
            url_val = entry.get("url", "")
            items.append(
                HotspotItem(
                    title=title,
                    url=url_val or "https://news.163.com/",
                    source="netease",
                    hot_value=str(hot_value) if hot_value else None,
                )
            )
        return items
