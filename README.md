# CI/CD Demo

Минимальный проект для задания CI/CD.

Pipeline:
1. Linter
2. Build image
3. Deploy STG
4. Tests STG
5. Manual Deploy PROD
6. Tests PROD

STG/PROD deployment в учебном проекте сделан как stub: workflow собирает Docker image и сохраняет его как GitHub Actions artifact. Реальный сервер можно подключить позже.

Для production рекомендуется создать GitHub Environment `production` и включить Required reviewers.
