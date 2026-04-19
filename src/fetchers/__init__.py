from .base import BaseFetcher
from .weibo import WeiboHotFetcher
from .zhihu import ZhihuHotFetcher
from .baidu import BaiduHotFetcher
from .toutiao import ToutiaoHotFetcher
from .tencent import TencentNewsFetcher
from .netease import NeteaseNewsFetcher

__all__ = [
    "BaseFetcher",
    "WeiboHotFetcher",
    "ZhihuHotFetcher",
    "BaiduHotFetcher",
    "ToutiaoHotFetcher",
    "TencentNewsFetcher",
    "NeteaseNewsFetcher",
]
