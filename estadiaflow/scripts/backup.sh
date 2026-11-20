#!/usr/bin/env bash
# Backup do banco (dump lógico) e das fotos. Uso na VM, na pasta do projeto:
#   scripts/backup.sh [pasta-de-destino]      (padrão: ~/backups)
# Mantém os últimos 14 dias. Agende no cron (ver docs/BACKUP_RESTORE.md).
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="${1:-$HOME/backups}"
STAMP="$(date +%F_%H%M)"
mkdir -p "$DEST"

# O dump roda dentro do contêiner e usa as variáveis dele: a senha não aparece na linha de comando do host.
docker compose exec -T mariadb sh -c \
  'mariadb-dump --single-transaction --routines --triggers -uroot -p"$MARIADB_ROOT_PASSWORD" "$MARIADB_DATABASE"' \
  | gzip > "$DEST/db-$STAMP.sql.gz"

# Um dump vazio ou truncado não pode passar por backup válido.
gunzip -t "$DEST/db-$STAMP.sql.gz"
gunzip -c "$DEST/db-$STAMP.sql.gz" | tail -n 5 | grep -q "Dump completed" || { echo "ERRO: dump incompleto" >&2; exit 1; }

docker compose exec -T api tar -czf - -C /app storage > "$DEST/storage-$STAMP.tar.gz"

find "$DEST" -name 'db-*.sql.gz' -mtime +14 -delete
find "$DEST" -name 'storage-*.tar.gz' -mtime +14 -delete
echo "Backup concluído: $DEST/db-$STAMP.sql.gz e $DEST/storage-$STAMP.tar.gz"
