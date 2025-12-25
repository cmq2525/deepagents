# 通用智能体示例 / Universal Agent Example

这个示例展示了如何使用 deepagents 库创建一个支持多领域任务的通用智能体，包括渐进式工具加载功能。

This example demonstrates how to create a universal agent using the deepagents library that supports multi-domain tasks with progressive tool loading.

## 功能特性 / Features

### 核心功能 / Core Capabilities

1. **调查研究报告 / Research Reports**
   - 信息收集和分析 / Information gathering and analysis
   - 结构化报告撰写 / Structured report writing
   - 来源引用 / Source citation

2. **数据分析 / Data Analysis**
   - 数据文件处理 / Data file processing
   - 统计分析 / Statistical analysis
   - 报告生成 / Report generation

3. **渐进式工具加载 / Progressive Tool Loading**
   - 基础工具始终可用 / Basic tools always available
   - 按需加载高级功能 / Advanced features loaded on-demand
   - 灵活的配置选项 / Flexible configuration options

### 内置工具 / Built-in Tools

#### 基础工具（始终可用）/ Basic Tools (Always Available)

- **文件操作 / File Operations**
  - `ls`: 列出目录内容 / List directory contents
  - `read_file`: 分块读取文件 / Read files in chunks
    - 支持 `offset` 和 `limit` 参数进行分页 / Supports `offset` and `limit` for pagination
    - 适合处理大文件 / Ideal for handling large files
  - `write_file`: 创建新文件 / Create new files
  - `edit_file`: 编辑现有文件 / Edit existing files
  - `glob`: 模式匹配查找文件 / Pattern matching for files
  - `grep`: 文本搜索 / Text search

- **任务管理 / Task Management**
  - `write_todos`: 创建任务列表 / Create task lists
  - `read_todos`: 读取任务状态 / Read task status
  - `task`: 委托给子智能体 / Delegate to sub-agents

#### 可选工具（按需加载）/ Optional Tools (On-Demand Loading)

- **网络搜索 / Internet Search** (`enable_search=True`)
  - 需要 Tavily API key / Requires Tavily API key
  - 实时信息检索 / Real-time information retrieval
  
- **命令执行 / Command Execution** (`enable_execution=True`)
  - 需要工作目录 / Requires workspace directory
  - 支持 shell 命令 / Supports shell commands
  - 沙盒环境执行 / Sandboxed execution

## 安装 / Installation

```bash
# 基础安装 / Basic installation
pip install deepagents

# 启用搜索功能 / Enable search functionality
pip install deepagents tavily-python

# 设置 API key / Set API key
export TAVILY_API_KEY="your-api-key-here"
```

## 使用方法 / Usage

### 基础示例 / Basic Example

```python
from examples.universal_agent import create_universal_agent

# 创建基础智能体（仅文件操作）
# Create basic agent (file operations only)
agent = create_universal_agent()

# 执行任务 / Execute task
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "创建一个关于人工智能的研究报告"
    }]
})
```

### 启用搜索功能 / Enable Search

```python
# 创建支持搜索的智能体
# Create agent with search capability
agent = create_universal_agent(enable_search=True)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "搜索并总结最新的AI技术进展"
    }]
})
```

### 完整功能配置 / Full Feature Configuration

```python
# 创建具有所有功能的智能体
# Create agent with all features
agent = create_universal_agent(
    enable_search=True,          # 启用搜索 / Enable search
    enable_execution=True,        # 启用命令执行 / Enable execution
    workspace_dir="/path/to/dir"  # 工作目录 / Workspace directory
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "分析数据文件并生成可视化报告"
    }]
})
```

## 示例任务 / Example Tasks

### 1. 研究报告 / Research Report

```python
agent = create_universal_agent(enable_search=True)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        请完成以下研究任务：
        1. 研究量子计算的最新进展
        2. 整理关键技术突破
        3. 撰写一份结构化的研究报告
        4. 将报告保存到 /research_report.md
        """
    }]
})
```

### 2. 数据分析 / Data Analysis

```python
agent = create_universal_agent(
    enable_execution=True,
    workspace_dir="/path/to/data"
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        分析 /data/sales.csv 文件：
        1. 使用分块读取预览数据结构
        2. 计算关键统计指标
        3. 生成分析报告
        4. 保存到 /analysis_report.md
        """
    }]
})
```

### 3. 复杂项目规划 / Complex Project Planning

```python
agent = create_universal_agent()

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        规划一个新项目的开发流程：
        1. 创建详细的任务列表
        2. 定义每个阶段的可交付成果
        3. 设置里程碑
        4. 保存规划文档到 /project_plan.md
        """
    }]
})
```

## 分块文件处理 / Chunked File Processing

处理大文件时，使用分块读取避免上下文溢出：

When handling large files, use chunked reading to avoid context overflow:

```python
agent = create_universal_agent()

# 智能体会自动使用分块读取
# Agent will automatically use chunked reading
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        分析 /large_log.txt 文件：
        1. 首先用 read_file(path, limit=100) 预览前100行
        2. 根据需要继续读取：read_file(path, offset=100, limit=200)
        3. 提取关键错误信息
        4. 生成摘要报告
        """
    }]
})
```

## 最佳实践 / Best Practices

### 1. 任务规划 / Task Planning

对于复杂任务，首先创建任务列表：

For complex tasks, create a task list first:

```python
# 智能体会自动使用 write_todos 进行规划
# Agent will automatically use write_todos for planning
"请创建一个任务列表来完成这个复杂的研究项目"
```

### 2. 子智能体委托 / Sub-agent Delegation

将独立的子任务委托给子智能体：

Delegate independent subtasks to sub-agents:

```python
# 智能体会使用 task 工具创建子智能体
# Agent will use task tool to create sub-agents
"使用子智能体分别研究三个不同的主题，然后整合结果"
```

### 3. 文件组织 / File Organization

保持工作目录的良好组织：

Maintain good organization of workspace:

```python
"""
请组织项目文件：
1. 创建 /reports/ 目录用于报告
2. 创建 /data/ 目录用于数据文件
3. 创建 /analysis/ 目录用于分析结果
"""
```

## 配置选项 / Configuration Options

### 后端选择 / Backend Selection

```python
from deepagents.backends import (
    StateBackend,      # 临时存储（默认）/ Ephemeral (default)
    FilesystemBackend, # 持久化存储 / Persistent storage
    CompositeBackend,  # 混合存储 / Hybrid storage
)

# 使用持久化存储
# Use persistent storage
agent = create_universal_agent(
    workspace_dir="/path/to/persistent/workspace"
)
```

### 自定义模型 / Custom Model

```python
from langchain.chat_models import init_chat_model

agent = create_universal_agent(
    model=init_chat_model("openai:gpt-4o"),
    enable_search=True,
)
```

## 故障排除 / Troubleshooting

### 搜索功能不可用 / Search Not Available

```bash
# 安装 tavily-python
pip install tavily-python

# 设置 API key
export TAVILY_API_KEY="your-key"
```

### 命令执行失败 / Command Execution Fails

确保提供了工作目录：

Ensure workspace directory is provided:

```python
agent = create_universal_agent(
    enable_execution=True,
    workspace_dir="/tmp/workspace"  # 必须提供 / Must provide
)
```

## 运行示例 / Run Example

```bash
# 运行基础示例 / Run basic example
python examples/universal_agent.py

# 使用 Python REPL 交互测试 / Interactive testing with Python REPL
python -i examples/universal_agent.py
>>> agent = create_universal_agent()
>>> result = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
```

## 更多信息 / More Information

- [DeepAgents 文档](https://docs.langchain.com/oss/python/deepagents/overview)
- [示例仓库](https://github.com/langchain-ai/deepagents-quickstarts)
- [API 参考](https://reference.langchain.com/python/deepagents/)

## 许可证 / License

MIT License - 参见主项目许可证 / See main project license
