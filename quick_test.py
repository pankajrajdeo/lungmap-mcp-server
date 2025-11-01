#!/usr/bin/env python3
"""
Quick test of LungMAP MCP Server
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from langchain_mcp_adapters.client import MultiServerMCPClient

async def test_lungmap():
    """Test the LungMAP MCP server."""
    print("🫁 Testing LungMAP MCP Server")
    print("=" * 50)
    
    # Configure client for LungMAP server
    server_config = {
        "lungmap": {
            "transport": "stdio",
            "command": "python",
            "args": [str(Path(__file__).parent / "lungmap_mcp_server.py")]
        }
    }
    
    print("🔗 Connecting to LungMAP MCP server...")
    client = MultiServerMCPClient(server_config)
    
    try:
        # Get available tools
        print("🛠️  Loading LungMAP tools...")
        tools = await client.get_tools()
        print(f"✅ Loaded {len(tools)} tools from LungMAP MCP server")
        
        # Display tools
        print("\n📋 Available tools:")
        for tool in tools:
            print(f"  - {tool.name}")
        
        print("\n✅ LungMAP MCP server test successful!")
        print("The server is ready to use with Claude Desktop.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_lungmap())

