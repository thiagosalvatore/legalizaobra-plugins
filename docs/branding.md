# LegalizaObra icon

The plugin uses the app's current mark: a white house outline inside a teal
rounded square. The file is a copy of `public/logo_icon.png` from the
`obra-certa-frontend` repository, unchanged.

```text
plugins/legalizaobra/assets/legalizaobra.png   176 x 176 PNG, transparent corners
```

Both manifests reference it as `logo` and `composerIcon`:
`extensions.com.openai.interface` in `plugin.json`, and `interface` in
`.codex-plugin/plugin.json`. Paths are relative to the plugin root.

176 px meets OpenAI's 48 px minimum, but it is not high resolution. When a larger
original of the same mark exists (512 px PNG or an SVG from the design source),
replace the file and keep the same path. Do not upscale the 176 px file or use the
older helmet-and-house mark (`android-chrome-512x512.png`), which the app no
longer shows.

Dark-mode variants (`logoDark`, `composerIconDark`) are not set.

Sources:
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/build/plugins
