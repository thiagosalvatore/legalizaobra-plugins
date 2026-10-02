---
name: simular-inss-e-orcamento
description: Simular o INSS de uma obra, ajustar a remuneração de um mês da simulação, criar e enviar orçamentos, gerar o PDF do orçamento e mandar contratos para assinatura no LegalizaObra. Use quando o usuário perguntar quanto vai pagar de INSS, quanto economiza, ou quiser fazer uma proposta para um cliente.
---

# Simulação de INSS, orçamento e contrato

A simulação calcula o INSS de uma obra antes de cadastrá-la. Ela mostra quanto a Receita cobraria (INSS original) e quanto o cliente paga com o LegalizaObra (INSS otimizado). Para explicar os números, veja `references/calculo-inss.md`.

## 1. Simular

1. Sem assinatura, a conta tem **10 simulações novas por mês**. Confira com `get_simulation_usage()` (`remaining`, `resets_at`). Com assinatura, `is_unlimited` é `true`.
2. Chame `simulate_inss_costs(simulation={…})`:
   - `state` (sigla, ex.: `SP`) e `start_date`: obrigatórios.
   - `end_date`: opcional. Sem ela, o sistema calcula pela área.
   - `used_concreto_usinado`: opcional.
   - `main_areas` e `complementary_areas`: mesmos campos da obra (veja a skill `cadastrar-obra`).
3. Para **ajustar** uma simulação (mudar datas, áreas, estado), chame de novo passando o `simulation_id` que veio no resultado. Isso recalcula a mesma simulação e **não gasta** o limite gratuito.
4. Mostre ao usuário: área equivalente (`resulting_area_in_square_meters`), custo estimado (`estimated_cost`), RMT e RMT otimizado (`rmt`, `adjusted_rmt`), INSS original (`inss_owed`), INSS otimizado (`inss_owed_after_optimization`) e a economia (diferença e %).
5. A tabela mês a mês (`cost_breakdown`) só vem para quem tem assinatura. Se `monthly_breakdown_requires_subscription` for `true`, diga que o detalhe mensal faz parte do plano.

"Você atingiu o limite de simulações gratuitas deste mês": ofereça o plano (`get_billing_portal_link`) ou esperar até `resets_at`.

## 2. Ajustar a remuneração de um mês (com assinatura)

`update_simulation_month_salary(simulation_id, month, salary, redistribute=true)`:
- `month`: qualquer dia do mês (AAAA-MM-DD), dentro do período da simulação.
- `salary`: **sempre informe**. Use um valor ≥ 0 para fixar o mês, ou `null` para voltar ao valor automático.
- `redistribute=true`: o saldo restante do RMT otimizado é espalhado pelos outros meses não ajustados.

## 3. Orçamento

1. `create_quote_from_simulation(simulation_id, quote={…})` (com assinatura):
   - Informe **um** dos dois: `client_id` (cliente existente) **ou** `client` (dados de um cliente novo: `full_name`, `type`, `document`, `email`, `phone`).
   - `service_price` (> 0) é o preço do serviço do usuário. `description` é opcional.
   - Cada simulação tem um orçamento só ("Esta simulação já tem um orçamento").
   - O resultado traz `client_link`: o link público do orçamento para mandar ao cliente.
2. Outras ações:
   - Listar: `list_quotes(limit, offset)`, mais novos primeiro.
   - Mudar preço ou descrição: `update_quote(quote_id, changes={price?, description?})`.
   - Excluir: `delete_quote(quote_id)`. Confirme antes.
   - PDF do orçamento: `list_templates(template_type="quote")` para achar o modelo, depois `get_quote_pdf_link(quote_id, template_id)`. O link vale 15 minutos.
3. Quando o cliente fechar, crie a obra com `create_obra_from_quote` (skill `cadastrar-obra`).

## 4. Contrato para assinatura

1. `list_templates(template_type="contract")` para escolher o modelo.
2. Opcional: prévia com `get_contract_preview_link(quote_id, template_id)`.
3. `send_contract_for_signature(contract={template_id, quote_id, message?})`. Regras:
   - O orçamento precisa ter cliente, com documento, e-mail e telefone.
   - O e-mail de quem assina pela conta tem que ser diferente do e-mail do cliente.
   - Só pode haver um contrato ativo por orçamento.
   O resultado traz os links de assinatura (`signing_urls`).
4. Acompanhar: `list_documents(status?, client_id?)`. Status: `pending`, `pending_signature`, `signed`, `cancelled`. Evite `get_document` quando não precisar: ele traz o PDF inteiro em base64, que é muito grande.
5. Cancelar: `delete_document(document_id)`. Isso cancela o contrato de vez e não funciona em contrato já assinado. Confirme antes.
