"""大模型客户端"""

from __future__ import annotations

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass


@dataclass
class ChatResult:
    """对话结果"""

    content: str
    duration_ms: int
    input_tokens: int
    output_tokens: int

    def __str__(self) -> str:
        return self.content


class ModelClient:
    """火山引擎大模型客户端"""

    DEFAULT_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    def __init__(self, api_key: str | None = None, endpoint: str | None = None):
        self.api_key = api_key or os.environ.get("ARK_API_KEY")
        self.endpoint = endpoint or os.environ.get("ARK_ENDPOINT") or self.DEFAULT_ENDPOINT

        if not self.api_key:
            raise ValueError("缺少配置，请设置环境变量: ARK_API_KEY")

    def chat(self, model: str, content: str) -> ChatResult:
        """进行一轮对话

        Args:
            model: 模型名称
            content: 用户输入内容

        Returns:
            ChatResult 包含回复内容、耗时和 token 使用量
        """
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content,
                        }
                    ],
                }
            ],
        }

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

            usage = result.get("usage", {})
            return ChatResult(
                content=result["choices"][0]["message"]["content"],
                duration_ms=duration_ms,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
            )
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise RuntimeError(f"API 调用失败 ({e.code}): {error_body}")
