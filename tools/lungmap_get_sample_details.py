# ================================================================================
# lungmap_get_sample_details.py
# ================================================================================

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import ResponseFormat

class GetSampleDetailsInput(BaseModel):
    sample_id: str = Field(..., description="The LungMAP ID for the sample (e.g., 'LMSP0000001176').")
    response_format: ResponseFormat = Field(default=ResponseFormat.DETAILED, description="CONCISE: key fields only | DETAILED: includes all IDs for follow-up queries")

@tool
def lungmap_get_sample_details(
    sample_id: str,
    response_format: str = "detailed"
) -> Dict[str, Any]:
    """Retrieves detailed information for a specific LungMAP sample ID.

    USE THIS WHEN:
    - You have a single, specific sample_id and need to know more about it.
    - You need to find the subject (donor) information or parent dataset for a known sample.

    DO NOT USE WHEN:
    - You are searching for samples based on characteristics like age or sex. Use `lungmap_search_datasets` with sample filters for that.

    Args:
        sample_id: The LungMAP sample ID (e.g., "LMSP0000000123")
        response_format: Response detail level - options: 'concise', 'detailed'
    """
    # Create input object from parameters
    inputs = GetSampleDetailsInput(
        sample_id=sample_id,
        response_format=ResponseFormat(response_format)
    )
    try:
        sample_data = make_api_call(f"/id/{inputs.sample_id}", {}, "lungmap_get_sample_details")
        
        if not sample_data or not isinstance(sample_data, list) or not sample_data:
            error_message = (
                f"Sample ID '{inputs.sample_id}' not found.\n\n"
                f"Next steps:\n"
                f"• Verify the ID starts with 'LMSP'\n"
                f"• Use `lungmap_search_datasets(include_samples=True)` to find valid sample IDs\n"
                f"• Check if you meant to use a dataset ID (starts with 'LMEX') instead"
            )
            return create_standard_response(success=False, error=error_message, query_params={"sample_id": inputs.sample_id})
        
        sample_record = sample_data[0]
        results = {"sample_record": sample_record}

        subject_id = sample_record.get('subject_id')
        if subject_id:
            subject_data = make_api_call(f"/id/{subject_id}", {}, "lungmap_get_sample_details")
            if subject_data and isinstance(subject_data, list): results['subject_record'] = subject_data[0]

        dataset_id = sample_record.get('dataset_id')
        if dataset_id:
            dataset_data = make_api_call(f"/id/{dataset_id}", {}, "lungmap_get_sample_details")
            if dataset_data and isinstance(dataset_data, list): results['dataset_record'] = dataset_data[0]

        metadata = {"sample_id": inputs.sample_id, "subject_id": subject_id, "dataset_id": dataset_id}
        next_steps = []
        if dataset_id: next_steps.append(f"Use `lungmap_get_dataset_details(dataset_id='{dataset_id}')` for more details on the parent dataset.")
        metadata["next_steps"] = next_steps

        if inputs.response_format == ResponseFormat.CONCISE:
            concise_sample = {k: v for k, v in results.get("sample_record", {}).items() if k in ["sample_id", "species_common_name", "age_range_label", "sex_label"]}
            concise_subject = {k: v for k, v in results.get("subject_record", {}).items() if k in ["subject_id", "species_common_name"]}
            concise_dataset = {k: v for k, v in results.get("dataset_record", {}).items() if k in ["dataset_id", "label"]}
            results = {"sample_record": concise_sample, "subject_record": concise_subject, "dataset_record": concise_dataset}

        return create_standard_response(success=True, data=results, query_params=inputs.model_dump(), metadata=metadata)
        
    except Exception as e:
        return handle_api_error(e, "lungmap_get_sample_details", inputs.model_dump())