#!/usr/bin/env python3
"""通用智能体演示脚本 / Universal Agent Demo Script

演示如何使用通用智能体完成实际任务
Demonstrates how to use the universal agent to complete real-world tasks
"""

import os
from pathlib import Path

from examples.universal_agent import create_universal_agent


def demo_basic_research():
    """演示基础研究任务 / Demonstrate basic research task."""
    print("=" * 80)
    print("演示 1: 基础研究任务 / Demo 1: Basic Research Task")
    print("=" * 80)
    
    agent = create_universal_agent()
    
    task = """请帮我完成以下研究任务：

1. 创建一个关于"深度学习在自然语言处理中的应用"的研究大纲
2. 大纲应包括以下部分：
   - 引言
   - 主要技术（如 Transformer、BERT、GPT 等）
   - 应用场景
   - 未来展望
3. 将大纲保存到 /research_outline.md
"""
    
    print(f"\n任务: {task}\n")
    print("执行中...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 提取最终的 AI 消息
    ai_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
    if ai_messages:
        print("智能体响应:")
        print(ai_messages[-1].content)
    
    print("\n✓ 演示 1 完成\n")


def demo_data_analysis():
    """演示数据分析任务 / Demonstrate data analysis task."""
    print("=" * 80)
    print("演示 2: 数据分析任务 / Demo 2: Data Analysis Task")
    print("=" * 80)
    
    # 创建临时工作目录
    workspace = "/tmp/universal_agent_demo"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    # 创建示例数据文件
    sample_data = """日期,销售额,订单数
2024-01-01,15000,45
2024-01-02,18000,52
2024-01-03,22000,63
2024-01-04,19000,55
2024-01-05,21000,60
2024-01-06,25000,71
2024-01-07,23000,67
"""
    
    data_file = Path(workspace) / "sales_data.csv"
    data_file.write_text(sample_data, encoding="utf-8")
    
    agent = create_universal_agent(
        enable_execution=True,
        workspace_dir=workspace,
    )
    
    task = f"""请分析工作目录中的 sales_data.csv 文件：

1. 使用 read_file 读取数据（先预览前5行）
2. 计算以下统计信息：
   - 总销售额
   - 平均每日销售额
   - 平均订单数
   - 最高单日销售额
3. 生成分析报告并保存到 /analysis_report.md

工作目录: {workspace}
"""
    
    print(f"\n任务: {task}\n")
    print("执行中...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 提取最终的 AI 消息
    ai_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
    if ai_messages:
        print("智能体响应:")
        print(ai_messages[-1].content)
    
    print("\n✓ 演示 2 完成\n")


def demo_project_planning():
    """演示项目规划任务 / Demonstrate project planning task."""
    print("=" * 80)
    print("演示 3: 项目规划任务 / Demo 3: Project Planning Task")
    print("=" * 80)
    
    agent = create_universal_agent()
    
    task = """请帮我规划一个新的机器学习项目：

项目名称: 图像分类系统

要求:
1. 创建详细的任务列表（使用 write_todos）
2. 包括以下阶段：
   - 数据收集和预处理
   - 模型选择和训练
   - 模型评估和优化
   - 部署和监控
3. 每个阶段列出具体的子任务
4. 将完整的项目计划保存到 /project_plan.md
"""
    
    print(f"\n任务: {task}\n")
    print("执行中...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 提取最终的 AI 消息
    ai_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
    if ai_messages:
        print("智能体响应:")
        print(ai_messages[-1].content)
    
    # 显示任务列表
    if "todos" in result:
        print("\n创建的任务列表:")
        print(result["todos"])
    
    print("\n✓ 演示 3 完成\n")


def demo_chunked_file_processing():
    """演示分块文件处理 / Demonstrate chunked file processing."""
    print("=" * 80)
    print("演示 4: 分块文件处理 / Demo 4: Chunked File Processing")
    print("=" * 80)
    
    # 创建临时工作目录
    workspace = "/tmp/universal_agent_demo"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    # 创建大型日志文件
    large_log = ""
    for i in range(200):
        large_log += f"[2024-01-01 10:{i%60:02d}:00] INFO: Processing request #{i}\n"
        if i % 10 == 0:
            large_log += f"[2024-01-01 10:{i%60:02d}:00] ERROR: Connection timeout for request #{i}\n"
    
    log_file = Path(workspace) / "application.log"
    log_file.write_text(large_log, encoding="utf-8")
    
    agent = create_universal_agent(workspace_dir=workspace)
    
    task = f"""请分析大型日志文件 /application.log：

1. 使用分块读取策略（先读取前50行查看结构）
2. 统计错误（ERROR）数量
3. 提取前5个错误的时间戳和详情
4. 生成日志分析摘要并保存到 /log_summary.md

注意：这是一个大文件（约200行），请使用 read_file 的 offset 和 limit 参数进行分块读取。
"""
    
    print(f"\n任务: {task}\n")
    print("执行中...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 提取最终的 AI 消息
    ai_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
    if ai_messages:
        print("智能体响应:")
        print(ai_messages[-1].content)
    
    print("\n✓ 演示 4 完成\n")


def demo_search_enabled():
    """演示启用搜索的智能体 / Demonstrate agent with search enabled."""
    print("=" * 80)
    print("演示 5: 启用搜索功能 / Demo 5: Search-Enabled Agent")
    print("=" * 80)
    
    # 检查是否有 Tavily API key
    if not os.environ.get("TAVILY_API_KEY"):
        print("\n⚠ 跳过此演示: 未设置 TAVILY_API_KEY")
        print("要启用搜索功能，请设置: export TAVILY_API_KEY='your-key'")
        print("获取 API key: https://www.tavily.com/\n")
        return
    
    agent = create_universal_agent(enable_search=True)
    
    task = """请使用搜索功能研究以下主题：

主题: 2024年人工智能的主要突破

要求:
1. 搜索最新的AI技术进展
2. 总结3-5个重要突破
3. 为每个突破提供简短描述
4. 保存研究报告到 /ai_breakthroughs_2024.md
"""
    
    print(f"\n任务: {task}\n")
    print("执行中...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    
    # 提取最终的 AI 消息
    ai_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
    if ai_messages:
        print("智能体响应:")
        print(ai_messages[-1].content)
    
    print("\n✓ 演示 5 完成\n")


def main():
    """运行所有演示 / Run all demonstrations."""
    print("\n" + "=" * 80)
    print("通用智能体演示 / Universal Agent Demonstrations")
    print("=" * 80 + "\n")
    
    demos = [
        ("基础研究任务", demo_basic_research),
        ("数据分析任务", demo_data_analysis),
        ("项目规划任务", demo_project_planning),
        ("分块文件处理", demo_chunked_file_processing),
        ("启用搜索功能", demo_search_enabled),
    ]
    
    print("可用的演示:\n")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")
    
    print("\n请选择要运行的演示 (1-5, 或按 Enter 运行全部):")
    choice = input("> ").strip()
    
    if choice == "":
        # 运行所有演示
        for _, demo_func in demos:
            try:
                demo_func()
            except Exception as e:
                print(f"\n✗ 演示失败: {e}\n")
    elif choice.isdigit() and 1 <= int(choice) <= len(demos):
        # 运行选定的演示
        _, demo_func = demos[int(choice) - 1]
        try:
            demo_func()
        except Exception as e:
            print(f"\n✗ 演示失败: {e}\n")
    else:
        print("无效的选择")
    
    print("\n" + "=" * 80)
    print("演示完成 / Demonstrations Complete")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
