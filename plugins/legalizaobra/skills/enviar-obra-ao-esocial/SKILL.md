---
name: enviar-obra-ao-esocial
description: Preparar e enviar uma obra ao eSocial no LegalizaObra, incluindo a procuração do cliente no gov.br. Use quando o usuário quiser enviar a obra ao eSocial, saber o que falta para enviar, mandar as instruções de procuração ao cliente ou entender um erro do eSocial.
---

# Enviar a obra ao eSocial

O envio registra no eSocial o empregador (o cliente), a obra, as rubricas, a tributação e os pedreiros. **É um envio oficial e não pode ser desfeito.** Depois dele, a obra e os dados dos pedreiros não podem mais ser editados nem excluídos.

## 1. Conferir se a obra está pronta

Use `get_my_account` e `get_obra(obra_id)` e confira, nesta ordem:

| Item | Como conferir | Se faltar |
|---|---|---|
| Certificado digital da conta | Só dá para ver no app. | O usuário envia o arquivo .pfx em Configurações → Certificado, em https://legalizaobra.com. |
| Procuração do cliente | Não há como conferir pela ferramenta. Pergunte ao usuário. | Passo 2. |
| CNO da obra | `cno` em `get_obra`. | `update_obra(obra_id, changes={cno})` (skill `cadastrar-obra`). |
| Pelo menos um pedreiro | `employments` em `get_obra`. | Skill `gerenciar-pedreiros`. |
| Todo mês da obra com um pedreiro ativo | Compare as datas dos vínculos com `start_date`/`end_date` da obra. | Ajuste os vínculos. O erro lista os meses descobertos (MM/AAAA). |
| Assinatura ativa | `subscription_status` em `get_my_account`. | O usuário assina no app (https://legalizaobra.com). |
| Ainda não enviada | `esocial_status` = `pendente`. | Se já é `finalizado`, a obra já está no eSocial. |

## 2. Procuração do cliente

O cliente autoriza, no portal da Receita, o titular do certificado da conta a enviar por ele. Sem isso, o eSocial e a guia falham por falta de autorização.

1. `get_procuracao_link(client_id)` gera um link com as instruções, incluindo o CPF/CNPJ que o cliente tem que autorizar. O link vale 30 dias.
2. Ou `send_procuracao_email(client_id)` manda o link por e-mail ao cliente (o cliente precisa ter e-mail).
3. As duas falham se a conta ainda não tem certificado digital.
4. O que o cliente faz, com uma conta gov.br nível prata ou ouro:
   1. Entra com a conta gov.br em https://servicos.receitafederal.gov.br/servico/autorizacoes.
   2. Clica em "+ Nova Autorização".
   3. Informa o CPF/CNPJ autorizado (está no link), com validade de até 5 anos.
   4. Seleciona "Todos" os serviços.
   5. Assina.
5. O sistema não confere se a procuração foi feita. Pergunte ao usuário se o cliente já concluiu.

## 3. Enviar

1. Mostre ao usuário o resumo: obra, cliente, CNO, pedreiros e período. Diga claramente que **o envio não pode ser desfeito** e que, depois dele, a obra e os pedreiros ficam travados. Espere a confirmação.
2. Chame `send_obra_to_esocial(obra_id)`. Ela devolve uma operação.
3. Acompanhe com `get_operation_status(job_id)` até `succeeded` ou `failed`. O envio pode levar alguns minutos.
4. Em `succeeded`, confira `get_obra`: `esocial_status` passa a `finalizado`. As folhas de cada mês aparecem em `get_obra_monthly_payments`.
5. Ofereça os próximos passos:
   - Gerar as guias dos meses que já passaram (skill `gerar-guia-darf`).
   - Ligar a transmissão automática: `set_automatic_esocial_transmission(obra_id, enabled=true)`. Com ela, o sistema gera a DARF do mês sozinho no último dia do mês e manda por e-mail ao cliente.

## Erros e o que dizer

| Mensagem (ou parte dela) | O que fazer |
|---|---|
| "Nenhum certificado digital cadastrado" | Enviar o certificado no app. |
| Certificado "inválido ou expirou" / não pôde ser lido | Reenviar o certificado e a senha no app. |
| Não autorizado (código 411) | Falta a procuração do cliente, ou ela foi feita para outro CPF/CNPJ. Refazer o passo 2. |
| "Informe o CNO da obra antes de enviar ao eSocial" | Preencher o CNO. |
| "Cadastre ao menos um funcionário" / meses sem pedreiro | Ajustar os pedreiros. |
| "Já existe um envio em andamento" | Esperar a operação atual terminar. |
| Erro do servidor do eSocial (301) ou "costuma ser temporário" | Esperar alguns minutos e tentar de novo. Repetir o envio é seguro: o que já foi aceito não é duplicado. |
| "N trabalhadores rejeitados pelo eSocial" | Mostrar o motivo de cada pedreiro como veio na mensagem, pedir o dado certo ao usuário e corrigir com `update_employee`. Se o problema é o CPF, o usuário corrige no app. |
| Outra mensagem do eSocial | Mostrar a mensagem como veio e sugerir conferir os dados do cliente e da obra. |
