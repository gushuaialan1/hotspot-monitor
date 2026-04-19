import logging
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class ZhihuHotFetcher(BaseFetcher):
    source_name = "zhihu"

    def fetch(self) -> List[HotspotItem]:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        resp = self._get(url, headers={"Referer": "https://www.zhihu.com/"})
        resp.raise_for_status()
        data = resp.json()
        entries = data.get("data", [])

        items = []
        for entry in entries:
            target = entry.get("target", {})
            title = target.get("title", "")
            if not title:
                continue
            question_id = target.get("id", "")
            excerpt = target.get("excerpt", "")
            hot_value = entry.get("detail_text", "")
            items.append(
                HotspotItem(
                    title=title,
                    url=f"https://www.zhihu.com/question/{question_id}",
                    source="zhihu",
                    hot_value=hot_value or None,
                    excerpt=excerpt or None,
                )
            )
        return items
