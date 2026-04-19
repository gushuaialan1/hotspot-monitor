import logging
from typing import List

from src.fetchers.base import BaseFetcher
from src.models import HotspotItem

logger = logging.getLogger(__name__)


class ToutiaoHotFetcher(BaseFetcher):
    source_name = "toutiao"

    def fetch(self) -> List[HotspotItem]:
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        resp = self._get(url, headers={"Referer": "https://www.toutiao.com/"})
        resp.raise_for_status()
        data = resp.json()
        entries = data.get("data", [])

        items = []
        for entry in entries:
            title = entry.get("Title", "")
            if not title:
                continue
            url_val = entry.get("Url", "")
            cluster_id = entry.get("ClusterId", "")
            label = entry.get("Label", "")
            real_url = url_val or f"https://www.toutiao.com/trending/{cluster_id}/"
            items.append(
                HotspotItem(
                    title=title,
                    url=real_url,
                    source="toutiao",
                    hot_value=label or None,
                )
            )
        return items
