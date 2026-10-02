---
name: gerar-guia-darf
description: Gerar a guia de INSS (DARF) de cada mês de uma obra já enviada ao eSocial, ajustar pagamentos antes de enviar, baixar a DARF ou o recibo e mandar a DARF por e-mail ao cliente no LegalizaObra. Use quando o usuário pedir a guia, a DARF, o boleto do INSS do mês ou o recibo de um pedreiro.
---

# Guia mensal (DARF)

Só funciona para obras já enviadas ao eSocial (skill `enviar-obra-ao-esocial`). O app gera a DARF; quem paga é o cliente.

## 1. Ver os meses

`get_obra_monthly_payments(obra_id)` lista cada mês com:
- `payroll_id`: o id da folha do mês, usado nas outras ferramentas.
- `has_darf`: se a DARF já foi gerada.
- `esocial_transmitted_at`: quando a folha foi enviada ao eSocial.
- Valores: `salary`, `cpp_owed`, `fine` (multa), `mora`, `maed`, `inss_owed`.
- `employee_payments`: um pagamento por pedreiro, com `payment_id` e `loaded_to_esocial`.

A lista fica vazia enquanto a obra não foi enviada ao eSocial.

## 2. (Opcional) Ajustar um pagamento antes de gerar a guia

`update_payment(obra_id, payment_id, changes={…})`. Só funciona enquanto o pagamento não foi enviado ("O pagamento não pode ser modificado" depois). Três jeitos:

- **Normal:** `{salary, redistribute}`. O `salary` é o valor final do mês. Com `redistribute=true`, o saldo do RMT otimizado é espalhado pelos outros meses pendentes.
- **Reconciliação** (para bater com valores já pagos fora do app): `{salary, fine_override, mora_override, maed_override, total_payment_override: true}`. Os três overrides vão juntos, sempre.
- **Voltar ao calculado:** `{reset_overrides: true}`, sem outros campos.

## 3. Gerar a guia

Pode gerar quando:
- o mês já começou (não dá para gerar mês futuro);
- o mês não foi importado do eSocial (nesse caso, a guia é emitida direto no eSocial);
- a DARF do mês ainda não existe (`has_darf` = `false`);
- a conta tem assinatura ativa.

Passos:
1. Explique ao usuário: a guia envia as remunerações e os pagamentos do mês ao eSocial, fecha a folha do mês e emite a DARF. **Não pode ser desfeito.** Os valores do mês ficam travados. A folha é do cliente no mês: se o cliente tiver outras obras, os pedreiros dessas obras no mesmo mês entram no mesmo envio. Espere a confirmação.
2. `generate_month_guide(obra_id, payroll_id)`. Devolve uma operação.
3. Acompanhe com `get_operation_status(job_id)` até `succeeded` ou `failed`.
4. Em `succeeded`, confira `has_darf` em `get_obra_monthly_payments` e entregue a DARF (passo 4).

Para vários meses atrasados, gere um mês de cada vez, do mais antigo para o mais novo, e espere cada operação terminar.

**"A folha foi enviada ao eSocial, mas…" (guia pendente):** a folha já foi enviada; só a DARF falhou, em geral porque a Receita ainda está processando. Espere alguns minutos e chame `generate_month_guide` de novo: agora ela só emite a DARF. Outra saída é o usuário emitir a guia no e-CAC (DCTFWeb).

## 4. Entregar a DARF

- **Link:** `get_darf_link(obra_id, payroll_id)`. Abre o PDF; vale 15 minutos. Se expirar, gere outro.
- **E-mail ao cliente:** `email_darf_to_client(obra_id, payroll_id)`. Vai para o e-mail do cliente da obra, com cópia para a conta.
- **Recibo de um pedreiro:** `get_payment_receipt_link(obra_id, payment_id)`, só depois que o pagamento dele foi enviado (`loaded_to_esocial` = `true`). Antes disso o link abre "Arquivo não encontrado".
- "A DARF deste mês ainda não foi gerada": gere a guia primeiro.

## Transmissão automática

Com `set_automatic_esocial_transmission(obra_id, enabled=true)`, no último dia de cada mês o sistema gera a guia do mês corrente, se ainda não existir, e manda a DARF por e-mail ao cliente. Meses passados não entram: gere esses à mão. Para desligar, use `enabled=false`.
