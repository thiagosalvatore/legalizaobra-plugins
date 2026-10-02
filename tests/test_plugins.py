"""Offline package regression checks; not an OAuth or host integration test."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "legalizaobra"
MCP_ENDPOINT = "https://api.legalizaobra.com/mcp"
FIRST_DEFAULT_PROMPT = "Show me what I can do with my LegalizaObra account."
OPENAI_LISTING_URLS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
SHARED_IDENTITY_FIELDS = ("name", "version", "description", "author", "homepage", "keywords", "repository", "license")


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
        portable, legacy, claude = load("plugin.json"), load(".codex-plugin/plugin.json"), load(".claude-plugin/plugin.json")
        for field in SHARED_IDENTITY_FIELDS:
            self.assertEqual(portable[field], legacy[field], field)
            self.assertEqual(portable[field], claude[field], field)
        self.assertEqual(portable["name"], PLUGIN.name)
        self.assertRegex(portable["version"], r"^\d+\.\d+\.\d+$")
        ui = portable["extensions"]["com.openai"]["interface"]
        self.assertLessEqual(len(ui["shortDescription"]), 30)
        prompts = ui["defaultPrompt"]
        self.assertEqual(prompts[0], FIRST_DEFAULT_PROMPT)
        self.assertLessEqual(len(prompts), 3)
        self.assertEqual(len(set(prompts)), len(prompts))
        for prompt in prompts:
            self.assertLessEqual(len(prompt), 128)
        for key, value in ui.items():
            self.assertEqual(value, legacy["interface"][key], key)

    def test_portable_mcp_transport(self):
        portable = load("mcp.json")
        self.assertEqual(portable["$schema"], "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json")
        self.assertEqual(portable["mcpServers"]["legalizaobra"]["type"], "streamable-http")

    def test_legacy_mcp_transport(self):
        self.assertEqual(load(".mcp.json")["mcpServers"]["legalizaobra"]["type"], "http")

    def test_both_mcp_configs_use_same_endpoint_without_credentials(self):
        for filename in ("mcp.json", ".mcp.json"):
            server = load(filename)["mcpServers"]["legalizaobra"]
            self.assertEqual(server["url"], MCP_ENDPOINT)
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

    def test_openai_listing_urls_use_https(self):
        ui = load("plugin.json")["extensions"]["com.openai"]["interface"]
        for key in OPENAI_LISTING_URLS:
            self.assertTrue(ui[key].startswith("https://"), key)

    def test_openai_review_has_the_cases_initial_mcp_review_requires(self):
        review = load("plugin.json")["extensions"]["com.openai"]["review"]
        positive, negative = review["test_cases"]["positive"], review["test_cases"]["negative"]
        self.assertEqual(len(positive), 5)
        self.assertEqual(len(negative), 3)
        for case in positive:
            for field in ("description", "prompt", "tools_triggered", "expected_behavior"):
                self.assertTrue(case.get(field), field)
        for case in negative:
            self.assertTrue(case.get("description"))
            self.assertTrue(case.get("prompt"))
        for key in ("test_credentials", "reviewer_instructions"):
            self.assertNotIn(key, review)
        self.assertTrue(review["demo_recording_url"].startswith("https://"))

    def test_claude_marketplace_resolves_plugin_from_repository_root(self):
        catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["name"], load(".claude-plugin/plugin.json")["name"])
        self.assertEqual(entry["description"], load(".claude-plugin/plugin.json")["description"])
        self.assertEqual((ROOT / entry["source"]).resolve(), PLUGIN.resolve())

    def test_claude_directory_listing_fields(self):
        claude = load(".claude-plugin/plugin.json")
        self.assertEqual(claude["icon"], "./assets/legalizaobra.png")
        for key in ("supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
            self.assertTrue(claude[key].startswith("https://"), key)

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
