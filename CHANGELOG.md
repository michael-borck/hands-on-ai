# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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