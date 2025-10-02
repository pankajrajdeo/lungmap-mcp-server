# Installation & Deployment Guide

Complete guide for setting up the LungMAP MCP Server in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Basic Installation](#basic-installation)
3. [Virtual Environment Setup](#virtual-environment-setup)
4. [Claude Desktop Configuration](#claude-desktop-configuration)
5. [LangChain Integration](#langchain-integration)
6. [Testing & Verification](#testing--verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- **Python 3.10+** - Check with `python3 --version`
- **pip** or **uv** - Package manager
- **Internet connection** - For API calls to LungMAP

### Optional

- **Claude Desktop** - For GUI interaction
- **LangChain/LangGraph** - For programmatic agent use
- **Virtual environment** - Recommended for isolation

## Basic Installation

### Step 1: Create Project Directory

```bash
mkdir lungmap-mcp-server
cd lungmap-mcp-server
```

### Step 2: Create Directory Structure

```bash
mkdir -p tools tests
touch tools/__init__.py
touch tests/__init__.py
```

### Step 3: Add Files

Place all files in the correct locations:

```
lungmap-mcp-server/
├── lungmap_mcp_server.py       # Main server file
├── pyproject.toml               # Dependencies
├── setup.sh                     # Setup script
├── test_server.py               # Test script
├── README.md
├── QUICKSTART.md
├── INSTALLATION.md
└── tools/                       # All tool files here
    ├── __init__.py
    ├── api_client.py
    ├── constants.py
    ├── types.py
    └── [8 tool files].py
```

### Step 4: Install Dependencies

**Using pip:**
```bash
pip install -e .
```

**Using uv (faster):**
```bash
pip install uv  # If not already installed
uv pip install -e .
```

**Manual installation:**
```bash
pip install "mcp>=1.9.1" "requests>=2.31.0" "pydantic>=2.0.0" "langchain-core>=0.1.0"
```

### Step 5: Verify Installation

```bash
python3 test_server.py
```

You should see all tests pass with ✅ marks.

## Virtual Environment Setup

### Using venv (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .

# Verify
python test_server.py
```

### Using conda

```bash
# Create environment
conda create -n lungmap python=3.11

# Activate
conda activate lungmap

# Install dependencies
pip install -e .

# Verify
python test_server.py
```

### Using uv

```bash
# Create and use in one go
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -e .
```

## Claude Desktop Configuration

### Step 1: Locate Config File

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Get Absolute Paths

```bash
# Get server path
cd /path/to/lungmap-mcp-server
pwd  # Copy this output

# If using venv, also get Python path
which python  # On macOS/Linux
where python  # On Windows
```

### Step 3: Edit Configuration

**Without virtual environment:**

```json
{
  "mcpServers": {
    "lungmap": {
      "command": "python3",
      "args": ["/Users/yourname/lungmap-mcp-server/lungmap_mcp_server.py"]
    }
  }
}
```

**With virtual environment:**

```json
{
  "mcpServers": {
    "lungmap": {
      "command": "/Users/yourname/lungmap-mcp-server/venv/bin/python",
      "args": ["/Users/yourname/lungmap-mcp-server/lungmap_mcp_server.py"]
    }
  }
}
```

### Step 4: Restart Claude Desktop

1. Completely quit Claude Desktop
2. Relaunch the application
3. Look for the 🔌 MCP icon in the interface
4. Click it to see "lungmap" listed

### Step 5: Test in Claude

Try asking:
```
What LungMAP tools are available?
```

```
Search for human lung development datasets
```

## LangChain Integration

### Installation

```bash
pip install langchain-mcp-adapters langgraph langchain-openai
```

### Basic Usage

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import os

async def main():
    # Set your OpenAI API key
    os.environ["OPENAI_API_KEY"] = "your-key-here"
    
    # Configure server
    server_params = StdioServerParameters(
        command="python3",
        args=["/full/path/to/lungmap_mcp_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # Load tools
            tools = await load_mcp_tools(session)
            print(f"Loaded {len(tools)} tools")
            
            # Create agent
            agent = create_react_agent("gpt-4", tools)
            
            # Query
            response = await agent.ainvoke({
                "messages": "Find human RNA-seq datasets about lung development"
            })
            
            print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### With MultiServerMCPClient

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient({
    "lungmap": {
        "command": "python3",
        "args": ["/full/path/to/lungmap_mcp_server.py"],
        "transport": "stdio",
    }
})

tools = await client.get_tools()
agent = create_react_agent("gpt-4", tools)
response = await agent.ainvoke({
    "messages": "What datasets are available?"
})
```

## Testing & Verification

### Test Server Startup

```bash
python3 test_server.py
```

Expected output:
```
🧪 Testing LungMAP MCP Server

📡 Connecting to server...
✅ Connection established

🛠️  Available tools:
  • search_datasets
  • get_dataset_details
  • get_sample_details
  • get_analysis_results
  • get_molecular_entities
  • get_infrastructure_resources
  • list_controlled_vocabulary
  • search_media

Total tools: 8

💬 Available prompts:
  • search_workflow: Prompt for dataset search workflow
  • analysis_workflow: Prompt for analysis workflow
  • discovery_workflow: Prompt for exploratory data discovery

Total prompts: 3

📚 Available resources:
  • lungmap://api/base_url
  • lungmap://api/documentation

Total resources: 2

🔍 Testing search_datasets tool...
✅ Tool call successful!

💡 Testing search_workflow prompt...
✅ Prompt retrieved successfully!

📖 Testing api_base_url resource...
✅ Resource read successfully!
Resource content: https://www.lungmap.net/api

==================================================
✅ All tests passed!
==================================================
```

### Manual Testing

Test individual components:

```bash
# Test imports
python3 -c "from tools.api_client import make_api_call; print('✅ Imports OK')"

# Test API connectivity
python3 -c "import requests; r = requests.get('https://www.lungmap.net/api/datasets', params={'limit': 1}); print('✅ API OK' if r.status_code == 200 else '❌ API Error')"

# Test server module
python3 -c "import lungmap_mcp_server; print('✅ Server module OK')"
```

### Claude Desktop Testing

1. Open Claude Desktop
2. Click the 🔌 icon (bottom right or top bar)
3. Verify "lungmap" appears in the list
4. Click "lungmap" to see tool details
5. Ask Claude: "What tools do you have available?"

### Logging Setup (Optional)

Add debug logging to server:

```python
# At the top of lungmap_mcp_server.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/lungmap_mcp_server.log'
)
logger = logging.getLogger(__name__)
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'tools'`

**Solutions:**
```bash
# Ensure you're in the project directory
cd /path/to/lungmap-mcp-server

# Reinstall
pip install -e .

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/lungmap-mcp-server"

# Verify structure
ls tools/__init__.py  # Should exist
```

### Server Won't Start

**Problem:** Server hangs or crashes on startup

**Solutions:**
```bash
# Check Python version
python3 --version  # Must be 3.10+

# Test with timeout
timeout 5 python3 lungmap_mcp_server.py

# Check for syntax errors
python3 -m py_compile lungmap_mcp_server.py

# Run with error output
python3 -u lungmap_mcp_server.py 2>&1 | tee server.log
```

### Claude Desktop Not Connecting

**Problem:** Server doesn't appear in Claude Desktop

**Solutions:**

1. **Check config file path:**
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify JSON syntax
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. **Use absolute paths:**
```json
{
  "mcpServers": {
    "lungmap": {
      "command": "/usr/local/bin/python3",  // Full path
      "args": ["/Users/name/lungmap-mcp-server/lungmap_mcp_server.py"]  // Full path
    }
  }
}
```

3. **Check Claude Desktop logs:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Look for error messages
```

4. **Restart completely:**
- Quit Claude Desktop (Cmd+Q on Mac)
- Wait 5 seconds
- Relaunch

### API Connection Issues

**Problem:** Tools return errors or empty results

**Solutions:**
```bash
# Test API directly
curl "https://www.lungmap.net/api/datasets?limit=1"

# Check internet connection
ping www.lungmap.net

# Test from Python
python3 -c "import requests; print(requests.get('https://www.lungmap.net/api/datasets', params={'limit': 1}).json())"
```

### Permission Errors

**Problem:** Permission denied errors

**Solutions:**
```bash
# Make server executable
chmod +x lungmap_mcp_server.py

# Check file ownership
ls -la lungmap_mcp_server.py

# Fix permissions
chmod 644 lungmap_mcp_server.py
```

### Virtual Environment Issues

**Problem:** Server can't find modules in venv

**Solutions:**
```bash
# Deactivate and reactivate
deactivate
source venv/bin/activate

# Reinstall in venv
pip install --force-reinstall -e .

# Use full Python path in config
which python  # Copy this path to config
```

## Platform-Specific Notes

### macOS

- Use `python3` not `python`
- Config location: `~/Library/Application Support/Claude/`
- May need to allow in Security & Privacy settings

### Windows

- Use `python` or `py` command
- Config location: `%APPDATA%\Claude\`
- Use backslashes in paths or forward slashes
- May need to run as Administrator

### Linux

- Install Python 3.10+ from package manager
- Config location: `~/.config/Claude/`
- May need to install `python3-venv` package

## Next Steps

After successful installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for usage examples
2. Read [README.md](README.md) for full documentation
3. Try the example queries in Claude Desktop
4. Explore the LungMAP API at https://www.lungmap.net

## Getting Help

- **Server issues:** Run `python3 test_server.py` and check output
- **Claude Desktop:** Check logs in `~/Library/Logs/Claude/`
- **API questions:** Visit https://www.lungmap.net
- **MCP protocol:** Visit https://modelcontextprotocol.io
