# alfa-bank-pdp-backend

# Запуск

1. Создайте копии файлов `.env.template` в теже папки где они находятся (`/infra` и `/src`) и переименуйте в `.env`.
2. Выполнить команду `make up` из корня проекта (билдит docker образы и запускает контейнеры в соответствии с `docker-compose.yaml` из папки `/infra`)
3. http://localhost/openapi

> Перед запуском проверьте, что порты указанные в файлах `.env` не заняты системой

# Dev

## Перед началом работы

- Установить poetry https://python-poetry.org/docs/#installation
- Изменить настройки poetry для хранения виртуального окружения командой `poetry config virtualenvs.in-project true`
- Выполнить команду `poetry install` для установки зависимостей
- Выполнить команду `poetry shell` для активации виртуального окружения
- Выполнить команду `pre-commit install` для инициализации pre-commit (запускает во время коммитов хуки из файла .pre-commit-config)

> Можно вносить изменения в файлы с запущенными контейнерами, изменения будут видны сразу из-за того, что папка с исходным кодом замаунтина в контейнер.

## Создание миграций

- cd src
- alembic revision --autogenerate -m "your comment"
- Проверьте созданные миграции в папке `src/database/migrations/versions` 
- alembic upgrade head
