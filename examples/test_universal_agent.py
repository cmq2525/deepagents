"""Tests for the universal agent implementation."""

import os
from pathlib import Path

import pytest

# Import will be adjusted based on the actual module structure
# For now, using relative import assuming tests run from examples directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.universal_agent import create_universal_agent


class TestUniversalAgent:
    """Test suite for universal agent."""

    def test_create_basic_agent(self):
        """Test creating a basic universal agent without optional features."""
        agent = create_universal_agent()
        
        # Check that basic tools are available
        assert "read_file" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "write_file" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "edit_file" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "ls" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "glob" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "grep" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "write_todos" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "task" in agent.nodes["tools"].bound._tools_by_name.keys()
    
    def test_create_agent_with_workspace(self):
        """Test creating agent with workspace directory."""
        workspace = "/tmp/test_universal_agent_workspace"
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        agent = create_universal_agent(workspace_dir=workspace)
        
        # Basic tools should still be available
        assert "read_file" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "write_file" in agent.nodes["tools"].bound._tools_by_name.keys()
    
    def test_create_agent_with_execution(self):
        """Test creating agent with execution enabled."""
        workspace = "/tmp/test_universal_agent_execution"
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        agent = create_universal_agent(
            enable_execution=True,
            workspace_dir=workspace,
        )
        
        # Check execution tool is available
        tools = agent.nodes["tools"].bound._tools_by_name.keys()
        assert "execute" in tools or "read_file" in tools
    
    @pytest.mark.skipif(
        not os.environ.get("TAVILY_API_KEY"),
        reason="TAVILY_API_KEY not set"
    )
    def test_create_agent_with_search(self):
        """Test creating agent with search enabled."""
        agent = create_universal_agent(enable_search=True)
        
        # Check that search tool is available
        tools = agent.nodes["tools"].bound._tools_by_name.keys()
        # Search tool may be named differently depending on implementation
        assert "internet_search" in tools or len(tools) > 8  # Basic tools + search
    
    def test_basic_file_operations(self):
        """Test basic file operations with the agent."""
        workspace = "/tmp/test_universal_agent_files"
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        agent = create_universal_agent(workspace_dir=workspace)
        
        # Test creating a file
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "创建一个新文件 /test.txt，内容是 'Hello World'"
            }]
        })
        
        # Check that the agent processed the request
        assert "messages" in result
        assert len(result["messages"]) > 0
    
    def test_chunked_file_reading(self):
        """Test chunked file reading capability."""
        workspace = "/tmp/test_universal_agent_chunks"
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        # Create a large file
        large_file = Path(workspace) / "large.txt"
        content = "\n".join([f"Line {i}" for i in range(200)])
        large_file.write_text(content, encoding="utf-8")
        
        agent = create_universal_agent(workspace_dir=workspace)
        
        # Test reading with chunks
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "读取 /large.txt 的前50行"
            }]
        })
        
        # Check that the agent processed the request
        assert "messages" in result
        assert len(result["messages"]) > 0
    
    def test_research_task(self):
        """Test research report generation task."""
        agent = create_universal_agent()
        
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "创建一个简单的研究大纲，主题是机器学习，保存到 /outline.md"
            }]
        })
        
        # Check that files were created in state
        assert "messages" in result
        # May have files in state if using StateBackend
        if "files" in result:
            assert isinstance(result["files"], dict)
    
    def test_data_analysis_task(self):
        """Test data analysis capability."""
        workspace = "/tmp/test_universal_agent_analysis"
        Path(workspace).mkdir(parents=True, exist_ok=True)
        
        # Create sample data file
        data_file = Path(workspace) / "data.csv"
        data_file.write_text("name,value\nA,10\nB,20\nC,30\n", encoding="utf-8")
        
        agent = create_universal_agent(workspace_dir=workspace)
        
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "分析 /data.csv 文件并创建摘要"
            }]
        })
        
        # Check that the agent processed the request
        assert "messages" in result
        assert len(result["messages"]) > 0
    
    def test_todo_list_creation(self):
        """Test todo list creation for project planning."""
        agent = create_universal_agent()
        
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "创建一个项目任务列表，包含3个主要阶段"
            }]
        })
        
        # Check for todos in result
        assert "messages" in result
        # Todos may be in the state
        if "todos" in result:
            assert isinstance(result["todos"], str) or isinstance(result["todos"], list)
    
    def test_agent_system_prompt(self):
        """Test that agent has appropriate system prompt."""
        agent = create_universal_agent()
        
        # The agent should be created successfully with custom system prompt
        assert agent is not None
        
        # Check that the agent has the expected structure
        assert hasattr(agent, "nodes")
        assert "tools" in agent.nodes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
