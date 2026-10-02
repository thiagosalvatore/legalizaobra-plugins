# LegalizaObra plugins

Source packages for [LegalizaObra](https://legalizaobra.com) integrations.
One plugin directory serves both OpenAI (ChatGPT and Codex) and Claude (Claude Code,
claude.ai and Cowork). Each host reads its own manifest; all hosts share the same
skills, MCP server and icon.

## Repository layout

```text
.agents/plugins/marketplace.json   OpenAI repository marketplace catalog
.claude-plugin/marketplace.json    Claude Code marketplace catalog
plugins/legalizaobra/              The plugin, for OpenAI and Claude hosts
  plugin.json                     Portable identity and OpenAI presentation
  mcp.json                        Portable MCP configuration
  .codex-plugin/plugin.json        Codex compatibility manifest
  .claude-plugin/plugin.json       Claude manifest and directory listing fields
  .mcp.json                       MCP configuration for Codex and Claude Code
  assets/legalizaobra.png         Plugin icon (logo and composer icon)
  skills/<name>/SKILL.md          Workflow skills, written in pt-BR
  LICENSE                         MIT, for the package files only
docs/authentication.md            OAuth setup and troubleshooting
docs/branding.md                  Reusing the existing website icon
docs/releasing.md                 Packaging and updating the existing plugin
tests/test_plugins.py             Offline regression checks
```

## Current status

The source version is **0.3.1**. The MCP server no longer asks for or returns CPF and
CNPJ, and it removed or renamed three tools. The skills now match the server's
48 tools. The package name and icon do not change.

OAuth login, MCP initialization, tool discovery and a read-only tool call
were verified against production on 2026-10-02, after the Supabase project moved to
ES256 signing keys. See [authentication](docs/authentication.md).
Installing a plugin and authorizing an account are separate operations.

The icon is the app's current mark. See [branding](docs/branding.md).

Publishing this source to GitHub does not update the existing private account
plugin, deploy the MCP server, or publish a public directory listing.

## Test and package

Python 3.9 or newer is sufficient; the tests use only the standard library.

```sh
python3 -m unittest discover -s tests -v
claude plugin validate --strict plugins/legalizaobra
claude plugin validate --strict .
mkdir -p dist
python3 -m zipfile -c dist/legalizaobra-0.3.1.zip plugins/legalizaobra
python3 -m zipfile -t dist/legalizaobra-0.3.1.zip
```

The `claude plugin validate` commands need Claude Code 2.1.281 or newer.

The plugin ZIP has a single `legalizaobra/` root, including compatibility dotfiles.
The full repository ZIP is not a single-plugin upload. Never package credentials,
OAuth tokens, client secrets, customer records, or a `.git/` directory.

## Use the repository marketplace

After the source has been pushed to GitHub, supported Codex clients can register
this catalog with:

```sh
codex plugin marketplace add thiagosalvatore/legalizaobra-plugins
```

For a local checkout, use `codex plugin marketplace add .` from the repository root.
Open the Plugins directory in the desktop app, select **LegalizaObra Plugins**,
and install the listed plugin. Restart the app or start a new chat as needed to
load newly installed capabilities.

The catalog requests authentication on install through `policy.authentication`.
This is a host policy, not an OAuth implementation, and does not guarantee a
browser window will open on every surface. It does not retroactively modify the
private copy already installed from Plugin Creator. See
[authentication](docs/authentication.md) and [release management](docs/releasing.md).

Choose the repo-distributed or account-distributed copy intentionally; registering
this marketplace does not migrate the existing private plugin's identity.

## Use from Claude Code

```sh
claude plugin marketplace add thiagosalvatore/legalizaobra-plugins
claude plugin install legalizaobra@legalizaobra-plugins
```

From a local checkout, use `claude plugin marketplace add ./` instead. Then sign in
once with `/mcp` in a session, or `claude mcp login plugin:legalizaobra:legalizaobra`
in a terminal. Claude Code registers itself with the OAuth server and opens the
browser. Skills run as `/legalizaobra:<skill>`, and Claude also picks them by their
description.

## Future packages and skills

Add new packages under `plugins/<package-name>/`, each with its host's required
manifest and only its own files. A new host joins an existing plugin by adding its
manifest next to the others, as Claude did, rather than by copying the skills.
Keep host-specific catalogs separate when their formats differ.

Portable skills live at `skills/<skill-name>/SKILL.md` inside a plugin, with a
`name` that matches the folder and a `description` of when to use it. A skill names
only tools the MCP server actually exposes; check them against the server's tool
registry when the server changes.

## References

- [OpenAI plugin packaging and marketplace format](https://developers.openai.com/plugins/build/plugins)
- [OpenAI MCP and OAuth client configuration](https://developers.openai.com/codex/mcp)
- [OpenAI plugin authentication](https://developers.openai.com/plugins/build/auth)
- [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code MCP and OAuth](https://code.claude.com/docs/en/mcp)
