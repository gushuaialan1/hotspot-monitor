# PROJECT_BRIEF: Hotspot Monitor

## Background
为三个短视频账号每日提供热点筛选报告：
- **历史账号**：找能与古代历史、传统文化、名人典故结合的热点
- **情感账号**：找能触发情感共鸣、人生感悟、亲情爱情友情类的热点
- **个人智慧账号**：找能引发成长思考、职场智慧、认知提升的热点

每个方向每日筛选5篇热点，附带链接和筛选理由，生成HTML页面，早上7点定时发送。

## Data Sources (Verified)
以下数据源已通过curl验证，无需认证：

| Platform | URL | Method | Notes |
|----------|-----|--------|-------|
| 微博热搜 | `https://weibo.com/ajax/side/hotSearch` | GET JSON | 50条，含热度值 |
| 知乎热榜 | `https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50` | GET JSON | 50条，含图片和摘要 |
| 百度热搜 | `https://top.baidu.com/board?tab=realtime` | GET HTML + extract `<!--s-data-->` | 51条，需正则提取 |
| 今日头条 | `https://www.toutiao.com/hot-event/hot-board/` | GET HTML or API | 热榜数据 |
| 腾讯新闻 | `https://r.inews.qq.com/gw/event/hot_ranking_list` | GET JSON | 50条 |
| 网易新闻 | `https://gw.m.163.com/nc-main/api/v1/hqc/no-repeat-hot-list` | GET JSON | 30条 |

## Tech Stack
- Python 3.12+
- `requests` for HTTP
- `jinja2` for HTML templating
- Kimi API (via requests, NOT openai SDK) for content filtering
- Hermes `send_message` for delivery

## Architecture

```
src/
  __init__.py
  models.py        # dataclass: HotspotItem, FilteredResult
  fetchers/
    __init__.py
    base.py        # BaseFetcher ABC
    weibo.py       # WeiboHotFetcher
    zhihu.py       # ZhihuHotFetcher
    baidu.py       # BaiduHotFetcher
    toutiao.py     # ToutiaoHotFetcher
    tencent.py     # TencentNewsFetcher
    netease.py     # NeteaseNewsFetcher
  aggregator.py    # 聚合去重，生成 HotspotItem 列表
  selector.py      # LLM 筛选，输出三个方向的 top 5
  renderer.py      # Jinja2 渲染 HTML
  sender.py        # 调用 Hermes send_message (通过脚本或直接生成消息)
  config.py        # 配置类，支持环境变量
main.py            # CLI entry point
config.yaml        # 用户可配置：数据源开关、LLM参数、账号方向定义
templates/
  report.html      # Jinja2 模板
requirements.txt
```

## Deliverables

### 1. `src/models.py`
```python
@dataclass
class HotspotItem:
    title: str
    url: str
    source: str          # weibo/zhihu/baidu/etc
    hot_value: Optional[str] = None  # 热度值/排名
    excerpt: Optional[str] = None

@dataclass
class SelectedItem:
    title: str
    url: str
    source: str
    reason: str          # LLM 筛选理由
    score: int           # 1-10 匹配度
    account_type: str    # history / emotion / wisdom
```

### 2. `src/fetchers/*.py`
每个 fetcher 继承 `BaseFetcher`，实现 `fetch() -> List[HotspotItem]`。
- 统一的 headers (User-Agent, Referer)
- 超时和重试机制
- 错误处理（不要因为一个源失败导致整体崩溃）

### 3. `src/selector.py`
使用 Kimi API 进行批量筛选。

Prompt 设计要求：
- 输入：所有热点的 JSON 列表（标题、链接、来源、摘要）
- 输出：严格 JSON 格式，三个键：`history`、`emotion`、`wisdom`
- 每个方向 5 条，含 `title`、`url`、`reason`、`score`
- 如果某方向匹配不足，允许返回少于 5 条

Kimi API 调用：
```python
POST https://api.kimi.com/coding/v1/chat/completions
Headers: Authorization: Bearer <key>, User-Agent: KimiCLI/0.77
Body: {"model": "kimi-for-coding", "messages": [...], "response_format": {"type": "json_object"}}
```
API key 从环境变量 `KIMI_API_KEY` 读取。

### 4. `src/renderer.py`
Jinja2 渲染一个简洁的 HTML 报告，包含：
- 日期标题
- 三个板块，每个板块 5 条
- 每条包含：标题链接、来源、筛选理由、匹配分数
- 响应式设计，手机端友好

### 5. `main.py`
入口脚本：
```bash
python main.py --output ./output/report.html
```
流程：
1. 加载配置
2. 并行抓取所有数据源
3. 聚合去重（按 title 去重）
4. LLM 筛选
5. 渲染 HTML
6. 保存文件

### 6. `config.yaml`
```yaml
accounts:
  history:
    name: "古今结合·历史"
    description: "找能与古代历史、传统文化、名人典故结合的热点"
  emotion:
    name: "情感共鸣"
    description: "..."
  wisdom:
    name: "个人智慧"
    description: "..."

sources:
  weibo: true
  zhihu: true
  baidu: true
  toutiao: true
  tencent: true
  netease: true

llm:
  model: "kimi-for-coding"
  max_tokens: 4096
  temperature: 0.3
```

## Acceptance Criteria
- [ ] 至少3个数据源能正常抓取
- [ ] 聚合后去重正确
- [ ] LLM 筛选输出有效 JSON
- [ ] HTML 报告渲染正常
- [ ] 代码不含任何 emojis
- [ ] 错误处理健壮（单个数据源失败不影响整体）
- [ ] `python -m py_compile` 检查通过

## Notes
- 不要引入 openai/anthropic SDK，用 requests 直接调用 Kimi API
- 不要在代码中使用 emoji
- 错误处理要优雅，打印日志但不中断主流程
