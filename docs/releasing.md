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

Do not introduce an empty Claude marketplace that claims a working integration.
Create and validate host-specific packages/catalogs when the Claude work begins.

## Public submission

A public GitHub repository is not an OpenAI directory listing. Prepare review,
branding, authentication and publication metadata separately when public
submission is requested. Keep credentials, customer records and OAuth tokens out
of every source tree, archive, test fixture and issue.

References:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
