"""
Basic tests for LungMAP MCP Server tools
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.api_client import make_api_call
from tools.constants import BASE_URL


def test_api_client_import():
    """Test that API client can be imported"""
    from tools.api_client import make_api_call, create_standard_response
    assert callable(make_api_call)
    assert callable(create_standard_response)


def test_constants_import():
    """Test that constants can be imported"""
    from tools.constants import BASE_URL, DEFAULT_FORMAT
    assert BASE_URL == "https://www.lungmap.net/api"
    assert DEFAULT_FORMAT == "json"


def test_tools_import():
    """Test that all tools can be imported"""
    from tools.lungmap_search_datasets import lungmap_search_datasets
    from tools.lungmap_get_dataset_details import lungmap_get_dataset_details
    from tools.lungmap_get_sample_details import lungmap_get_sample_details
    from tools.lungmap_get_analysis_results import lungmap_get_analysis_results
    from tools.lungmap_get_molecular_entities import lungmap_get_molecular_entities
    from tools.lungmap_get_infrastructure_resources import lungmap_get_infrastructure_resources
    from tools.lungmap_list_controlled_vocabulary import lungmap_list_controlled_vocabulary
    from tools.lungmap_search_media import lungmap_search_media
    
    # Test that functions are callable
    assert callable(lungmap_search_datasets)
    assert callable(lungmap_get_dataset_details)
    assert callable(lungmap_get_sample_details)
    assert callable(lungmap_get_analysis_results)
    assert callable(lungmap_get_molecular_entities)
    assert callable(lungmap_get_infrastructure_resources)
    assert callable(lungmap_list_controlled_vocabulary)
    assert callable(lungmap_search_media)


def test_server_import():
    """Test that the main server can be imported"""
    import lungmap_mcp_server
    assert hasattr(lungmap_mcp_server, 'mcp')


if __name__ == "__main__":
    # Run basic tests
    test_api_client_import()
    test_constants_import()
    test_tools_import()
    test_server_import()
    print("✅ All basic tests passed!")
