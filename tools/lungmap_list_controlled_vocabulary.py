# ================================================================================
# lungmap_list_controlled_vocabulary.py
# ================================================================================

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import MAX_LIMITS, ResponseFormat

class VocabCategory(str, Enum):
    AGE_RANGES = "age_ranges"
    DATASET_TYPES = "dataset_types"
    HEALTH_STATUSES = "health_statuses"
    RACES = "races"
    SAMPLE_TYPES = "sample_types"
    SEXES = "sexes"
    SPECIES = "species"
    STRAINS = "strains"

class ListControlledVocabularyInput(BaseModel):
    category: VocabCategory = Field(..., description="The category of controlled vocabulary terms to retrieve.")
    response_format: ResponseFormat = Field(default=ResponseFormat.CONCISE, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")

@tool
def lungmap_list_controlled_vocabulary(
    category: str,
    response_format: str = "concise"
) -> Dict[str, Any]:
    """An internal utility tool to discover valid filter values for other tools.

    USE THIS WHEN:
    - You need to know the available options for a filter in another tool.
    - For example, to get a list of all possible `races` or `strains` to use in `lungmap_search_datasets`.

    DO NOT USE WHEN:
    - You are trying to find actual data. This tool only returns metadata/vocabulary.

    Args:
        category: Vocabulary category to retrieve - options: 'species', 'dataset_types', 'age_ranges', 'sample_types', 'sexes', 'races', 'strains'
        response_format: Response detail level - options: 'concise', 'detailed'
    """
    # Create input object from parameters
    inputs = ListControlledVocabularyInput(
        category=VocabCategory(category),
        response_format=ResponseFormat(response_format)
    )
    endpoint = f"/controlled_vocabulary/{inputs.category.value}"
    params = {"limit": MAX_LIMITS["vocabulary"]}
    try:
        results = make_api_call(endpoint, params, "lungmap_list_controlled_vocabulary")
        if not results and isinstance(results, list):
            return create_standard_response(success=True, data=[], query_params=params, metadata={"message": f"No vocabulary found for category: {inputs.category.value}"})
        
        if inputs.response_format == ResponseFormat.CONCISE:
            results = [{k: v for k, v in item.items() if k in ["id", "label"]} for item in results]

        return create_standard_response(success=True, data=results, query_params=params)
    except Exception as e:
        return handle_api_error(e, "lungmap_list_controlled_vocabulary", params)