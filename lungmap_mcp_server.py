"""
LungMAP MCP Server
Provides access to LungMAP API tools via Model Context Protocol
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any
import os
import json
import logging
from collections import deque
import time
from fastapi.responses import JSONResponse
from fastapi import Request

# Import all the tool modules
from tools.lungmap_search_datasets import lungmap_search_datasets
from tools.lungmap_get_dataset_details import lungmap_get_dataset_details
from tools.lungmap_get_sample_details import lungmap_get_sample_details
from tools.lungmap_get_analysis_results import lungmap_get_analysis_results
from tools.lungmap_get_molecular_entities import lungmap_get_molecular_entities
from tools.lungmap_get_infrastructure_resources import lungmap_get_infrastructure_resources
from tools.lungmap_list_controlled_vocabulary import lungmap_list_controlled_vocabulary
from tools.lungmap_search_media import lungmap_search_media

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("lungmap_mcp")

# Initialize FastMCP server
mcp = FastMCP("LungMAP")


# Simple in-process rate limiter (per-tool), 60 requests/minute
class SimpleRateLimiter:
    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.calls: Dict[str, deque] = {}

    def allow(self, key: str) -> bool:
        window_start = time.time() - 60
        q = self.calls.setdefault(key, deque())
        # Drop old timestamps
        while q and q[0] < window_start:
            q.popleft()
        if len(q) >= self.max_per_minute:
            return False
        q.append(time.time())
        return True


_rate_limiter = SimpleRateLimiter(max_per_minute=int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")))

def _rate_limit_or_error(tool_name: str) -> Dict[str, Any] | None:
    if not _rate_limiter.allow(tool_name):
        return {
            "success": False,
            "error": f"Rate limit exceeded for {tool_name}. Try again later.",
            "metadata": {"retry_after_seconds": 60}
        }
    return None

# Register all tools using the @mcp.tool() decorator
@mcp.tool()
def search_datasets(
    text_query: Optional[str] = None,
    dataset_ids: Optional[List[str]] = None,
    species: Optional[str] = None,
    dataset_types: Optional[List[str]] = None,
    sample_age_ranges: Optional[List[str]] = None,
    sample_sex: Optional[str] = None,
    include_samples: bool = False,
    include_analyses: bool = False,
    include_genes: bool = False,
    include_analysis_entities: bool = False,
    include_anatomy: bool = False,
    limit: int = 5
):
    """Search and filter LungMAP datasets, genes, and other entities. This is the primary discovery tool."""
    rl = _rate_limit_or_error("search_datasets")
    if rl: return rl
    return lungmap_search_datasets(
        text_query=text_query,
        dataset_ids=dataset_ids,
        species=species,
        dataset_types=dataset_types,
        sample_age_ranges=sample_age_ranges,
        sample_sex=sample_sex,
        include_samples=include_samples,
        include_analyses=include_analyses,
        include_genes=include_genes,
        include_analysis_entities=include_analysis_entities,
        include_anatomy=include_anatomy,
        limit=limit
    )

@mcp.tool()
def get_dataset_details(
    dataset_id: str,
    include_images: bool = False,
    include_image_files: bool = False,
    include_files: bool = False,
    include_resources: bool = False,
    response_format: str = "detailed"
):
    """Retrieves comprehensive details for a SINGLE dataset, including files, images, and metadata."""
    rl = _rate_limit_or_error("get_dataset_details")
    if rl: return rl
    return lungmap_get_dataset_details(
        dataset_id=dataset_id,
        include_images=include_images,
        include_image_files=include_image_files,
        include_files=include_files,
        include_resources=include_resources,
        response_format=response_format
    )

@mcp.tool()
def get_sample_details(
    sample_id: str,
    response_format: str = "detailed"
):
    """Retrieves detailed information for a specific LungMAP sample ID."""
    rl = _rate_limit_or_error("get_sample_details")
    if rl: return rl
    return lungmap_get_sample_details(
        sample_id=sample_id,
        response_format=response_format
    )

@mcp.tool()
def get_analysis_results(
    analysis_ids: Optional[List[str]] = None,
    dataset_ids: Optional[List[str]] = None,
    detail_level: str = "standard",
    analyses_limit: int = 5
):
    """Get computational analysis results for datasets or specific analysis IDs."""
    rl = _rate_limit_or_error("get_analysis_results")
    if rl: return rl
    return lungmap_get_analysis_results(
        analysis_ids=analysis_ids,
        dataset_ids=dataset_ids,
        detail_level=detail_level,
        analyses_limit=analyses_limit
    )

@mcp.tool()
def get_molecular_entities(
    entity_type: str,
    entity_ids: Optional[List[str]] = None,
    include_members: bool = False,
    response_format: str = "concise",
    limit: int = 10
):
    """Retrieves detailed information for specific molecular and ontological entities."""
    rl = _rate_limit_or_error("get_molecular_entities")
    if rl: return rl
    return lungmap_get_molecular_entities(
        entity_type=entity_type,
        entity_ids=entity_ids,
        include_members=include_members,
        response_format=response_format,
        limit=limit
    )

@mcp.tool()
def get_infrastructure_resources(
    resource_type: str,
    resource_ids: Optional[List[str]] = None,
    site_ids: Optional[List[str]] = None,
    response_format: str = "concise",
    limit: int = 10
):
    """Look up LungMAP infrastructure resources like researchers, sites, and tools."""
    rl = _rate_limit_or_error("get_infrastructure_resources")
    if rl: return rl
    return lungmap_get_infrastructure_resources(
        resource_type=resource_type,
        resource_ids=resource_ids,
        site_ids=site_ids,
        response_format=response_format,
        limit=limit
    )

@mcp.tool()
def list_controlled_vocabulary(
    category: str,
    response_format: str = "concise"
):
    """An internal utility tool to discover valid filter values for other tools."""
    rl = _rate_limit_or_error("list_controlled_vocabulary")
    if rl: return rl
    return lungmap_list_controlled_vocabulary(
        category=category,
        response_format=response_format
    )

@mcp.tool()
def search_media(
    media_type: str,
    file_type_ids: Optional[List[str]] = None,
    omero_ids: Optional[List[str]] = None,
    limit: int = 10,
    response_format: str = "concise"
):
    """Search for files or images across all datasets."""
    rl = _rate_limit_or_error("search_media")
    if rl: return rl
    return lungmap_search_media(
        media_type=media_type,
        file_type_ids=file_type_ids,
        omero_ids=omero_ids,
        limit=limit,
        response_format=response_format
    )

@mcp.tool()
def search(query: str, limit: int = 10) -> Dict[str, Any]:
    """Simplified search returning IDs and titles for generalized consumers (e.g., ChatGPT)."""
    rl = _rate_limit_or_error("search")
    if rl: return rl
    try:
        res = lungmap_search_datasets(
            text_query=query,
            include_genes=True,
            include_analysis_entities=True,
            include_anatomy=True,
            limit=limit,
        )
    except Exception as e:
        return {"success": False, "error": f"search failed: {e}", "query_params": {"query": query, "limit": limit}}
    items = res.get("data", []) if isinstance(res, dict) else []
    simplified = []
    for item in items or []:
        simplified.append({
            "id": item.get("dataset_id") or item.get("id"),
            "title": item.get("label") or item.get("title") or "",
            "url": f"https://www.lungmap.net/entity/{item.get('dataset_id') or item.get('id') or ''}"
        })
    return {"success": True, "data": simplified, "query_params": {"query": query, "limit": limit}}

@mcp.tool()
def fetch(id: str) -> Dict[str, Any]:
    """Fetch details for a specific LungMAP resource by ID (datasets primarily)."""
    try:
        details = lungmap_get_dataset_details(
            dataset_id=id,
            include_files=True,
            include_images=True,
            include_resources=False,
            response_format="detailed",
        )
        if not details or not details.get("success"):
            return {"success": False, "error": f"Not found: {id}", "query_params": {"id": id}}
        base = details.get("data", {}).get("base_record", {})
        return {
            "success": True,
            "data": {
                "id": id,
                "title": base.get("label", ""),
                "url": f"https://www.lungmap.net/entity/{id}",
                "record": base,
            },
            "query_params": {"id": id}
        }
    except Exception as e:
        return {"success": False, "error": f"fetch failed: {e}", "query_params": {"id": id}}

# Add prompts for common workflows
@mcp.prompt()
def search_workflow():
    """Prompt for dataset search workflow"""
    return """You are helping a researcher search the LungMAP database. 

Common workflows:
1. Start with search_datasets() to find datasets
2. Use get_dataset_details() to explore a specific dataset
3. Use get_analysis_results() to see computational results
4. Use get_sample_details() for sample information
5. Use get_infrastructure_resources() to find researchers/sites
6. Use list_controlled_vocabulary() to check valid filter values

When searching:
- Use text_query for general searches (minimum 4 characters)
- Apply filters like species, dataset_types, age_ranges for precision
- Set include_samples=True to see demographic data
- Set include_analyses=True to preview available analyses
- If unsure about filter values, call list_controlled_vocabulary() first"""

@mcp.prompt()
def analysis_workflow():
    """Prompt for analysis workflow"""
    return """You are helping a researcher analyze LungMAP data.

Analysis workflow:
1. Find datasets with search_datasets()
2. Get analysis results with get_analysis_results()
3. For gene lists, use get_molecular_entities(entity_type='entity_set')
4. Explore specific genes/proteins in the results

Detail levels for analyses:
- basic: Just metadata (~20 tokens)
- standard: Adds gene lists (~100 tokens)
- comprehensive: Adds conditions, replicates (~500 tokens)
- full: Everything including files (~1000+ tokens)"""

@mcp.prompt()
def discovery_workflow():
    """Prompt for exploratory data discovery"""
    return """You are helping a researcher explore LungMAP data.

Discovery tips:
1. Start broad with search_datasets(text_query="lung development")
2. Use filters to narrow: species, dataset_types, age_ranges
3. Include related entities: include_genes=True, include_anatomy=True
4. Follow up with detailed queries using the IDs found
5. Use search_media() to find files/images across datasets

Available dataset types:
- rna_seq, proteomics, imaging, single_cell, atac_seq, chip_seq

Available species:
- human, mouse

Media search:
- Use search_media(media_type="files") for protocols, data files
- Use search_media(media_type="images") for histology, microscopy"""

# Add resources for API documentation
@mcp.resource("lungmap://api/base_url")
def api_base_url() -> str:
    """LungMAP API base URL"""
    return "https://www.lungmap.net/api"

@mcp.resource("lungmap://api/documentation")
def api_documentation() -> str:
    """LungMAP API documentation reference"""
    return """LungMAP API Documentation

Base URL: https://www.lungmap.net/api

Main Endpoints:
- /search - Full-text search across all entities
- /datasets - List and filter datasets
- /samples - Sample metadata
- /analyses - Computational analysis results
- /controlled_vocabulary/* - Valid filter values

ID Formats:
- Datasets: LMEX* (e.g., LMEX0000000661)
- Samples: LMSP* (e.g., LMSP0000001176)
- Analyses: LMAN* (e.g., LMAN0000000037)

For more details: https://www.lungmap.net"""

# Health resource for monitoring
@mcp.resource("lungmap://health")
def health_check() -> str:
    return json.dumps({
        "status": "healthy",
        "service": "LungMAP MCP Server",
        "version": "0.1.0"
    })

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        path = os.getenv("MCP_SSE_PATH", "/sse")
        # Optional bearer token auth for SSE
        token = os.getenv("LUNGMAP_MCP_TOKEN")
        try:
            if token:
                app = mcp.get_app()
                @app.middleware("http")
                async def auth_middleware(request: Request, call_next):
                    if request.url.path.startswith(path):
                        auth = request.headers.get("authorization", "")
                        if not auth.startswith("Bearer ") or auth.split(" ", 1)[1] != token:
                            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
                    return await call_next(request)
        except Exception:
            # Fallback silently if app is unavailable in current FastMCP version
            pass
        logger.info(f"Starting MCP server (SSE) on {host}:{port}{path}")
        mcp.run(transport="sse", host=host, port=port, path=path)
    else:
        logger.info("Starting MCP server (stdio)")
        mcp.run(transport="stdio")
