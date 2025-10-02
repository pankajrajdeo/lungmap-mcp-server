# ================================================================================
# lungmap_get_analysis_results.py
# ================================================================================

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import DEFAULT_LIMITS, MAX_LIMITS, ResponseFormat

class AnalysisDetailLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    FULL = "full"

class GetAnalysisResultsInput(BaseModel):
    analysis_ids: Optional[List[str]] = Field(default=None, description="Specific analysis IDs to retrieve (e.g., ['LMAN0000000037']).")
    dataset_ids: Optional[List[str]] = Field(default=None, description="Get all analyses for these datasets.")
    detail_level: AnalysisDetailLevel = Field(
        default=AnalysisDetailLevel.STANDARD,
        description=(
            "Controls the level of detail in the response. Estimates are per analysis. "
            "BASIC: ~20 tokens. Just analysis metadata. "
            "STANDARD: ~100 tokens. Adds gene lists (entity sets). "
            "COMPREHENSIVE: ~500 tokens. Adds entities, conditions, and replicates. "
            "FULL: ~1000+ tokens. Adds everything, including files and all replicate data."
        )
    )
    analyses_limit: int = Field(default=5, description=f"Maximum analyses to return. Max value is {MAX_LIMITS['analyses']}.", gt=0, le=MAX_LIMITS["analyses"])

@tool
def lungmap_get_analysis_results(
    analysis_ids: Optional[List[str]] = None,
    dataset_ids: Optional[List[str]] = None,
    detail_level: str = "standard",
    analyses_limit: int = 5
) -> Dict[str, Any]:
    """Get computational analysis results for datasets or specific analysis IDs.

    USE THIS WHEN:
    - You have a dataset ID and want to see the analyses performed on it.
    - You need to find gene lists, pathways, or differential expression results.

    DO NOT USE FOR:
    - General dataset discovery. Use `lungmap_search_datasets` instead.

    Args:
        analysis_ids: List of specific analysis IDs to retrieve (e.g., ["LMAN0000000456"])
        dataset_ids: List of dataset IDs to get analyses for (e.g., ["LMEX0000000661"])
        detail_level: Analysis detail level - options: 'basic', 'standard', 'comprehensive', 'full'
        analyses_limit: Maximum number of analyses to return per dataset (max value is 20)
    """
    # Create input object from parameters
    inputs = GetAnalysisResultsInput(
        analysis_ids=analysis_ids,
        dataset_ids=dataset_ids,
        detail_level=AnalysisDetailLevel(detail_level),
        analyses_limit=analyses_limit
    )
    params = {"limit": inputs.analyses_limit}
    if inputs.analysis_ids: params["analysis_ids[]"] = inputs.analysis_ids
    if inputs.dataset_ids: params["dataset_ids[]"] = inputs.dataset_ids
    try:
        analyses_data = make_api_call("/analyses", params, "lungmap_get_analysis_results")
        if not isinstance(analyses_data, list) or not analyses_data:
            return create_standard_response(success=True, data=[], query_params=params, metadata={"message": "No analyses found for the given criteria. Try a different dataset or analysis ID."})
        
        analysis_ids_found = [a.get('analysis_id') for a in analyses_data if a.get('analysis_id')]
        
        detail_map = {
            AnalysisDetailLevel.STANDARD: {"entity_sets": True},
            AnalysisDetailLevel.COMPREHENSIVE: {"entity_sets": True, "entities": True, "conditions": True, "replicates": True},
            AnalysisDetailLevel.FULL: {"entity_sets": True, "entities": True, "conditions": True, "replicates": True, "files": True, "biological_replicates": True, "technical_replicates": True, "condition_annotations": True, "condition_tools": True}
        }
        includes = detail_map.get(inputs.detail_level, {})
        
        def fetch_and_group(endpoint, key, ids):
            data = make_api_call(endpoint, {"analysis_ids[]": ids, "limit": 1000}, "lungmap_get_analysis_results")
            if isinstance(data, list):
                by_analysis = {aid: [] for aid in ids}
                for item in data: by_analysis.setdefault(item.get('analysis_id'), []).append(item)
                for a in analyses_data: a[key] = by_analysis.get(a['analysis_id'], [])

        if includes.get("entity_sets"): fetch_and_group("/analyses/entity_sets", "entity_sets", analysis_ids_found)
        if includes.get("entities"): fetch_and_group("/analyses/entities", "entities", analysis_ids_found)
        if includes.get("conditions"): fetch_and_group("/analyses/conditions", "conditions", analysis_ids_found)
        if includes.get("replicates"): fetch_and_group("/technical_replicates", "replicates", analysis_ids_found) # Note: API uses technical_replicates for general replicate info
        if includes.get("biological_replicates"): fetch_and_group("/biological_replicates", "biological_replicates", analysis_ids_found)
        if includes.get("technical_replicates"): fetch_and_group("/technical_replicates", "technical_replicates", analysis_ids_found)
        if includes.get("files"): fetch_and_group("/analyses/files", "files", analysis_ids_found)
        if includes.get("condition_annotations"): fetch_and_group("/analyses/conditions/annotations", "condition_annotations", analysis_ids_found)
        if includes.get("condition_tools"): fetch_and_group("/analyses/conditions/tools", "condition_tools", analysis_ids_found)

        metadata = {"count": len(analyses_data), "detail_level": inputs.detail_level.value}
        if len(analyses_data) >= inputs.analyses_limit: metadata["message"] = f"Showing first {inputs.analyses_limit} of {len(analyses_data)}+ results. To see more, increase the `analyses_limit` parameter."

        return create_standard_response(success=True, data=analyses_data, query_params=params, metadata=metadata)
    except Exception as e:
        return handle_api_error(e, "lungmap_get_analysis_results", params)
