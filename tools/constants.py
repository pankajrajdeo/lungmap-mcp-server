# ================================================================================
# constants.py
# ================================================================================

"""
Centralized constants and mappings for LungMAP API tools.
All hardcoded API mappings are defined here to ensure consistency and easy maintenance.
"""

from typing import Dict, List
from enum import Enum

# Base API configuration
BASE_URL = "https://www.lungmap.net/api"
DEFAULT_FORMAT = "json"

# Error messages for consistent error handling
ERROR_MESSAGES = {
    "api_error": "API request failed",
    "network_error": "Network connection failed",
    "validation_error": "Input validation failed",
    "not_found": "Resource not found",
    "unauthorized": "Unauthorized access"
}

# Query validation constants
MIN_QUERY_LENGTH = 1  # Now accepts 1+ characters (was 4)

# Species mappings (human-readable to API taxon IDs)
# Source: NCBI taxonomy IDs used by LungMAP API
# To update: These are standard NCBI taxonomy IDs, unlikely to change
SPECIES_MAP = {
    "human": "taxid_9606",
    "mouse": "taxid_10090"
}

# Sex mappings (human-readable to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/sexes
# To update: Use get_valid_filter_values tool with VocabCategory.SEXES
SEX_MAP = {
    "male": "LMCV0000000001",
    "female": "LMCV0000000002", 
    "unknown": "LMCV0000000003"
}

# Search category mappings (human-readable to API search category IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/
# To update: Use get_valid_filter_values tool with VocabCategory.SEARCH_CATEGORIES
# or query the API directly at /api/controlled_vocabulary/search_categories
SEARCH_CATEGORY_MAP = {
    "gene": "LMSC0000000002",
    "cell_type": "LMSC0000000013", 
    "anatomy": "LMSC0000000001"
}

# Default limits for different tool types
DEFAULT_LIMITS = {
    "search": 10,
    "datasets": 5,
    "samples": 10,
    "analyses": 5,
    "molecular": 10,
    "resources": 10,
    "metadata": 5,
    "vocabulary": 500
}

# Maximum limits to prevent overwhelming responses
MAX_LIMITS = {
    "search": 100,
    "datasets": 100,
    "samples": 100,
    "analyses": 100,
    "molecular": 100,
    "resources": 100,
    "metadata": 100,
    "vocabulary": 1000
}

# Age range mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/age_ranges
AGE_RANGE_MAP = {
    "prenatal": "LMAR0000000001",
    "newborn": "LMAR0000000002", 
    "infant": "LMAR0000000003",
    "child": "LMAR0000000004",
    "adolescent": "LMAR0000000005",
    "adult": "LMAR0000000013",
    "elderly": "LMAR0000000014"
}

# Dataset type mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/dataset_types
DATASET_TYPE_MAP = {
    "rna_seq": "LMXT0000000001",
    "proteomics": "LMXT0000000015", 
    "imaging": "LMXT0000000020",
    "single_cell": "LMXT0000000025",
    "atac_seq": "LMXT0000000030",
    "chip_seq": "LMXT0000000035"
}

# Sample type mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/sample_types
SAMPLE_TYPE_MAP = {
    "whole_lung": "LMCV0000000080",
    "sorted_cells": "LMCV0000000083",
    "tissue_section": "LMCV0000000085",
    "primary_cells": "LMCV0000000087",
    "cell_line": "LMCV0000000090"
}

# Health status mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/health_statuses
HEALTH_STATUS_MAP = {
    "healthy": "LMCV0000000050",
    "diseased": "LMCV0000000051",
    "unknown": "LMCV0000000052"
}

# Race mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/races
RACE_MAP = {
    "white": "LMCV0000000013",
    "black": "LMCV0000000014", 
    "asian": "LMCV0000000015",
    "hispanic": "LMCV0000000016",
    "other": "LMCV0000000017",
    "unknown": "LMCV0000000018"
}

# Mouse strain mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/strains
STRAIN_MAP = {
    "c57bl6": "LMCV0000000070",
    "balb_c": "LMCV0000000071",
    "dba2": "LMCV0000000072",
    "fvb": "LMCV0000000073"
}

# Mouse genotype mappings (natural language to API IDs)
# Source: LungMAP controlled vocabulary API at /api/controlled_vocabulary/genotypes
GENOTYPE_MAP = {
    "wild_type": "LMCV0000000080",
    "heterozygous": "LMCV0000000081",
    "homozygous": "LMCV0000000082",
    "transgenic": "LMCV0000000083"
}

# Detail level enum for controlling response verbosity
class DetailLevel(str, Enum):
    """Control response verbosity and included data."""
    BASIC = "basic"      # Core fields only
    STANDARD = "standard"  # Includes common associations  
    FULL = "full"        # Everything available

# Response format enum for token efficiency
class ResponseFormat(str, Enum):
    """Control response detail level for token efficiency."""
    CONCISE = "concise"  # Minimal fields, ~30% of tokens
    DETAILED = "detailed"  # All fields including IDs
