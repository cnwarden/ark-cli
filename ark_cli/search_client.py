"""联网搜索客户端"""

from __future__ import annotations

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass


@dataclass
class SearchResult:
    """搜索结果项"""

    title: str
    site_name: str
    url: str
    snippet: str
    publish_time: str


@dataclass
class SearchResponse:
    """搜索响应"""

    results: list[SearchResult]
    result_count: int
    duration_ms: int
    query: str


class SearchClient:
    """火山引擎联网搜索客户端"""

    DEFAULT_ENDPOINT = "https://open.feedcoopapi.com/search_api/web_search"

    def __init__(self, api_key: str | None = None, endpoint: str | None = None):
        self.api_key = api_key or os.environ.get("SEARCH_API_KEY")
        self.endpoint = endpoint or os.environ.get("SEARCH_ENDPOINT") or self.DEFAULT_ENDPOINT

        if not self.api_key:
            raise ValueError("缺少配置，请设置环境变量: SEARCH_API_KEY")

    def search(
        self,
        query: str,
        search_type: str = "web",
        count: int = 10,
        time_range: str = "OneWeek",
    ) -> SearchResponse:
        """执行搜索

        Args:
            query: 搜索关键词 (1-100字符)
            search_type: 搜索类型 (web/web_summary/image)
            count: 返回条数 (最多50条，默认10条)
            time_range: 时间范围 (OneDay/OneWeek/OneMonth/OneYear)

        Returns:
            SearchResponse 包含搜索结果列表和统计信息
        """
        data: dict = {
            "Query": query,
            "SearchType": search_type,
            "Count": count,
            "Filter": {
                "NeedUrl": True,
                "AuthInfoLevel": 1,
                "NeedContent": True
            },
        }

        data["TimeRange"] = time_range

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            start_time = time.time()
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
            duration_ms = int((time.time() - start_time) * 1000)

            # 检查错误
            if "ResponseMetadata" in result:
                metadata = result["ResponseMetadata"]
                if "Error" in metadata:
                    error = metadata["Error"]
                    raise RuntimeError(f"API 错误 ({error.get('CodeN', 'unknown')}): {error.get('Message', 'unknown error')}")

            # 解析结果
            api_result = result.get("Result", {})
            web_results = api_result.get("WebResults", []) or []
            search_context = api_result.get("SearchContext", {})

            results = []
            for item in web_results:
                results.append(SearchResult(
                    title=item.get("Title", ""),
                    site_name=item.get("SiteName", ""),
                    url=item.get("Url", ""),
                    snippet=item.get("Snippet", ""),
                    publish_time=item.get("PublishTime", ""),
                ))

            return SearchResponse(
                results=results,
                result_count=api_result.get("ResultCount", 0),
                duration_ms=duration_ms,
                query=search_context.get("OriginQuery", query),
            )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise RuntimeError(f"API 调用失败 ({e.code}): {error_body}")
