<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/77/Alfa-Bank.svg" alt="AlfaBankHackathon">
</p>

<br>


<div id="header" align="center">

[![Python](https://img.shields.io/badge/Python-%203.11-blue?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%200.100.1-blue?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-%202.0.25-blue?style=flat-square&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-%202.5.3-blue?style=flat-square&logo=pydantic)](https://docs.pydantic.dev/latest/)
[![Redis](https://img.shields.io/badge/Redis-%204.6.0-blue?style=flat-square&logo=redis)](https://redis.io/)
[![Alembic](https://img.shields.io/badge/Alembic-%202.5.3-blue?style=flat-square&logo=sqlite)](https://alembic.sqlalchemy.org/en/latest/)

[![Swagger](https://img.shields.io/badge/Swagger-black?style=flat-square&logo=swagger)](https://swagger.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-white?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-black?style=flat-square&logo=githubactions)](https://github.com/features/actions)

[![Docker](https://img.shields.io/badge/Docker-%2024.0.5-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%202.21.0-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-%200.23.1-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/Nginx-%201.22.1-blue?style=flat-square&logo=nginx)](https://www.nginx.com/)
</div>

***

Документация Swagger к API проекта доступна [ТУТ](https://alfa-idp.ddns.net/openapi)

Документация Redoc к API проекта доступна [ТУТ](https://alfa-idp.ddns.net/docs)

***

Архив со скриншотами [ТУТ](https://cloud.mail.ru/public/2jqo/MHzFP3MWA)

***

<details><summary><h1>Сервис индивидуального плана развития сотрудников</h1></summary>

* **MVP:**
  + Цель: Проект для отслеживания индивидуальных планов развития.
  + Кто молодец?: Проект выполнен командой №1 в рамках хакатона от **Альфа-Банка**.

* **Что умеет:**
  + Создавать и управлять ИПР.
  + Устанавливать личные цели и задачи.
  + Отслеживать выполнение поставленных задач.
  + Анализировать проделанную работу.

* **Общение:**
  + Обратная связь в виде комментариев.
  + Аналитика по ИПР.

</details>

<details><summary><h1>Как установить?</h1></summary>

## Запуск проекта локально в Docker-контейнерах с помощью Docker Compose

Склонируйте проект из репозитория:

```shell
git clone https://github.com/Alfa-PDP/backend.git
```

Перейдите в директорию проекта:

```shell
cd backend/
```

Перейдите в директорию **src** и создайте файл **.env**:

```shell
cd src/
```

```shell
nano .env
```

Добавьте строки, содержащиеся в файле **.env.template** и подставьте
свои значения.

Пример из .env файла:

```dotenv
PROJECT_NAME="Alfa-Bank PDP"                  # Название проекта
PROJECT_HOST=alfa-bank-pdp-backend-api        # Названия контейнера бэкенда
PROJECT_PORT=8080                             # Порт бэкенда
ENVIRONMENT=local                             # Выбор окружения

REDIS_PORT=6379                               # Порт Redis
REDIS_HOST=alfa-bank-pdp-backend-redis        # Название контейнера Redis

POSTGRES_DB=pdp_database                      # Название вашей бд
POSTGRES_USER=admin                           # Ваше имя пользователя для бд
POSTGRES_PASSWORD=super_password              # Ваш пароль для бд
POSTGRES_HOST=alfa-bank-pdp-backend-db        # Название контейнера бд
POSTGRES_PORT=5432                            # Порт бд. Стандартное значение - 5432
SQLALCHEMY_ECHO=True                          # Включение логирования SQLAlchemy

JWT_SECRET_KEY=jwt_super_secret               # Секретный ключ шифрования JWT
ENCODE_ALGORITHM=HS256                        # Алгоритм шифрования
```

Так же перейдите в директорию **infra** и создайте там аналогичный файл **.env** на примере **.env.template**.

```shell
cd ../infra
```

```shell
nano .env
```

Пример из .env файла:

```dotenv
FRONTEND_PORT=80                              # Порт для обращения к бэкенду извне
BACKEND_PORT=8080                             # Локальный порт бэкенда
REDIS_PORT=6379                               # Порт Redis

POSTGRES_DB=pdp_database                      # Название вашей бд
POSTGRES_USER=admin                           # Ваше имя пользователя для бд
POSTGRES_PASSWORD=super_password              # Ваш пароль для бд
POSTGRES_HOST=alfa-bank-pdp-backend-db        # Название контейнера бд
POSTGRES_PORT=5432                            # Порт бд. Стандартное значение - 5432
```

Перед началом работы нужно обязательно:

+ Установить poetry https://python-poetry.org/docs/#installation
+ Изменить настройки poetry для хранения виртуального окружения командой `poetry config virtualenvs.in-project true`
+ Выполнить команду `poetry install` для установки зависимостей
+ Выполнить команду `poetry shell` для активации виртуального окружения
+ Выполнить команду `pre-commit install` для инициализации pre-commit (запускает во время коммитов хуки из файла
  .pre-commit-config)

> Можно вносить изменения в файлы с запущенными контейнерами, изменения будут видны сразу из-за того, что папка с исходным кодом замаунтина в контейнер.

Чтобы создать собственные миграции перейдите в директорию **src** и создайте миграции
при помощи **Alembic**:

```shell
cd src/
```

```shell
alembic revision --autogenerate -m "your comment"
```

Проверьте созданные миграции в папке `src/database/migrations/versions`

Примените миграции:

```shell
alembic upgrade head
```

</details>


<details><summary><h1>Тестирование</h1></summary>

Чтобы добавить библиотеку для тестирования используйте флаг -G test для poetry (`poetry add pytest-asyncio -G tests`)

Для запуска тестов перейдите в корень проекта и выполните команду:

```shell
make run-tests
```

> Docker создаст отдельную БД для тестов, проведёт миграции и запустит тесты. По окончании
> тестирования тестовая БД будет удалена автоматически.

</details>

**Над кодом Backend'а трудились:**

- [Михаил Спиридонов](https://github.com/mspiridonov2706)

- [Максим Головин](https://github.com/PrimeStr)

- [Павел Ермеев](https://github.com/pavelermeev)

- [Кирилл Широков](https://github.com/KirillShirokov)
