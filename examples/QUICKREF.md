# 快速参考指南 / Quick Reference Guide

## 安装 / Installation

```bash
# 基础安装 / Basic installation
pip install deepagents

# 可选：搜索功能 / Optional: Search capability
pip install tavily-python
export TAVILY_API_KEY="your-key"
```

## 基本使用 / Basic Usage

```python
from examples.universal_agent import create_universal_agent

# 创建基础智能体 / Create basic agent
agent = create_universal_agent()

# 执行任务 / Execute task
result = agent.invoke({
    "messages": [{"role": "user", "content": "创建一个研究报告"}]
})
```

## 配置选项 / Configuration Options

### 1. 基础配置 / Basic Configuration
```python
# 仅文件操作 / File operations only
agent = create_universal_agent()
```

### 2. 添加命令执行 / Add Command Execution
```python
agent = create_universal_agent(
    enable_execution=True,
    workspace_dir="/path/to/workspace"
)
```

### 3. 添加搜索功能 / Add Search Capability
```python
agent = create_universal_agent(
    enable_search=True  # 需要 TAVILY_API_KEY / Requires TAVILY_API_KEY
)
```

### 4. 完整配置 / Full Configuration
```python
agent = create_universal_agent(
    enable_search=True,
    enable_execution=True,
    workspace_dir="/path/to/workspace"
)
```

## 内置工具 / Built-in Tools

### 文件操作 / File Operations
- `ls` - 列出目录 / List directory
- `read_file(path, offset=0, limit=500)` - 读取文件（支持分块）/ Read file (chunked)
- `write_file(path, content)` - 写入文件 / Write file
- `edit_file(path, old_str, new_str)` - 编辑文件 / Edit file
- `glob(pattern)` - 文件模式匹配 / File pattern matching
- `grep(pattern, path, glob)` - 文本搜索 / Text search

### 任务管理 / Task Management
- `write_todos` - 创建任务列表 / Create task list
- `task` - 委托给子智能体 / Delegate to sub-agent

### 可选工具 / Optional Tools
- `execute(command)` - 执行命令（需要 workspace_dir）/ Execute command (requires workspace_dir)
- `internet_search(query)` - 网络搜索（需要 API key）/ Internet search (requires API key)

## 常见任务 / Common Tasks

### 研究报告 / Research Report
```python
agent = create_universal_agent(enable_search=True)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        研究人工智能的最新进展：
        1. 搜索最新信息
        2. 整理关键发现
        3. 撰写报告并保存到 /report.md
        """
    }]
})
```

### 数据分析 / Data Analysis
```python
agent = create_universal_agent(
    enable_execution=True,
    workspace_dir="/path/to/data"
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        分析 /data/sales.csv：
        1. 读取数据（使用分块读取）
        2. 计算统计指标
        3. 生成分析报告
        """
    }]
})
```

### 项目规划 / Project Planning
```python
agent = create_universal_agent()

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        创建项目计划：
        1. 使用 write_todos 创建任务列表
        2. 定义各阶段的可交付成果
        3. 保存计划到 /plan.md
        """
    }]
})
```

## 分块读取示例 / Chunked Reading Example

```python
# 对于大文件，智能体会自动使用分块读取
# For large files, agent automatically uses chunked reading

agent = create_universal_agent(workspace_dir="/path")

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        处理 /large_log.txt：
        1. 先读取前100行预览结构
        2. 根据需要继续读取后续部分
        3. 提取关键信息
        """
    }]
})
```

## 后端选项 / Backend Options

### 状态后端（默认）/ State Backend (Default)
```python
# 临时存储 / Ephemeral storage
agent = create_universal_agent()
```

### 文件系统后端 / Filesystem Backend
```python
# 持久化存储 + 命令执行 / Persistent storage + command execution
agent = create_universal_agent(workspace_dir="/path/to/workspace")
```

## 运行示例 / Run Examples

```bash
# 查看基本功能 / View basic functionality
python examples/universal_agent.py

# 运行功能验证 / Run functional verification
python examples/verify_functionality.py

# 查看使用示例 / View usage examples
python examples/usage_examples.py

# 运行演示（需要 API key）/ Run demo (requires API key)
python examples/demo.py
```

## 测试 / Testing

```bash
# 运行测试 / Run tests
pytest examples/test_universal_agent.py -v

# 运行非 API 测试 / Run non-API tests
pytest examples/test_universal_agent.py -v -k "not search"
```

## 故障排除 / Troubleshooting

### 搜索功能不可用 / Search Not Available
```bash
pip install tavily-python
export TAVILY_API_KEY="your-key-here"
```

### 命令执行失败 / Command Execution Fails
```python
# 确保提供了 workspace_dir / Ensure workspace_dir is provided
agent = create_universal_agent(
    enable_execution=True,
    workspace_dir="/tmp/workspace"  # Required!
)
```

### 导入错误 / Import Error
```bash
# 安装 deepagents / Install deepagents
cd libs/deepagents
pip install -e .
```

## 更多资源 / More Resources

- [完整 README](README.md) - 详细文档 / Detailed documentation
- [DeepAgents 文档](https://docs.langchain.com/oss/python/deepagents/overview) - 官方文档 / Official docs
- [示例代码](.) - 所有示例文件 / All example files
