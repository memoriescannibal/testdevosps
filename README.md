# Mini service: static site + GitHub Pages

Проект переделан из FastAPI-сервиса в минимальный статический сайт.

## Что изменилось

- FastAPI, Docker и GHCR больше не нужны.
- Содержимое для публикации лежит в `site/`.
- GitHub Actions публикует `site/` через GitHub Pages.
- До деплоя CI проверяет структуру и содержимое сайта.
- После деплоя CI запускает автотесты против реального URL Pages и проверяет HTTP-заголовки:
  - `Content-Type` должен быть `text/html`;
  - `Cache-Control` должен содержать `max-age=600`;
  - URL деплоя должен использовать HTTPS.

GitHub Pages не предоставляет `.htaccess`/аналог для произвольной настройки response headers, поэтому тесты проверяют заголовки, которые реально отдаёт Pages, а не пытаются задать их в HTML.

## Запуск тестов локально

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest tests/test_static.py
```

Для проверки заголовков уже опубликованного сайта:

```bash
BASE_URL="https://<owner>.github.io/<repository>/" pytest tests/test_headers.py
```

## GitHub Pages

В репозитории откройте **Settings → Pages** и выберите **GitHub Actions** как Source.

Дальше push в `main` запускает:

```text
test → deploy → deployed-header-tests
```

GitHub Pages официально поддерживает публикацию статических файлов через `configure-pages`, `upload-pages-artifact` и `deploy-pages`.
