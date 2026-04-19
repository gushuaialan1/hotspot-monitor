import argparse
import concurrent.futures
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.aggregator import aggregate
from src.config import Config
from src.fetchers import (
    BaiduHotFetcher,
    NeteaseNewsFetcher,
    TencentNewsFetcher,
    ToutiaoHotFetcher,
    WeiboHotFetcher,
    ZhihuHotFetcher,
)
from src.models import HotspotItem, SelectedItem
from src.renderer import render_report, save_report
from src.selector import select_hotspots
from src.sender import send_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

FETCHER_MAP = {
    "weibo": WeiboHotFetcher,
    "zhihu": ZhihuHotFetcher,
    "baidu": BaiduHotFetcher,
    "toutiao": ToutiaoHotFetcher,
    "tencent": TencentNewsFetcher,
    "netease": NeteaseNewsFetcher,
}


def run_fetchers(config: Config) -> list[list[HotspotItem]]:
    enabled = [name for name, cls in FETCHER_MAP.items() if config.is_source_enabled(name)]
    results: list[list[HotspotItem]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(enabled)) as executor:
        futures = {}
        for name in enabled:
            fetcher = FETCHER_MAP[name]()
            futures[executor.submit(fetcher.safe_fetch)] = name

        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                items = future.result()
                results.append(items)
            except Exception as e:
                logger.error("Unexpected error from %s: %s", name, e)
                results.append([])
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Hotspot Monitor")
    parser.add_argument("--output", default="./output/report.html", help="Output HTML path")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--no-send", action="store_true", help="Skip sending report")
    args = parser.parse_args()

    config = Config(args.config)
    logger.info("Starting hotspot monitor with sources: %s", list(config.sources.keys()))

    results = run_fetchers(config)
    aggregated = aggregate(results)

    if not aggregated:
        logger.error("No hotspots fetched from any source")
        return 1

    try:
        selected = select_hotspots(aggregated, config)
    except Exception as e:
        logger.error("LLM selection failed: %s", e)
        return 1

    if not selected:
        logger.warning("No hotspots selected")

    html = render_report(selected, config)
    save_report(html, args.output)
    logger.info("Report saved to %s", args.output)

    if not args.no_send:
        send_report(args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
