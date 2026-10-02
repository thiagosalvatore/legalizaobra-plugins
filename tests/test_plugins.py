"""Offline package regression checks; not an OAuth or host integration test."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "legalizaobra"


def load(relative: str) -> dict:
    return json.loads((PLUGIN / relative).read_text(encoding="utf-8"))


def read_frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}
    end = lines.index("---", 1)
    fields = (line.split(":", 1) for line in lines[1:end] if ":" in line)
    return {key.strip(): value.strip() for key, value in fields}


class PluginPackageTests(unittest.TestCase):
    def test_identity_and_compatibility_metadata_stay_in_sync(self):
        portable, legacy = load("plugin.json"), load(".codex-plugin/plugin.json")
        for field in ("name", "version", "description", "author", "homepage", "keywords"):
            self.assertEqual(portable[field], legacy[field], field)
        self.assertEqual(portable["name"], PLUGIN.name)
        self.assertRegex(portable["version"], r"^\d+\.\d+\.\d+$")
        ui = portable["extensions"]["com.openai"]["interface"]
        self.assertLessEqual(len(ui["shortDescription"]), 30)
        self.assertEqual(ui["defaultPrompt"], "Show me what I can do with my LegalizaObra account.")
        for key, value in ui.items():
            self.assertEqual(value, legacy["interface"][key], key)

    def test_portable_mcp_transport(self):
        portable = load("mcp.json")
        self.assertEqual(portable["$schema"], "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json")
        self.assertEqual(portable["mcpServers"]["legalizaobra"]["type"], "streamable-http")

    def test_legacy_mcp_transport(self):
        self.assertEqual(load(".mcp.json")["mcpServers"]["legalizaobra"]["type"], "http")

    def test_both_mcp_configs_use_same_endpoint_without_credentials(self):
        expected = "https://tsixskhxm25cenfxnpcwhhk3ze0wdzxj.lambda-url.sa-east-1.on.aws/mcp"
        for filename in ("mcp.json", ".mcp.json"):
            server = load(filename)["mcpServers"]["legalizaobra"]
            self.assertEqual(server["url"], expected)
            self.assertFalse(server.get("headers"))
            for key in ("clientSecret", "client_secret", "access_token", "refresh_token", "bearerToken"):
                self.assertNotIn(key, server)

    def test_manifest_has_no_legacy_top_level_fields(self):
        portable = load("plugin.json")
        for key in ("skills", "mcpServers", "apps", "interface"):
            self.assertNotIn(key, portable)
        self.assertEqual(load(".codex-plugin/plugin.json")["mcpServers"], "./.mcp.json")

    def test_marketplace_resolves_plugin_from_repository_root(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["name"], load("plugin.json")["name"])
        self.assertEqual(entry["source"]["source"], "local")
        self.assertEqual((ROOT / entry["source"]["path"]).resolve(), PLUGIN.resolve())
        self.assertEqual(entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
        self.assertEqual(entry["category"], "Productivity")

    def test_every_skill_declares_matching_name_and_description(self):
        skill_dirs = sorted(path for path in (PLUGIN / "skills").iterdir() if path.is_dir())
        self.assertTrue(skill_dirs)
        for skill_dir in skill_dirs:
            frontmatter = read_frontmatter(skill_dir / "SKILL.md")
            self.assertEqual(frontmatter.get("name"), skill_dir.name)
            self.assertTrue(frontmatter.get("description"), skill_dir.name)
        self.assertEqual(load(".codex-plugin/plugin.json")["skills"], "./skills/")

    def test_both_manifests_declare_the_bundled_icon(self):
        portable = load("plugin.json")["extensions"]["com.openai"]["interface"]
        for key in ("logo", "composerIcon"):
            self.assertEqual(portable[key], "./assets/legalizaobra.png")

    def test_referenced_icons_are_real_contained_files(self):
        ui = load("plugin.json")["extensions"]["com.openai"]["interface"]
        for key in ("logo", "composerIcon", "logoDark", "composerIconDark"):
            if key not in ui:
                continue  # No placeholder or missing asset may be declared.
            reference = ui[key]
            self.assertTrue(reference.startswith("./assets/"))
            path = (PLUGIN / reference).resolve()
            self.assertTrue(path.is_relative_to(PLUGIN.resolve()))
            self.assertTrue(path.is_file(), reference)
            self.assertGreater(path.stat().st_size, 0)
            self.assertLessEqual(path.stat().st_size, 5 * 1024 * 1024)
            self.assertIn(path.suffix.lower(), (".png", ".jpg", ".jpeg", ".svg", ".webp"))


if __name__ == "__main__":
    unittest.main()
