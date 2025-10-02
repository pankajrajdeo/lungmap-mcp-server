# ================================================================================
# api_client.py
# ================================================================================

"""
Centralized API client for LungMAP tools.
Provides consistent error handling and response formatting across all tools.
Adds connection pooling, retries, and timeouts for production robustness.
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import logging
from typing import List, Dict, Any, Optional, Union
import json
from .constants import BASE_URL, DEFAULT_FORMAT, ERROR_MESSAGES
from .types import StandardResponse, ResponseMetadata


class LungMAPAPIError(Exception):
    """Custom exception for LungMAP API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


_session: Optional[requests.Session] = None
_cache: Dict[str, Any] = {}
_cache_expiry: Dict[str, float] = {}
_CACHE_TTL_SECONDS = 60.0
logger = logging.getLogger("lungmap_mcp.api_client")


def _get_session() -> requests.Session:
    """Create or return a shared HTTP session with retries and pooling."""
    global _session
    if _session is None:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        _session = session
    return _session


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
        session = _get_session()
        # Build cache key
        key = f"{endpoint}|{json.dumps(params, sort_keys=True)}"
        now = time.time()
        if key in _cache and _cache_expiry.get(key, 0) > now:
            return _cache[key]

        start = time.time()
        response = session.get(
            f"{BASE_URL}{endpoint}", params=params, timeout=30
        )
        # Handle 404 explicitly as not found
        if response.status_code == 404:
            raise LungMAPAPIError(
                f"{tool_name}: Resource not found at {endpoint}",
                status_code=404,
            )
        response.raise_for_status()
        data = response.json()
        duration = (time.time() - start) * 1000.0
        logger.info(f"GET {endpoint} {response.status_code} in {duration:.1f}ms")
        # Cache successful 200s only
        if response.status_code == 200:
            _cache[key] = data
            _cache_expiry[key] = now + _CACHE_TTL_SECONDS
        return data

    except requests.exceptions.HTTPError as http_err:
        status = getattr(http_err.response, "status_code", None) if hasattr(http_err, "response") else response.status_code if 'response' in locals() else None
        # Avoid leaking internal details; provide concise status-based messages
        if status and status >= 500:
            error_msg = f"{tool_name}: Upstream service temporarily unavailable (HTTP {status})"
        else:
            error_msg = f"{tool_name}: Request failed with status {status or 'unknown'}"
        raise LungMAPAPIError(error_msg, status)

    except requests.exceptions.RequestException as req_err:
        error_msg = f"{tool_name}: Network error: {req_err}"
        raise LungMAPAPIError(error_msg)

    except Exception as e:
        error_msg = f"{tool_name}: Unexpected error: {e}"
        raise LungMAPAPIError(error_msg)


MAX_RESPONSE_SIZE_BYTES = 100_000


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
    
    # Enforce a soft response size limit to avoid overwhelming clients
    try:
        serialized = json.dumps(response)
        if len(serialized.encode("utf-8")) > MAX_RESPONSE_SIZE_BYTES:
            # Replace data with a guidance error
            return {
                "success": False,
                "data": None,
                "error": f"Response too large. Please narrow your query or lower limits.",
                "query_params": query_params or {},
                "metadata": {"truncated": True, "hint": "Use more specific filters or smaller limits."}
            }
    except Exception:
        # If size check fails, return original response
        pass

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
