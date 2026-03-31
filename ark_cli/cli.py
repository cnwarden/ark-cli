"""命令行入口"""

import argparse
import sys

from ark_cli import __version__


def handle_tos(args):
    """处理 TOS 相关命令"""
    from ark_cli.tos_client import TosClient

    try:
        client = TosClient()
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    if args.action == "upload":
        if not all([args.bucket, args.input, args.output]):
            print("错误: upload 操作需要 -bucket, -i, -o 参数", file=sys.stderr)
            sys.exit(1)

        try:
            url = client.upload(args.bucket, args.input, args.output)
            print(url)
        except FileNotFoundError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"上传失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "ls":
        if not args.bucket:
            print("错误: ls 操作需要 -bucket 参数", file=sys.stderr)
            sys.exit(1)

        try:
            prefix = args.input or ""
            # TOS 对象 key 不以 / 开头，/ 表示根目录
            if prefix == "/":
                prefix = ""
            # 移除开头的 /
            prefix = prefix.lstrip("/")
            items = client.list_objects(args.bucket, prefix=prefix)

            if not items:
                print("(空)")
                return

            # 格式化输出
            for item in items:
                if item["type"] == "dir":
                    print(f"{'DIR':<10} {'-':<20} {item['key']}")
                else:
                    size_str = _format_size(item["size"])
                    print(f"{size_str:<10} {item['last_modified']:<20} {item['key']}")
        except Exception as e:
            print(f"列表失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "geturl":
        if not all([args.bucket, args.input]):
            print("错误: geturl 操作需要 -bucket, -i 参数", file=sys.stderr)
            sys.exit(1)

        try:
            url = client.get_url(args.bucket, args.input)
            print(url)
        except Exception as e:
            print(f"获取链接失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "lsb":
        try:
            items = client.list_buckets()

            if not items:
                print("(空)")
                return

            for item in items:
                print(f"{item['creation_date']:<20} {item['name']}")
        except Exception as e:
            print(f"列表失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "rm":
        if not all([args.bucket, args.input]):
            print("错误: rm 操作需要 -bucket, -i 参数", file=sys.stderr)
            sys.exit(1)

        try:
            client.delete(args.bucket, args.input)
            print(f"已删除: {args.input}")
        except Exception as e:
            print(f"删除失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "stats":
        if not args.bucket:
            print("错误: stats 操作需要 -bucket 参数", file=sys.stderr)
            sys.exit(1)

        try:
            info = client.stats(args.bucket)
            print(f"Bucket:      {info['name']}")
            print(f"Location:    {info['location']}")
            print(f"Created:     {info['creation_date']}")
            print(f"Storage:     {info['storage_class']}")
            print(f"Redundancy:  {info['az_redundancy']}")
            print(f"Versioning:  {info['versioning']}")
            print(f"Endpoint:    {info['extranet_endpoint']}")
        except Exception as e:
            print(f"获取统计失败: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"错误: 不支持的操作: {args.action}", file=sys.stderr)
        sys.exit(1)


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f}{unit}" if unit != "B" else f"{size}{unit}"
        size /= 1024
    return f"{size:.1f}PB"


def handle_model(args):
    """处理大模型相关命令"""
    from ark_cli.model_client import ModelClient

    if not all([args.model, args.content]):
        print("错误: model 产品需要 -m 和 -c 参数", file=sys.stderr)
        sys.exit(1)

    try:
        client = ModelClient()
        result = client.chat(args.model, args.content)
        print(result.content)
        print()
        print(f"[耗时: {result.duration_ms}ms | tokens: {result.input_tokens} in / {result.output_tokens} out]")
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"调用失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="ark-cli",
        description="火山引擎命令行工具 - 让人类和 AI Agent 都能在终端中操作火山引擎",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-p", "--product",
        choices=["tos", "model"],
        help="产品名称",
    )
    parser.add_argument(
        "-a", "--action",
        choices=["upload", "ls", "lsb", "geturl", "rm", "stats"],
        help="操作类型",
    )
    parser.add_argument(
        "-bucket",
        help="bucket 名称",
    )
    parser.add_argument(
        "-i", "--input",
        help="路径（本地文件或云上对象 key）",
    )
    parser.add_argument(
        "-o", "--output",
        help="云上对象 key（仅 upload 使用）",
    )
    parser.add_argument(
        "-m", "--model",
        help="模型名称 (例如: doubao-seed-2-0-mini-260215)",
    )
    parser.add_argument(
        "-c", "--content",
        help="对话内容",
    )

    args = parser.parse_args()

    if args.product == "tos":
        handle_tos(args)
    elif args.product == "model":
        handle_model(args)
    elif args.product:
        print(f"错误: 不支持的产品: {args.product}", file=sys.stderr)
        sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
