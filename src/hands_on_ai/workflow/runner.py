"""
A tiny file-based workflow runner: the Interpretable Context Methodology (ICM).

Instead of a coordination framework, a workflow is just a folder of numbered
stages. Each stage has a ``CONTEXT.md`` (its instructions) and an ``output/``
folder. One orchestrating model reads each stage's instructions plus the
previous stage's output, and writes a new readable file. A human reviews (and
can edit) the output between stages.

    workspace/
    ├── CONTEXT.md            # optional: shared system prompt / overall goal
    ├── references/           # optional: stable rules (the "factory")
    └── stages/
        ├── 01_research/
        │   ├── CONTEXT.md    # what this stage should do
        │   └── output/       # output.md is written here
        └── 02_draft/
            ├── CONTEXT.md
            └── output/

Run **one stage at a time** and review the output file before continuing. This
runner is deliberately sequential and human-in-the-loop, not an autonomous loop:

    from hands_on_ai.workflow import Pipeline

    pipe = Pipeline("workspace")
    pipe.status()        # show stages and which are done
    pipe.run_next()      # runs stage 01, writes output.md, stops for review
    # ...open stages/01_research/output/output.md, edit if needed...
    pipe.run_next()      # runs stage 02 using stage 01's reviewed output
"""

from pathlib import Path

from ..chat import get_response

OUTPUT_NAME = "output.md"

_DEFAULT_SYSTEM = (
    "You are a careful assistant executing one stage of a multi-step workflow. "
    "Follow the stage instructions exactly and produce only the requested output."
)


def init_workspace(path: str | Path, stages: list[str], system: str | None = None) -> Path:
    """
    Create a starter workspace with numbered stage folders.

    Args:
        path: Directory to create the workspace in.
        stages: List of stage names, e.g. ``["research", "draft"]`` →
            ``stages/01_research``, ``stages/02_draft``.
        system: Optional shared instruction written to the workspace ``CONTEXT.md``.

    Returns:
        Path: the workspace root.
    """
    root = Path(path)
    (root / "references").mkdir(parents=True, exist_ok=True)
    if system:
        (root / "CONTEXT.md").write_text(system, encoding="utf-8")

    for i, name in enumerate(stages, start=1):
        stage = root / "stages" / f"{i:02d}_{name}"
        (stage / "output").mkdir(parents=True, exist_ok=True)
        contract = stage / "CONTEXT.md"
        if not contract.exists():
            contract.write_text(
                f"# Stage {i:02d}: {name}\n\n"
                "Describe what this stage should do with the input it receives.\n",
                encoding="utf-8",
            )
    return root


class Pipeline:
    """Run a folder-based (ICM) workflow one reviewable stage at a time."""

    def __init__(self, path: str | Path):
        self.root = Path(path)
        self.stages_dir = self.root / "stages"
        if not self.stages_dir.is_dir():
            raise FileNotFoundError(f"No 'stages/' folder found in {self.root}")

    # --- structure helpers ---

    def _stages(self):
        """Stage folders in numbered order."""
        return sorted(
            (p for p in self.stages_dir.iterdir() if p.is_dir()),
            key=lambda p: p.name,
        )

    @staticmethod
    def _output_path(stage):
        return stage / "output" / OUTPUT_NAME

    def _is_done(self, stage):
        out = self._output_path(stage)
        return out.exists() and out.read_text(encoding="utf-8").strip() != ""

    @staticmethod
    def _read(path):
        return path.read_text(encoding="utf-8").strip() if path.exists() else ""

    def _references(self, stage):
        """Concatenate workspace-level and stage-level reference files (the 'factory')."""
        texts = []
        for refs_dir in (self.root / "references", stage / "references"):
            if refs_dir.is_dir():
                for f in sorted(refs_dir.glob("*.md")):
                    texts.append(self._read(f))
        return "\n\n".join(t for t in texts if t)

    def _build_messages(self, stage, prev_stage):
        """Assemble the (system, prompt) for a stage from its contract + context."""
        system = self._read(self.root / "CONTEXT.md") or _DEFAULT_SYSTEM
        contract = self._read(stage / "CONTEXT.md") or f"# {stage.name}"

        parts = [contract]
        refs = self._references(stage)
        if refs:
            parts.append("## References (rules to follow)\n\n" + refs)
        if prev_stage is not None:
            prev = self._read(self._output_path(prev_stage))
            if prev:
                parts.append("## Input (output of the previous stage)\n\n" + prev)

        return system, "\n\n".join(parts)

    # --- running ---

    def status(self):
        """Print and return ``[(stage_name, done), ...]``."""
        rows = [(s.name, self._is_done(s)) for s in self._stages()]
        for name, done in rows:
            print(f"  [{'x' if done else ' '}] {name}")
        return rows

    def run_next(self, model: str | None = None):
        """
        Run the next not-yet-completed stage, write its output, and stop.

        This is the human-in-the-loop default: run one stage, then review (and
        optionally edit) ``output/output.md`` before calling ``run_next`` again.

        Returns:
            dict with ``stage``, ``output_path`` and ``output``, or ``None`` if
            every stage is already done.
        """
        stages = self._stages()
        for i, stage in enumerate(stages):
            if not self._is_done(stage):
                prev = stages[i - 1] if i > 0 else None
                system, prompt = self._build_messages(stage, prev)
                result = get_response(prompt, system=system, model=model)

                out = self._output_path(stage)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(result, encoding="utf-8")
                return {"stage": stage.name, "output_path": str(out), "output": result}
        return None

    def run_all(self, model: str | None = None, max_steps: int = 50):
        """
        Run every remaining stage in order (no review pause between them).

        Use this only once you trust the pipeline. The review-first ``run_next``
        is the recommended way to drive it. ``max_steps`` is a safety bound.
        """
        results = []
        for _ in range(max_steps):
            r = self.run_next(model=model)
            if r is None:
                break
            results.append(r)
        return results

    def reset(self):
        """Delete all stage outputs so the workflow can be re-run from the start."""
        for stage in self._stages():
            out = self._output_path(stage)
            if out.exists():
                out.unlink()
