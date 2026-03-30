# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

ark-cli 是火山引擎命令行工具，让人类和 AI Agent 都能在终端中操作火山引擎。

## 技术栈

- 语言: Python
- 包管理: uv
- 许可证: MIT

## 开发命令

```bash
# 初始化项目
uv init

# 安装依赖
uv sync

# 添加依赖
uv add <package>

# 添加开发依赖
uv add --dev <package>

# 运行脚本
uv run python <script.py>

# 运行测试
uv run pytest

# 代码检查
uv run ruff check .

# 代码格式化
uv run ruff format .
```

## 项目结构

待项目初始化后补充
