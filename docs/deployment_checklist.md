# Deployment Checklist

Use this checklist to ensure your LungMAP MCP Server is properly deployed and configured.

## Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.10 or higher installed
- [ ] pip or uv package manager available
- [ ] Internet connection available
- [ ] Sufficient disk space (minimum 100MB)

### File Structure
- [ ] Project directory created
- [ ] `tools/` directory created
- [ ] `tools/__init__.py` exists
- [ ] All 8 tool files in `tools/` directory:
  - [ ] `api_client.py`
  - [ ] `constants.py`
  - [ ] `types.py`
  - [ ] `lungmap_search_datasets.py`
  - [ ] `lungmap_get_dataset_details.py`
  - [ ] `lungmap_get_sample_details.py`
  - [ ] `lungmap_get_analysis_results.py`
  - [ ] `lungmap_get_molecular_entities.py`
  - [ ] `lungmap_get_infrastructure_resources.py`
  - [ ] `lungmap_list_controlled_vocabulary.py`
  - [ ] `lungmap_search_media.py`
- [ ] `lungmap_mcp_server.py` in root directory
- [ ] `pyproject.toml` in root directory
- [ ] `README.md` exists
- [ ] `test_server.py` exists

## Installation Checklist

### Dependency Installation
- [ ] Dependencies installed (`pip install -e .`)
- [ ] No import errors when running Python
- [ ] `mcp` package version >= 1.9.1
- [ ] `requests` package installed
- [ ] `pydantic` package installed
- [ ] `langchain-core` package installed

### Verification Tests
- [ ] `python3 -c "import mcp"` succeeds
- [ ] `python3 -c "from tools.api_client import make_api_call"` succeeds
- [ ] `python3 -c "import lungmap_mcp_server"` succeeds
- [ ] `python3 test_server.py` passes all tests

## Configuration Checklist

### Path Configuration
- [ ] Absolute path to `lungmap_mcp_server.py` obtained
- [ ] If using venv: absolute path to venv Python obtained
- [ ] Paths verified (no ~/ or relative paths)
- [ ] Paths tested from command line

### Claude Desktop Configuration
- [ ] Config file location identified
- [ ] Backup of original config created
- [ ] Server configuration added to `mcpServers`
- [ ] JSON syntax validated
- [ ] Absolute paths used in configuration
- [ ] Configuration saved

### Environment Variables (if needed)
- [ ] `PYTHONPATH` set if required
- [ ] `OPENAI_API_KEY` set if using LangChain
- [ ] Any proxy settings configured

## Testing Checklist

### Server Startup Tests
- [ ] Server starts without errors
- [ ] Server responds to initialization
- [ ] No import errors in logs
- [ ] No connection errors in logs

### Tool Tests
- [ ] All 8 tools listed when server queried
- [ ] `search_datasets` tool callable
- [ ] `get_dataset_details` tool callable
- [ ] `get_sample_details` tool callable
- [ ] `get_analysis_results` tool callable
- [ ] `get_molecular_entities` tool callable
- [ ] `get_infrastructure_resources` tool callable
- [ ] `list_controlled_vocabulary` tool callable
- [ ] `search_media` tool callable

### Prompt Tests
- [ ] All 3 prompts available
- [ ] `search_workflow` prompt retrievable
- [ ] `analysis_workflow` prompt retrievable
- [ ] `discovery_workflow` prompt retrievable

### Resource Tests
- [ ] All 2 resources available
- [ ] `lungmap://api/base_url` readable
- [ ] `lungmap://api/documentation` readable

### API Connectivity Tests
- [ ] Can reach https://www.lungmap.net/api
- [ ] Search endpoint returns results
- [ ] Dataset endpoint returns results
- [ ] No rate limiting errors
- [ ] Response times reasonable (< 5 seconds)

## Claude Desktop Integration Checklist

### Initial Setup
- [ ] Claude Desktop installed
- [ ] Config file edited correctly
- [ ] Claude Desktop restarted completely
- [ ] MCP icon (🔌) visible in interface

### Connection Verification
- [ ] "lungmap" server listed in MCP servers
- [ ] Server shows as "Connected"
- [ ] No error messages in server list
- [ ] Claude Desktop logs show successful connection

### Functional Testing
- [ ] Ask "What tools are available?" - Claude lists LungMAP tools
- [ ] Ask "Search for lung datasets" - Claude uses search_datasets tool
- [ ] Ask "Get details for LMEX0000000661" - Claude uses get_dataset_details
- [ ] Verify tool responses appear in chat
- [ ] Check that responses contain actual data

## LangChain Integration Checklist

### Installation
- [ ] `langchain-mcp-adapters` installed
- [ ] `langgraph` installed
- [ ] `langchain-openai` installed (if using OpenAI)
- [ ] API keys configured

### Integration Tests
- [ ] Tools load successfully with `load_mcp_tools()`
- [ ] Agent creation succeeds
- [ ] Agent can invoke tools
- [ ] Responses formatted correctly
- [ ] No timeout errors

## Performance Checklist

### Response Times
- [ ] Server startup < 3 seconds
- [ ] Tool initialization < 1 second
- [ ] Simple queries < 5 seconds
- [ ] Complex queries < 15 seconds
- [ ] No hanging requests

### Resource Usage
- [ ] Memory usage reasonable (< 500MB)
- [ ] CPU usage normal (< 50% sustained)
- [ ] No memory leaks over time
- [ ] Logs don't grow excessively

## Security Checklist

### File Permissions
- [ ] Server file not world-writable
- [ ] Config file not world-readable
- [ ] Virtual environment isolated
- [ ] No sensitive data in logs

### API Access
- [ ] Using HTTPS for API calls
- [ ] No API keys hardcoded
- [ ] Rate limiting respected
- [ ] Error messages don't leak sensitive info

## Documentation Checklist

### User Documentation
- [ ] README.md is clear and complete
- [ ] QUICKSTART.md provides fast path
- [ ] INSTALLATION.md covers all scenarios
- [ ] Examples work as documented

### Technical Documentation
- [ ] All tools have docstrings
- [ ] Parameter descriptions are accurate
- [ ] Return types documented
- [ ] Edge cases documented

## Maintenance Checklist

### Regular Checks
- [ ] Test server weekly
- [ ] Check for dependency updates monthly
- [ ] Verify API still accessible
- [ ] Review logs for errors
- [ ] Test after system updates

### Update Process
- [ ] Backup current configuration
- [ ] Update dependencies safely
- [ ] Test after updates
- [ ] Roll back if issues found
- [ ] Document any changes

## Troubleshooting Reference

### Quick Diagnostic Commands

```bash
# Check Python version
python3 --version

# Test imports
python3 -c "import mcp; import requests; import pydantic; print('OK')"

# Test server module
python3 -c "import lungmap_mcp_server; print('OK')"

# Test API connection
curl "https://www.lungmap.net/api/datasets?limit=1"

# Run full test suite
python3 test_server.py

# Check Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Common Issues Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Import errors | `pip install --force-reinstall -e .` |
| Server won't start | Check paths are absolute |
| Claude not connecting | Restart Claude Desktop completely |
| API errors | Check internet connection |
| Permission denied | `chmod 644 lungmap_mcp_server.py` |
| Tools not found | Verify `tools/__init__.py` exists |

## Sign-Off

### Deployment Sign-Off

- [ ] All checklist items completed
- [ ] Tests passing consistently
- [ ] Documentation reviewed
- [ ] Users can connect successfully
- [ ] Ready for production use

### Post-Deployment

- [ ] Monitoring in place
- [ ] Support contacts documented
- [ ] Escalation path defined
- [ ] Feedback mechanism established

**Deployed by:** ________________  
**Date:** ________________  
**Version:** 0.1.0  
**Environment:** ________________

## Support Information

- **Documentation:** README.md, QUICKSTART.md, INSTALLATION.md
- **Test Script:** `python3 test_server.py`
- **Log Location:** Check Claude Desktop logs or `/tmp/lungmap_mcp_server.log`
- **LungMAP API:** https://www.lungmap.net
- **MCP Protocol:** https://modelcontextprotocol.io

## Notes

Use this space for deployment-specific notes:

```
[Add any environment-specific configuration notes here]
```
