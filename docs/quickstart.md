# 🚀 Quick Start Guide

Get your LungMAP MCP Server running in **5 minutes**.

## ⚡ Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
pip install -e .
```

### 2. Test the Server
```bash
python scripts/test_server.py
```

Expected output:
```
🧪 Testing LungMAP MCP Server
📡 Connecting to server...
✅ Connection established
🛠️  Lists available tools
✅ All tests passed!
```

### 3. Use with Claude Desktop

**Find your config file:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "lungmap": {
      "command": "python3",
      "args": ["/absolute/path/to/lungmap_mcp_server.py"]
    }
  }
}
```

**Get the absolute path:**
```bash
cd /path/to/lungmap-mcp-server
pwd  # Copy this output
```

### 4. Restart Claude Desktop
1. Quit Claude Desktop completely
2. Relaunch the application
3. Look for the 🔌 MCP icon
4. Verify "lungmap" appears in the connected servers

## 🧪 Try It Out

In Claude, ask these questions:

```
Find human RNA-seq datasets about lung development
```

```
Get details for dataset LMEX0000000661 including files and images
```

```
What analysis results are available for dataset LMEX0000000661?
```

```
Show me mouse datasets with samples from newborn mice
```

## 🔧 Advanced Setup

### With Virtual Environment
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### With uv (Faster)
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check Python version (must be 3.10+)
python3 --version

# Test imports
python3 -c "from tools.api_client import make_api_call; print('✅ OK')"

# Run with error output
python3 -u lungmap_mcp_server.py
```

### Claude Desktop Not Connecting
1. **Use absolute paths** (not ~/ or relative paths)
2. **Check JSON syntax** - validate your config file
3. **Restart Claude Desktop** completely (Cmd+Q on Mac)
4. **Check logs** in `~/Library/Logs/Claude/` (macOS)

### Import Errors
```bash
# Ensure you're in the project directory
cd lungmap-mcp-server

# Reinstall
pip install --force-reinstall -e .

# Check structure
ls tools/__init__.py  # Should exist
```

## 📚 Next Steps

- Read the full [README.md](../README.md) for comprehensive documentation
- Check [Installation Guide](installation_guide.md) for detailed setup
- Explore [Configuration Examples](mcp_config_examples.json) for different clients
- Visit [LungMAP website](https://www.lungmap.net) to learn about the data

## 🆘 Need Help?

- **🐛 Issues:** [GitHub Issues](https://github.com/pankajrajdeo/lungmap-mcp-server/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/pankajrajdeo/lungmap-mcp-server/discussions)
- **📖 LungMAP:** [Official Documentation](https://www.lungmap.net)
- **🔧 MCP:** [MCP Documentation](https://modelcontextprotocol.io)

---

**🎉 That's it! You're ready to explore lung research data with AI assistance.**