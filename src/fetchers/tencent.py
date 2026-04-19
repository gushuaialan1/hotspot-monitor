import logging
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class TencentNewsFetcher(BaseFetcher):
    source_name = "tencent"

    def fetch(self) -> List[HotspotItem]:
        url = "https://r.inews.qq.com/gw/event/hot_ranking_list"
        resp = self._get(url)
        resp.raise_for_status()
        data = resp.json()
        idlist = data.get("idlist", [])
        if not idlist:
            return []

        newslist = idlist[0].get("newslist", [])
        items = []
        for idx, entry in enumerate(newslist):
            if idx == 0:
                continue
            title = entry.get("title", "")
            if not title:
                continue
            abstract = entry.get("abstract", "")
            hot_score = ""
            hot_event = entry.get("hotEvent", {})
            if hot_event:
                hot_score = hot_event.get("hotScore", "")
            news_url = entry.get("surl", "")
            items.append(
                HotspotItem(
                    title=title,
                    url=news_url or "https://news.qq.com/",
                    source="tencent",
                    hot_value=str(hot_score) if hot_score else None,
                    excerpt=abstract or None,
                )
            )
        return items
