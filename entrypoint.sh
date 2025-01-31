#!/bin/sh

set -e

echo "Waiting for MariaDB..."

while ! mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" >/dev/null 2>&1; do
    echo "MariaDB is unavailable - sleeping"
    sleep 1
done

echo "MariaDB is up - executing command"

# Применяем миграции
poetry run python manage.py migrate

# Собираем статические файлы
poetry run python manage.py collectstatic --noinput

# Выполняем переданную команду
exec "$@"
