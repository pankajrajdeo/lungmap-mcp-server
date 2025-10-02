# ================================================================================
# lungmap_search_datasets.py
# ================================================================================

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from langchain_core.tools import tool
from .api_client import make_api_call, create_standard_response, handle_api_error
from .constants import (
    SEARCH_CATEGORY_MAP, SPECIES_MAP, DATASET_TYPE_MAP, SAMPLE_TYPE_MAP,
    DEFAULT_LIMITS, MAX_LIMITS, ResponseFormat, DetailLevel, AGE_RANGE_MAP, SEX_MAP
)

class Species(str, Enum):
    HUMAN = "human"
    MOUSE = "mouse"

class SearchLungmapDatasetsInput(BaseModel):
    text_query: Optional[str] = Field(
        default=None,
        description=(
            "Search dataset names/descriptions. Best with 4+ characters. "
            "USE FOR: 'lung development', 'SFTPC', 'collagen'. "
            "DO NOT USE FOR: Single letters or very short terms (handled automatically)."
        )
    )
    dataset_ids: Optional[List[str]] = Field(
        default=None,
        description="Get multiple specific datasets by ID. USE WHEN: You have a list of dataset IDs. DO NOT USE WHEN: You have a single ID and need all details (use `lungmap_get_dataset_details` instead)."
    )
    species: Optional[Species] = Field(default=None, description="Filter by organism: 'human' or 'mouse'.")
    dataset_types: Optional[List[str]] = Field(default=None, description="Filter by experiment type. Options: 'rna_seq', 'proteomics', 'imaging', 'single_cell', 'atac_seq', 'chip_seq'.")
    sample_age_ranges: Optional[List[str]] = Field(default=None, description="Only return datasets containing samples in these age ranges. Options: 'prenatal', 'newborn', 'infant', 'child', 'adolescent', 'adult', 'elderly'.")
    sample_sex: Optional[str] = Field(default=None, description="Only return datasets containing samples of this sex. Options: 'male', 'female', 'unknown'.")
    include_samples: bool = Field(default=False, description="Include sample details for each dataset. Adds ~100-200 tokens per dataset.")
    include_analyses: bool = Field(default=False, description="Include analysis summaries for each dataset. Adds ~50-100 tokens per dataset.")
    include_genes: bool = Field(default=False, description="Also return gene results found in search. Adds ~50-100 tokens per gene.")
    include_analysis_entities: bool = Field(default=False, description="Also return analysis entity results found in search. Adds ~50-100 tokens per entity.")
    include_anatomy: bool = Field(default=False, description="Also return anatomy results found in search. Adds ~50-100 tokens per anatomy term.")
    limit: int = Field(default=5, description=f"Maximum datasets to return. Max value is {MAX_LIMITS['datasets']}.", gt=0, le=MAX_LIMITS["datasets"])

    @field_validator('text_query')
    @classmethod
    def sanitize_query(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v2 = v.strip()
        if not v2:
            return None
        forbidden = ['<', '>', ';', '|']
        if any(ch in v2 for ch in forbidden):
            raise ValueError("Invalid characters in query")
        return v2

@tool
def lungmap_search_datasets(
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
) -> Dict[str, Any]:
    """Search and filter LungMAP datasets, genes, and other entities. This is the primary discovery tool.
    
    USE THIS WHEN:
    - Discovering datasets using text search, filters, or both.
    - Getting multiple datasets at once by their IDs.
    - Finding datasets that contain samples with specific demographic characteristics (e.g., age, sex).
    - Searching for genes, analysis entities, or anatomy terms (use include_genes=True, etc.).
    - User asks "What about [gene/protein]?" and you want to find related entities.
    - For comprehensive/general/ambiguous queries, use include_genes=True, include_analysis_entities=True, include_anatomy=True.

    DO NOT USE WHEN:
    - You have ONE dataset_id and need all its files, images, and detailed metadata. Use `lungmap_get_dataset_details` for that.
    - You have a single sample ID. Use `lungmap_get_sample_details` instead.

    Args:
        text_query: Free-text search terms to find datasets by title, description, or keywords (minimum 4 characters)
        dataset_ids: List of specific dataset IDs to retrieve (e.g., ["LMEX0000000661", "LMEX0000000702"])
        species: Filter by species - options: 'human', 'mouse', 'rat', 'pig', 'monkey', 'rabbit'
        dataset_types: List of dataset types - options: 'rna_seq', 'microarray', 'histology', 'proteomics', 'methylation'
        sample_age_ranges: List of sample age ranges - options: 'prenatal', 'neonatal', 'pediatric', 'adult', 'unknown'
        sample_sex: Filter by sample sex - options: 'male', 'female', 'unknown'
        include_samples: Include sample details for each dataset (adds ~100-200 tokens per dataset)
        include_analyses: Include analysis summaries for each dataset (adds ~50-100 tokens per dataset)
        include_genes: Also return gene results found in search (adds ~50-100 tokens per gene)
        include_analysis_entities: Also return analysis entity results found in search (adds ~50-100 tokens per entity)
        include_anatomy: Also return anatomy results found in search (adds ~50-100 tokens per anatomy term)
        limit: Maximum datasets to return (max value is 50)
    """
    # Create input object from parameters
    inputs = SearchLungmapDatasetsInput(
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
    params = {"limit": inputs.limit}
    endpoint = "/datasets"
    metadata = {"strategy": "filter_search", "warnings": []}
    query_text = inputs.text_query.strip() if inputs.text_query else ""
    if query_text and len(query_text) < 4:
        SHORT_TERM_STRATEGIES = {
            "rna": {"dataset_types": ["rna_seq"], "hint": "RNA-seq datasets"},
            "dna": {"dataset_types": ["chip_seq", "atac_seq"], "hint": "DNA-based assays"},
            "ms": {"dataset_types": ["proteomics"], "hint": "Mass spectrometry"},
            "sc": {"dataset_types": ["single_cell"], "hint": "Single-cell experiments"},
        }
        term_lower = query_text.lower()
        if term_lower in SHORT_TERM_STRATEGIES:
            strategy = SHORT_TERM_STRATEGIES[term_lower]
            if not inputs.dataset_types: inputs.dataset_types = strategy["dataset_types"]
            metadata["strategy"] = "short_query_mapped"
            metadata["mapping"] = f"'{query_text}' → {strategy['hint']}"
            query_text = ""
        else:
            metadata["warnings"].append(f"Query '{query_text}' is very short. For better results, use longer terms or filters.")
    # Predefine optional collections to avoid undefined references later
    gene_results: List[Dict[str, Any]] = []
    analysis_results: List[Dict[str, Any]] = []
    anatomy_results: List[Dict[str, Any]] = []

    if inputs.dataset_ids:
        params["dataset_ids[]"] = inputs.dataset_ids
    elif query_text and len(query_text) >= 4:
        search_params = {"queries[]": [query_text], "limit": inputs.limit * 2}
        if inputs.species: search_params["taxon_ids[]"] = [SPECIES_MAP[inputs.species.value]]
        try:
            search_results = make_api_call("/search", search_params, "lungmap_search_datasets")
            # Filter for dataset results and extract dataset IDs
            dataset_ids_from_search = list(set(
                r.get('id') for r in search_results 
                if r.get('search_category_label') == 'Dataset' and r.get('id')
            ))
            
            # Collect additional entities that might be relevant
            gene_results = [r for r in search_results if r.get('search_category_label') == 'Gene']
            analysis_results = [r for r in search_results if r.get('search_category_label') == 'Analysis Entity']
            anatomy_results = [r for r in search_results if r.get('search_category_label') == 'Anatomy']
            if dataset_ids_from_search:
                params["dataset_ids[]"] = dataset_ids_from_search
                metadata["strategy"] = "text_search_then_filter"
            else:
                # Check if user requested additional result types
                additional_results = []
                if inputs.include_genes and gene_results:
                    additional_results.extend(gene_results[:5])  # Limit to 5 genes
                    metadata["included_genes"] = len(gene_results[:5])
                if inputs.include_analysis_entities and analysis_results:
                    additional_results.extend(analysis_results[:5])  # Limit to 5 analysis entities
                    metadata["included_analysis_entities"] = len(analysis_results[:5])
                
                # If user requested additional types and we found them, return them
                if additional_results:
                    metadata["strategy"] = "text_search_entities"
                    return create_standard_response(success=True, data=additional_results, query_params=params, metadata=metadata)
                
                # Otherwise, provide helpful guidance
                if gene_results or analysis_results:
                    guidance = []
                    if gene_results:
                        gene_names = [g.get('label', '') for g in gene_results[:3]]
                        guidance.append(f"Found {len(gene_results)} gene(s): {', '.join(gene_names)}")
                    if analysis_results:
                        guidance.append(f"Found {len(analysis_results)} analysis entities")
                    
                    metadata["message"] = f"No datasets found matching '{query_text}', but {len(gene_results + analysis_results)} related entities were found. {'. '.join(guidance)}. Try using broader terms or different filters."
                    metadata["found_genes"] = len(gene_results)
                    metadata["found_analysis_entities"] = len(analysis_results)
                else:
                    metadata["message"] = f"No datasets found matching '{query_text}'. Try broader terms or use filters."
                return create_standard_response(success=True, data=[], query_params=params, metadata=metadata)
        except Exception as e:
            metadata["warnings"].append(f"Text search failed, using filters only: {str(e)}")
    if inputs.species: params["taxon_ids[]"] = [SPECIES_MAP[inputs.species.value]]
    if inputs.dataset_types: params["dataset_type_ids[]"] = [DATASET_TYPE_MAP[dt.lower()] for dt in inputs.dataset_types if dt.lower() in DATASET_TYPE_MAP]
    if inputs.sample_age_ranges or inputs.sample_sex:
        sample_params = {"limit": 1000}
        if inputs.sample_age_ranges: sample_params["age_range_ids[]"] = [AGE_RANGE_MAP[age.lower()] for age in inputs.sample_age_ranges if age.lower() in AGE_RANGE_MAP]
        if inputs.sample_sex: sample_params["sex_ids[]"] = [SEX_MAP[inputs.sample_sex.lower()]]
        all_samples = make_api_call("/samples", sample_params, "lungmap_search_datasets")
        if isinstance(all_samples, list):
            valid_dataset_ids = set(s['dataset_id'] for s in all_samples if s.get('dataset_id'))
            if "dataset_ids[]" in params:
                params["dataset_ids[]"] = list(set(params["dataset_ids[]"]) & valid_dataset_ids)
            else:
                params["dataset_ids[]"] = list(valid_dataset_ids)
            if not params["dataset_ids[]"]:
                metadata["message"] = "No datasets found with the specified sample characteristics. Try removing sample filters."
                return create_standard_response(success=True, data=[], query_params=params, metadata=metadata)
    try:
        datasets = make_api_call(endpoint, params, "lungmap_search_datasets")
        if not datasets or not isinstance(datasets, list):
            metadata["message"] = "No datasets match your criteria. Try broadening your search."
            return create_standard_response(success=True, data=[], query_params=params, metadata=metadata)
        total_available = len(datasets)
        if len(datasets) >= inputs.limit:
            datasets = datasets[:inputs.limit]
            metadata["message"] = f"Showing first {inputs.limit} of {total_available}+ results. To get more specific results, add more filters or increase the limit."
        if inputs.include_samples:
            dataset_ids_found = [d['dataset_id'] for d in datasets]
            samples_data = make_api_call("/datasets/samples", {"dataset_ids[]": dataset_ids_found, "limit": 100}, "lungmap_search_datasets")
            if isinstance(samples_data, list):
                samples_by_dataset = {did: [] for did in dataset_ids_found}
                for s in samples_data: samples_by_dataset.setdefault(s.get('dataset_id'), []).append(s)
                for d in datasets: d['samples'] = samples_by_dataset.get(d['dataset_id'], [])
        
        # Add additional entity types if requested (always defined lists)
        all_results = datasets.copy()
        if inputs.include_genes and gene_results:
            to_add = gene_results[:3]
            all_results.extend(to_add)
            metadata["included_genes"] = len(to_add)
        if inputs.include_analysis_entities and analysis_results:
            to_add = analysis_results[:3]
            all_results.extend(to_add)
            metadata["included_analysis_entities"] = len(to_add)
        if inputs.include_anatomy and anatomy_results:
            to_add = anatomy_results[:3]
            all_results.extend(to_add)
            metadata["included_anatomy"] = len(to_add)
            
        return create_standard_response(success=True, data=all_results, query_params=params, metadata=metadata)
    except Exception as e:
        return handle_api_error(e, "lungmap_search_datasets", params)