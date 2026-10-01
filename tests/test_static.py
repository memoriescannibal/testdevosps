from pathlib import Path

ROOT = Path(__file__).parents[1]
SITE = ROOT / "site"


def test_index_exists_and_contains_html():
    index = SITE / "index.html"

    assert index.is_file()
    content = index.read_text(encoding="utf-8")

    assert "<!doctype html>" in content.lower()
    assert '<meta charset="utf-8">' in content.lower()
    assert "<title>Mini service — static</title>" in content


def test_404_exists():
    assert (SITE / "404.html").is_file()


def test_pages_artifact_has_no_server_code():
    forbidden = {"Dockerfile", "requirements.txt", "app"}

    for name in forbidden:
        assert not (SITE / name).exists()
