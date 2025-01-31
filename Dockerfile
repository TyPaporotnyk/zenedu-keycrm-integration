FROM python:3.12-alpine AS python

FROM python AS python-build-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apk update && apk add --no-cache \
    build-base \
    py3-cryptography \
    py3-mysqlclient \
    mariadb-dev \
    build-base \
    freetype-dev \
    tzdata \
    mysql-client

ADD pyproject.toml /app

# Копируем и делаем entrypoint исполняемым
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh && \
    sed -i 's/\r$//' /app/entrypoint.sh

# Создаем пользователя для приложения
RUN adduser -D appuser && \
    chown -R appuser:appuser /app

# Устанавливаем Poetry и зависимости от имени appuser
USER appuser
RUN pip install --user --upgrade pip && \
    pip install --user poetry

# Добавляем путь к пользовательским бинарникам в PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN poetry install --no-root --no-interaction --no-ansi

COPY --chown=appuser:appuser . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
