"""
LungMAP MCP Server
Provides access to LungMAP API tools via Model Context Protocol
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, List

# Import all the tool modules
from tools.lungmap_search_datasets import lungmap_search_datasets
from tools.lungmap_get_dataset_details import lungmap_get_dataset_details
from tools.lungmap_get_sample_details import lungmap_get_sample_details
from tools.lungmap_get_analysis_results import lungmap_get_analysis_results
from tools.lungmap_get_molecular_entities import lungmap_get_molecular_entities
from tools.lungmap_get_infrastructure_resources import lungmap_get_infrastructure_resources
from tools.lungmap_list_controlled_vocabulary import lungmap_list_controlled_vocabulary
from tools.lungmap_search_media import lungmap_search_media

# Initialize FastMCP server
mcp = FastMCP("LungMAP")

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
    return lungmap_search_media(
        media_type=media_type,
        file_type_ids=file_type_ids,
        omero_ids=omero_ids,
        limit=limit,
        response_format=response_format
    )

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

When searching:
- Use text_query for general searches (minimum 4 characters)
- Apply filters like species, dataset_types, age_ranges for precision
- Set include_samples=True to see demographic data
- Set include_analyses=True to preview available analyses"""

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

Available dataset types:
- rna_seq, proteomics, imaging, single_cell, atac_seq, chip_seq

Available species:
- human, mouse"""

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

if __name__ == "__main__":
    # Run the server with stdio transport
    mcp.run(transport="stdio")
