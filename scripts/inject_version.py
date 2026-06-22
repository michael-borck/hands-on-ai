#!/usr/bin/env python3

# tools/inject_version.py
# inject_version.py - Sync version.json with project_browser.html and pyproject.toml

from pathlib import Path
import json
import re

HTML_PATH = Path("project_browser.html")
TOML_PATH = Path("pyproject.toml")
VERSION_FILE = Path("version.json")

# Load version
with open(VERSION_FILE) as f:
    version = json.load(f)["version"]

# Inject into HTML
html_text = HTML_PATH.read_text(encoding="utf-8")
html_text = re.sub(r'const CURRENT_VERSION = "[^"]*";',
                   f'const CURRENT_VERSION = "{version}";',
                   html_text)
HTML_PATH.write_text(html_text, encoding="utf-8")
print(f"✅ Injected version {version} into project_browser.html")

# Inject into pyproject.toml
if TOML_PATH.exists():
    toml_text = TOML_PATH.read_text(encoding="utf-8")
    # Anchor to line start so we only touch the project `version`, not other
    # keys that end in "version" (e.g. [tool.mypy] python_version).
    toml_text = re.sub(r'^version\s*=\s*"[^"]*"', f'version = "{version}"',
                       toml_text, count=1, flags=re.MULTILINE)
    TOML_PATH.write_text(toml_text, encoding="utf-8")
    print(f"✅ Synced version in pyproject.toml → {version}")
