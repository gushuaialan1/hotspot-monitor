import json
import logging
from typing import Dict, List

import requests

from src.config import Config
from src.models import HotspotItem, SelectedItem

logger = logging.getLogger(__name__)

KIMI_API_URL = "https://api.kimi.com/coding/v1/chat/completions"

SYSTEM_PROMPT = """你是一个热点内容筛选助手。你的任务是从给定热点列表中，为三个短视频账号方向各筛选最匹配的5条热点。

三个账号方向：
1. history（古今结合·历史）：找能与古代历史、传统文化、名人典故结合的热点
2. emotion（情感共鸣）：找能触发情感共鸣、人生感悟、亲情爱情友情类的热点
3. wisdom（个人智慧）：找能引发成长思考、职场智慧、认知提升的热点

输出要求：
- 严格返回JSON格式，顶层有history、emotion、wisdom三个键
- 每个键对应的值为一个数组，最多5个元素
- 每个元素包含：title（标题）、url（链接）、reason（筛选理由，50字以内）、score（匹配分数，1-10整数）
- 如果某方向匹配不足5条，允许返回少于5条，但不允许虚构不存在的热点
- 只能从输入列表中选择热点

输入格式为JSON数组，每个元素包含title、url、source、excerpt字段。"""


def _build_messages(items: List[HotspotItem]) -> List[Dict[str, str]]:
    simplified = []
    for item in items:
        simplified.append({
            "title": item.title,
            "url": item.url,
            "source": item.source,
            "excerpt": item.excerpt or "",
        })
    user_content = json.dumps(simplified, ensure_ascii=False)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def select_hotspots(items: List[HotspotItem], config: Config) -> List[SelectedItem]:
    if not items:
        logger.warning("No items to select from")
        return []

    api_key = config.kimi_api_key
    llm_cfg = config.llm
    messages = _build_messages(items)

    payload = {
        "model": llm_cfg.get("model", "kimi-for-coding"),
        "messages": messages,
        "max_tokens": llm_cfg.get("max_tokens", 4096),
        "temperature": llm_cfg.get("temperature", 0.3),
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "KimiCLI/0.77",
        "Content-Type": "application/json",
    }

    logger.info("Calling Kimi API for selection with %d items", len(items))
    resp = requests.post(
        KIMI_API_URL,
        headers=headers,
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    result = resp.json()

    content = result["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    selected = []
    for account_type in ("history", "emotion", "wisdom"):
        entries = parsed.get(account_type, [])
        if not isinstance(entries, list):
            logger.warning("Expected list for %s, got %s", account_type, type(entries))
            continue
        for entry in entries:
            title = entry.get("title", "")
            if not title:
                continue
            selected.append(
                SelectedItem(
                    title=title,
                    url=entry.get("url", ""),
                    source=entry.get("source", "unknown"),
                    reason=entry.get("reason", ""),
                    score=int(entry.get("score", 0)),
                    account_type=account_type,
                )
            )

    logger.info("Selected %d items across 3 accounts", len(selected))
    return selected
