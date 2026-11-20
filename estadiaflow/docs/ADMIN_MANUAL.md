# Manual administrativo

Para quem administra uma organização no painel. A instalação está em `DEPLOYMENT.md` e `DEPLOY_GCP.md`.

## Papéis

| Papel | Pode |
|---|---|
| Proprietário | Tudo, inclusive alterar os dados da organização |
| Administrador | Tudo, exceto alterar os dados da organização |
| Gestor | Reservas, hóspedes, limpezas, manutenção, atendimento, base de conhecimento e relatórios |
| Diarista | Ver e executar as próprias limpezas e abrir chamado de manutenção |

O gestor não revela senhas de Wi-Fi nem códigos de acesso, não gerencia usuários e não mexe nas integrações.

## Primeiros passos

1. **Imóveis:** cadastre cada imóvel com horários de check-in e check-out, tempo de limpeza, Wi-Fi, código de acesso e instruções.
2. **Diaristas:** cadastre as diaristas e defina a diarista padrão de cada imóvel.
3. **Imóveis → Calendários:** cole o link iCal do Airbnb e da Booking.com de cada anúncio.
4. **Configurações → Base de conhecimento:** escreva o que o assistente pode responder (regras da casa, estacionamento, eletrodomésticos).
5. **Configurações → Integrações:** conecte WhatsApp e Google Calendar, se for usar.

## Usuários

- Crie em **Configurações → Usuários**. A senha inicial exige 10 caracteres, com letras e números.
- Para tirar o acesso de alguém, desative o usuário. O efeito é imediato, mesmo que a pessoa esteja conectada.
- Ainda não há troca nem recuperação de senha pela interface. Se alguém esquecer a senha, é preciso desativar o usuário e criar outro.

## Reservas

- Reservas manuais não podem se sobrepor no mesmo imóvel. Entre a saída de um hóspede e a entrada do próximo precisa caber o tempo de limpeza.
- Reservas importadas por iCal chegam sem nome nem telefone do hóspede. Complete o cadastro para o assistente reconhecer a pessoa no WhatsApp.
- Um conflito entre canais (por exemplo, Airbnb e Booking.com no mesmo período) aparece em **Visão geral → Conflitos**. O sistema avisa, mas não cancela nada: a decisão é sua.
- Cancelar não apaga: a reserva fica no histórico como cancelada.

## Limpezas

- Cada reserva gera uma limpeza para depois do check-out, com a janela até a próxima entrada.
- O sistema escolhe uma diarista livre no horário, começando pela padrão do imóvel. Você pode trocar.
- A diarista inicia, marca o checklist, envia fotos e confirma. Nenhuma limpeza é concluída sozinha.
- Limpeza atrasada ou com janela curta demais aparece em destaque na visão geral.

## Atendimento com IA

- O assistente responde pelo WhatsApp usando só os dados do imóvel, da reserva e da base de conhecimento.
- Wi-Fi e código de acesso só são informados para reserva confirmada, a partir de 48 horas antes do check-in.
- Pedidos de desconto, alteração de reserva, check-in antecipado e check-out tardio ficam em **Atendimento → Solicitações** para você decidir.
- Quando o assistente não sabe ou o hóspede pede uma pessoa, a conversa passa para a equipe e você é avisado.
- Ao responder por uma conversa, o assistente para de responder nela. Para devolvê-la, mude o status para "IA".

## Segredos do imóvel

Senha do Wi-Fi e código de acesso ficam cifrados. Para ver, use o botão de revelar no imóvel; cada visualização fica registrada na auditoria com seu nome e a hora.

## Auditoria

**Configurações → Auditoria** mostra quem fez o quê: logins, reservas criadas e canceladas, limpezas concluídas, segredos revelados, mudanças de usuários e de integrações. Os registros não podem ser alterados.

## Rotina sugerida

| Quando | O quê |
|---|---|
| Todo dia | Visão geral: check-ins, check-outs, limpezas atrasadas, conflitos e solicitações |
| Toda semana | Conferir se os calendários iCal sincronizaram sem erro |
| Todo mês | Revisar usuários ativos e a base de conhecimento |
| Todo trimestre | Testar a restauração do backup (`BACKUP_RESTORE.md`) |

## Limites atuais

- O nome e o fuso horário da organização só são alterados pela API (`PATCH /organization`); não há tela para isso.
- Não há valores, pagamentos nem relatórios financeiros.
- Não há página pública de reservas.
- A lista de hóspedes mostra no máximo 500 registros; use a busca para achar os demais.
- Áudios e imagens enviados pelo WhatsApp não são lidos pelo assistente.
