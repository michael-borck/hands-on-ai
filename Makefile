# Makefile for Hands-On AI development tasks

.PHONY: help test test-basic lint format ci install-dev sync-version requirements build bundle docs deploy-docs chat-repl rag-repl agent-repl doctor chat-web rag-web agent-web generate-bot-gallery spelling-au build-project-browser build-all lint-mini-projects generate-project-index lint-chat-projects lint-rag-projects lint-agent-projects lint-all-projects clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install-dev           Install dev dependencies"
	@echo "  test                  Run all tests with pytest"
	@echo "  test-basic            Run basic imports test directly"
	@echo "  lint                  Run Ruff linter"
	@echo "  format                Auto-format code with Ruff"
	@echo "  ci                    Run linter and tests together"
	@echo "  build                 Build distribution packages"
	@echo "  bundle                Create offline zip"
	@echo "  sync-version          Sync version across files"
	@echo "  requirements          Generate requirements files"
	@echo "  docs                  Build MkDocs site"
	@echo "  deploy-docs           Deploy site to GitHub Pages"
	@echo "  chat-repl             Start HandsOnAI chat interactive mode"
	@echo "  rag-repl              Start HandsOnAI RAG interactive mode"
	@echo "  agent-repl            Start HandsOnAI agent interactive mode"
	@echo "  chat-web              Start HandsOnAI chat web interface"
	@echo "  rag-web               Start HandsOnAI RAG web interface"
	@echo "  agent-web             Start HandsOnAI agent web interface"
	@echo "  doctor                Run system diagnostic for HandsOnAI"
	@echo "  generate-bot-gallery  Generate the bot gallery markdown"
	@echo "  generate-project-index Generate the projects/index.md file"
	@echo "  spelling-au           Convert American spelling to Australian/British spelling"
	@echo "  lint-mini-projects    Lint the combined mini-projects.md file"
	@echo "  lint-chat-projects    Lint chat mini-projects"
	@echo "  lint-rag-projects     Lint RAG mini-projects"
	@echo "  lint-agent-projects   Lint agent mini-projects"
	@echo "  lint-all-projects     Lint all module-specific mini-projects"
	@echo "  build-project-browser Generate the project_browser.html"
	@echo "  build-all             Sync version, rebuild docs and project browser"
	@echo "  clean                 Clean up build artifacts"

# 🧪 Run and check
test:
	pytest

test-basic:
	python test_hands_on_ai.py

lint:
	ruff src/hands_on_ai tests scripts

format:
	ruff format src/hands_on_ai tests scripts

# 💼 Run linter and tests together
ci: lint test

# 🔧 Project setup
install-dev:
	pip install -r requirements-dev.txt

sync-version:
	scripts/inject_version.py --all
	@echo "✅ Synced version across pyproject.toml and version.json"

requirements:
	uv pip compile pyproject.toml --output-file=requirements.txt
	uv pip compile pyproject.toml --extra=dev --output-file=requirements-dev.txt
	@echo "✅ Regenerated requirements.txt and requirements-dev.txt"

# 🏗️ Build and distribute
build:
	python -m build

bundle:
	scripts/build_zip.py

# 📚 Documentation
docs:
	$(MAKE) generate-bot-gallery
	$(MAKE) generate-project-index
	mkdocs build --clean

deploy-docs:
	$(MAKE) generate-bot-gallery
	$(MAKE) generate-project-index
	mkdocs gh-deploy --force

# 🧪 Run CLI modules in interactive mode
chat-repl:
	chat interactive

rag-repl:
	rag interactive

agent-repl:
	agent interactive

# 🩺 Run diagnostic check
doctor:
	handsonai doctor

# 🌐 Run web interfaces
chat-web:
	chat web

rag-web:
	rag web

agent-web:
	agent web

# Rebuild Bot gallery markdown from doc strings
generate-bot-gallery:
	scripts/generate_bot_gallery.py --flat --out docs/bot-gallery.md

# 🇦🇺 Convert American spelling to Australian/British spelling in docs
spelling-au:
	scripts/convert_spelling.py --verbose

# 🌐 Regenerate HTML-based project browser
build-project-browser:
	scripts/project_browser.py --output docs/project_browser.html
	cp docs/project_browser.html project_browser.html

# 🛠️ Rebuild everything: sync version, docs, browser, mini-projects
build-all:
	$(MAKE) sync-version
	$(MAKE) generate-project-index
	$(MAKE) generate-bot-gallery
	$(MAKE) build-project-browser
	$(MAKE) docs

# Lint mini-projects markdown files
lint-mini-projects:
	scripts/lint_mini_projects.py

# Generate the projects index.md file
generate-project-index:
	scripts/generate_project_index.py

# Lint chat mini-projects markdown files
lint-chat-projects:
	scripts/lint_mini_projects.py docs/projects/chat

# Lint rag mini-projects markdown files
lint-rag-projects:
	scripts/lint_mini_projects.py docs/projects/rag

# Lint agent mini-projects markdown files
lint-agent-projects:
	scripts/lint_mini_projects.py docs/projects/agent

# Lint all module-specific mini-projects
lint-all-projects: lint-chat-projects lint-rag-projects lint-agent-projects

clean:
	rm -rf build dist *.egg-info __pycache__ .pytest_cache .mypy_cache