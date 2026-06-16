"""
Tests for configuration precedence.

Documented and intended order (lowest to highest):
defaults < config file < environment variables.
"""

import json

import hands_on_ai.config as cfg


def _write_config(tmp_path, data):
    f = tmp_path / "config.json"
    f.write_text(json.dumps(data))
    return f


def test_env_var_overrides_config_file(tmp_path, monkeypatch):
    monkeypatch.setattr(cfg, "CONFIG_PATH", _write_config(tmp_path, {"model": "from-file"}))
    monkeypatch.setenv("HANDS_ON_AI_MODEL", "from-env")

    # Environment variable wins over the config file.
    assert cfg.load_config()["model"] == "from-env"


def test_config_file_overrides_default(tmp_path, monkeypatch):
    monkeypatch.setattr(cfg, "CONFIG_PATH", _write_config(tmp_path, {"model": "from-file"}))
    monkeypatch.delenv("HANDS_ON_AI_MODEL", raising=False)

    # With no env var, the config file wins over the built-in default.
    assert cfg.load_config()["model"] == "from-file"


def test_default_used_when_nothing_set(tmp_path, monkeypatch):
    # Point at a non-existent config file and clear the env var.
    monkeypatch.setattr(cfg, "CONFIG_PATH", tmp_path / "does-not-exist.json")
    monkeypatch.delenv("HANDS_ON_AI_MODEL", raising=False)

    assert cfg.load_config()["model"] == cfg.DEFAULT_MODEL
