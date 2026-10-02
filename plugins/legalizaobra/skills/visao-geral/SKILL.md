---
name: visao-geral
description: Ponto de partida para qualquer pedido sobre o LegalizaObra. Use para saber o que a conta pode fazer, entender a ordem do processo (cliente, obra, pedreiros, eSocial, DARF), acompanhar operações em andamento e decidir qual skill usar.
---

# LegalizaObra — visão geral

O LegalizaObra regulariza o INSS de obras no Brasil. Uma **obra** pertence a um **cliente** (o dono da obra) e tem **pedreiros**. O app calcula o INSS da obra, envia a obra e os pedreiros ao eSocial e gera a guia de pagamento (**DARF**) de cada mês.

Responda sempre em português, em linguagem simples. Use os termos do app (obra, pedreiro, folha, guia, DARF). Veja `references/glossario.md` quando precisar explicar um termo.

## Antes de tudo

1. Chame `get_my_account`. Confira:
   - `subscription_status`: só `active` ou `trialing` liberam obras, eSocial e guias. Sem assinatura, o usuário só pode simular (10 simulações grátis por mês).
   - `my_roles`: `admin` e `editor` podem alterar dados. `read_only` só lê. `quote_management` cuida de simulações, orçamentos e clientes. `contract_management` cuida de contratos.
2. Nunca invente ids. Use as ferramentas de listagem (`list_clients`, `list_obras`, `get_obra`, `list_employees`, `get_obra_monthly_payments`, `list_quotes`) para achar o id certo. Se houver mais de um resultado parecido, pergunte ao usuário qual é.

## Ordem do processo

| Etapa | Skill |
|---|---|
| Simular o INSS e fazer orçamento | `simular-inss-e-orcamento` |
| Cadastrar cliente e obra | `cadastrar-obra` |
| Cadastrar pedreiros na obra | `gerenciar-pedreiros` |
| Pedir a procuração e enviar a obra ao eSocial | `enviar-obra-ao-esocial` |
| Gerar a guia (DARF) de cada mês | `gerar-guia-darf` |
| Encerrar a obra (e próximos passos: SERO, CND) | `encerrar-obra` |

## Operações em segundo plano

Estas ferramentas não terminam na hora. Elas devolvem uma operação com `job_id`:
`send_obra_to_esocial`, `generate_month_guide`, `add_existing_employee_to_obra`, `end_employment`.

1. Guarde o `job_id`.
2. Chame `get_operation_status(job_id)` até o `status` ser `succeeded` ou `failed`. Enquanto estiver `queued` ou `running`, diga ao usuário que está em andamento e consulte de novo.
3. Se `failed`, leia `error_message` e explique ao usuário com palavras simples.
4. Depois de `succeeded`, leia o estado de novo (`get_obra` ou `get_obra_monthly_payments`). O `result` da guia vem vazio.

Chamar a mesma ferramenta de novo enquanto a operação ainda roda devolve a mesma operação. Não cria uma segunda. Uma operação parada há mais de 15 minutos aparece como `failed` ("A operação foi interrompida…"). Nesse caso, confira o estado da obra antes de tentar de novo. `list_recent_operations` mostra as últimas operações da conta.

## Ações que exigem confirmação

Antes de chamar qualquer uma destas, explique o que vai acontecer e espere o "sim" do usuário:

- **Envio oficial ao governo, não pode ser desfeito:** `send_obra_to_esocial`, `generate_month_guide`, `end_employment`, e `add_existing_employee_to_obra` quando a obra já está no eSocial.
- **Apaga ou trava dados:** `finalize_obra`, `delete_obra`, `delete_client`, `delete_employee`, `remove_employee_from_obra`, `delete_quote`, `cancel_contract_signature`, e `change_obra_end_date` quando encurta uma obra que já está no eSocial.

## O que só dá para fazer no app

Mande o usuário para https://legalizaobra.com nestes casos:

- Cadastrar ou mudar o **CPF/CNPJ** de clientes e cadastrar **pedreiros novos**. Nunca peça CPF ou CNPJ ao usuário.
- Enviar ou trocar o **certificado digital** (Configurações → Certificado). Sem ele, nada vai ao eSocial.
- Convidar pessoas e mudar papéis da equipe.
- Criar ou editar modelos de contrato.
- Importar remunerações antigas do eSocial (arquivos XML).
- Mudar o plano. Para isso, `get_billing_portal_link` gera o link do portal de pagamento.

O programa de indicação (código, indicações e créditos) aparece em `get_referral_summary`. Os valores vêm em centavos.

## Erros comuns

- "Não encontramos uma conta Legaliza Obra para este login": o usuário entrou com um e-mail diferente do que usa no app.
- "Seu usuário não tem permissão…": o papel do usuário não permite a ação. Peça para um administrador da conta.
- "Você precisa de uma assinatura ativa…": a conta não tem plano ativo. Ofereça `get_billing_portal_link`.
- Links de download (`get_darf_link`, `get_quote_pdf_link` etc.) valem 15 minutos. Se expirar, gere outro.
