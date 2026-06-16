"""
Shared configuration for all hands-on-ai modules.
Handles server settings, paths, and fallback messages.
"""

import json
import logging
import os
from pathlib import Path

# Default settings
DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "llama3"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_CHUNK_SIZE = 500
CONFIG_DIR = Path.home() / ".hands-on-ai"
CONFIG_PATH = CONFIG_DIR / "config.json"

# Setup logging
log = logging.getLogger("hands_on_ai")
log.setLevel(logging.WARNING)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
log.addHandler(handler)

if os.environ.get("HANDS_ON_AI_LOG") == "debug":
    log.setLevel(logging.DEBUG)


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)


def load_default_config():
    """
    Load the default configuration packaged with HandsOnAI.
    
    Returns:
        dict: Default configuration settings
    """
    try:
        from importlib.resources import files
        path = files("hands_on_ai.data") / "default_config.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"Failed to read default config: {e}")
        # Fallback to hardcoded defaults if file can't be loaded
        return {
            "server": DEFAULT_SERVER,
            "model": DEFAULT_MODEL,
            "embedding_model": DEFAULT_EMBEDDING_MODEL,
            "chunk_size": DEFAULT_CHUNK_SIZE,
        }


def load_config():
    """
    Load configuration from config file or environment variables.
    
    Returns:
        dict: Configuration settings
    """
    # Precedence (lowest to highest): defaults < config file < environment variables.

    # Start with default configuration
    config = load_default_config()

    # User config file overrides the defaults
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                file_config = json.load(f)
                # Update only keys that exist in file
                for key in file_config:
                    config[key] = file_config[key]
        except Exception as e:
            log.warning(f"Failed to read config.json: {e}")

    # Environment variables have the highest priority (override file and defaults)
    if "HANDS_ON_AI_SERVER" in os.environ:
        config["server"] = os.environ["HANDS_ON_AI_SERVER"]

    if "HANDS_ON_AI_MODEL" in os.environ:
        config["model"] = os.environ["HANDS_ON_AI_MODEL"]

    if "HANDS_ON_AI_EMBEDDING_MODEL" in os.environ:
        config["embedding_model"] = os.environ["HANDS_ON_AI_EMBEDDING_MODEL"]

    if "HANDS_ON_AI_API_KEY" in os.environ:
        config["api_key"] = os.environ["HANDS_ON_AI_API_KEY"]

    return config


def save_config(config):
    """
    Save configuration to config file.
    
    Args:
        config (dict): Configuration settings to save
    """
    ensure_config_dir()
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        log.warning(f"Failed to write config.json: {e}")


def load_fallbacks(module="chat"):
    """
    Load fallback personality messages from user, local, or default locations.
    
    Args:
        module (str): Module name to load fallbacks for
        
    Returns:
        dict: Fallback messages by personality
    """
    # First try user override
    user_file = CONFIG_DIR / f"{module}_fallbacks.json"
    
    # Then try package data
    if user_file.exists():
        try:
            with user_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Failed to read user fallbacks: {e}")
    
    # Otherwise use built-in fallbacks from package data
    try:
        from importlib.resources import files
        path = files(f"hands_on_ai.{module}.data") / "fallbacks.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"Failed to read built-in fallbacks: {e}")
        return {"default": ["Retrying..."]}


def get_server_url():
    """Get the server URL from config."""
    return load_config()["server"]


def get_model():
    """Get the default model from config."""
    return load_config()["model"]


def get_embedding_model():
    """Get the default embedding model from config."""
    return load_config()["embedding_model"]


def get_chunk_size():
    """Get the default chunk size from config."""
    return load_config()["chunk_size"]


def get_api_key():
    """Get the API key from config if available."""
    return load_config().get("api_key", "")