# Backup e recuperação

## O que precisa ser guardado

| Item | Onde está | Sem ele |
|---|---|---|
| Banco de dados | Volume `mariadb-data` | Perde-se tudo |
| Fotos de limpeza | Volume `storage` | Perdem-se as fotos; o banco fica com referências quebradas |
| `ENCRYPTION_KEY` | Arquivo `.env` | Senhas de Wi-Fi, códigos de acesso e tokens das integrações ficam ilegíveis, mesmo com o banco restaurado |
| Arquivo `.env` completo | Na VM | É preciso recriar todos os segredos e reconectar as integrações |

Guarde uma cópia do `.env` fora da VM, em um cofre de senhas. Ele não entra no backup automático de propósito.

O Redis não precisa de backup: os agendamentos são recriados quando o worker inicia.

## Backup

```bash
scripts/backup.sh              # grava em ~/backups
scripts/backup.sh /mnt/backups # ou em outra pasta
```

O script gera `db-AAAA-MM-DD_HHMM.sql.gz` e `storage-AAAA-MM-DD_HHMM.tar.gz`, confere se o dump está íntegro e completo e apaga os arquivos com mais de 14 dias.

O dump usa `--single-transaction`: não bloqueia o sistema e retrata um instante consistente.

### Agendar

```bash
crontab -e
```

```
30 3 * * * cd /home/USUARIO/estadiaflow && scripts/backup.sh >> /home/USUARIO/backups/backup.log 2>&1
```

### Cópia fora da VM

Um backup que mora no mesmo disco não protege contra a perda da VM. Envie para um bucket:

```bash
gcloud storage buckets create gs://SEU-BUCKET-backups --location=southamerica-east1
gcloud storage rsync ~/backups gs://SEU-BUCKET-backups
```

Acrescente a segunda linha ao cron, logo após o backup. Ative também o snapshot diário do disco, descrito em `DEPLOY_GCP.md`.

## Restauração

```bash
scripts/restore.sh ~/backups/db-2026-11-16_0330.sql.gz ~/backups/storage-2026-11-16_0330.tar.gz
```

O script pede a confirmação `RESTAURAR`, para a API, o worker e o painel, carrega o dump, restaura as fotos e sobe tudo de novo. O segundo argumento é opcional.

**A restauração substitui os dados atuais.** Tudo o que foi gravado depois do backup se perde.

### Recuperação em uma VM nova

1. Crie a VM e instale o Docker (`DEPLOY_GCP.md`, seções 2 e 4).
2. Traga o código e o `.env` guardado, com a mesma `ENCRYPTION_KEY`.
3. `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`
4. Copie os arquivos de backup para a VM.
5. `scripts/restore.sh <dump> <fotos>`
6. Aponte o DNS para o novo IP.
7. Confira: login, uma reserva recente, uma foto de limpeza e a revelação da senha do Wi-Fi de um imóvel. Este último confirma que a `ENCRYPTION_KEY` é a correta.

## Teste de restauração

Faça ao menos uma vez antes de entrar em produção e depois a cada trimestre. Restaure em um banco separado, sem tocar no principal:

```bash
docker compose exec -T mariadb sh -c 'mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" -e "CREATE DATABASE restore_test"'
gunzip -c ~/backups/db-ARQUIVO.sql.gz | docker compose exec -T mariadb sh -c 'mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" restore_test'
docker compose exec -T mariadb sh -c 'mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" -e "SELECT COUNT(*) FROM restore_test.Reservation; DROP DATABASE restore_test"'
```

Compare a contagem com a do banco principal.

## O que foi verificado

Na auditoria de 16/11/2026, o dump e a restauração foram executados em MariaDB 10.11 fora do Docker: as contagens de seis tabelas e o checksum da tabela de imóveis ficaram idênticos. Os scripts `backup.sh` e `restore.sh`, que usam `docker compose`, tiveram só a sintaxe conferida. Rode os dois uma vez em homologação antes de confiar neles.

## Limites

- A perda máxima de dados é o intervalo entre backups: 24 horas com o agendamento acima. Para menos, agende mais vezes ou ative o log binário do MariaDB.
- Não há replicação nem failover automático.
