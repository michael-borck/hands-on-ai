"""
Tests for the file-based (ICM) workflow runner.

get_response is monkeypatched so no network/LLM is needed; the fake records the
prompts it was sent so we can verify context threading between stages.
"""

import hands_on_ai.workflow.runner as runner_mod
from hands_on_ai.workflow import Pipeline, init_workspace


def _fake_get_response_factory(calls):
    """Fake that records (system, prompt) and echoes a marker per stage."""
    def fake(prompt, system="", model=None, **kwargs):
        calls.append({"system": system, "prompt": prompt})
        # Echo something identifiable so the next stage's prompt can be checked.
        return f"RESULT for prompt ending: ...{prompt.strip()[-20:]}"
    return fake


def _make_workspace(tmp_path):
    init_workspace(tmp_path, ["research", "draft"], system="You are a workflow agent.")
    (tmp_path / "stages" / "01_research" / "CONTEXT.md").write_text(
        "Research the topic and list 3 facts.", encoding="utf-8")
    (tmp_path / "stages" / "02_draft" / "CONTEXT.md").write_text(
        "Write a paragraph from the research.", encoding="utf-8")
    return tmp_path


def test_init_workspace_structure(tmp_path):
    init_workspace(tmp_path, ["research", "draft"])
    assert (tmp_path / "stages" / "01_research" / "CONTEXT.md").exists()
    assert (tmp_path / "stages" / "02_draft" / "output").is_dir()


def test_run_next_advances_one_stage_at_a_time(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(runner_mod, "get_response", _fake_get_response_factory(calls))
    ws = _make_workspace(tmp_path)
    pipe = Pipeline(ws)

    # All stages start incomplete.
    assert pipe.status() == [("01_research", False), ("02_draft", False)]

    r1 = pipe.run_next()
    assert r1["stage"] == "01_research"
    assert (tmp_path / "stages" / "01_research" / "output" / "output.md").exists()
    # Only the first stage ran.
    assert len(calls) == 1
    assert pipe.status() == [("01_research", True), ("02_draft", False)]

    r2 = pipe.run_next()
    assert r2["stage"] == "02_draft"
    # Stage 2's prompt must include stage 1's output (context threading) + system.
    assert "Input (output of the previous stage)" in calls[1]["prompt"]
    assert "RESULT for prompt ending" in calls[1]["prompt"]
    assert calls[1]["system"] == "You are a workflow agent."

    # Nothing left to run.
    assert pipe.run_next() is None
    assert len(calls) == 2


def test_run_all_and_reset(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(runner_mod, "get_response", _fake_get_response_factory(calls))
    ws = _make_workspace(tmp_path)
    pipe = Pipeline(ws)

    results = pipe.run_all()
    assert [r["stage"] for r in results] == ["01_research", "02_draft"]
    assert all(done for _, done in pipe.status())

    pipe.reset()
    assert all(not done for _, done in pipe.status())


def test_references_are_included(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(runner_mod, "get_response", _fake_get_response_factory(calls))
    ws = _make_workspace(tmp_path)
    (ws / "references" / "voice.md").write_text("Always write in a calm tone.", encoding="utf-8")

    Pipeline(ws).run_next()
    assert "References (rules to follow)" in calls[0]["prompt"]
    assert "calm tone" in calls[0]["prompt"]


def test_missing_stages_dir_raises(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        Pipeline(tmp_path)  # no stages/ folder
