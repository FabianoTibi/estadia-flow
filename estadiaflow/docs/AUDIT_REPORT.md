# Relatório de auditoria — 16/11/2026

Auditoria do projeto no estado em que se encontrava em 16/11/2026, antes do rebranding para EstadiaFlow (aplicado em 17/11/2026, sem mudança de comportamento).

**Recomendação: NÃO PUBLICAR como SaaS comercial.** O núcleo operacional está sólido e testado, mas cinco módulos essenciais do produto não existem, nenhuma integração externa foi exercitada com credenciais reais e o empacotamento Docker nunca foi executado.

Classificação usada: APROVADO, REPROVADO, PENDENTE, NÃO TESTADO.

## 1. Funcionalidades

| Módulo | Situação | Evidência ou motivo |
|---|---|---|
| Login | APROVADO | Testes de integração; sessão, cookie e limite de tentativas conferidos ao vivo |
| Cadastro de conta | REPROVADO | Não existe. Organização e proprietário só nascem por script |
| Organizações | APROVADO | Isolamento testado; edição só altera campos permitidos |
| Usuários e permissões | APROVADO | 4 papéis, 25 permissões; diarista recebeu 403 em 6 áreas administrativas |
| Dashboard | APROVADO | Testes e navegação em 1360 px e 390 px |
| Imóveis | APROVADO | Testes; segredos cifrados e revelados só com permissão |
| Reservas | APROVADO | 12 testes, incluindo concorrência |
| Hóspedes | APROVADO com ressalva | A listagem devolve no máximo 500 registros e não tem paginação |
| Calendário | APROVADO | Testes e navegação |
| Limpeza | APROVADO | Fluxo completo testado; conclusão exige confirmação |
| Manutenção | APROVADO | Básico, testado |
| Relatórios | PENDENTE | Só ocupação por imóvel |
| WhatsApp | NÃO TESTADO com a API real | Código testado com dublês; faltam credenciais |
| Inteligência artificial | NÃO TESTADO com a API real | Idem |
| Google Calendar | NÃO TESTADO com a API real | Idem |
| Minha Página de Reservas | REPROVADO | Não implementado |
| Vitrine pública | REPROVADO | Não implementado |
| Pagamentos | REPROVADO | Não implementado |
| Assinaturas | REPROVADO | Não implementado |
| Portal do hóspede | REPROVADO | Não implementado |

## 2. Testes executados

| Teste | Resultado |
|---|---|
| Checagem de tipos, 6 pacotes | APROVADO |
| 14 testes de regras puras | APROVADO |
| 25 testes do core (cifra, IA, adaptadores) | APROVADO |
| 111 testes de integração da API em MariaDB real | APROVADO |
| Vulnerabilidades conhecidas nas dependências de produção (`pnpm audit`) | APROVADO: nenhuma |
| Navegação nas 11 telas, desktop e celular | APROVADO: sem rolagem horizontal, sem erro de página |
| Backup e restauração do MariaDB | APROVADO: contagens e checksum idênticos após restaurar |
| Build e subida das imagens Docker | NÃO TESTADO: sem daemon Docker no ambiente |
| `prisma migrate deploy` | NÃO TESTADO: download do motor bloqueado no ambiente |
| Testes E2E automatizados | REPROVADO: não existem no repositório |
| Teste de carga | NÃO TESTADO |

Nenhum teste executado foi reprovado. Os itens reprovados acima são ausências.

### Cenários de reserva

| Cenário | Situação |
|---|---|
| Reserva normal | APROVADO |
| Datas indisponíveis | APROVADO (409 com a reserva em conflito) |
| Duas reservas simultâneas | APROVADO (só uma é gravada) |
| Cancelamento | APROVADO (libera o período, fica na auditoria) |
| Webhook repetido (WhatsApp) | APROVADO |
| Falha na sincronização externa | APROVADO com dublês (iCal e Google não cancelam nem confirmam nada) |
| Overbooking vindo de outro canal | APROVADO (importado, sinalizado e notificado) |
| Pagamento pendente, aprovado, recusado, duplicado | REPROVADO: não há pagamentos |
| Expiração de bloqueio temporário | REPROVADO: não há bloqueio temporário |

Dentro do sistema não há overbooking possível entre reservas manuais. Entre canais, o iCal tem atraso de até 15 minutos e o sistema ainda não exporta calendário para Airbnb e Booking.com; conflitos assim são detectados e sinalizados, não evitados.

### Multi-tenancy (teste ao vivo com duas organizações)

| Verificação | Resultado |
|---|---|
| Ler imóvel, reserva, hóspede e limpeza de outra organização | 404 em todos |
| Alterar imóvel, revelar segredo e cancelar reserva de outra organização | 404 em todos |
| Criar reserva em imóvel de outra organização | 400 |
| Listagens, relatório e dashboard da outra organização | Vazios ou só com dados próprios |
| Trocar o slug da organização pelo de outra via API | Ignorado |

APROVADO. O filtro está no backend; o frontend não participa.

## 3. Segurança

| Item | Situação | Observação |
|---|---|---|
| SQL injection | APROVADO | Nenhuma consulta SQL montada à mão; tudo passa pelo Prisma. Tentativas ao vivo sem efeito |
| XSS | APROVADO | Nenhum uso de HTML bruto; carga maliciosa gravada foi exibida como texto e não executou |
| CSRF | APROVADO | Cookie SameSite=Lax e recusa de origem estranha (403) |
| Sessão | APROVADO com ressalva | Cookie httpOnly, 8 h. Não há revogação de sessão nem troca de senha |
| Autenticação | PENDENTE | Sem dois fatores, sem recuperação de senha, sem bloqueio de conta |
| Autorização | APROVADO | Toda rota tem verificação de permissão, exceto login, logout, saúde e webhook assinado |
| Rate limiting | APROVADO | Login bloqueou na 7ª tentativa dentro de 1 minuto (429) |
| Upload | APROVADO | Arquivo falso com extensão .jpg recusado; 9,5 MB recusado (413) |
| Segredos expostos | APROVADO | Nenhum no repositório; senhas não aparecem nos logs |
| Webhooks | APROVADO | Sem assinatura ou com assinatura falsa: 401 |
| Cabeçalhos | PENDENTE | HSTS, nosniff e frame-options presentes; Content-Security-Policy ausente |
| LGPD | REPROVADO | Sem aviso de privacidade, consentimento, exportação nem exclusão de dados pessoais |

### Vulnerabilidades e fragilidades encontradas

| # | Achado | Gravidade |
|---|---|---|
| 1 | LGPD não atendida (ver acima) | Alta para uso comercial |
| 2 | Sem troca nem recuperação de senha | Alta |
| 3 | Sem dois fatores e sem bloqueio de conta | Média |
| 4 | Sessão não revogável antes de 8 h, salvo desativando o usuário | Média |
| 5 | Content-Security-Policy ausente | Média |
| 6 | Fotos em disco local, sem antivírus | Baixa |
| 7 | Verificação de saúde só consulta o banco, não o Redis | Baixa |

Nenhuma falha crítica de acesso indevido foi encontrada.

## 4. Banco de dados

| Item | Situação |
|---|---|
| Integridade referencial | APROVADO: 47 chaves estrangeiras em 25 tabelas, nenhum registro órfão |
| Índices | APROVADO: toda tabela com organização tem índice iniciando por ela; a consulta de conflito usa índice |
| Consistência transacional | APROVADO: reservas com transação e bloqueio de linha |
| Migrations | PENDENTE: 1 migration, aplicada só pelo setup dos testes |
| Backup e recuperação | APROVADO localmente; scripts para Docker escritos e não executados |

Nenhuma migração foi executada nesta auditoria.

## 5. Performance

| Item | Situação |
|---|---|
| Tempo de resposta da API com os dados de demonstração | 6 a 22 ms |
| Listagem de hóspedes com 20.000 registros | 53 ms, mas devolve só 500 |
| Paginação | PENDENTE: só reservas e auditoria paginam; 9 de 45 consultas de lista têm limite |
| Consultas N+1 | Não encontradas nas telas principais |
| Processamento assíncrono | APROVADO: IA, iCal, agenda e notificações em fila |
| Cache | Não há; ainda não é necessário |
| Carga com muitos usuários | NÃO TESTADO |

O ponto que quebra primeiro com o crescimento é a falta de paginação em hóspedes, limpezas, conversas e manutenção.

## 6. Docker e infraestrutura

| Item | Situação |
|---|---|
| Dockerfile e Compose de produção | PENDENTE: escritos, validados só na sintaxe |
| Portas internas | APROVADO: no arquivo de produção só 80 e 443 ficam expostas |
| HTTPS e proxy reverso | PENDENTE: Caddy configurado, não executado |
| Health checks | PENDENTE: existem para banco, Redis e API; faltam para worker e painel |
| Persistência | APROVADO no desenho: volumes para banco, filas, fotos e certificados |
| Logs | PENDENTE: estruturados, mas sem rotação configurada no Docker |
| Execução em produção | PENDENTE: API e worker rodam TypeScript direto, sem build compilado |
| Monitoramento e alertas | REPROVADO: não há |
| Backups automáticos | PENDENTE: script pronto, agendamento a fazer na VM |

## 7. Correções realizadas

Nenhuma alteração no código da aplicação. Foram acrescentados `scripts/backup.sh`, `scripts/restore.sh` e os documentos `BACKUP_RESTORE.md`, `ADMIN_MANUAL.md`, `PRODUCTION_CHECKLIST.md` e este relatório.

## 8. Pendências externas e credenciais

| Dependência | Para quê |
|---|---|
| App da Meta, número e templates aprovados | WhatsApp |
| Chave da Gemini API | Assistente |
| Cliente OAuth do Google | Agenda |
| Conta e sandbox do gateway | Pagamentos |
| Domínio e DNS | HTTPS, webhooks e OAuth |
| Busca de anterioridade no INPI | Nome e símbolo |
| Política de privacidade e termos de uso | LGPD |

## 9. Riscos para produção

1. Vender um produto cujos módulos de reserva direta, pagamento e assinatura não existem.
2. Integrações que nunca falaram com as APIs reais podem falhar no primeiro uso.
3. A primeira subida em Docker pode exigir ajustes; nunca foi feita.
4. Sem monitoramento, uma falha do worker passa despercebida: limpezas deixam de ser geradas e a IA para de responder.
5. Sem recuperação de senha, cada esquecimento vira atendimento manual.
6. Exposição legal por tratar dados pessoais de hóspedes sem as rotinas da LGPD.

## 10. Recomendação final

**REPROVADO para publicação comercial.**

**APROVADO para piloto controlado** com um proprietário, cinco imóveis e uso interno, desde que antes sejam cumpridos os itens obrigatórios de `PRODUCTION_CHECKLIST.md`: subida em Docker verificada, HTTPS, segredos próprios, backup agendado e testado, e ao menos uma integração validada com credencial real.

A publicação depende de autorização expressa do proprietário do projeto.
