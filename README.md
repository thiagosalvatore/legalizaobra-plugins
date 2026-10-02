# LegalizaObra plugins

Source packages for [LegalizaObra](https://legalizaobra.com) integrations.
The existing OpenAI plugin is included now. Additional plugins, including Claude
packages, can be added as separate self-contained directories without moving or
renaming this package. No Claude plugin or skills are implemented in this release.

## Repository layout

```text
.agents/plugins/marketplace.json   OpenAI repository marketplace catalog
plugins/legalizaobra/              Existing OpenAI/portable MCP-only package
  plugin.json                     Portable identity and OpenAI presentation
  mcp.json                        Portable MCP configuration
  .codex-plugin/plugin.json        Compatibility manifest
  .mcp.json                       Compatibility MCP configuration
docs/authentication.md            OAuth setup and troubleshooting
docs/branding.md                  Reusing the existing website icon
docs/releasing.md                 Packaging and updating the existing plugin
tests/test_plugins.py             Offline regression checks
```

## Current status

The source version is **0.1.1**, based on the saved private plugin's 0.1.0 source.
The package preserves its name, endpoint, metadata and default prompt. It corrects
the legacy transport spelling without changing the portable transport.

OAuth is the authentication method reported by the service owner. Successful
login, authenticated MCP initialization, and tool discovery remain unverified.
Installing a plugin and authorizing an account are separate operations.

The original website icon has **not** been retrieved or bundled. There are no
placeholder images or broken image references. See [branding](docs/branding.md).

Publishing this source to GitHub does not update the existing private account
plugin, deploy the MCP server, or publish a public directory listing.

## Test and package

Python 3.9 or newer is sufficient; the tests use only the standard library.

```sh
python3 -m unittest discover -s tests -v
mkdir -p dist
python3 -m zipfile -c dist/legalizaobra-0.1.1.zip plugins/legalizaobra
python3 -m zipfile -t dist/legalizaobra-0.1.1.zip
```

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

## Future packages and skills

Add new packages under `plugins/<package-name>/`, each with its host's required
manifest and only its own files. Do not add a dummy Claude package or claim
compatibility before implementing and testing it. Keep host-specific catalogs
separate when their formats differ.

Future portable skills belong at `skills/<skill-name>/SKILL.md` inside a plugin.
A skill should describe when it applies and how to use actual server tools. Do not
hardcode tool names, permissions, or scopes that have not been discovered.

## References

- [OpenAI plugin packaging and marketplace format](https://developers.openai.com/plugins/build/plugins)
- [OpenAI MCP and OAuth client configuration](https://developers.openai.com/codex/mcp)
- [OpenAI plugin authentication](https://developers.openai.com/plugins/build/auth)
