# 🫁 LungMAP MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A **Model Context Protocol (MCP) server** that provides AI assistants with powerful tools to access the **Lung Molecular Atlas Program (LungMAP)** API for lung research data discovery and analysis.

## 🚀 Quick Start

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

## 💡 Usage Examples

### Search for Datasets
```python
search_datasets(
    text_query="lung development",
    species="human", 
    dataset_types=["rna_seq"],
    limit=5
)
```

### Comprehensive Gene Search
```python
search_datasets(
    text_query="ACE2",
    include_genes=True,
    include_analysis_entities=True,
    include_anatomy=True
)
```

### Get Dataset Details
```python
get_dataset_details(
    dataset_id="LMEX0000000661",
    include_files=True,
    include_images=True,
    include_resources=True
)
```

### Explore Analysis Results
```python
get_analysis_results(
    dataset_ids=["LMEX0000000661"],
    detail_level="comprehensive",
    analyses_limit=5
)
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