# ================================================================================
# lungmap_get_infrastructure_resources.py
# ================================================================================

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import MAX_LIMITS, ResponseFormat

class ResourceType(str, Enum):
    RESEARCHERS = "researchers"
    SITES = "sites"
    TOOLS = "tools"

class GetInfrastructureResourcesInput(BaseModel):
    resource_type: ResourceType = Field(..., description="The type of resource to query.")
    resource_ids: Optional[List[str]] = Field(default=None, description="A list of specific resource IDs to retrieve.")
    site_ids: Optional[List[str]] = Field(default=None, description="SITE/RESEARCHER ONLY. Filter by site IDs.")
    response_format: ResponseFormat = Field(default=ResponseFormat.CONCISE, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")
    limit: int = Field(default=10, description=f"Maximum number of results to return. Max value is {MAX_LIMITS['resources']}.", gt=0, le=MAX_LIMITS["resources"])

@tool
def lungmap_get_infrastructure_resources(
    resource_type: str,
    resource_ids: Optional[List[str]] = None,
    site_ids: Optional[List[str]] = None,
    response_format: str = "concise",
    limit: int = 10
) -> Dict[str, Any]:
    """Look up LungMAP infrastructure resources like researchers, sites, and tools.

    USE THIS WHEN:
    - Finding who conducted research (researchers).
    - Identifying which institutions contributed data (sites).
    - Discovering what software or technologies were used (tools, technologies).

    DO NOT USE for biological data like datasets, samples, or genes. Use `lungmap_search_datasets` for that.

    Args:
        resource_type: Type of resource to retrieve - options: 'researchers', 'sites', 'tools'
        resource_ids: List of specific resource IDs to retrieve (e.g., ["LMRS0000000174"])
        site_ids: Filter resources by site IDs (e.g., ["LMSI0000000026"])
        response_format: Response detail level - options: 'concise', 'detailed'
        limit: Maximum number of resources to return (max value is 50)
    """
    # Create input object from parameters
    inputs = GetInfrastructureResourcesInput(
        resource_type=ResourceType(resource_type),
        resource_ids=resource_ids,
        site_ids=site_ids,
        response_format=ResponseFormat(response_format),
        limit=limit
    )
    params = {"limit": inputs.limit}
    endpoint = f"/{inputs.resource_type.value}"
    if inputs.resource_ids: params[f"{inputs.resource_type.value[:-1]}_ids[]"] = inputs.resource_ids
    if inputs.resource_type in [ResourceType.RESEARCHERS, ResourceType.SITES] and inputs.site_ids: params["site_ids[]"] = inputs.site_ids
    
    try:
        results = make_api_call(endpoint, params, "lungmap_get_infrastructure_resources")
        if not results and isinstance(results, list):
            return create_standard_response(success=True, data=[], query_params=params, metadata={"message": "No resources found for the given criteria."})

        if inputs.response_format == ResponseFormat.CONCISE and isinstance(results, list):
            results = [{k: v for k, v in item.items() if k in ["id", "label"]} for item in results]

        return create_standard_response(success=True, data=results, query_params=params)
    except Exception as e:
        return handle_api_error(e, "lungmap_get_infrastructure_resources", params)