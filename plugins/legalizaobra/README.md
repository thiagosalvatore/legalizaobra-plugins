# LegalizaObra

Version: 0.2.0

Plugin for the existing LegalizaObra service at https://legalizaobra.com: the MCP
connection, workflow skills and the app icon. No replacement server, custom UI,
credentials, or shared tokens.

## Files

- `plugin.json`: portable Agent Plugins 1.0 manifest and OpenAI listing metadata.
- `mcp.json`: portable MCP configuration (`type: streamable-http`).
- `.codex-plugin/plugin.json`: compatibility manifest for older hosts.
- `.mcp.json`: Codex compatibility MCP configuration (`type: http`).
- `assets/legalizaobra.png`: icon used as `logo` and `composerIcon`.
- `skills/`: workflow skills, in pt-BR.

Both configurations point to:

```text
https://tsixskhxm25cenfxnpcwhhk3ze0wdzxj.lambda-url.sa-east-1.on.aws/mcp
```

## Connection and authentication

The service owner confirms that the server uses OAuth. Authenticate through the
host's supported browser sign-in and consent flow. The host discovers OAuth
metadata from the server; no client secrets or access/refresh tokens belong in
this package. A pre-registered client ID must only be added if the real provider
configuration requires it, with the verified callback details.

Installation alone does not prove authentication. Some hosts initiate OAuth on
first protected use, or provide a separate Authenticate/Connect action.

OAuth login, MCP initialization, `tools/list` (50 tools) and the read-only
`get_my_account` were verified on 2026-10-02. Verify with a read-only tool; do not
invoke a write to test login.

## Branding

`assets/legalizaobra.png` is set as `logo` and `composerIcon` in the portable
OpenAI interface and the compatibility interface. Paths are relative to this
plugin root.

## Skills

| Skill | Use it to |
|---|---|
| `visao-geral` | Check the account, learn the overall order, follow background operations. |
| `cadastrar-obra` | Create or change clients and obras. |
| `simular-inss-e-orcamento` | Simulate INSS, create quotes, send contracts for signature. |
| `gerenciar-pedreiros` | Add, edit, remove or end pedreiros on an obra. |
| `enviar-obra-ao-esocial` | Get the client's procuração and send the obra to eSocial. |
| `gerar-guia-darf` | Generate and deliver each month's DARF. |
| `encerrar-obra` | Change the end date, finalize the obra, explain SERO and CND. |

Each skill lives at `skills/<skill-name>/SKILL.md`, with a `name` that matches the
folder. Portable hosts discover the `skills/` directory; only the compatibility
manifest declares `"skills": "./skills/"`. Do not add a `skills` field to the root
manifest. Increment the version when publishing changes.

## Documentation

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/codex/mcp
