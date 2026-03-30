# ark-cli

火山引擎命令行工具 — 让人类和 AI Agent 都能在终端中操作火山引擎

## 安装

```bash
uv sync
```

## 配置

### TOS 对象存储

设置环境变量：

```bash
export TOS_ACCESS_KEY="your-access-key"
export TOS_SECRET_KEY="your-secret-key"

# 可选，默认为北京区域
export TOS_ENDPOINT="tos-cn-beijing.volces.com"
export TOS_REGION="cn-beijing"
```

### 大模型服务

设置环境变量：

```bash
export ARK_API_KEY="your-api-key"
```

## 使用

### 查看版本

```bash
ark-cli -v
```

### TOS 文件上传

```bash
ark-cli -p tos -a upload -bucket <bucket_name> -i <local_filepath> -o <remote_filepath>
```

示例：

```bash
ark-cli -p tos -a upload -bucket my-bucket -i ./test.txt -o data/test.txt
```

成功后返回带签名的临时访问链接（24小时有效）：

```
https://my-bucket.tos-cn-beijing.volces.com/data/test.txt?X-Tos-Algorithm=...&X-Tos-Expires=...&X-Tos-Signature=...
```

### TOS Bucket 列表

```bash
ark-cli -p tos -a lsb
```

输出格式：

```
2024-03-30 10:00:00  my-bucket
2024-03-28 15:30:00  another-bucket
```

### TOS 文件列表

列出 bucket 根目录：

```bash
ark-cli -p tos -a ls -bucket <bucket_name>
```

列出指定路径下的文件：

```bash
ark-cli -p tos -a ls -bucket <bucket_name> -i <prefix>
```

示例：

```bash
ark-cli -p tos -a ls -bucket my-bucket -i /
ark-cli -p tos -a ls -bucket my-bucket -i data/
```

输出格式：

```
DIR        -                    data/subdir/
1.2KB      2024-03-30 10:00:00  data/test.txt
256B       2024-03-30 09:30:00  data/config.json
```

### TOS 获取临时链接

获取已上传文件的临时访问链接（24小时有效）：

```bash
ark-cli -p tos -a geturl -bucket <bucket_name> -i <object_key>
```

示例：

```bash
ark-cli -p tos -a geturl -bucket my-bucket -i data/test.txt
```

### TOS 删除文件

```bash
ark-cli -p tos -a rm -bucket <bucket_name> -i <object_key>
```

示例：

```bash
ark-cli -p tos -a rm -bucket my-bucket -i data/test.txt
```

### TOS Bucket 统计

获取 bucket 的元数据信息：

```bash
ark-cli -p tos -a stats -bucket <bucket_name>
```

示例：

```bash
ark-cli -p tos -a stats -bucket my-bucket
```

输出格式：

```
Bucket:      my-bucket
Location:    cn-beijing
Created:     2025-05-12 12:29:06
Storage:     Storage_Class_Standard
Redundancy:  Az_Redundancy_Single_Az
Versioning:  Versioning_Unknown
Endpoint:    tos-cn-beijing.volces.com
```

### 大模型对话

```bash
ark-cli -p model -m <model_name> -c <content>
```

可用模型示例：`doubao-seed-2-0-mini-260215`

示例：

```bash
ark-cli -p model -m doubao-seed-2-0-mini-260215 -c "你好，请介绍一下你自己"
```
