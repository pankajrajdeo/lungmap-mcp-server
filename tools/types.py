# ================================================================================
# types.py
# ================================================================================

"""
Type definitions for LungMAP tools.

Provides TypedDict classes for better IDE support and type checking.
"""

from typing import TypedDict, List, Dict, Any, Optional, Union


class StandardResponse(TypedDict):
    """Standard response format used by all LungMAP tools."""
    success: bool
    data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]
    error: Optional[str]
    query_params: Dict[str, Any]
    metadata: Dict[str, Any]


class ResponseMetadata(TypedDict, total=False):
    """Metadata structure included in all tool responses."""
    count: int
    has_more: bool
    next_steps: List[str]
    filters_applied: Dict[str, Any]
    endpoint_used: str
    query_length: int
    data_types_filtered: Optional[List[str]]
    species_filtered: Optional[str]
    search_categories_used: Optional[List[str]]
    associated_data_included: List[str]
    resource_type: Optional[str]
    entity_type: Optional[str]
    category: Optional[str]
    total_available: int
    included_data: Dict[str, Any]
    query_type: Optional[str]
    resource_id: Optional[str]
    dataset_id: Optional[str]
    sample_id: Optional[str]
    analysis_context: bool
    dataset_context: bool
    include_members: Optional[bool]
    message: Optional[str]


class SearchMetadata(ResponseMetadata):
    """Metadata specific to search operations."""
    query_length: int
    data_types_filtered: Optional[List[str]]
    species_filtered: Optional[List[str]]
    search_categories_used: Optional[List[str]]


class DatasetMetadata(ResponseMetadata):
    """Metadata specific to dataset operations."""
    filters_applied: Dict[str, Any]
    associated_data_included: List[str]
    species_filtered: Optional[str]


class SampleMetadata(ResponseMetadata):
    """Metadata specific to sample operations."""
    endpoint_used: str
    species_filtered: Optional[str]
    dataset_context: bool
    analysis_context: bool
    filters_applied: Dict[str, Any]


class AnalysisMetadata(ResponseMetadata):
    """Metadata specific to analysis operations."""
    query_type: str
    included_data: Dict[str, Any]
    filters_applied: Dict[str, Any]


class MolecularMetadata(ResponseMetadata):
    """Metadata specific to molecular data operations."""
    entity_type: str
    endpoint_used: str
    filters_applied: Dict[str, Any]
    include_members: Optional[bool]


class ResourceMetadata(ResponseMetadata):
    """Metadata specific to resource operations."""
    resource_type: str
    endpoint_used: str
    filters_applied: Dict[str, Any]


class ValidFilterMetadata(ResponseMetadata):
    """Metadata specific to valid filter value operations."""
    category: str
    endpoint_used: str
    total_available: int


class MetadataFileMetadata(ResponseMetadata):
    """Metadata specific to metadata and file operations."""
    resource_id: str
    resource_type: str
    dataset_id: Optional[str]
    sample_id: Optional[str]
    included_data: Dict[str, Any]


# Union type for all possible metadata types
AnyMetadata = Union[
    ResponseMetadata,
    SearchMetadata,
    DatasetMetadata,
    SampleMetadata,
    AnalysisMetadata,
    MolecularMetadata,
    ResourceMetadata,
    ValidFilterMetadata,
    MetadataFileMetadata
]
