---
name: gerenciar-pedreiros
description: Cadastrar, vincular, editar, remover ou desligar pedreiros (trabalhadores) de uma obra no LegalizaObra. Use quando o usuário quiser adicionar um pedreiro à obra, corrigir dados de um pedreiro, tirar um pedreiro da obra ou encerrar o vínculo de quem saiu.
---

# Pedreiros da obra

O pedreiro é cadastrado uma vez na conta (único por CPF). Ele é ligado a cada obra por um **vínculo**, com datas, cargo, CBO e tipo. O sistema calcula sozinho quanto cada pedreiro recebe por mês: não existe campo de salário.

## Regras que valem sempre

- **Tipo de vínculo** (`employment_type`): `mei` ou `autonomous`. Se o cliente da obra é empresa (CNPJ), **só `mei`** é aceito.
- **Datas:** o início do vínculo tem que estar dentro das datas da obra. O fim, se houver, também; não pode ser depois de hoje e tem que ser depois do início.
- **Cobertura:** para enviar a obra ao eSocial, todos os meses entre o início e o fim da obra precisam ter pelo menos um pedreiro ativo. Ao planejar os vínculos, cubra o período inteiro.
- Padrões: `role` = `PEDREIRO ALVENARIA`, `cbo` = `715210`.

## Adicionar um pedreiro à obra

1. Procure na conta: `list_employees(name=…)` ou `list_employees(document=<CPF só números>)`.
2. **Já existe:** `add_existing_employee_to_obra(obra_id, employee_id, employment={start_date, end_date?, employment_type, role?, cbo?})`. Não pode haver dois vínculos do mesmo pedreiro na mesma obra com datas sobrepostas.
3. **Não existe:** `add_new_employee_to_obra(obra_id, employee={…})`. Peça ao usuário todos os campos:

| Campo | Valores |
|---|---|
| `full_name`, `cpf` | CPF com dígitos verificadores válidos. |
| `birthday` | AAAA-MM-DD. |
| `gender` | `male` ou `female`. |
| `race` | `white` (branca), `black` (preta), `asian` (amarela), `brown` (parda), `indigenous` (indígena). |
| `schooling_level` | `no_school`, `incomplete_elementary`, `complete_elementary`, `incomplete_high_school`, `complete_high_school`, `incomplete_university`, `complete_university`, `postgraduate`, `masters_degree`, `doctorate`. |
| `country_of_birth` | Nome do país, ex.: `Brasil`. |
| `address` | `street`, `number`, `zip_code` (só números), `city`, `state` (sigla), `city_code` (código IBGE do município, 7 dígitos), `complement?`. |
| `start_date`, `end_date?`, `employment_type`, `role?`, `cbo?` | Regras acima. |

Se o usuário não souber o código IBGE, procure pelo CEP (por exemplo, no ViaCEP o campo `ibge`) e confirme com ele.

4. As duas ferramentas são **operações em segundo plano**. Acompanhe com `get_operation_status(job_id)` (veja a skill `visao-geral`). Erros de CPF inválido ou CPF repetido aparecem no `error_message` da operação.

**Se a obra já está no eSocial** (`esocial_status` = `finalizado` em `get_obra`), adicionar um pedreiro envia o evento de início ao eSocial (S-2300) e, se tiver data de fim, também o de término (S-2399). É um envio oficial: **confirme com o usuário antes**. O vínculo só é salvo se o eSocial aceitar.

## Antes do envio ao eSocial

- Corrigir dados pessoais: `update_employee(employee_id, changes={…})`. O CPF não muda.
- Tirar da obra: `remove_employee_from_obra(obra_id, employee_id)`. Confirme antes.
- Cadastrar só na conta, sem obra: `create_employee(employee={…})`, com os mesmos dados pessoais e endereço.
- Excluir da conta: `delete_employee(employee_id)`. Apaga também os vínculos. Confirme antes.

## Depois do envio ao eSocial

- Os dados do pedreiro ficam travados ("Pedreiro está vinculado a uma obra enviada ao e-Social e não pode ser alterado"). Ele também não pode ser excluído nem removido da obra.
- Quando um pedreiro sai, encerre o vínculo: `end_employment(obra_id, employment_id, end_date)`. O `employment_id` está em `employments` no resultado de `get_obra`. Isso envia o término ao eSocial (S-2399) e **não pode ser desfeito**: confirme a data com o usuário. Pagamentos ainda não enviados depois do mês de saída são apagados e o valor é redistribuído.
- "Este vínculo já foi encerrado": nada a fazer.
