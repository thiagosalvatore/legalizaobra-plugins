# Changelog

## 0.2.0

- Add seven pt-BR workflow skills: `visao-geral`, `cadastrar-obra`,
  `simular-inss-e-orcamento`, `gerenciar-pedreiros`, `enviar-obra-ao-esocial`,
  `gerar-guia-darf`, `encerrar-obra`. They name the MCP server's real tools and say
  which calls file with the government and need the user's confirmation.
- Bundle the app icon (`assets/legalizaobra.png`) as `logo` and `composerIcon`.
- Declare `skills` in the Codex compatibility manifest and update the long description.
- Document the Codex 401 after login: Supabase could not sign the `openid` ID token
  with an HS256 key. Fixed by moving the project to ES256 signing keys.

## 0.1.1 — prepared source release

- Import the existing portable plugin and saved compatibility files into a
  multi-plugin repository layout, preserving the stable name and MCP endpoint.
- Align the Codex compatibility `.mcp.json` transport with the documented `http`
  spelling; retain `streamable-http` in portable `mcp.json`.
- Add a repository marketplace that requests authentication on installation.
- Add offline regression tests, packaging steps, OAuth diagnostics and branding
  instructions. No skills or Claude plugins are bundled yet.
- The original website icon is still missing. Live OAuth, MCP discovery, host
  loading and server behavior remain unverified. This source version is not
  automatically an uploaded private-plugin release or a public listing.

## 0.1.0

- Initial MCP-only LegalizaObra package, saved as a private personal plugin.
