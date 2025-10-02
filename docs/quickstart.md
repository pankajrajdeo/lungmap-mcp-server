# Quick Start Guide

Get your LungMAP MCP Server running in 5 minutes.

## Step 1: Prepare Your Files

Create this directory structure:

```
lungmap-mcp-server/
├── lungmap_mcp_server.py
├── pyproject.toml
├── setup.sh
├── test_server.py
├── README.md
├── QUICKSTART.md
└── tools/
    ├── __init__.py
    ├── api_client.py
    ├── constants.py
    ├── types.py
    ├── lungmap_search_datasets.py
    ├── lungmap_get_dataset_details.py
    ├── lungmap_get_sample_details.py
    ├── lungmap_get_analysis_results.py
    ├── lungmap_get_molecular_entities.py
    ├── lungmap_get_infrastructure_resources.py
    ├── lungmap_list_controlled_vocabulary.py
    └── lungmap_search_media.py
```

## Step 2: Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create directories
mkdir -p tools tests
touch tools/__init__.py

# Install dependencies
pip install -e .
```

## Step 3: Test the Server

```bash
python3 test_server.py
```

You should see:
```
🧪 Testing LungMAP MCP Server
📡 Connecting to server...
✅ Connection established

🛠️  Available tools:
  • search_datasets
  • get_dataset_details
  ...
✅ All tests passed!
```

## Step 4: Use with Claude Desktop

1. Find your config file:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "lungmap": {
      "command": "python3",
      "args": ["/full/path/to/lungmap_mcp_server.py"]
    }
  }
}
```

3. Restart Claude Desktop

4. Look for the 🔌 icon indicating MCP servers are connected

## Step 5: Try It Out

In Claude, try these queries:

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

## Step 6: Use with LangChain (Optional)

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

async def main():
    server_params = StdioServerParameters(
        command="python3",
        args=["/full/path/to/lungmap_mcp_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Load tools
            tools = await load_mcp_tools(session)
            
            # Create agent
            agent = create_react_agent("openai:gpt-4", tools)
            
            # Use the agent
            response = await agent.ainvoke({
                "messages": "Find human lung development datasets"
            })
            
            print(response)

asyncio.run(main())
```

## Troubleshooting

### "Module not found" errors
```bash
# Ensure you're in the project directory
cd lungmap-mcp-server

# Reinstall
pip install -e .
```

### Server won't start
```bash
# Check Python version (must be 3.10+)
python3 --version

# Test imports manually
python3 -c "from tools.api_client import make_api_call; print('OK')"
```

### Claude Desktop not connecting
1. Use absolute paths (not ~/ or relative paths)
2. Check the Claude Desktop logs
3. Restart Claude Desktop completely
4. Verify the JSON syntax is correct

## Common Use Cases

### 1. Find Datasets
```python
search_datasets(
    text_query="SFTPC",
    species="human",
    dataset_types=["rna_seq"],
    limit=5
)
```

### 2. Deep Dive Into a Dataset
```python
get_dataset_details(
    dataset_id="LMEX0000000661",
    include_files=True,
    include_images=True
)
```

### 3. Analyze Results
```python
get_analysis_results(
    dataset_ids=["LMEX0000000661"],
    detail_level="comprehensive"
)
```

### 4. Explore Gene Lists
```python
# First, get analysis results to find entity set IDs
# Then:
get_molecular_entities(
    entity_type="entity_set",
    entity_ids=["found_entity_set_id"],
    include_members=True
)
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [LungMAP website](https://www.lungmap.net)
- Check available filters with `list_controlled_vocabulary()`
- Try the workflow prompts in Claude Desktop

## Support

- **Server issues:** Check the logs and test_server.py output
- **API questions:** Visit https://www.lungmap.net
- **MCP protocol:** Visit https://modelcontextprotocol.io

Happy researching!