# Changelog

## 0.3.0

- Add the Claude plugin. `plugins/legalizaobra` now has `.claude-plugin/plugin.json`,
  and the repository root has `.claude-plugin/marketplace.json`. Claude Code uses the
  same skills, `.mcp.json` and icon as Codex.
- Add the Anthropic directory listing fields (`icon`, `supportUrl`,
  `privacyPolicyUrl`, `termsOfServiceUrl`) and an MIT `LICENSE` for the package files.
- Add `repository` and `license` to all manifests. The tests keep the shared identity
  fields equal in all three manifests.
- Verified in Claude Code 2.1.287: install from the local marketplace, OAuth login,
  50 tools listed, and a read-only `get_my_account` call.
- Move the MCP endpoint in `mcp.json` and `.mcp.json` to
  `https://api.legalizaobra.com/mcp`.
- Add the OpenAI directory submission metadata to the root `plugin.json`: listing
  URLs, capabilities, three default prompts, `brandColor` `#146971`, the onboarding
  skill, review test cases, and publication settings for Brazil with a pt-BR
  translation. The Codex manifest repeats the listing fields.

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
