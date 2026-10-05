# Digital Eye Gateway

Минимальный каркас приложения Home Assistant для ARM64 (aarch64), включая Raspberry Pi 5 с 64-битной Home Assistant OS.

Сейчас приложение только пишет сообщение о запуске и остаётся запущенным через `sleep infinity`. Подключение цифрового глазка, Firebase, видео и событий ещё не реализовано.

## Файлы

- `Dockerfile` — образ на базе `ghcr.io/home-assistant/base:latest`.
- `run.sh` — запуск через bashio.
- `config.yaml` — описание приложения Home Assistant, версия 0.1.0.
- `.github/workflows/build.yaml` — сборка, проверка запуска и публикация ARM64-образа в GHCR.

## Образ

`ghcr.io/alexmerfy/digital-eye-gateway:0.1.0`

Workflow также публикует тег `latest`. Home Assistant использует тег, совпадающий с `version` в `config.yaml`.

## Сборка

Workflow запускается при изменении файлов приложения в `main` и вручную через Actions → Build and publish ARM64 → Run workflow. Используется встроенный `GITHUB_TOKEN` с правом `packages: write`; отдельный токен не нужен.

Перед публикацией workflow проверяет архитектуру образа и запуск контейнера. Это проверка каркаса, а не работы с настоящим глазком или Home Assistant.

## Установка

После успешной публикации сделайте пакет GHCR публичным в настройках пакета, если он был создан приватным. Публичность репозитория сама по себе не гарантирует публичность контейнера.

Для локального приложения скопируйте `config.yaml`, `Dockerfile` и `run.sh` в `/addons/digital_eye_gateway/` на Home Assistant OS, обновите список локальных приложений и установите Digital Eye Gateway. Благодаря полю `image` Supervisor скачает опубликованный образ.

Не добавляйте в репозиторий Firebase credentials, service account JSON и другие секреты.
