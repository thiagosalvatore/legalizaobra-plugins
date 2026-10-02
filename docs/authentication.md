# OAuth setup and troubleshooting

## What is known

The service owner reports OAuth authentication. The initial private release is an
MCP-only package, not a registered browser-hosted app mapping. A 401 was reported
during its initial preparation; that response alone does not validate discovery,
PKCE, client registration, token exchange, scopes, or tool access.

For this source update, direct network requests failed in the preparation
environment, and the connected tools did not expose LegalizaObra. Live server
behavior and its current response headers could not be inspected. These are
verification limits, not evidence that the production server is down or broken.

## Login "succeeds" but the server returns 401 (fixed 2026-10-02)

Codex shows its localhost "you can close this window" page as soon as the browser
returns the authorization code, before it exchanges the code for a token. If the
exchange fails, Codex saves no credential and sends no token, so every request gets
`401 invalid_token "Authentication required"`.

The cause was the Supabase project's JWT signing key. Codex requests every scope the
authorization server advertises, including `openid`. With `openid`, Supabase issues
an ID token, and it can only sign one with an asymmetric key (RS256 or ES256). The
project still used the legacy HS256 secret, so the token endpoint returned
`500 "Error generating ID token"`. Moving the project to an ES256 signing key in
Project Settings → JWT Keys fixed it. The backend checks tokens with `get_claims`,
which handles both key types.

To check a login without the plugin, use a separate server name:

```sh
SERVER='mcp_servers.legalizaobra-debug.url="https://tsixskhxm25cenfxnpcwhhk3ze0wdzxj.lambda-url.sa-east-1.on.aws/mcp"'
codex mcp login legalizaobra-debug -c "$SERVER"
codex mcp logout legalizaobra-debug -c "$SERVER"
```

"Successfully logged in" means the token exchange worked.

The Lambda Function URL renames the 401's `WWW-Authenticate` header to
`x-amzn-Remapped-www-authenticate`. Codex still finds the metadata at
`/.well-known/oauth-protected-resource/mcp`, but clients that rely only on the
header cannot.

## Installed but no sign-in window

Installation is not authorization. Depending on the host, authentication can occur
on first protected tool use or via an explicit Authenticate/Connect control.
Start a new chat, select the installed LegalizaObra plugin, and request:

> Show the tools actually available through LegalizaObra. Use read-only operations
> only, and do not create or modify anything.

The repository marketplace sets `policy.authentication` to `ON_INSTALL` for
repo-based installs. This preference does not repair server OAuth discovery or
change the previously installed private package.

## Separate the host/plugin layer from the server layer

In a local Codex installation, inspect the active MCP servers with `/mcp` and the
configured direct servers with `codex mcp list`. Select the server's authentication
action when the client presents one.

To test the same endpoint independently of the installed plugin, use a distinct
configuration name so you do not overwrite an existing direct server:

```sh
codex mcp add legalizaobra-debug --url https://tsixskhxm25cenfxnpcwhhk3ze0wdzxj.lambda-url.sa-east-1.on.aws/mcp
codex mcp login legalizaobra-debug
```

This creates a separate direct MCP test connection; it does not establish that
the installed plugin has authenticated. Complete credentials and consent in the
browser, never in chat, a command argument, or a repository file. If the name
already exists, inspect it before adding or changing it.

Alternatively, run MCP Inspector locally:

```sh
npx @modelcontextprotocol/inspector
```

Choose Streamable HTTP, enter the configured endpoint, and use its OAuth/Auth
settings to inspect discovery and complete the sign-in flow. Test initialization,
tool discovery, then a read-only tool. Do not test writes merely to prove access.

## Discovery checks

1. A protected HTTP request should provide a usable OAuth challenge. Inspect
   `WWW-Authenticate` on a 401 response and follow its advertised resource metadata
   URL. The metadata should be public, not itself blocked by account login.
2. Protected resource metadata must identify the resource and its real
   authorization server(s). Fetch the authorization server's advertised discovery
   metadata; do not guess authorization endpoints or permission scopes.
3. Verify the provider advertises and implements authorization code with PKCE S256,
   suitable token endpoint authentication methods, and a supported client
   registration method (CIMD, DCR, or a correctly pre-registered client).
4. Register the exact callback emitted by the host. Browser-hosted ChatGPT and
   local Codex can use different callbacks. Check issuer and resource/audience
   validation, including matching `iss` responses when issuer support is advertised.
5. After sign-in, validate the token exchange, then MCP initialization and tool
   discovery. Successful login alone does not validate account isolation or tools.

For a quick unauthenticated header inspection from an environment with network:

```sh
curl --silent --show-error --max-time 15 --dump-header - --output /dev/null \
  'https://tsixskhxm25cenfxnpcwhhk3ze0wdzxj.lambda-url.sa-east-1.on.aws/mcp'
```

Do not paste tokens, authorization codes, cookies, client secrets, or customer data
into issues or chat. Error messages and redacted header/metadata samples are enough
to begin diagnosis. Never disable authentication to make discovery appear to work.

## Tool-level linking in ChatGPT

For tool-level OAuth prompting, OpenAI additionally documents per-tool
`securitySchemes`, protected resource metadata, and authentication error results
carrying `_meta["mcp/www_authenticate"]`. This is distinct from a transport-level
HTTP 401 challenge. Do not assume every HTTP-level auth failure should instead be
returned as a successful JSON response, or that server metadata alone tests the
whole linking flow. These policies belong in the server implementation, not in
`plugin.json`.

## Compatibility adjustment in 0.1.1

The original saved compatibility file used `type: streamable-http` in `.mcp.json`.
Current OpenAI Codex documentation uses `type: http` for that legacy format. This
release aligns it while retaining `type: streamable-http` in portable `mcp.json`.
Both represent the same intended remote transport; no server setting changes.

This is a compatibility correction, **not a confirmed explanation** for the
reported missing sign-in window. Modern hosts may read the portable configuration
instead. No host-side success claim is made from offline checks.

## Browser ChatGPT versus desktop

Imported packages that declare MCP servers may be desktop-only even when the URL
is remote HTTPS. Browser testing can require registering the MCP server through
ChatGPT developer mode. Only bind a real registered app ID that you have verified;
do not invent one or use a plugin ID as an app ID. Adding a mapping alone does not
guarantee access or remove host restrictions.

## Sources

- [OpenAI OAuth flow and linking signals](https://developers.openai.com/plugins/build/auth)
- [Codex MCP, login commands, callbacks, and legacy plugin transport](https://developers.openai.com/codex/mcp)
- [Plugin packaging and authentication policy](https://developers.openai.com/plugins/build/plugins)
- [Plugins and desktop-only limitations](https://help.openai.com/en/articles/20001256)
- [Connecting and testing an MCP server](https://developers.openai.com/plugins/deploy/connect-chatgpt)
