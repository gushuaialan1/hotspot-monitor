#!/usr/bin/env python3
"""
Daily hotspot collection script for cronjob injection.
Outputs a text summary to stdout, which is injected into the cronjob prompt.
"""

import datetime
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, "/home/gushuaialan/hotspot-monitor")
os.chdir("/home/gushuaialan/hotspot-monitor")

# Load API key
with open("/home/gushuaialan/.openclaw/openclaw.json", encoding="utf-8") as f:
    cfg = json.load(f)
os.environ["KIMI_API_KEY"] = cfg["env"]["KIMI_API_KEY"]

from src.aggregator import aggregate
from src.config import Config
from src.fetchers import (
    BaiduHotFetcher,
    NeteaseNewsFetcher,
    TencentNewsFetcher,
    WeiboHotFetcher,
)
from src.renderer import render_report, save_report
from src.selector import select_hotspots


def main() -> int:
    fetchers = [
        WeiboHotFetcher(),
        BaiduHotFetcher(),
        TencentNewsFetcher(),
        NeteaseNewsFetcher(),
    ]
    results = [f.safe_fetch() for f in fetchers]
    aggregated = aggregate(results)

    if not aggregated:
        print("今日未能获取任何热点，请检查数据源状态。")
        return 1

    config = Config("config.yaml")
    selected = select_hotspots(aggregated, config)

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Save HTML report
    html = render_report(selected, config)
    html_path = f"output/report_{today.replace('-', '')}.html"
    save_report(html, html_path)

    # Build text summary for stdout
    lines = [f"热点筛选日报 {today}", ""]

    grouped = defaultdict(list)
    for s in selected:
        grouped[s.account_type].append(s)

    account_names = {
        "history": "古今结合·历史",
        "emotion": "情感共鸣",
        "wisdom": "个人智慧",
    }

    for key in ("history", "emotion", "wisdom"):
        items = grouped.get(key, [])
        lines.append(f"【{account_names[key]}】")
        if not items:
            lines.append("  今日暂无匹配热点")
            lines.append("")
            continue
        for idx, s in enumerate(items, 1):
            lines.append(f"{idx}. {s.title}")
            lines.append(f"   匹配度: {s.score}/10 | 理由: {s.reason}")
            lines.append(f"   链接: {s.url}")
        lines.append("")

    lines.append(f"HTML报告已保存至: {html_path}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
