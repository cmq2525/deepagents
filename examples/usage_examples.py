#!/usr/bin/env python3
"""完整使用示例 / Complete Usage Example

演示通用智能体的各种实际应用场景
Demonstrates various practical use cases of the universal agent
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from universal_agent import create_universal_agent


def example_file_operations():
    """示例：基础文件操作 / Example: Basic file operations."""
    print("\n" + "=" * 80)
    print("示例 1: 基础文件操作 / Example 1: Basic File Operations")
    print("=" * 80 + "\n")
    
    agent = create_universal_agent()
    
    print("演示任务：智能体可以执行基础的文件读写操作")
    print("Demo Task: Agent can perform basic file read/write operations")
    print("\n智能体具有以下基础工具:")
    print("Agent has the following basic tools:")
    
    tools = sorted(agent.nodes["tools"].bound._tools_by_name.keys())
    for tool in tools:
        print(f"  - {tool}")
    
    print("\n这些工具支持:")
    print("These tools support:")
    print("  ✓ 分块读取大文件 (offset/limit 参数)")
    print("  ✓ Chunked reading of large files (offset/limit parameters)")
    print("  ✓ 创建和编辑文件")
    print("  ✓ Creating and editing files")
    print("  ✓ 文件搜索和模式匹配")
    print("  ✓ File search and pattern matching")
    print("  ✓ 任务规划和委托")
    print("  ✓ Task planning and delegation")


def example_progressive_loading():
    """示例：渐进式工具加载 / Example: Progressive tool loading."""
    print("\n" + "=" * 80)
    print("示例 2: 渐进式工具加载 / Example 2: Progressive Tool Loading")
    print("=" * 80 + "\n")
    
    # 阶段 1: 基础智能体 / Stage 1: Basic agent
    print("阶段 1: 创建基础智能体（仅文件操作）")
    print("Stage 1: Create basic agent (file operations only)")
    basic_agent = create_universal_agent()
    basic_tools = set(basic_agent.nodes["tools"].bound._tools_by_name.keys())
    print(f"  工具数量 / Tool count: {len(basic_tools)}")
    print(f"  工具列表 / Tools: {', '.join(sorted(basic_tools))}")
    
    # 阶段 2: 添加命令执行 / Stage 2: Add command execution
    print("\n阶段 2: 添加命令执行功能")
    print("Stage 2: Add command execution capability")
    workspace = "/tmp/universal_agent_workspace"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    exec_agent = create_universal_agent(
        enable_execution=True,
        workspace_dir=workspace
    )
    exec_tools = set(exec_agent.nodes["tools"].bound._tools_by_name.keys())
    print(f"  工具数量 / Tool count: {len(exec_tools)}")
    
    if "execute" in exec_tools:
        print("  ✓ 命令执行工具已加载")
        print("  ✓ Command execution tool loaded")
    
    # 阶段 3: 添加搜索功能 / Stage 3: Add search capability
    print("\n阶段 3: 添加搜索功能（如果配置了 API key）")
    print("Stage 3: Add search capability (if API key configured)")
    
    import os
    if os.environ.get("TAVILY_API_KEY"):
        search_agent = create_universal_agent(
            enable_search=True,
            enable_execution=True,
            workspace_dir=workspace
        )
        search_tools = set(search_agent.nodes["tools"].bound._tools_by_name.keys())
        print(f"  工具数量 / Tool count: {len(search_tools)}")
        
        if "internet_search" in search_tools:
            print("  ✓ 搜索工具已加载")
            print("  ✓ Search tool loaded")
    else:
        print("  ⚠ 跳过：未设置 TAVILY_API_KEY")
        print("  ⚠ Skipped: TAVILY_API_KEY not set")
    
    print("\n总结 / Summary:")
    print("  渐进式加载允许根据需求动态配置智能体能力")
    print("  Progressive loading allows dynamic configuration of agent capabilities")
    print("  基础工具始终可用，高级功能按需启用")
    print("  Basic tools always available, advanced features enabled on-demand")


def example_chunked_reading():
    """示例：分块文件读取 / Example: Chunked file reading."""
    print("\n" + "=" * 80)
    print("示例 3: 分块文件读取 / Example 3: Chunked File Reading")
    print("=" * 80 + "\n")
    
    # 创建测试文件 / Create test file
    workspace = "/tmp/universal_agent_chunked"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    test_file = Path(workspace) / "large_data.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        for i in range(500):
            f.write(f"Line {i+1}: This is data entry number {i+1}\n")
    
    print(f"创建了包含 500 行的测试文件")
    print(f"Created test file with 500 lines")
    print(f"文件路径 / File path: {test_file}")
    
    agent = create_universal_agent(workspace_dir=workspace)
    
    print("\n智能体可以使用分块读取策略:")
    print("Agent can use chunked reading strategy:")
    print("  1. read_file(path, limit=50) - 读取前50行")
    print("     read_file(path, limit=50) - Read first 50 lines")
    print("  2. read_file(path, offset=50, limit=50) - 读取第51-100行")
    print("     read_file(path, offset=50, limit=50) - Read lines 51-100")
    print("  3. 继续按需读取... / Continue reading as needed...")
    
    print("\n这避免了将整个大文件加载到上下文中")
    print("This avoids loading entire large files into context")


def example_backend_options():
    """示例：后端选项 / Example: Backend options."""
    print("\n" + "=" * 80)
    print("示例 4: 后端配置选项 / Example 4: Backend Configuration Options")
    print("=" * 80 + "\n")
    
    print("选项 1: 状态后端（默认）")
    print("Option 1: State Backend (Default)")
    print("  - 临时存储，仅在对话期间保留")
    print("  - Ephemeral storage, persists only during conversation")
    print("  - 适合一次性任务")
    print("  - Suitable for one-time tasks")
    
    state_agent = create_universal_agent()
    print("  ✓ 状态后端智能体已创建")
    print("  ✓ State backend agent created")
    
    print("\n选项 2: 文件系统后端")
    print("Option 2: Filesystem Backend")
    print("  - 持久化存储到真实文件系统")
    print("  - Persistent storage to real filesystem")
    print("  - 支持命令执行")
    print("  - Supports command execution")
    print("  - 适合需要持久化的项目")
    print("  - Suitable for projects requiring persistence")
    
    workspace = "/tmp/universal_agent_persistent"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    fs_agent = create_universal_agent(workspace_dir=workspace)
    print(f"  ✓ 文件系统后端智能体已创建")
    print(f"  ✓ Filesystem backend agent created")
    print(f"  工作目录 / Workspace: {workspace}")


def example_use_cases():
    """示例：实际应用场景 / Example: Real-world use cases."""
    print("\n" + "=" * 80)
    print("示例 5: 实际应用场景 / Example 5: Real-world Use Cases")
    print("=" * 80 + "\n")
    
    print("场景 1: 研究报告生成")
    print("Use Case 1: Research Report Generation")
    print("  任务 / Task:")
    print("    研究某个技术主题，撰写结构化报告")
    print("    Research a technical topic, write structured report")
    print("  工具需求 / Tools needed:")
    print("    - 文件操作（保存报告）")
    print("    - File operations (save report)")
    print("    - 搜索功能（如需最新信息）")
    print("    - Search (if latest info needed)")
    print("    - 任务规划（复杂研究）")
    print("    - Task planning (complex research)")
    
    print("\n场景 2: 数据分析")
    print("Use Case 2: Data Analysis")
    print("  任务 / Task:")
    print("    分析 CSV/JSON 文件，生成统计报告")
    print("    Analyze CSV/JSON files, generate statistical report")
    print("  工具需求 / Tools needed:")
    print("    - 分块文件读取（大数据文件）")
    print("    - Chunked file reading (large data files)")
    print("    - 命令执行（数据处理脚本）")
    print("    - Command execution (data processing scripts)")
    print("    - 文件操作（保存结果）")
    print("    - File operations (save results)")
    
    print("\n场景 3: 代码项目管理")
    print("Use Case 3: Code Project Management")
    print("  任务 / Task:")
    print("    组织项目文件，创建文档，运行测试")
    print("    Organize project files, create docs, run tests")
    print("  工具需求 / Tools needed:")
    print("    - 文件操作（创建/编辑文件）")
    print("    - File operations (create/edit files)")
    print("    - glob/grep（查找文件和代码）")
    print("    - glob/grep (find files and code)")
    print("    - 命令执行（运行构建和测试）")
    print("    - Command execution (run builds and tests)")
    print("    - 子智能体（委托专门任务）")
    print("    - Sub-agents (delegate specialized tasks)")
    
    print("\n场景 4: 文档生成")
    print("Use Case 4: Documentation Generation")
    print("  任务 / Task:")
    print("    从代码生成 API 文档，创建教程")
    print("    Generate API docs from code, create tutorials")
    print("  工具需求 / Tools needed:")
    print("    - 文件操作（读取代码，写文档）")
    print("    - File operations (read code, write docs)")
    print("    - grep（查找文档注释）")
    print("    - grep (find doc comments)")
    print("    - 任务规划（组织文档结构）")
    print("    - Task planning (organize doc structure)")


def main():
    """运行所有示例 / Run all examples."""
    print("\n" + "=" * 80)
    print("通用智能体完整使用示例 / Universal Agent Complete Usage Examples")
    print("=" * 80)
    
    examples = [
        ("基础文件操作", example_file_operations),
        ("渐进式工具加载", example_progressive_loading),
        ("分块文件读取", example_chunked_reading),
        ("后端配置选项", example_backend_options),
        ("实际应用场景", example_use_cases),
    ]
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ 示例 '{name}' 失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("示例演示完成 / Examples Demonstration Complete")
    print("=" * 80)
    
    print("\n开始使用 / Get Started:")
    print("  from examples.universal_agent import create_universal_agent")
    print("  agent = create_universal_agent()")
    print("  result = agent.invoke({'messages': [{'role': 'user', 'content': '你的任务'}]})")
    print()


if __name__ == "__main__":
    main()
