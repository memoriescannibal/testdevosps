import os
import urllib.request


def test_deployed_site():
    url = os.environ.get("BASE_URL")
    if not url:
        return
    with urllib.request.urlopen(url, timeout=10) as response:
        assert response.status == 200
        assert "text/html" in response.headers.get("Content-Type", "")
