#!/bin/bash
set -e

if [ ! -f ./ssl/server.crt ] || [ ! -f ./ssl/server.key ]; then
  echo "Генерируем self-signed SSL сертификат в ./ssl/"
  mkdir -p ssl
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/server.key -out ssl/server.crt \
    -subj "/CN=localhost"
fi

echo "Запуск FastAPI admin panel с HTTPS..."
export $(cat .env | grep -v '^#' | xargs)
uvicorn app.main:app --host $ADMIN_PANEL_HOST --port $ADMIN_PANEL_PORT \
  --ssl-keyfile $ADMIN_PANEL_SSL_KEY --ssl-certfile $ADMIN_PANEL_SSL_CERT
