import os
from html.parser import HTMLParser
from urllib.request import Request, urlopen

import pytest


BASE_URL = os.getenv("BASE_URL")

pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="BASE_URL is required for deployed GitHub Pages checks",
)


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def get_page():
    request = Request(BASE_URL, method="GET")
    with urlopen(request, timeout=20) as response:
        return (
            response.status,
            {key.lower(): value for key, value in response.headers.items()},
            response.read().decode("utf-8"),
        )


def test_pages_returns_html():
    status, headers, _ = get_page()

    assert status == 200
    assert headers["content-type"].lower().startswith("text/html")


def test_pages_has_cache_control():
    _, headers, _ = get_page()

    assert "cache-control" in headers


def test_pages_uses_https():
    assert BASE_URL.lower().startswith("https://")


def test_pages_has_expected_title():
    _, _, body = get_page()
    parser = TitleParser()
    parser.feed(body)

    assert parser.title.strip() == "Mini service — static"
