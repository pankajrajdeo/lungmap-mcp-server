# ================================================================================
# lungmap_get_dataset_details.py
# ================================================================================

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import MAX_LIMITS, ResponseFormat

class GetDatasetDetailsInput(BaseModel):
    dataset_id: str = Field(..., description="The LungMAP ID for the dataset (e.g., 'LMEX0000000661').")
    include_images: bool = Field(False, description="Set to true to find associated images.")
    include_image_files: bool = Field(False, description="When `include_images` is true, set this to true to also find files for each image.")
    include_files: bool = Field(False, description="Set to true to find files associated with the parent dataset.")
    include_resources: bool = Field(False, description="Set to true to find related resources like technologies, sites, and researchers.")
    response_format: ResponseFormat = Field(default=ResponseFormat.DETAILED, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")

@tool
def lungmap_get_dataset_details(
    dataset_id: str,
    include_images: bool = False,
    include_image_files: bool = False,
    include_files: bool = False,
    include_resources: bool = False,
    response_format: str = "detailed"
) -> Dict[str, Any]:
    """Retrieves comprehensive details for a SINGLE dataset, including files, images, and metadata.

    USE THIS WHEN:
    - You have a SINGLE dataset_id and need all associated information.
    - You need to find raw data files, images, or external database links (e.g., GEO).
    - You are doing a deep-dive into one specific dataset.

    DO NOT USE WHEN:
    - You are searching or filtering for datasets. Use `lungmap_search_datasets` instead.
    - You need to get information for multiple datasets at once. Use `lungmap_search_datasets` with a list of `dataset_ids`.

    Args:
        dataset_id: The LungMAP dataset ID (e.g., "LMEX0000000661")
        include_images: Include image metadata and thumbnails (adds ~200-500 tokens)
        include_image_files: Include image file details and OMERO links (adds ~100-300 tokens)
        include_files: Include raw data files and external database links (adds ~50-200 tokens)
        include_resources: Include researcher, site, and technology information (adds ~50-150 tokens)
        response_format: Response detail level - options: 'concise', 'detailed'
    """
    # Create input object from parameters
    inputs = GetDatasetDetailsInput(
        dataset_id=dataset_id,
        include_images=include_images,
        include_image_files=include_image_files,
        include_files=include_files,
        include_resources=include_resources,
        response_format=ResponseFormat(response_format)
    )
    """WARNING: Setting all 'include_*' flags to True can result in a very large response."""
    try:
        base_record_data = make_api_call(f"/id/{inputs.dataset_id}", {}, "lungmap_get_dataset_details")
        if not base_record_data or not isinstance(base_record_data, list) or not base_record_data:
            error_message = (
                f"Dataset ID '{inputs.dataset_id}' not found. \n\n"
                f"Next steps:\n"
                f"• Verify the ID starts with 'LMEX'\n"
                f"• Use `lungmap_search_datasets()` to find valid dataset IDs"
            )
            return create_standard_response(success=False, error=error_message, query_params={"dataset_id": inputs.dataset_id})
        
        base_record = base_record_data[0]
        results = {"base_record": base_record}
        metadata = {"dataset_id": inputs.dataset_id, "warnings": []}

        if inputs.include_images:
            images_data = make_api_call("/images", {"dataset_ids[]": [inputs.dataset_id], "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details")
            if isinstance(images_data, list) and images_data:
                if len(images_data) == MAX_LIMITS['metadata']: metadata["warnings"].append(f"Image list truncated to {MAX_LIMITS['metadata']}. Dataset may have more images.")
                if inputs.include_image_files:
                    image_ids = [img['image_id'] for img in images_data]
                    image_files_data = make_api_call("/images/files", {"image_ids[]": image_ids, "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details")
                    if isinstance(image_files_data, list):
                        files_by_image = {img_id: [] for img_id in image_ids}
                        for f in image_files_data: files_by_image.setdefault(f.get('image_id'), []).append(f)
                        for img in images_data: img['files'] = files_by_image.get(img['image_id'], [])
                results['images'] = images_data

        if inputs.include_files:
            files_data = make_api_call("/datasets/files", {"dataset_ids[]": [inputs.dataset_id], "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details")
            if isinstance(files_data, list):
                if len(files_data) == MAX_LIMITS['metadata']: metadata["warnings"].append(f"File list truncated to {MAX_LIMITS['metadata']}. Dataset may have more files.")
                results['files'] = files_data

        if inputs.include_resources:
            results['resources'] = {
                "technologies": make_api_call("/technologies", {"dataset_ids[]": [inputs.dataset_id], "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details"),
                "sites": make_api_call("/sites", {"dataset_ids[]": [inputs.dataset_id], "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details"),
                "researchers": make_api_call("/datasets/researchers", {"dataset_ids[]": [inputs.dataset_id], "limit": MAX_LIMITS['metadata']}, "lungmap_get_dataset_details")
            }

        # Convert enum to string value for serialization
        query_params = inputs.model_dump()
        query_params['response_format'] = inputs.response_format.value
        
        return create_standard_response(success=True, data=results, query_params=query_params, metadata=metadata)
        
    except Exception as e:
        # Convert enum to string value for serialization
        query_params = inputs.model_dump()
        query_params['response_format'] = inputs.response_format.value
        
        return handle_api_error(e, "lungmap_get_dataset_details", query_params)
