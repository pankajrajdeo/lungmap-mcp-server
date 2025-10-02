# 📦 Installation Guide

Complete setup guide for the LungMAP MCP Server in various environments.

## 🎯 Quick Start (Recommended)

```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
pip install -e .
python scripts/test_server.py
```

## 📋 Prerequisites

- **Python 3.10+** - Check with `python3 --version`
- **pip** or **uv** - Package manager
- **Internet connection** - For API calls to LungMAP

## 🔧 Installation Options

### Option 1: Standard Installation
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
pip install -e .
```

### Option 2: Virtual Environment (Recommended)
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Option 3: Using uv (Fastest)
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Option 4: Conda Environment
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
conda create -n lungmap python=3.11
conda activate lungmap
pip install -e .
```

## 🧪 Verification

```bash
# Test server startup
python scripts/test_server.py

# Expected output:
# 🧪 Testing LungMAP MCP Server
# ✅ Connection established
# ✅ All tests passed!
```

## 🔗 Claude Desktop Integration

### 1. Locate Config File

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### 2. Get Absolute Paths
```bash
# Get server path
cd /path/to/lungmap-mcp-server
pwd  # Copy this output

# If using venv, get Python path
which python  # macOS/Linux
where python  # Windows
```

### 3. Edit Configuration

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

### 4. Restart Claude Desktop
1. **Completely quit** Claude Desktop
2. **Relaunch** the application
3. **Look for** 🔌 MCP icon in interface
4. **Verify** "lungmap" appears in connected servers

## 🐍 LangChain Integration

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

async def main():
    server_params = StdioServerParameters(
        command="python3",
        args=["/absolute/path/to/lungmap_mcp_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"Loaded {len(tools)} tools")

asyncio.run(main())
```

## 🐳 Docker Setup (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

CMD ["python", "lungmap_mcp_server.py"]
```

## 🧪 Testing & Validation

### Automated Testing
```bash
# Run all tests
python scripts/test_server.py

# Test individual components
python tests/test_tools.py

# Manual API test
python -c "import requests; r = requests.get('https://www.lungmap.net/api/datasets', params={'limit': 1}); print('✅ API OK' if r.status_code == 200 else '❌ API Error')"
```

### Claude Desktop Testing
1. Open Claude Desktop
2. Click 🔌 icon (bottom right or top bar)
3. Verify "lungmap" appears in the list
4. Ask: "What LungMAP tools are available?"

## 🐛 Troubleshooting

### Import Errors
```bash
# Problem: ModuleNotFoundError: No module named 'tools'
# Solution:
cd lungmap-mcp-server
pip install -e .
export PYTHONPATH="${PYTHONPATH}:/path/to/lungmap-mcp-server"
```

### Server Won't Start
```bash
# Problem: Server hangs or crashes
# Solution:
python3 --version  # Must be 3.10+
python3 -m py_compile lungmap_mcp_server.py
python3 -u lungmap_mcp_server.py 2>&1 | tee server.log
```

### Claude Desktop Not Connecting
```bash
# Problem: Server doesn't appear in Claude Desktop
# Solutions:
# 1. Validate JSON syntax
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Use absolute paths
{
  "mcpServers": {
    "lungmap": {
      "command": "/usr/local/bin/python3",
      "args": ["/Users/name/lungmap-mcp-server/lungmap_mcp_server.py"]
    }
  }
}

# 3. Check Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp*.log
```

### API Connection Issues
```bash
# Test API connectivity
curl "https://www.lungmap.net/api/datasets?limit=1"
ping www.lungmap.net
```

## 📱 Platform-Specific Notes

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

## ✅ Success Checklist

- [ ] Python 3.10+ installed
- [ ] Repository cloned
- [ ] Dependencies installed (`pip install -e .`)
- [ ] Server tests pass (`python scripts/test_server.py`)
- [ ] Claude Desktop config updated
- [ ] Claude Desktop restarted
- [ ] MCP server appears in Claude Desktop
- [ ] Can ask Claude about LungMAP tools

## 🆘 Getting Help

- **🐛 Server issues:** Run `python scripts/test_server.py` and check output
- **🔧 Claude Desktop:** Check logs in `~/Library/Logs/Claude/`
- **📚 API questions:** Visit [lungmap.net](https://www.lungmap.net)
- **🤖 MCP protocol:** Visit [modelcontextprotocol.io](https://modelcontextprotocol.io)

---

**🎉 Ready to explore lung research data with AI assistance!**