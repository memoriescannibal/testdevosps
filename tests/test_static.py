from pathlib import Path

SITE = Path("site")


def test_index_exists():
    assert (SITE / "index.html").exists()


def test_index_is_html():
    text = (SITE / "index.html").read_text()
    assert "<!doctype html>" in text.lower()
    assert '<meta charset="utf-8">' in text.lower()
    assert "<title>Mini service — static</title>" in text
    assert "<h1>Mini service</h1>" in text


def test_404_exists():
    assert (SITE / "404.html").exists()
