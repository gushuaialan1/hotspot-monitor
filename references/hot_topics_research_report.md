# 中国实时热点数据源与API调研报告

> 调研时间: 2026-04-19  
> 用途: 热点监控与内容筛选系统（历史/情感/个人智慧方向）  
> 目标: 每天早上获取热点新闻，通过LLM筛选适合内容

---

## 一、微博热搜 / 知乎热榜 / 百度热搜

### 1.1 微博热搜 ⭐推荐

| 项目 | 详情 |
|------|------|
| **API地址** | `https://weibo.com/ajax/side/hotSearch` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | JSON |
| **数据量** | 约50条 |
| **更新频率** | 实时（每分钟） |
| **访问方式** | 直接API调用 |

**验证状态**: ✅ 已验证（2026-04-19），返回50条实时热搜

**请求示例**:
```bash
curl -H "User-Agent: Mozilla/5.0" \
     -H "Referer: https://weibo.com/" \
     "https://weibo.com/ajax/side/hotSearch"
```

**关键字段**:
- `word`: 热搜词
- `word_scheme`: 话题标签
- `mid`: 微博ID
- `onboard_time`: 上榜时间戳

**限制条件**:
- 需要设置合理的User-Agent和Referer
- 频率过高可能触发反爬
- 建议缓存60分钟

---

### 1.2 知乎热榜 ⭐推荐

| 项目 | 详情 |
|------|------|
| **API地址** | `https://api.zhihu.com/topstory/hot-lists/total?limit=50` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证（可选Cookie增强） |
| **返回格式** | JSON |
| **数据量** | 50条 |
| **更新频率** | 实时 |
| **访问方式** | 直接API调用 |

**验证状态**: ✅ 已验证（2026-04-19），返回50条热榜问题

**请求示例**:
```bash
curl -H "User-Agent: Mozilla/5.0" \
     "https://api.zhihu.com/topstory/hot-lists/total?limit=50"
```

**关键字段**:
- `target.title`: 问题标题
- `target.excerpt`: 摘要
- `target.created`: 创建时间
- `detail_text`: 热度值（如 "1234 万热度"）
- `children[0].thumbnail`: 封面图

**限制条件**:
- 无Cookie时可能返回部分内容
- 频率限制不明，建议适当缓存

---

### 1.3 百度热搜 ⭐推荐

| 项目 | 详情 |
|------|------|
| **API地址** | `https://top.baidu.com/board?tab=realtime` |
| **方法** | GET（页面爬虫） |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | HTML（内含JSON） |
| **数据量** | 约50条 |
| **更新频率** | 实时 |
| **访问方式** | 页面解析 |

**验证状态**: ✅ 已验证（2026-04-19），从页面s-data注释提取51条

**提取方式**:
```javascript
// 页面HTML中包含 <!--s-data:{...}--> 注释
const match = html.match(/<!--s-data:(.*?)-->/s);
const data = JSON.parse(match[1]);
const items = data.data.cards[0].content;
```

**可选分类**:
- `realtime` - 热搜
- `novel` - 小说
- `movie` - 电影
- `teleplay` - 电视剧
- `car` - 汽车
- `game` - 游戏

**限制条件**:
- 依赖页面结构，若改版需更新解析逻辑
- 建议通过 `tab` 参数获取不同类别

---

## 二、国内新闻API

### 2.1 今日头条热榜 ⭐推荐

| 项目 | 详情 |
|------|------|
| **API地址** | `https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | JSON |
| **数据量** | 50条 |
| **更新频率** | 实时 |

**验证状态**: ✅ 已验证（2026-04-19），返回50条热点

**关键字段**:
- `Title`: 标题
- `ClusterId`: 话题ID
- `Label`: 标签（hot/breaking等）
- `Url`: 详情链接

---

### 2.2 腾讯新闻热点榜 ⭐推荐

| 项目 | 详情 |
|------|------|
| **API地址** | `https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=50` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | JSON |
| **数据量** | 50条（第一条为说明） |
| **更新频率** | 每10分钟 |

**验证状态**: ✅ 已验证（2026-04-19）

**关键字段**:
- `title`: 标题
- `abstract`: 摘要
- `source`: 来源
- `hotEvent.hotScore`: 热度值
- `timestamp`: 时间戳

---

### 2.3 网易新闻热点

| 项目 | 详情 |
|------|------|
| **API地址** | `https://gw.m.163.com/nc-main/api/v1/hqc/no-repeat-hot-list` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | JSON |
| **数据量** | 30条 |
| **更新频率** | 实时 |

**验证状态**: ✅ 已验证（2026-04-19），返回30条

**关键字段**:
- `title`: 标题
- `hotValue`: 热度值
- `commentCount`: 评论数
- `source`: 来源媒体
- `img`: 封面图

---

### 2.4 新浪新闻热榜

| 项目 | 详情 |
|------|------|
| **API地址** | `https://top.news.sina.com.cn/ws/GetTopDataList.php` |
| **方法** | GET |
| **是否需要认证** | ❌ 无需认证 |
| **返回格式** | JSONP (`var data = {...}`) |
| **数据量** | 可调 |
| **更新频率** | 每日 |

**验证状态**: ✅ 已验证（2026-04-19）

**请求参数**:
```
top_type=day       # 日榜
top_cat=news_china_suda  # 分类
top_time=20260418  # 日期 YYYYMMDD
top_num=20         # 数量
```

**分类列表**:
| type值 | 分类名 |
|--------|--------|
| `www_www_all_suda_suda` | 总排行 |
| `news_china_suda` | 国内新闻 |
| `news_world_suda` | 国际新闻 |
| `news_society_suda` | 社会新闻 |
| `sports_suda` | 体育 |
| `finance_0_suda` | 财经 |
| `ent_suda` | 娱乐 |
| `tech_news_suda` | 科技 |
| `news_mil_suda` | 军事 |

**限制条件**:
- 返回JSONP格式，需要去除 `var data = ` 前缀

---

### 2.5 其他国内新闻源

| 平台 | 访问方式 | 状态 | 备注 |
|------|---------|------|------|
| 澎湃新闻 | `https://api-hot.imsyy.top/thepaper` | 需自建 | 通过DailyHotApi聚合 |
| 36氪 | `https://api-hot.imsyy.top/36kr` | 需自建 | 通过DailyHotApi聚合 |
| 虎嗅 | `https://api-hot.imsyy.top/huxiu` | 需自建 | 通过DailyHotApi聚合 |
| IT之家 | `https://api-hot.imsyy.top/ithome` | 需自建 | 通过DailyHotApi聚合 |

---

## 三、国际新闻API

### 3.1 NewsAPI ⭐推荐（免费方案）

| 项目 | 详情 |
|------|------|
| **官网** | https://newsapi.org |
| **免费额度** | 100请求/天 |
| **是否需要认证** | ✅ 需要API Key（免费注册） |
| **支持中文** | ❌ 有限（主要英文源） |
| **数据量** | 每请求最多100条 |

**API端点**:
```
GET https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY
GET https://newsapi.org/v2/everything?q=AI&apiKey=YOUR_KEY
```

**限制条件**:
- 免费版仅支持开发/个人使用
- 不可用于商业生产环境
- 数据延迟约1小时
- 不支持 HTTPS（免费版）

---

### 3.2 GNews

| 项目 | 详情 |
|------|------|
| **官网** | https://gnews.io |
| **免费额度** | 100请求/天 |
| **是否需要认证** | ✅ 需要API Key |
| **支持中文** | ✅ 支持多语言 |

**API端点**:
```
GET https://gnews.io/api/v4/top-headlines?lang=zh&country=cn&apikey=YOUR_KEY
GET https://gnews.io/api/v4/search?q=technology&lang=zh&apikey=YOUR_KEY
```

---

### 3.3 NewsData.io

| 项目 | 详情 |
|------|------|
| **官网** | https://newsdata.io |
| **免费额度** | 200请求/天 |
| **是否需要认证** | ✅ 需要API Key |
| **支持中文** | ✅ |

**API端点**:
```
GET https://newsdata.io/api/1/news?apikey=YOUR_KEY&country=cn&language=zh
```

---

### 3.4 Currents API

| 项目 | 详情 |
|------|------|
| **官网** | https://currentsapi.services |
| **免费额度** | 有限 |
| **是否需要认证** | ✅ 需要API Key |
| **支持中文** | ✅ |

---

### 3.5 国际新闻API对比

| 服务 | 免费请求/天 | 需认证 | 中文支持 | 数据延迟 | 备注 |
|------|------------|--------|---------|---------|------|
| NewsAPI | 100 | ✅ | 有限 | ~1h | 开发免费，商用付费 |
| GNews | 100 | ✅ | ✅ | 实时 | 多语言支持好 |
| NewsData.io | 200 | ✅ | ✅ | 实时 | 额度最高 |
| Currents | ~100 | ✅ | ✅ | 实时 | 较新服务 |

**建议**: 对于中文热点监控，优先使用国内API（今日头条、腾讯、网易）。国际新闻API适合补充海外视角，推荐 NewsData.io（免费额度最高）。

---

## 四、开源热榜聚合项目

### 4.1 DailyHotApi / DailyHot ⭐⭐强烈推荐

| 项目 | 详情 |
|------|------|
| **GitHub** | https://github.com/imsyy/DailyHotApi |
| **Stars** | 3,750 ⭐ |
| **前端** | https://github.com/imsyy/DailyHot (889⭐) |
| **支持数据源** | 40+ 平台 |
| **部署方式** | Docker / Vercel / Railway / 手动 / npm包 |
| **特色功能** | RSS模式、JSON模式、缓存机制、自动更新 |

**支持的数据源列表**:

| 分类 | 平台 | 路由名 |
|------|------|--------|
| 社交媒体 | 微博 | `/weibo` |
| 社交媒体 | 知乎 | `/zhihu` |
| 社交媒体 | 知乎日报 | `/zhihu-daily` |
| 社交媒体 | 抖音 | `/douyin` |
| 社交媒体 | 快手 | `/kuaishou` |
| 搜索 | 百度 | `/baidu` |
| 搜索 | 百度贴吧 | `/tieba` |
| 视频 | 哔哩哔哩 | `/bilibili` |
| 视频 | AcFun | `/acfun` |
| 新闻 | 今日头条 | `/toutiao` |
| 新闻 | 腾讯新闻 | `/qq-news` |
| 新闻 | 新浪新闻 | `/sina-news` |
| 新闻 | 网易新闻 | `/netease-news` |
| 新闻 | 澎湃新闻 | `/thepaper` |
| 新闻 | 36氪 | `/36kr` |
| 新闻 | 虎嗅 | `/huxiu` |
| 新闻 | IT之家 | `/ithome` |
| 科技 | 稀土掘金 | `/juejin` |
| 科技 | CSDN | `/csdn` |
| 科技 | 少数派 | `/sspai` |
| 科技 | 简书 | `/jianshu` |
| 社区 | V2EX | `/v2ex` |
| 社区 | 虎扑 | `/hupu` |
| 社区 | 酷安 | `/coolapk` |
| 读书 | 微信读书 | `/weread` |
| 娱乐 | 豆瓣电影 | `/douban-movie` |
| 娱乐 | 豆瓣小组 | `/douban-group` |
| 游戏 | 英雄联盟 | `/lol` |
| 生活 | 历史上的今天 | `/history` |
| 应急 | 气象预警 | `/weatheralarm` |
| 应急 | 地震速报 | `/earthquake` |

**部署方式**:
```bash
# Docker部署
docker pull imsyy/dailyhot-api:latest
docker run --restart always -p 6688:6688 -d imsyy/dailyhot-api:latest

# Vercel一键部署
# 访问 https://vercel.com/new/imsyys-projects/clone?repository-url=https://github.com/imsyy/DailyHotApi-Vercel

# npm包
cnpm install dailyhot-api
```

**API调用**:
```bash
# JSON模弌
curl https://your-domain/weibo
curl https://your-domain/zhihu
curl https://your-domain/baidu?type=realtime

# RSS模弌
curl https://your-domain/weibo?type=rss
```

**配置说明**:
- 默认缓存60分钟（可配置）
- 部分接口需要 Puppeteer 环境
- 支持自定义请求超时

---

### 4.2 RSSHub ⭐⭐强烈推荐

| 项目 | 详情 |
|------|------|
| **GitHub** | https://github.com/DIYgod/RSSHub |
| **Stars** | 43,503 ⭐ |
| **官网** | https://rsshub.app |
| **支持数据源** | 数千个平台/路由 |
| **部署方式** | Docker / Vercel / 手动 |
| **特色功能** | 将任何内容转为RSS |

**与热点监控相关的路由**:

| 平台 | 路由示例 |
|------|---------|
| 微博热搜 | `/weibo/search/hot` |
| 知乎热榜 | `/zhihu/hotlist` |
| 知乎日报 | `/zhihu/daily` |
| 百度贴吧 | `/tieba/forum/xxx` |
| 哔哩哔哩 | `/bilibili/hot-search` |
| 网易新闻 | `/163/news/rank/xxx` |
| 澎湃新闻 | `/thepaper/xxx` |
| 今日头条 | 通过 `/toutiao/xxx` |

**部署方式**:
```bash
docker pull diygod/rsshub
docker run -d --name rsshub -p 1200:1200 diygod/rsshub
```

**限制条件**:
- 官方实例 `rsshub.app` 可能不稳定（被墙/限流）
- 强烈建议自建实例
- 部分路由需要Cookie/认证

---

### 4.3 Wechat2RSS

| 项目 | 详情 |
|------|------|
| **GitHub** | https://github.com/ttttmr/Wechat2RSS |
| **Stars** | 1,366 ⭐ |
| **用途** | 微信公众号转RSS |
| **特色** | 可订阅特定公众号获取垂直领域内容 |

---

### 4.4 其他相关项目

| 项目 | Stars | 用途 |
|------|-------|------|
| yihong0618/gitblog | 1,606⭐ | GitHub Issues写博客 |
| ttttmr/Wechat2RSS | 1,366⭐ | 微信公众号RSS化 |

---

## 五、推荐方案（针对您的系统）

### 方案A: 直接调用API（最轻量）⭐推荐

**架构**: 定时任务 → 直接调用各平台API → LLM筛选

**调用清单**:
1. 微博热搜: `https://weibo.com/ajax/side/hotSearch`
2. 知乎热榜: `https://api.zhihu.com/topstory/hot-lists/total?limit=50`
3. 百度热搜: `https://top.baidu.com/board?tab=realtime` + 正则提取
4. 今日头条: `https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc`
5. 腾讯新闻: `https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=50`
6. 网易新闻: `https://gw.m.163.com/nc-main/api/v1/hqc/no-repeat-hot-list`
7. 新浪新闻: `https://top.news.sina.com.cn/ws/GetTopDataList.php?...`

**优点**:
- 零部署成本
- 直接控制数据源
- 无需维护中间服务
- 响应速度快

**缺点**:
- 各API格式不一致，需要分别解析
- 若某平台改版需更新代码
- 需要处理各自反爬策略

---

### 方案B: 自建DailyHotApi（最全面）⭐推荐

**架构**: 定时任务 → DailyHotApi本地实例 → LLM筛选

**部署**:
```bash
docker run -d -p 6688:6688 --restart always imsyy/dailyhot-api:latest
```

**调用**:
```bash
# 获取所有热点
curl "http://localhost:6688/weibo"
curl "http://localhost:6688/zhihu"
curl "http://localhost:6688/baidu"
curl "http://localhost:6688/toutiao"
# ... 更多数据源
```

**优点**:
- 统一API格式
- 内置缓存（默认60分钟）
- 支持40+数据源
- 支持RSS输出
- 支持Vercel免费部署

**缺点**:
- 需要维护一个服务
- 部分接口需要Puppeteer环境
- 海外服务器可能访问国内源不稳定

---

### 方案C: 自建RSSHub + RSS阅读器

**架构**: RSSHub → RSS聚合 → LLM处理

**适合场景**:
- 如果您已有RSS工作流
- 需要订阅微信公众号等垂直内容

---

## 六、数据获取Python示例代码

```python
import requests, re, json
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 1. 微博热搜
def get_weibo():
    url = "https://weibo.com/ajax/side/hotSearch"
    r = requests.get(url, headers={**HEADERS, "Referer": "https://weibo.com/"})
    data = r.json()["data"]["realtime"]
    return [{"title": x["word"], "source": "weibo"} for x in data]

# 2. 知乎热榜
def get_zhihu():
    url = "https://api.zhihu.com/topstory/hot-lists/total?limit=50"
    r = requests.get(url, headers=HEADERS)
    data = r.json()["data"]
    return [{"title": x["target"]["title"], "source": "zhihu"} for x in data]

# 3. 百度热搜
def get_baidu():
    url = "https://top.baidu.com/board?tab=realtime"
    r = requests.get(url, headers=HEADERS)
    match = re.search(r'<!--s-data:(.*?)-->', r.text, re.DOTALL)
    data = json.loads(match.group(1))
    items = data["data"]["cards"][0]["content"]
    return [{"title": x["word"], "source": "baidu"} for x in items]

# 4. 今日头条
def get_toutiao():
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    r = requests.get(url, headers={**HEADERS, "Referer": "https://www.toutiao.com"})
    data = r.json()["data"]
    return [{"title": x["Title"], "source": "toutiao"} for x in data]

# 5. 腾讯新闻
def get_qq_news():
    url = "https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=50"
    r = requests.get(url, headers=HEADERS)
    data = r.json()["idlist"][0]["newslist"][1:]  # 跳过第一条说明
    return [{"title": x["title"], "source": "qq_news"} for x in data]

# 6. 网易新闻
def get_netease():
    url = "https://gw.m.163.com/nc-main/api/v1/hqc/no-repeat-hot-list"
    r = requests.get(url, headers=HEADERS)
    data = r.json()["data"]["items"]
    return [{"title": x["title"], "source": "netease"} for x in data]

# 聚合所有热点
all_hot = []
all_hot.extend(get_weibo())
all_hot.extend(get_zhihu())
all_hot.extend(get_baidu())
all_hot.extend(get_toutiao())
all_hot.extend(get_qq_news())
all_hot.extend(get_netease())

print(f"共获取 {len(all_hot)} 条热点")
```

---

## 七、注意事项与风险

1. **反爬策略**: 微博、知乎等平台可能有频率限制，建议设置合理的请求间隔（>5秒）和缓存机制
2. **Cookie要求**: 知乎部分接口在有Cookie时返回更完整数据（可选）
3. **页面改版**: 百度热搜依赖页面结构，若改版需更新正则表达式
4. **法律合规**: 仅用于个人研究/学习，遵守各平台robots.txt和使用条款
5. **国际新闻API**: 免费版有严格限制，生产环境建议购买付费套餐
6. **数据缓存**: 强烈建议实现本地缓存（60分钟），减少请求频率

---

## 八、总结建议

| 优先级 | 方案 | 适用场景 |
|--------|------|---------|
| ⭐⭐⭐ | 直接调用6个核心API | 快速启动、低成本、易维护 |
| ⭐⭐⭐ | 自建DailyHotApi | 需要40+数据源、统一格式、RSS输出 |
| ⭐⭐ | 自建RSSHub | 已有RSS工作流、需要公众号等垂直内容 |
| ⭐ | 国际新闻API | 补充海外视角（NewsData.io免费额度最高） |

**对于"热点监控与内容筛选系统"，推荐采用方案A（直接调用API）快速启动，后续如需扩展再引入DailyHotApi。**
