---
name: cadastrar-obra
description: Cadastrar, alterar ou excluir clientes e obras no LegalizaObra. Use quando o usuário quiser criar uma obra nova, cadastrar o dono da obra (cliente), informar o CNO, mudar áreas ou datas de uma obra que ainda não foi enviada ao eSocial.
---

# Cadastrar cliente e obra

Toda obra precisa de um cliente (o dono da obra). Crie ou ache o cliente primeiro.

## 1. Cliente

1. Procure com `list_clients(name=…)` ou `list_clients(document=…)`. O documento vai só com números.
2. Se não existir, crie com `create_client(client={…})`:
   - `full_name` (obrigatório).
   - `type`: `individual` para pessoa física (CPF) ou `company` para empresa (CNPJ).
   - `document`: CPF ou CNPJ, conferido pelos dígitos verificadores. Tem que bater com o `type`.
   - `email` e `phone` (10 ou 11 dígitos).
   - `is_construtora`: só para CNPJ. Marque `true` se a empresa é uma construtora.
3. **Para criar uma obra, o cliente precisa ter documento, e-mail e telefone.** A descrição de `create_client` diz que são opcionais, mas sem eles `create_obra` falha com "Complete as informações do cliente antes de criar uma obra". Peça os três ao usuário logo no começo.
4. Para corrigir um cliente, use `update_client(client_id, changes={…})` com só os campos que mudam.
5. "Já existe um cliente com este documento cadastrado": o cliente já existe. Procure com `list_clients(document=…)` e use esse.

## 2. Obra

Pré-requisitos: assinatura ativa e limite do plano. Se o plano já tem o máximo de obras em andamento, a criação falha ("maximum number of buildings in progress reached"). Explique ao usuário e ofereça finalizar uma obra concluída ou mudar de plano.

Chame `create_obra(obra={…})`:

| Campo | Regra |
|---|---|
| `name` | Obrigatório. |
| `client_id` | Obrigatório. Cliente da mesma conta, com perfil completo. |
| `start_date` | Obrigatório (AAAA-MM-DD). |
| `state` | Obrigatório. Sigla do estado em maiúsculas (ex.: `SP`). Uma sigla errada só falha depois ("Vau not found"). |
| `end_date` | Opcional. Sem ela, o sistema calcula: início + (área total ÷ 18) meses. Tem que ser depois do início. |
| `cno` | Opcional agora, 12 dígitos. **Obrigatório antes de enviar ao eSocial.** |
| `used_concreto_usinado` | Opcional. Gera crédito. Avise: guardar as notas fiscais por 5 anos, com o CNO da obra. |
| `automatic_esocial_transmission` | Opcional. Deixe `false` na criação. Só pode ser ligada depois do envio ao eSocial. |
| `main_areas` | Lista de áreas principais. Use `size_in_square_meters` (> 0). |
| `complementary_areas` | Opcional. Use `complementary_covered_built_area_in_square_meters` e/ou `complementary_uncovered_built_area_in_square_meters`. Pelo menos um > 0. |

Cada área também tem:
- `building_type`: `unifamiliar` (padrão), `multifamiliar`, `comercial`, `galpao`, `casa_popular`, `conjunto_habitacional`, `edificio_garagem`.
- `category`: `new_construction` (padrão), `expansion` (ampliação), `renovation` (reforma), `demolition`.
- `material`: `alvenaria` (padrão), `madeira`, `mista`.

Numa área principal, só `size_in_square_meters` conta. Numa complementar, só os campos coberta/descoberta contam. Inclua sempre pelo menos uma área principal. O app não aceita obra sem área, e o INSS é calculado a partir dela.

Depois de criar, mostre ao usuário o resumo com `get_obra_inss_costs(obra_id)`: RMT otimizado, INSS original, INSS otimizado.

### Caminho alternativo: a partir de um orçamento

Se já existe um orçamento (veja a skill `simular-inss-e-orcamento`), use `create_obra_from_quote(quote_id, obra={name, cno?, automatic_esocial_transmission?})`. Datas, estado, áreas e concreto vêm da simulação. O orçamento precisa ter cliente.

## 3. Alterar ou excluir

- `update_obra(obra_id, changes={…})`: mande só o que muda. Se você não mandar `main_areas` ou `complementary_areas`, elas ficam como estão. Se mandar uma lista, ela **substitui** a atual inteira: mande a lista completa.
- `delete_obra(obra_id)`: confirme antes.
- As duas **não funcionam** depois que a obra foi enviada ao eSocial ou finalizada ("Esta obra já foi enviada ao eSocial ou finalizada…"). Depois do envio, só a data de fim pode mudar (veja a skill `encerrar-obra`).
- `list_obras(client_id?, status?)` lista obras; `status` é `in_progress` ou `finalized`. `get_obra(obra_id)` mostra a obra com os vínculos dos pedreiros e o `esocial_status` (`pendente` = ainda não enviada; `finalizado` = já está no eSocial).

## Próximo passo

Cadastrar os pedreiros (skill `gerenciar-pedreiros`). Todos os meses da obra precisam ter pelo menos um pedreiro ativo para o envio ao eSocial.
