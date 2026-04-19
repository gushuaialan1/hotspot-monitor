import logging
import os
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class ZhihuHotFetcher(BaseFetcher):
    source_name = "zhihu"

    def fetch(self) -> List[HotspotItem]:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        headers = {"Referer": "https://www.zhihu.com/"}

        cookie = os.environ.get("ZHIHU_COOKIE", "")
        if cookie:
            headers["Cookie"] = cookie

        resp = self._get(url, headers=headers)
        if resp.status_code in (401, 403):
            logger.warning(
                "Zhihu returned %s (unauthenticated). "
                "Set ZHIHU_COOKIE env var to enable Zhihu fetching.",
                resp.status_code,
            )
            return []

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
