# LegalizaObra

Version: 0.3.0

LegalizaObra regularizes the INSS of construction works (obras) in Brazil. With this
plugin, you can ask the assistant to register clients, obras and pedreiros, simulate
the INSS of an obra, create quotes, send the obra to eSocial and generate each
month's DARF, all in your own LegalizaObra account. You need a LegalizaObra account
to sign in.

The plugin contains the MCP connection to the existing LegalizaObra service, seven
workflow skills and the app icon. It runs no local code. It sends requests only to
the LegalizaObra MCP server below, and only with the account you sign in with. No
replacement server, custom UI, credentials, or shared tokens.

## Files

- `plugin.json`: portable Agent Plugins 1.0 manifest and OpenAI listing metadata.
- `mcp.json`: portable MCP configuration (`type: streamable-http`).
- `.codex-plugin/plugin.json`: compatibility manifest for older hosts.
- `.claude-plugin/plugin.json`: Claude manifest, with the Anthropic directory
  listing fields (`icon`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`).
- `.mcp.json`: MCP configuration (`type: http`) read by Codex and Claude Code.
- `assets/legalizaobra.png`: icon used as `logo`, `composerIcon` and Claude `icon`.
- `skills/`: workflow skills, in pt-BR.
- `LICENSE`: MIT, for the files in this package. The service has its own terms.

Claude Code reads `.claude-plugin/plugin.json`, `.mcp.json` and `skills/`. It does
not read the root `plugin.json` or `mcp.json`.

Both MCP configurations point to:

```text
https://api.legalizaobra.com/mcp
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
`get_my_account` were verified in Codex on 2026-10-02, and in Claude Code 2.1.287 on
the same day. Verify with a read-only tool; do not invoke a write to test login.

In Claude Code, sign in with `/mcp` in a session, or run
`claude mcp login plugin:legalizaobra:legalizaobra` in a terminal.

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
folder. Portable hosts and Claude Code discover the `skills/` directory; only the
Codex compatibility manifest declares `"skills": "./skills/"`. Do not add a `skills`
field to the root or Claude manifest. Increment the version in all three manifests
when publishing changes.

## Documentation

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/codex/mcp
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/mcp
