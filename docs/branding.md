# Use the existing LegalizaObra icon

The owner requested the existing icon from https://legalizaobra.com, not a new
logo. The original image has not been retrieved: live website/asset downloads
failed in the preparation environment. No substitute, traced copy, or guessed
asset URL has been added.

Obtain the exact square brand mark from the website's assets or its source
repository. Prefer its original sufficiently large PNG or SVG. Do not stretch a
wide wordmark into a square or claim an upscaled small favicon is high resolution.

For a PNG named `legalizaobra.png`, copy it to:

```text
plugins/legalizaobra/assets/legalizaobra.png
```

OpenAI documents square PNG, JPEG, WebP, or SVG images at least 48 by 48 pixels and
at most 5 MiB, with raster dimensions no larger than 4096 by 4096. A 512 by 512
transparent PNG is a useful target when that original asset is available.

Merge the following into `extensions.com.openai.interface` in the portable
`plugin.json`, and into `interface` in `.codex-plugin/plugin.json`:

```json
{
  "logo": "./assets/legalizaobra.png",
  "composerIcon": "./assets/legalizaobra.png"
}
```

Use `.svg` in both paths when the actual included file is SVG. Add references only
after the file exists. Paths are relative to the plugin root, not the directory
containing the compatibility manifest. Keep metadata, version and defaultPrompt
synchronized; do not replace the rest of either manifest.

Dark-mode assets are optional. Reuse genuine existing brand assets if available;
otherwise leave `logoDark`, `composerIconDark`, and brand color overrides unset.

Run the offline tests and inspect the rendered icon in the intended host before
publishing. Rebuild and update the same private account plugin for that
installation to receive the icon; a GitHub commit alone does not update it.

Sources:
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/build/plugins
