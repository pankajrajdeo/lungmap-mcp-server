# ================================================================================
# api_client.py
# ================================================================================

"""
Centralized API client for LungMAP tools.
Provides consistent error handling and response formatting across all tools.
"""

import requests
from typing import List, Dict, Any, Optional, Union
from .constants import BASE_URL, DEFAULT_FORMAT, ERROR_MESSAGES
from .types import StandardResponse, ResponseMetadata


class LungMAPAPIError(Exception):
    """Custom exception for LungMAP API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


def make_api_call(
    endpoint: str, 
    params: Dict[str, Any], 
    tool_name: str = "unknown"
) -> Union[List[Dict], Dict[str, Any]]:
    """
    Centralized API call function with consistent error handling and response formatting.
    
    Args:
        endpoint: API endpoint (e.g., "/search", "/datasets")
        params: Query parameters
        tool_name: Name of the calling tool for error context
        
    Returns:
        API response data or error dictionary
        
    Raises:
        LungMAPAPIError: For API-related errors
    """
    # Ensure format is always specified
    if params is None:
        params = {}
    params['format'] = DEFAULT_FORMAT
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return []
        error_msg = f"{tool_name}: API endpoint {endpoint} returned HTTP {response.status_code}: {http_err}"
        raise LungMAPAPIError(error_msg, response.status_code)
        
    except requests.exceptions.RequestException as req_err:
        error_msg = f"{tool_name}: Request failed: {req_err}"
        raise LungMAPAPIError(error_msg)
        
    except Exception as e:
        error_msg = f"{tool_name}: Unexpected error: {e}"
        raise LungMAPAPIError(error_msg)


def create_standard_response(
    success: bool,
    data: Optional[Union[List[Dict], Dict]] = None,
    error: Optional[str] = None,
    query_params: Optional[Dict] = None,
    metadata: Optional[ResponseMetadata] = None
) -> StandardResponse:
    """
    Create a standardized response format for all tools.
    
    Args:
        success: Whether the operation was successful
        data: The actual data returned (list or dict)
        error: Error message if unsuccessful
        query_params: The parameters used in the query
        metadata: Additional metadata about the results
        
    Returns:
        Standardized response dictionary
    """
    response = {
        "success": success,
        "data": data,
        "error": error,
        "query_params": query_params or {},
        "metadata": metadata or {}
    }
    
    # Add count information if data is a list
    if success and isinstance(data, list):
        response["metadata"]["count"] = len(data)
        response["metadata"]["has_more"] = len(data) >= (query_params.get("limit", 10) if query_params else 10)
    
    return response


def handle_api_error(error: Exception, tool_name: str, query_params: Dict) -> StandardResponse:
    """
    Handle API errors and return standardized error response.
    
    Args:
        error: The exception that occurred
        tool_name: Name of the tool that failed
        query_params: The parameters that were used
        
    Returns:
        Standardized error response
    """
    if isinstance(error, LungMAPAPIError):
        error_message = error.message
        if error.status_code:
            error_message += f" (Status: {error.status_code})"
    else:
        error_message = f"{tool_name}: {str(error)}"
    
    return create_standard_response(
        success=False,
        error=error_message,
        query_params=query_params
    )
