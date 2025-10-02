# LungMAP MCP Server

A Model Context Protocol (MCP) server that provides access to the LungMAP (Lung Molecular Atlas Program) API tools for lung research data discovery and analysis.

## Features

### 8 Powerful Tools

1. **search_datasets** - Primary discovery tool for datasets, genes, and entities
2. **get_dataset_details** - Comprehensive details for a single dataset
3. **get_sample_details** - Sample metadata and donor information
4. **get_analysis_results** - Computational analysis results and gene lists
5. **get_molecular_entities** - Gene sets, probes, cell types, anatomy terms
6. **get_infrastructure_resources** - Researchers, sites, and technologies
7. **list_controlled_vocabulary** - Valid filter values for searches
8. **search_media** - Files and images across all datasets

### 3 Workflow Prompts

- **search_workflow** - Guide for dataset discovery
- **analysis_workflow** - Guide for data analysis
- **discovery_workflow** - Guide for exploratory research

### 2 Resource Endpoints

- **lungmap://api/base_url** - API base URL
- **lungmap://api/documentation** - API documentation reference

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Setup

1. **Clone or create the project directory:**

```bash
mkdir lungmap-mcp-server
cd lungmap-mcp-server
```

2. **Create the directory structure:**

```bash
mkdir tools
touch tools/__init__.py
```

3. **Copy all the tool files into the `tools/` directory:**

- `tools/api_client.py`
- `tools/constants.py`
- `tools/types.py`
- `tools/lungmap_search_datasets.py`
- `tools/lungmap_get_dataset_details.py`
- `tools/lungmap_get_sample_details.py`
- `tools/lungmap_get_analysis_results.py`
- `tools/lungmap_get_molecular_entities.py`
- `tools/lungmap_get_infrastructure_resources.py`
- `tools/lungmap_list_controlled_vocabulary.py`
- `tools/lungmap_search_media.py`

4. **Copy the server file and configuration:**

- `lungmap_mcp_server.py` (root directory)
- `pyproject.toml` (root directory)

5. **Install dependencies:**

Using pip:
```bash
pip install -e .
```

Using uv (recommended):
```bash
uv pip install -e .
```

## Running the Server

### Standalone (stdio)

Run the server directly:

```bash
python lungmap_mcp_server.py
```

### With MCP Client

For testing with an MCP client, configure your client with:

```json
{
  "mcpServers": {
    "lungmap": {
      "command": "python",
      "args": ["/absolute/path/to/lungmap_mcp_server.py"],
      "transport": "stdio"
    }
  }
}
```

### With Claude Desktop

Add to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "lungmap": {
      "command": "python",
      "args": ["/absolute/path/to/lungmap_mcp_server.py"]
    }
  }
}
```

### With LangChain/LangGraph

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

server_params = StdioServerParameters(
    command="python",
    args=["/absolute/path/to/lungmap_mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Load all LungMAP tools
        tools = await load_mcp_tools(session)
        
        # Create agent
        agent = create_react_agent("openai:gpt-4", tools)
        
        # Use the agent
        response = await agent.ainvoke({
            "messages": "Find human lung development datasets"
        })
```

## Usage Examples

### Example 1: Search for datasets

```python
# Search for RNA-seq datasets about lung development
search_datasets(
    text_query="lung development",
    species="human",
    dataset_types=["rna_seq"],
    limit=10
)
```

### Example 2: Get detailed dataset information

```python
# Get comprehensive details for a specific dataset
get_dataset_details(
    dataset_id="LMEX0000000661",
    include_files=True,
    include_images=True,
    include_resources=True
)
```

### Example 3: Analyze dataset results

```python
# Get analysis results with gene lists
get_analysis_results(
    dataset_ids=["LMEX0000000661"],
    detail_level="comprehensive",
    analyses_limit=5
)
```

### Example 4: Explore gene sets

```python
# Get members of a gene set found in analysis
get_molecular_entities(
    entity_type="entity_set",
    entity_ids=["ENTITY_SET_123"],
    include_members=True
)
```

## Project Structure

```
lungmap-mcp-server/
├── lungmap_mcp_server.py      # Main MCP server
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── tools/                      # Tool implementations
    ├── __init__.py
    ├── api_client.py           # API client utilities
    ├── constants.py            # Constants and mappings
    ├── types.py                # Type definitions
    ├── lungmap_search_datasets.py
    ├── lungmap_get_dataset_details.py
    ├── lungmap_get_sample_details.py
    ├── lungmap_get_analysis_results.py
    ├── lungmap_get_molecular_entities.py
    ├── lungmap_get_infrastructure_resources.py
    ├── lungmap_list_controlled_vocabulary.py
    └── lungmap_search_media.py
```

## API Reference

### Base URL
`https://www.lungmap.net/api`

### ID Formats
- **Datasets:** LMEX* (e.g., LMEX0000000661)
- **Samples:** LMSP* (e.g., LMSP0000001176)
- **Analyses:** LMAN* (e.g., LMAN0000000037)
- **Researchers:** LMRS* (e.g., LMRS0000000174)
- **Sites:** LMSI* (e.g., LMSI0000000026)

### Common Filters

**Species:** human, mouse

**Dataset Types:** rna_seq, proteomics, imaging, single_cell, atac_seq, chip_seq

**Age Ranges:** prenatal, newborn, infant, child, adolescent, adult, elderly

**Sex:** male, female, unknown

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
ruff check .
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. All tool files are in the `tools/` directory
2. The `tools/__init__.py` file exists
3. You've installed the package with `pip install -e .`

### Connection Issues

If the server won't start:
1. Check Python version (3.10+)
2. Verify all dependencies are installed
3. Ensure the path to `lungmap_mcp_server.py` is absolute

### API Rate Limits

The LungMAP API has rate limits. If you encounter 429 errors:
1. Reduce the `limit` parameter in queries
2. Add delays between requests
3. Cache results when possible

## Support

For issues with:
- **This MCP server:** Open an issue in the repository
- **LungMAP API:** Visit https://www.lungmap.net or https://support.lungmap.net
- **MCP Protocol:** Visit https://docs.claude.com

## License

This MCP server is provided as-is for accessing the LungMAP API. The LungMAP data and API are subject to their own terms of use.

## About LungMAP

The Lung Molecular Atlas Program (LungMAP) is an NHLBI-funded consortium focused on understanding lung development and disease through molecular profiling. Learn more at https://www.lungmap.net
