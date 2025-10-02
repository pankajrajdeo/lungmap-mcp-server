# ================================================================================
# lungmap_search_media.py
# ================================================================================

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import MAX_LIMITS, ResponseFormat

class MediaType(str, Enum):
    FILE = "files"
    IMAGE = "images"

class SearchMediaInput(BaseModel):
    media_type: MediaType = Field(..., description="The type of media to search for: 'files' or 'images'.")
    file_type_ids: Optional[List[str]] = Field(default=None, description="FILE ONLY. Filter by file type IDs.")
    omero_ids: Optional[List[str]] = Field(default=None, description="IMAGE ONLY. Filter by OMERO IDs.")
    limit: int = Field(default=10, description=f"Maximum number of results to return. Max value is {MAX_LIMITS['search']}.", gt=0, le=MAX_LIMITS["search"])
    response_format: ResponseFormat = Field(default=ResponseFormat.CONCISE, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")

@tool
def lungmap_search_media(
    media_type: str,
    file_type_ids: Optional[List[str]] = None,
    omero_ids: Optional[List[str]] = None,
    limit: int = 10,
    response_format: str = "concise"
) -> Dict[str, Any]:
    """Search for files or images across all datasets.

    USE THIS WHEN:
    - Looking for specific file types (e.g., 'protocol', 'image_original') across the entire database.
    - Finding images by their OMERO ID or other metadata, when you don't know the dataset.

    DO NOT USE WHEN:
    - You have a dataset ID and want its files or images (use `lungmap_get_dataset_details` for that).

    Args:
        media_type: Type of media to search for - options: 'file', 'image'
        file_type_ids: List of file type IDs to filter by (e.g., ["protocol", "image_original"])
        omero_ids: List of OMERO image IDs to retrieve specific images (e.g., ["12345", "67890"])
        limit: Maximum number of media items to return (max value is 100)
        response_format: Response detail level - options: 'concise', 'detailed'
    """
    # Create input object from parameters
    inputs = SearchMediaInput(
        media_type=MediaType(media_type),
        file_type_ids=file_type_ids,
        omero_ids=omero_ids,
        limit=limit,
        response_format=ResponseFormat(response_format)
    )
    params = {"limit": inputs.limit}
    endpoint = f"/{inputs.media_type.value}"

    if inputs.media_type == MediaType.FILE and inputs.file_type_ids:
        params["file_type_ids[]"] = inputs.file_type_ids
    if inputs.media_type == MediaType.IMAGE and inputs.omero_ids:
        params["omero_ids[]"] = inputs.omero_ids

    try:
        results = make_api_call(endpoint, params, "lungmap_search_media")
        if not results and isinstance(results, list):
            return create_standard_response(success=True, data=[], query_params=params, metadata={"message": "No media found for the given criteria."})

        if inputs.response_format == ResponseFormat.CONCISE and isinstance(results, list):
            concise_fields = ["id", "label", "path"] if inputs.media_type == MediaType.FILE else ["image_id", "omero_id", "dataset_id"]
            results = [{k: v for k, v in item.items() if k in concise_fields} for item in results]

        return create_standard_response(success=True, data=results, query_params=params)
    except Exception as e:
        return handle_api_error(e, "lungmap_search_media", params)
