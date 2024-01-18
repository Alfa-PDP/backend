FROM python:3.11-slim

# Основной путь приложения
ENV SRC_DIR=/opt

ENV APP_USER=backend-user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

# Создание no-root пользователя
RUN groupadd -r $APP_USER && \
    useradd -d $SRC_DIR -r -g $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -R $SRC_DIR

USER $APP_USER

# Установка зависимостей
WORKDIR $SRC_DIR

ENV PATH="/$SRC_DIR/.local/bin:${PATH}"
RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root --only main


# Копирования кода приложения
COPY ./src/app $SRC_DIR/app
COPY ./src/database $SRC_DIR/database
COPY ./src/alembic.ini alembic.ini
COPY ./src/gunicorn.conf.py gunicorn.conf.py

EXPOSE 8000

COPY infra/backend/entrypoint.sh /usr/local/bin/entrypoint.sh
