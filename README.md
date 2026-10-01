# Mini service: static site + GitHub Pages CI/CD

Минимальный статический сайт, используемый как демонстрационное приложение для тестового задания по CI/CD.

## Pipeline

Pipeline разделён на две ответственности:

```text
Pull Request / push main
        |
        v
  Quality checks
  - Ruff lint
  - Ruff format check
  - pytest
        |
        +---- main: CI only
        |
        +---- manual production deployment
                    |
                    v
              GitHub Pages
                    |
                    v
          HTTP smoke tests
```

### 1. Quality checks

На каждый Pull Request и push в `main`:

- устанавливается Python 3.12;
- устанавливаются development-зависимости;
- запускается Ruff;
- проверяется форматирование;
- запускаются тесты статического сайта.

Если проверка не проходит, production deployment недоступен.

### 2. Production deployment

Автоматического деплоя в production при push в `main` нет.

Production запускается только вручную через **Actions → CI/CD → Run workflow** с параметром `deploy_production=true`. Для дополнительной защиты рекомендуется создать GitHub Environment `production` и включить **Required reviewers**. GitHub Actions поддерживает approval gates для environments, поэтому deployment можно сделать двухшаговым: сначала workflow проходит CI, затем ответственный подтверждает публикацию.

После approval публикуется содержимое `site/` через GitHub Pages.

### 3. Post-deployment smoke tests

После публикации тесты выполняются против реального URL Pages и проверяют:

- HTTPS;
- HTTP 200;
- `Content-Type: text/html`;
- наличие `Cache-Control`;
- корректный HTML `<title>`.

Это проверяет не только исходный код, но и результат реального deployment.

## Staging / preview

GitHub Pages предоставляет один опубликованный site URL для репозитория. Отдельный `staging` environment сам по себе не создаёт второй публичный Pages URL: environment в GitHub Actions управляет approvals, protection rules и deployment history, но не является отдельным хостингом.

Поэтому для настоящего публичного staging URL я бы использовал отдельный Pages-репозиторий, например:

```text
production: https://<org>.github.io/demo-app/
staging:    https://<org>.github.io/demo-app-staging/
```

Оба репозитория могут использовать одинаковый workflow. В production deployment добавляется approval, а staging можно обновлять автоматически из `develop` или из merge в специальную staging-ветку.

Для одного тестового репозитория это сознательно не добавлено: второй Pages site потребовал бы второй репозиторий и создал бы лишнюю инфраструктуру для простой статической страницы.

## Monitoring

Для базового мониторинга production достаточно UptimeRobot:

```text
UptimeRobot
     |
     | HTTPS GET every 5 min
     v
GitHub Pages production URL
     |
     +-- HTTP 200 -> OK
     |
     +-- failure -> alert
```

Можно добавить email/Slack/Telegram уведомления после нескольких последовательных неудачных проверок. Для более сложного приложения мониторинг можно дополнить Sentry и отдельным health endpoint.

## Local checks

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest
```

Проверка deployed-версии дополнительно контролирует HTML `<title>`: `Mini service — static`. Это отделяет проверку содержимого страницы от проверки HTTP-заголовков.

Для проверки уже опубликованного сайта:

```bash
BASE_URL="https://<owner>.github.io/<repository>/" pytest tests/test_headers.py
```


## Portability

Репозиторий не содержит привязки к конкретному owner или URL: URL GitHub Pages берётся из output `actions/deploy-pages`, а smoke tests получают его через `BASE_URL`. Поэтому проект можно перенести в другой GitHub repository без изменения URL в коде.

Для нового repository требуется один раз включить **Settings → Pages → Build and deployment → Source: GitHub Actions**. Это ограничение GitHub Pages: `configure-pages` по умолчанию не включает Pages через обычный `GITHUB_TOKEN`; автоматическое enablement требует отдельного токена с расширенными правами.
