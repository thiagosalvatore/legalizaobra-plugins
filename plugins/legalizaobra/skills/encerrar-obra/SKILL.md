---
name: encerrar-obra
description: Mudar a data de fim, encerrar os vínculos e finalizar uma obra no LegalizaObra, e orientar os passos seguintes na Receita (aferição no SERO e CND). Use quando a obra acabou, vai acabar antes ou depois do previsto, ou o usuário perguntar como tirar a CND.
---

# Encerrar a obra

## 1. Mudar a data de fim

`change_obra_end_date(obra_id, end_date)`. É a única alteração permitida depois do envio ao eSocial.

- A nova data tem que ser depois do início da obra. Não funciona em obra finalizada.
- Depois do envio ao eSocial:
  - a data não pode ser antes do último mês já enviado ao eSocial;
  - não pode passar de 10 anos depois do início;
  - **encurtar apaga os pagamentos e folhas ainda não enviados depois do novo fim.** Confirme com o usuário antes. O valor restante é redistribuído pelos meses que sobram.
  - **estender** espalha o valor restante pelos novos meses.

## 2. Antes de finalizar

1. Gere as guias dos meses que faltam (skill `gerar-guia-darf`). Confira em `get_obra_monthly_payments` que todo mês tem `has_darf` = `true`.
2. Encerre os vínculos ainda abertos com `end_employment` (skill `gerenciar-pedreiros`). Cada encerramento é um envio ao eSocial.

## 3. Finalizar

`finalize_obra(obra_id)`:
- Marca a obra como finalizada no app. **Não envia nada ao eSocial.**
- **Não pode ser desfeito.** Depois disso: nenhuma guia nova, nenhum envio ao eSocial, nenhuma edição, nenhuma mudança de pedreiros.
- Em conta de empresa, libera uma vaga no limite de obras em andamento do plano.

Confirme com o usuário antes. Chamar de novo numa obra já finalizada não muda nada.

## 4. Próximos passos fora do app (na Receita, pelo e-CAC)

Explique ao usuário, que faz isso no e-CAC com a conta gov.br:

1. **Aferir a obra no SERO** (aferição indireta da obra).
2. **Abater o que já foi recolhido:** as remunerações declaradas no eSocial pelo app contam como crédito.
3. **Enviar a DCTFWeb e pagar a DARF** que restar. Parcelamento só depois do vencimento, com multa de 20% e juros Selic.
4. **Emitir a CND da obra.** Com ela, o dono averba a obra no cartório e pode vender o imóvel.

O app não faz essas etapas e não tem ferramenta para elas.
