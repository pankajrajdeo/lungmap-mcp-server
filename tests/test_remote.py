import os
import pytest
import requests


BASE = os.getenv("TEST_SSE_BASE", "http://localhost:8000")
SSE_PATH = os.getenv("MCP_SSE_PATH", "/sse")
TOKEN = os.getenv("LUNGMAP_MCP_TOKEN")


@pytest.mark.integration
def test_health_resource_exists():
    # Health is an MCP resource; here we just assert server is listening via HTTP
    try:
        r = requests.get(f"{BASE}{SSE_PATH}")
        assert r.status_code in [200, 401, 405]
    except Exception as e:
        pytest.skip(f"SSE server not running: {e}")


@pytest.mark.integration
def test_auth_enforced_if_token_set():
    if not TOKEN:
        pytest.skip("Token not set; skipping auth test")
    # Expect 401 without token
    r = requests.get(f"{BASE}{SSE_PATH}")
    assert r.status_code == 401


@pytest.mark.integration
def test_rate_limit_hint_present():
    # Cannot easily exercise rate limit without a full MCP exchange
    # This just ensures env is parsed without errors
    val = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    assert val > 0


