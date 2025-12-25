#!/usr/bin/env python3
"""通用智能体示例 (Universal Agent Example)

这个示例展示了如何使用 deepagents 库创建一个通用智能体，支持:
1. 调查研究报告
2. 数据分析
3. 渐进式加载技能和工具
4. 基础文件读写功能（支持分块读写）
5. 按需动态加载搜索和命令行执行工具

This example demonstrates creating a universal agent with deepagents that supports:
1. Research reports
2. Data analysis  
3. Progressive skill and tool loading
4. Basic file read/write (with chunked operations)
5. Dynamic loading of search and command execution tools on-demand
"""

import os
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend


def create_universal_agent(
    enable_search: bool = False,
    enable_execution: bool = False,
    workspace_dir: str | None = None,
    **kwargs: Any,
) -> Any:
    """创建通用智能体 / Create a universal intelligent agent.
    
    Args:
        enable_search: 是否启用搜索工具 / Whether to enable search tools
        enable_execution: 是否启用命令执行工具 / Whether to enable command execution
        workspace_dir: 工作目录路径 / Workspace directory path. If None, uses state backend.
        **kwargs: 其他参数传递给 create_deep_agent / Other arguments passed to create_deep_agent
    
    Returns:
        配置好的通用智能体 / Configured universal agent
    
    Example:
        ```python
        # 基础智能体，只有文件操作
        # Basic agent with only file operations
        agent = create_universal_agent()
        
        # 启用搜索功能
        # Enable search functionality
        agent = create_universal_agent(enable_search=True)
        
        # 启用所有功能
        # Enable all features
        agent = create_universal_agent(
            enable_search=True,
            enable_execution=True,
            workspace_dir="/path/to/workspace"
        )
        ```
    """
    # 配置后端 / Configure backend
    # FilesystemBackend 支持命令执行，StateBackend 不支持
    # FilesystemBackend supports command execution, StateBackend does not
    if workspace_dir:
        backend = FilesystemBackend(root_dir=workspace_dir)
    else:
        # Use factory function for StateBackend (requires runtime)
        backend = None  # Will use default StateBackend in create_deep_agent
    
    # 系统提示词 / System prompt
    system_prompt = """你是一个通用智能体，能够处理多种领域的任务，包括但不限于：

## 核心能力 (Core Capabilities)

1. **调查研究报告 (Research Reports)**
   - 收集和分析信息
   - 撰写结构化的研究报告
   - 引用可靠的来源

2. **数据分析 (Data Analysis)**
   - 读取和处理数据文件
   - 执行统计分析
   - 生成可视化和报告

3. **文件管理 (File Management)**
   - 支持分块读取大文件（使用 offset 和 limit 参数）
   - 分段写入大型输出
   - 高效的文件组织

## 工作流程指导 (Workflow Guidelines)

### 处理大文件 (Handling Large Files)
- 首次读取时使用 `read_file(path, limit=100)` 先查看文件结构
- 根据需要使用 `offset` 参数分段读取：`read_file(path, offset=100, limit=200)`
- 避免一次性读取整个大文件以防止上下文溢出

### 研究任务 (Research Tasks)
1. 使用搜索工具（如已启用）收集信息
2. 将关键信息保存到文件中以供后续参考
3. 分析和综合信息
4. 撰写结构化的报告

### 数据分析任务 (Data Analysis Tasks)
1. 先使用 `ls` 探索可用的数据文件
2. 使用分块读取预览大型数据文件
3. 根据需要使用命令行工具（如已启用）处理数据
4. 将分析结果保存到新文件

## 最佳实践 (Best Practices)

- 对复杂任务使用 `write_todos` 进行规划
- 使用 `task` 工具委托给子智能体处理独立的子任务
- 始终验证文件路径使用绝对路径（以 / 开头）
- 保持工作目录的组织性
"""

    # 如果启用搜索，添加搜索相关指导
    # Add search guidance if enabled
    if enable_search:
        system_prompt += """

## 搜索工具 (Search Tools)

你可以访问网络搜索工具来收集最新信息：
- 使用搜索工具查找当前事实和数据
- 引用搜索结果中的来源
- 验证多个来源的信息准确性
"""

    # 准备工具列表 / Prepare tools list
    tools = []
    
    # 如果启用搜索，添加搜索工具
    # Add search tool if enabled
    if enable_search:
        # 检查是否有 Tavily API key
        # Check for Tavily API key
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        if tavily_api_key:
            try:
                from tavily import TavilyClient
                
                tavily_client = TavilyClient(api_key=tavily_api_key)
                
                def internet_search(query: str, max_results: int = 5) -> str:
                    """在网络上搜索信息 / Search the internet for information.
                    
                    Args:
                        query: 搜索查询 / Search query
                        max_results: 最大结果数 / Maximum number of results
                    
                    Returns:
                        搜索结果 / Search results
                    """
                    try:
                        results = tavily_client.search(query, max_results=max_results)
                        return str(results)
                    except Exception as e:
                        return f"搜索错误 / Search error: {e}"
                
                tools.append(internet_search)
            except ImportError:
                print("警告: 启用了搜索但未安装 tavily-python。运行: pip install tavily-python")
                print("Warning: Search enabled but tavily-python not installed. Run: pip install tavily-python")
        else:
            print("警告: 启用了搜索但未设置 TAVILY_API_KEY 环境变量")
            print("Warning: Search enabled but TAVILY_API_KEY environment variable not set")
    
    # 创建智能体 / Create agent
    agent = create_deep_agent(
        system_prompt=system_prompt,
        tools=tools if tools else None,
        backend=backend,
        **kwargs,
    )
    
    return agent


def main():
    """主函数示例 / Main function example."""
    # 示例 1: 基础智能体
    # Example 1: Basic agent
    print("创建基础通用智能体...")
    print("Creating basic universal agent...")
    basic_agent = create_universal_agent()
    
    # 示例 2: 完整功能智能体
    # Example 2: Full-featured agent
    print("\n创建完整功能通用智能体...")
    print("Creating full-featured universal agent...")
    
    # 检查是否有 Tavily API key
    # Check for Tavily API key
    has_tavily = os.environ.get("TAVILY_API_KEY") is not None
    
    full_agent = create_universal_agent(
        enable_search=has_tavily,
        enable_execution=True,
        workspace_dir="/tmp/universal_agent_workspace",
    )
    
    print("\n智能体创建成功!")
    print("Agent created successfully!")
    
    # 示例使用
    # Example usage
    example_tasks = [
        "请创建一个简单的研究报告，主题是人工智能的发展历史。将报告保存到 /report.md",
        "分析当前目录中的数据文件，生成统计摘要",
        "创建一个待办事项列表，列出完成项目文档的所有步骤",
    ]
    
    print("\n示例任务 (Example Tasks):")
    for i, task in enumerate(example_tasks, 1):
        print(f"{i}. {task}")
    
    print("\n使用方法 (Usage):")
    print("agent.invoke({'messages': [{'role': 'user', 'content': '你的任务'}]})")


if __name__ == "__main__":
    main()
