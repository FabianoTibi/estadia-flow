#!/usr/bin/env bash
# Restaura o banco a partir de um dump. SUBSTITUI os dados atuais.
#   scripts/restore.sh ~/backups/db-AAAA-MM-DD_HHMM.sql.gz [~/backups/storage-....tar.gz]
set -euo pipefail
cd "$(dirname "$0")/.."
DUMP="${1:?informe o arquivo db-*.sql.gz}"
STORAGE="${2:-}"
gunzip -t "$DUMP"

read -r -p "Isto vai SUBSTITUIR o banco atual por $DUMP. Digite RESTAURAR para continuar: " answer
[ "$answer" = "RESTAURAR" ] || { echo "Cancelado."; exit 1; }

docker compose stop api worker web
gunzip -c "$DUMP" | docker compose exec -T mariadb sh -c 'mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" "$MARIADB_DATABASE"'
if [ -n "$STORAGE" ]; then
  docker compose run --rm -T --no-deps --user root --entrypoint sh api -c 'rm -rf /app/storage/* && tar -xzf - -C /app && chown -R node:node /app/storage' < "$STORAGE"
fi
docker compose up -d
echo "Restauração concluída. Confira o login e uma reserva recente."
