<p align="center">
  <h1 align="center">ark-cli</h1>
</p>

<p align="center">
  火山引擎命令行工具 — 让人类和 AI Agent 都能在终端中操作火山引擎
</p>

<p align="center">
  <a href="https://github.com/cnwarden/ark-cli/releases"><img src="https://img.shields.io/github/v/release/cnwarden/ark-cli?style=for-the-badge&color=FF6A00" alt="Release" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://github.com/cnwarden/ark-cli/stargazers"><img src="https://img.shields.io/github/stars/cnwarden/ark-cli?style=for-the-badge&color=f5a623" alt="Stars" /></a>
  <a href="https://github.com/cnwarden/ark-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-teal.svg?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  <a href="#ark-cli-是什么">介绍</a> · <a href="#核心能力">核心能力</a> · <a href="#快速开始">快速开始</a> · <a href="#命令参考">命令参考</a> · <a href="#贡献">贡献</a>
</p>

---

## ark-cli 是什么

ark-cli 是火山引擎的命令行工具，将 TOS 对象存储、大模型服务等操作封装为简洁的命令行接口。

### 为什么选择 ark-cli

- **开箱即用** — 默认配置北京区域，最少只需 2 个环境变量即可开始使用
- **AI Agent 友好** — 命令设计简洁，输出格式规范，便于 AI Agent 解析调用
- **临时链接** — 上传文件自动返回 24 小时有效的签名 URL
- **轻量依赖** — 基于 Python，使用 uv 包管理，安装简单

## 核心能力

| 模块 | 能力 |
|------|------|
| **TOS 对象存储** | 文件上传、列表、删除、临时链接生成、Bucket 统计 |
| **大模型服务** | 单轮对话、Token 用量统计、耗时统计 |

## 快速开始

### 安装

**从源码安装**

```bash
git clone https://github.com/cnwarden/ark-cli.git
cd ark-cli
uv sync
```

**从 Release 下载**

从 [Releases](https://github.com/cnwarden/ark-cli/releases/latest) 页面下载最新的 wheel 包：

```bash
pip install ark_cli-*.whl
```

### 配置凭证

```bash
# TOS 对象存储（必需）
export TOS_ACCESS_KEY="your-access-key"
export TOS_SECRET_KEY="your-secret-key"

# TOS 可选配置（默认北京区域）
export TOS_ENDPOINT="tos-cn-beijing.volces.com"
export TOS_REGION="cn-beijing"

# 大模型服务（使用 model 功能时必需）
export ARK_API_KEY="your-api-key"
```

### 验证安装

```bash
ark-cli -v
```

## 命令参考

```
ark-cli [-p PRODUCT] [-a ACTION] [OPTIONS]

Products:
  tos       TOS 对象存储操作
  model     大模型对话

TOS Actions:
  upload    上传文件
  ls        列出文件
  lsb       列出 Bucket
  geturl    获取临时链接
  rm        删除文件
  stats     Bucket 统计信息

Model Options:
  -m        模型名称（例如: doubao-seed-2-0-mini-260215）
  -c        对话内容
```

<details>
<summary>TOS 对象存储</summary>

```bash
# 上传文件（返回 24 小时有效的签名链接）
ark-cli -p tos -a upload -bucket my-bucket -i ./test.txt -o data/test.txt

# 列出 Bucket
ark-cli -p tos -a lsb

# 列出文件
ark-cli -p tos -a ls -bucket my-bucket
ark-cli -p tos -a ls -bucket my-bucket -i data/

# 获取临时链接
ark-cli -p tos -a geturl -bucket my-bucket -i data/test.txt

# 删除文件
ark-cli -p tos -a rm -bucket my-bucket -i data/test.txt

# Bucket 统计信息
ark-cli -p tos -a stats -bucket my-bucket
```

**输出示例**

列出文件：
```
DIR        -                    data/subdir/
1.2KB      2024-03-30 10:00:00  data/test.txt
256B       2024-03-30 09:30:00  data/config.json
```

Bucket 统计：
```
Bucket:      my-bucket
Location:    cn-beijing
Created:     2025-05-12 12:29:06
Storage:     Storage_Class_Standard
Redundancy:  Az_Redundancy_Single_Az
Versioning:  Versioning_Unknown
Endpoint:    tos-cn-beijing.volces.com
```

</details>

<details>
<summary>大模型对话</summary>

```bash
# 单轮对话
ark-cli -p model -m doubao-seed-2-0-mini-260215 -c "你好，请介绍一下你自己"
```

**输出示例**
```
嗨！👋 你好呀~ 请问有什么我可以帮你的吗？

[耗时: 5991ms | tokens: 50 in / 371 out]
```

</details>

## 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 语言 | [Python](https://www.python.org/) 3.9+ | |
| 包管理 | [uv](https://github.com/astral-sh/uv) | 快速的 Python 包管理器 |
| TOS SDK | [tos](https://github.com/volcengine/ve-tos-python-sdk) | 火山引擎 TOS 官方 SDK |
| 构建工具 | [hatchling](https://hatch.pypa.io/) | Python 构建后端 |

## 项目结构

```
ark-cli/
├── ark_cli/
│   ├── __init__.py          # 版本定义
│   ├── cli.py                # CLI 入口
│   ├── tos_client.py         # TOS 客户端封装
│   └── model_client.py       # 大模型客户端
├── pyproject.toml            # 项目配置
├── Makefile                  # 构建脚本
└── README.md
```

## 开发

```bash
# 克隆项目
git clone https://github.com/cnwarden/ark-cli.git
cd ark-cli

# 安装依赖
uv sync

# 运行
uv run ark-cli -v

# 构建
uv build

# 发布到 TOS
make publish
```

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

提交信息请遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

## License

[MIT](LICENSE)

## 相关链接

- [火山引擎控制台](https://console.volcengine.com/) — 获取 Access Key
- [TOS 文档](https://www.volcengine.com/docs/6349) — 对象存储文档
- [方舟大模型](https://www.volcengine.com/docs/82379) — 大模型服务文档
