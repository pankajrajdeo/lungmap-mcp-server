# ================================================================================
# lungmap_get_molecular_entities.py
# ================================================================================

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import MAX_LIMITS, ResponseFormat

class EntityType(str, Enum):
    PROBE = "probe"
    CELL_CARD = "cell_card"
    HUMAN_ANATOMY = "human_anatomy"
    MOUSE_ANATOMY = "mouse_anatomy"
    IMAGE_ENTITY = "image_entity"
    ENTITY_SET = "entity_set"

class GetMolecularEntitiesInput(BaseModel):
    entity_type: EntityType = Field(..., description="The type of entity to query.")
    entity_ids: Optional[List[str]] = Field(default=None, description="A list of specific entity IDs to retrieve.")
    include_members: bool = Field(False, description="ENTITY_SET ONLY. Set to true to also retrieve the members of each entity set.")
    response_format: ResponseFormat = Field(default=ResponseFormat.CONCISE, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")
    limit: int = Field(default=10, description=f"Maximum number of results to return. Max value is {MAX_LIMITS['molecular']}.", gt=0, le=MAX_LIMITS["molecular"])

@tool
def lungmap_get_molecular_entities(
    entity_type: str,
    entity_ids: Optional[List[str]] = None,
    include_members: bool = False,
    response_format: str = "concise",
    limit: int = 10
) -> Dict[str, Any]:
    """Retrieves detailed information for specific molecular and ontological entities.

    USE THIS WHEN:
    - You have the ID of a gene set from `lungmap_get_analysis_results` and want to see its members.
    - You need to find details about specific probes, cell types (cell_cards), or anatomy terms.

    DO NOT USE WHEN:
    - You are searching for datasets. Use `lungmap_search_datasets`.

    Args:
        entity_type: Type of entity to retrieve - options: 'entity_set', 'probe', 'cell_card', 'human_anatomy', 'mouse_anatomy', 'image_entity'
        entity_ids: List of specific entity IDs to retrieve (e.g., ["ENTITY_SET_123"])
        include_members: Include member details for entity sets (adds ~50-200 tokens per entity)
        response_format: Response detail level - options: 'concise', 'detailed'
        limit: Maximum number of entities to return (max value is 50)
    """
    # Create input object from parameters
    inputs = GetMolecularEntitiesInput(
        entity_type=EntityType(entity_type),
        entity_ids=entity_ids,
        include_members=include_members,
        response_format=ResponseFormat(response_format),
        limit=limit
    )
    endpoint_map = {
        EntityType.PROBE: "/probes",
        EntityType.CELL_CARD: "/ontologies/cellcards",
        EntityType.HUMAN_ANATOMY: "/ontologies/lungmap_human_anatomy",
        EntityType.MOUSE_ANATOMY: "/ontologies/lungmap_mouse_anatomy",
        EntityType.IMAGE_ENTITY: "/images/entities",
        EntityType.ENTITY_SET: "/entity_sets"
    }
    endpoint = endpoint_map[inputs.entity_type]

    params = {"limit": inputs.limit}
    if inputs.entity_ids:
        id_param_key = f"{inputs.entity_type.value}_ids[]"
        if inputs.entity_type == EntityType.CELL_CARD: id_param_key = "cellcards_ids[]"
        elif inputs.entity_type in [EntityType.HUMAN_ANATOMY, EntityType.MOUSE_ANATOMY]: id_param_key = "anatomy_ids[]"
        params[id_param_key] = inputs.entity_ids

    try:
        results = make_api_call(endpoint, params, "lungmap_get_molecular_entities")
        if not results and isinstance(results, list):
            return create_standard_response(success=True, data=[], query_params=params, metadata={"message": "No entities found for the given criteria."})

        if inputs.entity_type == EntityType.ENTITY_SET and isinstance(results, list) and results and inputs.include_members:
            set_ids_found = [s['entity_set_id'] for s in results]
            members_data = make_api_call("/entity_sets/entities", {"entity_set_ids[]": set_ids_found, "limit": 200}, "lungmap_get_molecular_entities")
            if isinstance(members_data, list):
                members_by_set = {sid:[] for sid in set_ids_found}
                for member in members_data: members_by_set.setdefault(member['entity_set_id'], []).append(member)
                for s in results: s['members'] = members_by_set.get(s['entity_set_id'], [])

        if inputs.response_format == ResponseFormat.CONCISE and isinstance(results, list):
            concise_fields = ["id", "label", "description"]
            if inputs.entity_type == EntityType.ENTITY_SET: concise_fields.append("members")
            results = [{k: v for k, v in item.items() if k in concise_fields} for item in results]

        return create_standard_response(success=True, data=results, query_params=params)
    except Exception as e:
        return handle_api_error(e, "lungmap_get_molecular_entities", params)
