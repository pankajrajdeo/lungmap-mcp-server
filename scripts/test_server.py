"""
Test script for LungMAP MCP Server
Run this to verify the server is working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the LungMAP MCP server"""
    
    print("🧪 Testing LungMAP MCP Server\n")
    
    # Get the absolute path to the server
    server_path = Path(__file__).parent / "lungmap_mcp_server.py"
    
    server_params = StdioServerParameters(
        command="python3",
        args=[str(server_path.absolute())],
    )
    
    try:
        print("📡 Connecting to server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connection established\n")
                
                # List available tools
                print("🛠️  Available tools:")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"  • {tool.name}")
                print(f"\nTotal tools: {len(tools_response.tools)}\n")
                
                # List available prompts
                print("💬 Available prompts:")
                prompts_response = await session.list_prompts()
                for prompt in prompts_response.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")
                print(f"\nTotal prompts: {len(prompts_response.prompts)}\n")
                
                # List available resources
                print("📚 Available resources:")
                resources_response = await session.list_resources()
                for resource in resources_response.resources:
                    print(f"  • {resource.uri}")
                print(f"\nTotal resources: {len(resources_response.resources)}\n")
                
                # Test a simple tool call
                print("🔍 Testing search_datasets tool...")
                tool_result = await session.call_tool(
                    "search_datasets",
                    arguments={
                        "text_query": "lung development",
                        "limit": 2
                    }
                )
                
                if tool_result.content:
                    print("✅ Tool call successful!")
                    print(f"Response length: {len(str(tool_result.content))} characters\n")
                else:
                    print("⚠️  Tool returned empty response\n")
                
                # Test getting a prompt
                print("💡 Testing search_workflow prompt...")
                prompt_result = await session.get_prompt(
                    "search_workflow"
                )
                
                if prompt_result.messages:
                    print("✅ Prompt retrieved successfully!")
                    print(f"Prompt length: {len(str(prompt_result.messages))} characters\n")
                else:
                    print("⚠️  Prompt returned empty response\n")
                
                # Test reading a resource
                print("📖 Testing api_base_url resource...")
                resource_result = await session.read_resource(
                    "lungmap://api/base_url"
                )
                
                if resource_result.contents:
                    print("✅ Resource read successfully!")
                    print(f"Resource content: {resource_result.contents[0].text}\n")
                else:
                    print("⚠️  Resource returned empty response\n")
                
                print("=" * 50)
                print("✅ All tests passed!")
                print("=" * 50)
                
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_server())
