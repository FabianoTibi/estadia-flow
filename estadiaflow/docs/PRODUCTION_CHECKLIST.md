# Checklist de produção

Marque cada item com evidência (comando executado, captura ou data). Itens **obrigatórios** bloqueiam a publicação.

## 1. Infraestrutura

- [ ] **Obrigatório.** `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build` concluiu sem erro.
- [ ] **Obrigatório.** `docker compose ps` mostra todos os serviços saudáveis e `migrate` encerrado com sucesso.
- [ ] **Obrigatório.** O painel abre em `https://SEU_DOMINIO` com certificado válido.
- [ ] **Obrigatório.** Só as portas 80 e 443 respondem de fora (`nmap` ou teste externo).
- [ ] VM com no mínimo 4 GB de memória.
- [ ] Rotação de logs do Docker configurada (`max-size` e `max-file` em `/etc/docker/daemon.json`).

## 2. Configuração

- [ ] **Obrigatório.** `NODE_ENV=production`.
- [ ] **Obrigatório.** `JWT_SECRET` e `ENCRYPTION_KEY` gerados para este ambiente.
- [ ] **Obrigatório.** Cópia do `.env` guardada fora da VM.
- [ ] **Obrigatório.** `WEB_URL` e `GOOGLE_REDIRECT_URI` com o domínio público em HTTPS.
- [ ] Senhas do MariaDB fortes e diferentes entre si.
- [ ] `.env` com permissão `600`.
- [ ] Seed de demonstração não executado em produção.

## 3. Dados e backup

- [ ] **Obrigatório.** `scripts/backup.sh` executado com sucesso.
- [ ] **Obrigatório.** Restauração testada em banco separado, com contagens conferidas.
- [ ] **Obrigatório.** Backup agendado no cron.
- [ ] Cópia dos backups fora da VM.
- [ ] Snapshot diário do disco ativado.

## 4. Acesso

- [ ] **Obrigatório.** Organização e proprietário criados com `create-owner`.
- [ ] **Obrigatório.** Login, logout e expiração de sessão conferidos no domínio final.
- [ ] Uma diarista criada e testada: ela só enxerga as próprias limpezas.
- [ ] Usuários de demonstração inexistentes em produção.

## 5. Integrações

Cada uma só conta como pronta depois de testada com credencial real.

- [ ] iCal: um calendário do Airbnb ou da Booking.com importado, reserva conferida.
- [ ] Gemini: uma pergunta de teste respondida; uma pergunta fora do cadastro encaminhada para humano.
- [ ] WhatsApp: webhook verificado na Meta; mensagem recebida e respondida; mensagem repetida não duplicou.
- [ ] WhatsApp: template de aviso à diarista aprovado e entregue.
- [ ] Google Calendar: conta conectada; reserva criada, alterada e cancelada refletida na agenda.

## 6. Fluxo operacional completo

- [ ] **Obrigatório.** Imóvel cadastrado, reserva criada, conflito recusado.
- [ ] **Obrigatório.** Limpeza gerada, atribuída, iniciada, checklist preenchido, foto enviada e concluída pela diarista.
- [ ] Chamado de manutenção aberto e resolvido.
- [ ] Registro das ações conferido na auditoria.

## 7. Segurança e conformidade

- [ ] **Obrigatório para uso comercial.** Política de privacidade e termos de uso publicados.
- [ ] **Obrigatório para uso comercial.** Procedimento para atender pedidos de titulares (acesso, correção e exclusão) definido.
- [ ] **Obrigatório para uso comercial.** Troca e recuperação de senha implementadas.
- [ ] Responsável por incidentes definido, com contato.
- [ ] Busca de anterioridade da marca no INPI.

## 8. Operação

- [ ] Monitoramento externo do endereço `https://SEU_DOMINIO/login` com alerta.
- [ ] Alerta para contêiner reiniciando ou parado.
- [ ] Procedimento de atualização testado (`git pull` e `docker compose up -d --build`).
- [ ] Pessoa responsável por acompanhar os logs do worker nas primeiras semanas.

## 9. Autorização

- [ ] **Obrigatório.** Relatório de auditoria lido pelo proprietário do projeto.
- [ ] **Obrigatório.** Autorização expressa de publicação, com data e nome.

## Situação em 16/11/2026

Nenhum item das seções 1 a 5 foi executado em ambiente real. Ver `AUDIT_REPORT.md`.
