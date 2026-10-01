import os
from urllib.request import Request, urlopen

import pytest


BASE_URL = os.getenv("BASE_URL")


pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="BASE_URL is required for deployed GitHub Pages header checks",
)


def get_headers():
    request = Request(BASE_URL, method="GET")
    with urlopen(request, timeout=20) as response:
        return response.status, {key.lower(): value for key, value in response.headers.items()}


def test_pages_returns_html():
    status, headers = get_headers()

    assert status == 200
    assert headers["content-type"].lower().startswith("text/html")


def test_pages_cache_header():
    _, headers = get_headers()

    assert "max-age=600" in headers["cache-control"].lower()


def test_pages_uses_https():
    assert BASE_URL.lower().startswith("https://")
