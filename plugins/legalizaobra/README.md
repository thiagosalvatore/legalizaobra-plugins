# LegalizaObra

Version: 0.1.1

MCP-only plugin for the existing LegalizaObra service at https://legalizaobra.com.
No replacement server, custom UI, bundled skills, credentials, or shared tokens.

## Files

- `plugin.json`: portable Agent Plugins 1.0 manifest and OpenAI listing metadata.
- `mcp.json`: portable MCP configuration (`type: streamable-http`).
- `.codex-plugin/plugin.json`: compatibility manifest for older hosts.
- `.mcp.json`: Codex compatibility MCP configuration (`type: http`).

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

An unauthenticated request reportedly returned 401 during the initial 0.1.0
preparation. A fresh endpoint and discovery check could not be completed in the
0.1.1 preparation environment. Successful OAuth authorization, MCP initialization,
and authenticated `tools/list` have not been verified. No application tools were
called, and no customer data was read or modified.

After connecting, discover actual tool names, descriptions, schemas and annotations.
Verify with a genuinely read-only tool; do not invoke a write to test login. Do not
infer capabilities or permission scopes from the marketing website.

## Branding

The original website icon is not included yet. The manifests intentionally do not
reference a missing image. Once the real icon is available, bundle it beneath
`assets/` and set both `logo` and `composerIcon` in the portable OpenAI interface
and the compatibility interface. Keep all paths relative to this plugin root.

## Future skills

Add skills at `skills/<skill-name>/SKILL.md` with YAML frontmatter containing a
matching `name` and a description of when to use it. Keep the existing plugin
identity and increment its version when publishing changes. Portable hosts
discover the `skills/` directory; do not add a legacy top-level `skills` field to
the root manifest.

## Documentation

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/codex/mcp
