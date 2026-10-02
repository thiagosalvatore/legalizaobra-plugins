# Source, account releases, and distribution

## Source of truth

This repository holds the editable source. The initial snapshot incorporates the
portable package and the two compatibility files read from the saved private
LegalizaObra account plugin. Keep its stable package name `legalizaobra`.

The private account plugin and a repository marketplace are separate distribution
paths. Pushing a commit does not automatically update the private account release.
Avoid creating another private plugin merely to publish a new version.

## Update the existing private account plugin

1. Read its current source and release metadata through Plugin Creator.
2. Preserve the existing plugin ID, scope, audience, endpoint, defaultPrompt and
   unrelated files. Do not expose personal account identifiers unnecessarily in
   this public repository.
3. Increment the version in both manifests and make the intended source changes.
4. Run `python3 -m unittest discover -s tests -v` from the repository root.
5. Create a ZIP containing only the `plugins/legalizaobra` directory as a single
   root named `legalizaobra/`, including its compatibility dotfiles.
6. Use the supported update flow for that same private plugin, guarded by the
   current release ID. Read back the saved source before claiming it was updated.
7. Refresh the installed copy as the host requires, then test actual connection,
   OAuth, tool discovery, and icon rendering. A ZIP or saved release is not a
   successful end-to-end test.

If the current session only exposes read actions, prepare the source and archive
without claiming it has been uploaded. Never request access tokens in chat to
work around missing write tools.

## Repository marketplace

The catalog at `.agents/plugins/marketplace.json` resolves plugin paths relative
to the repository root, not relative to `.agents/plugins/` itself. It can grow as
additional real packages are implemented. Its `ON_INSTALL` authentication policy
applies to supported repo-based installs, not to an already installed private copy.

## Claude marketplace

`.claude-plugin/marketplace.json` lists the same `plugins/legalizaobra` directory for
Claude Code. Its `source` is also relative to the repository root. Claude Code reads
the plugin's `.claude-plugin/plugin.json`, `.mcp.json` and `skills/`, so a skill or
MCP change reaches both hosts.

`version` is set in the Claude manifest, so Claude Code users keep the old copy until
it changes. Increment it together with the other two manifests; the tests fail when
they disagree. Users update with `claude plugin update legalizaobra@legalizaobra-plugins`.

Before pushing, run `claude plugin validate --strict plugins/legalizaobra` and
`claude plugin validate --strict .`. To test an install from the checkout:

```sh
claude plugin marketplace add ./
claude plugin install legalizaobra@legalizaobra-plugins
claude plugin details legalizaobra
```

`details` should list seven skills and the `legalizaobra` MCP server. Remove the test
install with `claude plugin uninstall legalizaobra@legalizaobra-plugins` and
`claude plugin marketplace remove legalizaobra-plugins`.

## Anthropic directory

The Anthropic directory lists a plugin on claude.ai and in Cowork. People who add it
there also get it in Claude Code, as `legalizaobra@synced`. Submitting needs a paid
claude.ai plan.

1. Push the release to GitHub. The directory reads the repository, not a ZIP.
2. Open https://claude.ai/directory/manage, select **Submit new**, then
   **Plugin bundle**.
3. Enter the repository `thiagosalvatore/legalizaobra-plugins` and the plugin path
   `plugins/legalizaobra`. Submit one plugin at a time.
4. Select **Validate**. Fix every finding marked **Blocking**, push, and select
   **Re-validate**.
5. Submit. Each later commit on the followed branch is validated and scanned again.

The directory reads `icon`, `supportUrl`, `privacyPolicyUrl` and `termsOfServiceUrl`
from `.claude-plugin/plugin.json`, and shows the plugin's `README.md` as the listing
description. It blocks a plugin without a `LICENSE` or with a README under 40 words,
and it blocks symbolic links and `.DS_Store` files in the plugin directory.

## Public submission

A public GitHub repository is not an OpenAI directory listing. Prepare review,
branding, authentication and publication metadata separately when public
submission is requested. Keep credentials, customer records and OAuth tokens out
of every source tree, archive, test fixture and issue.

References:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://code.claude.com/docs/en/plugins/publish
- https://claude.com/docs/plugins/pre-submission-checklist
