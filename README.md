# 🫁 LungMAP MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A **Model Context Protocol (MCP) server** that provides AI assistants with powerful tools to access the **Lung Molecular Atlas Program (LungMAP)** API for lung research data discovery and analysis.

## 🚀 Quick Start

### 🎥 Demo

[▶️ Watch the LungMAP MCP walkthrough](lungmap_mcp.mov)

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

### 3. Use with Claude Desktop

Add to your Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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

## 🛠️ Features

### 🔍 8 Powerful Research Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| **`search_datasets`** | Primary discovery tool | Find datasets, genes, analysis entities |
| **`get_dataset_details`** | Comprehensive dataset info | Deep dive into specific datasets |
| **`get_sample_details`** | Sample metadata | Donor information and demographics |
| **`get_analysis_results`** | Computational results | Gene lists and statistical analyses |
| **`get_molecular_entities`** | Gene sets & ontology | Gene sets, probes, anatomy terms |
| **`get_infrastructure_resources`** | Research infrastructure | Researchers, sites, technologies |
| **`list_controlled_vocabulary`** | Filter validation | Discover valid search parameters |
| **`search_media`** | Files & images | Find protocols, histology images |

### 🎯 3 Workflow Prompts

- **`search_workflow`** - Dataset discovery guidance
- **`analysis_workflow`** - Data analysis workflow  
- **`discovery_workflow`** - Exploratory research tips

### 📚 2 Resource Endpoints

- **`lungmap://api/base_url`** - API base URL reference
- **`lungmap://api/documentation`** - Complete API documentation

## 💡 Usage Examples (MCP)

Below are examples that use the MCP protocol. Tools are executed via an MCP client, not by importing Python functions directly.

### 1) Using Claude Desktop (No code)
- Add the server in Claude Desktop config (see Quick Start)
- Then ask natural language queries like:
  - "Find human RNA-seq datasets about lung development"
  - "Get details for dataset LMEX0000000661 including files and images"
  - "Search everything about ACE2"

Claude will call the MCP tools (e.g., `search_datasets`, `get_dataset_details`) behind the scenes.

### 2) Using the MCP Python Client (stdio)
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python3",
        args=["/absolute/path/to/lungmap_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Call a tool: search_datasets
            result = await session.call_tool(
                "search_datasets",
                arguments={
                    "text_query": "lung development",
                    "species": "human",
                    "dataset_types": ["rna_seq"],
                    "limit": 5,
                },
            )
            print(result.content)

            # Call a tool: get_dataset_details
            details = await session.call_tool(
                "get_dataset_details",
                arguments={
                    "dataset_id": "LMEX0000000661",
                    "include_files": True,
                    "include_images": True,
                    "include_resources": True,
                },
            )
            print(details.content)

asyncio.run(main())
```

### 3) Using LangChain MCP Adapters
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

async def main():
    server_params = StdioServerParameters(
        command="python3",
        args=["/absolute/path/to/lungmap_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Load all MCP tools as LangChain tools
            tools = await load_mcp_tools(session)

            # Create a ReAct agent and invoke it
            agent = create_react_agent("openai:gpt-4o-mini", tools)
            response = await agent.ainvoke({
                "messages": [{"role": "user", "content": "Search everything about ACE2"}]
            })
            print(response)

asyncio.run(main())
```

## 📁 Project Structure

```
lungmap-mcp-server/
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📄 pyproject.toml               # Python package config
├── 📄 lungmap_mcp_server.py        # Main MCP server
├── 📁 docs/                        # Documentation
│   ├── 📄 quickstart.md            # 5-minute setup guide
│   ├── 📄 installation_guide.md    # Detailed installation
│   ├── 📄 deployment_checklist.md  # Production checklist
│   └── 📄 mcp_config_examples.json # Configuration examples
├── 📁 scripts/                     # Utility scripts
│   ├── 🔧 setup_script.sh          # Automated setup
│   └── 🧪 test_server.py           # Server testing
├── 📁 tests/                       # Test suite
│   └── 🧪 test_tools.py            # Tool tests
└── 📁 tools/                       # Tool implementations
    ├── 📄 api_client.py            # API client utilities
    ├── 📄 constants.py             # Constants & mappings
    ├── 📄 types.py                 # Type definitions
    └── 📄 [8 lungmap tools].py     # Individual tools
```

## 🔧 Installation

### Prerequisites
- **Python 3.10+**
- **pip** or **uv** package manager

### Option 1: Quick Install
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
pip install -e .
```

### Option 2: With Virtual Environment
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Option 3: Using uv (Faster)
```bash
git clone https://github.com/pankajrajdeo/lungmap-mcp-server.git
cd lungmap-mcp-server
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 🧪 Testing

```bash
# Test server functionality
python scripts/test_server.py

# Test individual tools
python tests/test_tools.py

# Run with pytest (if installed)
pytest tests/
```

## 🔗 Integration

### Claude Desktop
See [Claude Desktop Setup Guide](docs/installation_guide.md#claude-desktop-configuration)

### LangChain/LangGraph
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

server_params = StdioServerParameters(
    command="python3",
    args=["/path/to/lungmap_mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await load_mcp_tools(session)
        # Use tools with your LangChain agent
```

## 📊 API Reference
## 🌐 Remote Deployment & Auth

Environment variables:

```bash
# Transport
MCP_TRANSPORT=sse   # or stdio
HOST=0.0.0.0
PORT=8000
MCP_SSE_PATH=/sse

# Auth (optional but recommended for SSE)
LUNGMAP_MCP_TOKEN=your-secret-token

# Rate limiting
MAX_REQUESTS_PER_MINUTE=60
```

Run with SSE locally:

```bash
MCP_TRANSPORT=sse PORT=8000 LUNGMAP_MCP_TOKEN=dev-token \
python lungmap_mcp_server.py
```

Health/resource checks via MCP client:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# For SSE, use appropriate client/URL; below shows stdio example
```

Security & limits:
- Bearer token required if `LUNGMAP_MCP_TOKEN` set.
- Per-tool rate limit defaults to 60 req/min; configure via env.
- Responses soft-capped at ~100KB; narrow queries or reduce limits if exceeded.

## 🤝 Connect Clients (ChatGPT, Claude, Cursor)

### ChatGPT (MCP over SSE)

1) Start server with SSE and token (see above)

2) Use the OpenAI Responses API with MCP tools (example):

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "o4-mini",
    "input": "Find human RNA-seq datasets about lung development",
    "tools": [{
      "type": "mcp",
      "server_label": "lungmap",
      "server_url": "http://localhost:8000/sse",
      "allowed_tools": ["search", "search_datasets", "get_dataset_details", "get_sample_details", "get_analysis_results", "get_molecular_entities", "get_infrastructure_resources", "list_controlled_vocabulary", "search_media", "fetch"],
      "require_approval": "never",
      "metadata": {
        "headers": {"Authorization": "Bearer dev-token"}
      }
    }]
  }'
```

Notes:
- `search`/`fetch` are provided for generic connectors; domain tools are also available.
- Pass the same Bearer token via `metadata.headers.Authorization`.

### Claude Desktop (Remote via @modelcontextprotocol/client)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lungmap-remote": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/client", "http://localhost:8000/sse"],
      "env": {
        "AUTHORIZATION": "Bearer dev-token"
      }
    }
  }
}
```

Then restart Claude Desktop and verify the MCP server is connected.

### Cursor / Local stdio

Add a local stdio server entry in your settings or run:

```bash
python lungmap_mcp_server.py   # stdio mode
```

Use the domain tools directly (e.g., `search_datasets`) from your agent.

## 🧪 Testing (stdio & SSE)

- Stdio test:

```bash
python scripts/test_server.py
```

- SSE integration tests (optional):

```bash
MCP_TRANSPORT=sse PORT=8000 LUNGMAP_MCP_TOKEN=dev-token \
python lungmap_mcp_server.py &

TEST_SSE_BASE=http://localhost:8000 pytest -q tests/test_remote.py
```


### Base URL
`https://www.lungmap.net/api`

### ID Formats
- **Datasets:** `LMEX*` (e.g., `LMEX0000000661`)
- **Samples:** `LMSP*` (e.g., `LMSP0000001176`) 
- **Analyses:** `LMAN*` (e.g., `LMAN0000000037`)
- **Researchers:** `LMRS*` (e.g., `LMRS0000000174`)
- **Sites:** `LMSI*` (e.g., `LMSI0000000026`)

### Common Filters
- **Species:** `human`, `mouse`
- **Dataset Types:** `rna_seq`, `proteomics`, `imaging`, `single_cell`, `atac_seq`, `chip_seq`
- **Age Ranges:** `prenatal`, `newborn`, `infant`, `child`, `adolescent`, `adult`, `elderly`
- **Sex:** `male`, `female`, `unknown`

## 🐛 Troubleshooting

### Common Issues

**❌ Import Errors**
```bash
# Ensure you're in the project directory
cd lungmap-mcp-server
pip install -e .
```

**❌ Server Won't Start**
```bash
# Check Python version
python3 --version  # Must be 3.10+

# Test server manually
python lungmap_mcp_server.py
```

**❌ Claude Desktop Not Connecting**
- Use absolute paths in config
- Restart Claude Desktop completely
- Check Claude Desktop logs

### Getting Help

- **🐛 Bug Reports:** [Open an issue](https://github.com/pankajrajdeo/lungmap-mcp-server/issues)
- **💡 Feature Requests:** [Start a discussion](https://github.com/pankajrajdeo/lungmap-mcp-server/discussions)
- **📚 LungMAP API:** [Official Documentation](https://www.lungmap.net)
- **🔧 MCP Protocol:** [MCP Documentation](https://modelcontextprotocol.io)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LungMAP Consortium** for providing the comprehensive lung research API
- **Anthropic** for the Model Context Protocol specification
- **Open Source Community** for the tools and libraries that made this possible

## 📖 About LungMAP

The **Lung Molecular Atlas Program (LungMAP)** is an NHLBI-funded consortium focused on understanding lung development and disease through molecular profiling. Learn more at [lungmap.net](https://www.lungmap.net).

---

**⭐ Star this repository if you find it useful!**
