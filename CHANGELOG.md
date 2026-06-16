# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Configuration precedence now matches the documentation: environment variables
  take priority over the user config file (`~/.hands-on-ai/config.json`), which in
  turn overrides the built-in defaults. Previously the config file silently
  overrode environment variables, so e.g. `HANDS_ON_AI_MODEL` could be ignored.
- `rag.utils` file-loader error messages no longer point at the empty `[rag]`
  install extra.

## [0.3.0] - 2026-06-16

### Added
- `chat.Conversation`: a multi-turn chat object that remembers history (resends
  the transcript each turn) and tracks `total_tokens` / `last_usage`.
- `get_response(..., return_usage=True)` returns a `(response, usage)` tuple so
  you can see token counts. New low-level `chat.chat_completion(messages, ...)`
  primitive shared by both.
- `workflow` module: a tiny file-based (ICM) orchestrator. `Pipeline` runs a
  folder of numbered stages one reviewable step at a time (`run_next`), threading
  each stage's output into the next: sequential and human-in-the-loop by design.
  Plus a "Understanding Workflows" concept page and a "Build a Pipeline" project.

### Changed
- Project tutorials updated to match the current library and security posture:
  RAG projects rewritten against the real `get_top_k` API; the calculator agent
  now teaches a safe AST evaluator instead of `eval`; statelessness and
  small-model expectation callouts added; assorted CLI-flag, secret-handling,
  syntax, and Python-version fixes.

## [0.2.2] - 2026-06-14

### Security
- Replaced `eval()`-based calculator tools with an AST-based safe evaluator.
  Emptying `__builtins__` is not a sandbox, so a crafted expression (e.g. via
  LLM/agent input) could reach `os`/`subprocess` and run arbitrary code.
- RAG indexes now load with `allow_pickle=False` to prevent code execution
  from a malicious `.npz` index file.

### Changed
- RAG `get_embeddings` now uses the OpenAI-compatible `/v1` endpoint, so it
  works with any provider instead of only Ollama's native `/api/embeddings`.
  Added a request timeout.

### Fixed
- README Python version requirement corrected to 3.10+ to match `pyproject.toml`.

### Removed
- Deleted dead `agent/tools.py` (shadowed by the `agent/tools/` package).

## [0.1.13] - 2025-05-24

### Added
- New centralized model utilities module (`models.py`)
- New CLI commands for model management (list, check, info)
- Model capability detection for determining format compatibility
- New `examples` directory with organized example scripts
- Comprehensive test scripts for model utilities
- New cleanup script to help users transition to the new structure

### Changed
- Moved model-related code from `formats.py` to the new module
- Enhanced doctor command to verify model availability
- Improved format selection based on model capabilities
- Moved example scripts from root directory to examples/ folder

### Fixed
- Fixed CLI command handling to properly work with subcommands
- Improved error handling in API calls with proper authentication

## [0.1.12] - 2025-05-24

### Added
- Added centralized model utilities module
- Created examples directory structure
- Initial model CLI commands implementation

### Fixed
- Updated ReAct agent format detection

## [0.1.11] - 2025-05-22

### Added
- JSON-based agent format for smaller models
- Auto-detection of model capabilities
- Robust JSON parsing with fallbacks

### Fixed
- Fixed tool calling in the agent module

## [0.1.10] - 2025-05-20

### Changed
- Bumped version number

### Fixed
- Updated agent run_agent function to work with get_response API

## [0.1.9] - 2025-05-18

### Added
- Added simple API access

### Changed
- Renamed project from ailabkit to hands-on-ai