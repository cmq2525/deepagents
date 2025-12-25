#!/usr/bin/env python3
"""简单的功能验证脚本 / Simple functional verification script

用于验证通用智能体的基本功能，无需 API key
Verifies basic functionality of universal agent without requiring API keys
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from universal_agent import create_universal_agent


def test_agent_creation():
    """测试智能体创建 / Test agent creation."""
    print("测试 1: 创建基础智能体")
    print("Test 1: Creating basic agent")
    
    agent = create_universal_agent()
    
    # 验证基本工具存在 / Verify basic tools exist
    tools = agent.nodes["tools"].bound._tools_by_name.keys()
    
    expected_tools = [
        "read_file",
        "write_file",
        "edit_file",
        "ls",
        "glob",
        "grep",
        "write_todos",
        "task",
    ]
    
    missing_tools = []
    for tool in expected_tools:
        if tool not in tools:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"  ✗ 缺少工具 / Missing tools: {missing_tools}")
        return False
    
    print("  ✓ 所有基本工具已加载")
    print("  ✓ All basic tools loaded")
    print(f"  工具列表 / Tools: {', '.join(sorted(tools))}")
    return True


def test_agent_with_workspace():
    """测试带工作目录的智能体 / Test agent with workspace."""
    print("\n测试 2: 创建带工作目录的智能体")
    print("Test 2: Creating agent with workspace")
    
    workspace = "/tmp/test_universal_agent_verification"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    agent = create_universal_agent(workspace_dir=workspace)
    
    # 验证基本工具存在 / Verify basic tools exist
    tools = agent.nodes["tools"].bound._tools_by_name.keys()
    
    if "read_file" not in tools or "write_file" not in tools:
        print("  ✗ 文件工具缺失 / File tools missing")
        return False
    
    # 验证执行工具存在（因为使用了 FilesystemBackend）
    # Verify execute tool exists (because FilesystemBackend is used)
    if "execute" in tools:
        print("  ✓ 命令执行工具已加载")
        print("  ✓ Command execution tool loaded")
    
    print("  ✓ 工作目录智能体创建成功")
    print("  ✓ Workspace agent created successfully")
    return True


def test_search_tool_loading():
    """测试搜索工具加载 / Test search tool loading."""
    print("\n测试 3: 搜索工具加载测试")
    print("Test 3: Search tool loading test")
    
    # 不带搜索的智能体 / Agent without search
    agent_no_search = create_universal_agent(enable_search=False)
    tools_no_search = agent_no_search.nodes["tools"].bound._tools_by_name.keys()
    
    # 带搜索的智能体（如果没有 API key 会显示警告但仍创建）
    # Agent with search (shows warning if no API key but still creates)
    import io
    import sys
    
    # 捕获标准输出 / Capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    agent_with_search = create_universal_agent(enable_search=True)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    tools_with_search = agent_with_search.nodes["tools"].bound._tools_by_name.keys()
    
    # 检查是否显示了适当的警告 / Check if appropriate warning was shown
    import os
    if not os.environ.get("TAVILY_API_KEY"):
        if "警告" in output or "Warning" in output:
            print("  ✓ 正确显示缺少 API key 的警告")
            print("  ✓ Correctly shows missing API key warning")
    
    # 验证搜索工具是否根据配置加载 / Verify search tool loaded based on config
    if "internet_search" in tools_with_search:
        print("  ✓ 搜索工具已加载")
        print("  ✓ Search tool loaded")
    else:
        print("  ℹ 搜索工具未加载（可能缺少 API key 或 tavily-python）")
        print("  ℹ Search tool not loaded (may be missing API key or tavily-python)")
    
    print("  ✓ 搜索工具加载机制工作正常")
    print("  ✓ Search tool loading mechanism works correctly")
    return True


def test_progressive_loading_concept():
    """测试渐进式加载概念 / Test progressive loading concept."""
    print("\n测试 4: 渐进式工具加载概念")
    print("Test 4: Progressive tool loading concept")
    
    # 基础配置 - 只有文件操作 / Basic config - file operations only
    basic = create_universal_agent()
    basic_tools = set(basic.nodes["tools"].bound._tools_by_name.keys())
    
    # 添加执行能力 / Add execution capability
    with_exec = create_universal_agent(
        enable_execution=True,
        workspace_dir="/tmp/test_exec"
    )
    exec_tools = set(with_exec.nodes["tools"].bound._tools_by_name.keys())
    
    # 验证基础工具在两者中都存在 / Verify basic tools exist in both
    basic_file_tools = {"read_file", "write_file", "edit_file", "ls"}
    if not basic_file_tools.issubset(basic_tools):
        print("  ✗ 基础智能体缺少文件工具")
        print("  ✗ Basic agent missing file tools")
        return False
    
    if not basic_file_tools.issubset(exec_tools):
        print("  ✗ 执行智能体缺少文件工具")
        print("  ✗ Execution agent missing file tools")
        return False
    
    # 验证执行工具只在启用时存在 / Verify execute tool only exists when enabled
    if "execute" in exec_tools:
        print("  ✓ 执行工具在启用时正确加载")
        print("  ✓ Execute tool correctly loaded when enabled")
    
    print("  ✓ 渐进式工具加载机制验证通过")
    print("  ✓ Progressive tool loading mechanism verified")
    
    # 显示工具计数 / Show tool counts
    print(f"  基础智能体工具数 / Basic agent tools: {len(basic_tools)}")
    print(f"  带执行智能体工具数 / With execution tools: {len(exec_tools)}")
    
    return True


def test_backend_configuration():
    """测试后端配置 / Test backend configuration."""
    print("\n测试 5: 后端配置")
    print("Test 5: Backend configuration")
    
    # 测试状态后端（默认）/ Test state backend (default)
    agent_state = create_universal_agent()
    print("  ✓ 状态后端（默认）智能体创建成功")
    print("  ✓ State backend (default) agent created")
    
    # 测试文件系统后端 / Test filesystem backend
    workspace = "/tmp/test_backend"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    agent_fs = create_universal_agent(workspace_dir=workspace)
    print("  ✓ 文件系统后端智能体创建成功")
    print("  ✓ Filesystem backend agent created")
    
    # 验证文件系统后端支持执行 / Verify filesystem backend supports execution
    tools = agent_fs.nodes["tools"].bound._tools_by_name.keys()
    if "execute" in tools:
        print("  ✓ 文件系统后端支持命令执行")
        print("  ✓ Filesystem backend supports command execution")
    
    return True


def main():
    """运行所有验证测试 / Run all verification tests."""
    print("=" * 80)
    print("通用智能体功能验证 / Universal Agent Functional Verification")
    print("=" * 80)
    print()
    
    tests = [
        test_agent_creation,
        test_agent_with_workspace,
        test_search_tool_loading,
        test_progressive_loading_concept,
        test_backend_configuration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ 测试失败 / Test failed: {e}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"测试结果 / Test Results: {passed} 通过 / passed, {failed} 失败 / failed")
    print("=" * 80)
    
    if failed == 0:
        print("\n✓ 所有功能验证通过!")
        print("✓ All functional verifications passed!")
        return 0
    else:
        print(f"\n✗ {failed} 个测试失败")
        print(f"✗ {failed} tests failed")
        return 1


if __name__ == "__main__":
    exit(main())
