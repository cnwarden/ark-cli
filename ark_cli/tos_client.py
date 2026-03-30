"""TOS 对象存储客户端"""

from __future__ import annotations

import os

import tos


class TosClient:
    """火山引擎 TOS 对象存储客户端"""

    DEFAULT_ENDPOINT = "tos-cn-beijing.volces.com"
    DEFAULT_REGION = "cn-beijing"

    def __init__(
        self,
        ak: str | None = None,
        sk: str | None = None,
        endpoint: str | None = None,
        region: str | None = None,
    ):
        self.ak = ak or os.environ.get("TOS_ACCESS_KEY")
        self.sk = sk or os.environ.get("TOS_SECRET_KEY")
        self.endpoint = endpoint or os.environ.get("TOS_ENDPOINT") or self.DEFAULT_ENDPOINT
        self.region = region or os.environ.get("TOS_REGION") or self.DEFAULT_REGION

        if not all([self.ak, self.sk]):
            raise ValueError(
                "缺少 TOS 配置，请设置环境变量: TOS_ACCESS_KEY, TOS_SECRET_KEY"
            )

        self.client = tos.TosClientV2(
            ak=self.ak,
            sk=self.sk,
            endpoint=self.endpoint,
            region=self.region,
        )

    def upload(self, bucket: str, local_path: str, object_key: str, expires: int = 86400) -> str:
        """上传文件到 TOS

        Args:
            bucket: bucket 名称
            local_path: 本地文件路径
            object_key: 云上对象 key
            expires: 临时链接过期时间（秒），默认 24 小时

        Returns:
            带签名的临时访问链接
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"文件不存在: {local_path}")

        self.client.put_object_from_file(bucket, object_key, local_path)

        # 生成预签名临时链接
        result = self.client.pre_signed_url(
            http_method=tos.HttpMethodType.Http_Method_Get,
            bucket=bucket,
            key=object_key,
            expires=expires,
        )

        return result.signed_url

    def list_objects(self, bucket: str, prefix: str = "", max_keys: int = 1000) -> list[dict]:
        """列出指定路径下的文件

        Args:
            bucket: bucket 名称
            prefix: 路径前缀
            max_keys: 最大返回数量

        Returns:
            文件列表，每个元素包含 key, size, last_modified
        """
        result = self.client.list_objects(
            bucket,
            prefix=prefix,
            max_keys=max_keys,
            delimiter="/",
        )

        items = []

        # 添加目录（common_prefixes）
        for cp in result.common_prefixes:
            items.append({
                "key": cp.prefix,
                "size": "-",
                "last_modified": "-",
                "type": "dir",
            })

        # 添加文件
        for obj in result.contents:
            # 跳过与 prefix 完全相同的项（目录本身）
            if obj.key == prefix:
                continue
            items.append({
                "key": obj.key,
                "size": obj.size,
                "last_modified": obj.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "file",
            })

        return items

    def get_url(self, bucket: str, object_key: str, expires: int = 86400) -> str:
        """获取对象的临时访问链接

        Args:
            bucket: bucket 名称
            object_key: 云上对象 key
            expires: 临时链接过期时间（秒），默认 24 小时

        Returns:
            带签名的临时访问链接
        """
        result = self.client.pre_signed_url(
            http_method=tos.HttpMethodType.Http_Method_Get,
            bucket=bucket,
            key=object_key,
            expires=expires,
        )

        return result.signed_url

    def list_buckets(self) -> list[dict]:
        """列出所有 bucket

        Returns:
            bucket 列表，每个元素包含 name, creation_date
        """
        result = self.client.list_buckets()

        items = []
        for bucket in result.buckets:
            creation_date = bucket.creation_date
            # 兼容 datetime 对象和字符串
            if hasattr(creation_date, "strftime"):
                creation_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")
            items.append({
                "name": bucket.name,
                "creation_date": creation_date,
            })

        return items

    def delete(self, bucket: str, object_key: str) -> None:
        """删除对象

        Args:
            bucket: bucket 名称
            object_key: 云上对象 key
        """
        self.client.delete_object(bucket, object_key)

    def stats(self, bucket: str) -> dict:
        """获取 bucket 元数据

        Args:
            bucket: bucket 名称

        Returns:
            包含 bucket 元数据的字典
        """
        result = self.client.get_bucket_info(bucket)
        info = result.bucket_info

        creation_date = info.creation_date
        if hasattr(creation_date, "strftime"):
            creation_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "name": info.name,
            "location": info.location,
            "creation_date": creation_date,
            "storage_class": str(info.storage_class).replace("StorageClassType.", ""),
            "az_redundancy": str(info.az_redundancy).replace("AzRedundancyType.", ""),
            "versioning": str(info.versioning).replace("VersioningStatusType.", ""),
            "extranet_endpoint": info.extranet_endpoint,
            "intranet_endpoint": info.intranet_endpoint,
        }
