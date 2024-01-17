# alfa-bank-pdp-backend

# Запуск

1. Создайте копии файлов `.env.template` в теже папки где они находятся (`/infra` и `/src`) и переименуйте в `.env`.
2. Выполнить команду `make up` из корня проекта (билдит docker образы и запускает контейнеры в соответствии с `docker-compose.yaml` из папки `/infra`)
3. http://localhost/openapi

> Перед запуском проверьте, что порты указанные в файлах `.env` не заняты системой

# Dev

## Перед началом работы

1. Установить poetry https://python-poetry.org/docs/#installation
2. Выполнить команду `poetry install` для установки зависимостей
3. Выполнить команду `poetry shell` для активации виртуального окружения
4. Выполнить команду `pre-commit install` для инициализации pre-commit (запускает во время коммитов хуки из файла .pre-commit-config)

> Можно вносить изменения в файлы с запущенными контейнерами, изменения будут видны сразу из-за того, что папка с исходным кодом замаунтина в контейнер.

## Структура проекта

### src
    > Код проекта
#### app
    > backend приложения
##### api
    > код с ручками
##### clients
    > абстрактные классы и реализации сторонних клиентов (redis, httpx)
##### core
    > Настройки, ошибки, настройка логирования проекта
##### deps
    > Зависимости проекта для dependency injection, которые прокидываются в сервисы. Про `dependency injection` в fastapi можно почитать тут https://fastapi.tiangolo.com/tutorial/dependencies/
##### middleware
    > Миддлваре для обработки запросов перед тем как они отправятся в ручку. `RequestIdHeaderMiddleware` для примера. В будущем можно убрать. Сам RequestId генерится на стороне nginx через `proxy_set_header`.
##### providers
    > Инициализация различных провайдеров и сохранение их в инстансе приложения. Здесь при запуске создаются все необходимые клиенты (redis, httpx, db сессия и т.д) и сохраняются в инстансе приложения, чтобы можно было получить доступ к клиентах по ходу работы приложения.
##### schemas
    > Схемы
##### services
    > Здесь лежат сервисы с которыми взаимодействуют ручки, в них через DI прокидываются необходимые зависимости.
##### main.py
    > Настройка и создание приложения
#### gunicorn.conf
    > Настройки для gunicorn (пока не нужно)

### infra
    > Здесь лежат файлы для деплоя приложения. 