import logging
from typing import Dict, List

from src.models import HotspotItem

logger = logging.getLogger(__name__)


def aggregate(items_list: List[List[HotspotItem]]) -> List[HotspotItem]:
    all_items = []
    for items in items_list:
        all_items.extend(items)

    seen: Dict[str, HotspotItem] = {}
    for item in all_items:
        key = item.title.strip()
        if not key:
            continue
        if key in seen:
            existing = seen[key]
            if item.hot_value and not existing.hot_value:
                seen[key] = item
            elif item.excerpt and not existing.excerpt:
                seen[key] = item
        else:
            seen[key] = item

    deduped = list(seen.values())
    logger.info("Aggregated %d items into %d unique", len(all_items), len(deduped))
    return deduped
