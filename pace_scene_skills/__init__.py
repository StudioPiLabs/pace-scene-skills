"""Load the skills in this repository from Python.

The skill directories are the product: each is a `SKILL.md` an agent reads,
and they stay copy-pasteable into `~/.claude/skills/`. This package is the
other reader. A program that compiles a skill into an LLM call should get the
same text an agent would follow, from the same file, rather than keeping its
own copy in a string constant -- which is the drift this repository exists to
stop.

    from pace_scene_skills import load

    s = load("derive-shot-design")
    s.description                  # what the frontmatter says it is for
    s.instructions                 # the SKILL.md body, frontmatter stripped
    s.reference("vocabulary.yaml") # parsed, from references/

`PACE_SKILLS_PATH` overrides where skills are read from, so a checkout can be
pointed at without reinstalling.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

__all__ = ["Skill", "load", "available", "skills_root", "SkillNotFound"]


class SkillNotFound(LookupError):
    """Raised with the names that do exist, since a typo is the likely cause."""


def skills_root() -> Path:
    """Where skills are read from.

    `PACE_SKILLS_PATH` first, so a working checkout can be used without
    reinstalling; otherwise the directory this package sits beside, which is
    the repository root in a checkout and the installed data directory in a
    wheel.
    """
    env = os.environ.get("PACE_SKILLS_PATH")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve().parent
    # Installed, the skill directories sit inside the package; in a checkout
    # they sit beside it at the repository root, where they can be copied
    # straight into ~/.claude/skills/. Whichever holds them is the root.
    for cand in (here, here.parent):
        if any((c / "SKILL.md").is_file() for c in cand.iterdir() if c.is_dir()):
            return cand
    return here.parent


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Frontmatter and body. A skill without frontmatter is not a skill."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md does not open with frontmatter")
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        raise ValueError("SKILL.md frontmatter is not terminated")
    import yaml

    meta = yaml.safe_load("\n".join(lines[1:end])) or {}
    return meta, "\n".join(lines[end + 1:]).strip() + "\n"


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    instructions: str
    path: Path

    def reference(self, filename: str) -> Any:
        """A file under this skill's `references/`.

        YAML and JSON come back parsed, anything else as text. The parsed form
        is the point: the numbers a program needs and the numbers an agent
        reads are then the same bytes.
        """
        p = self.path / "references" / filename
        if not p.is_file():
            have = sorted(x.name for x in (self.path / "references").glob("*")) \
                if (self.path / "references").is_dir() else []
            raise FileNotFoundError(f"{self.name} has no reference {filename!r}; has {have}")
        text = p.read_text()
        if p.suffix in (".yaml", ".yml"):
            import yaml
            return yaml.safe_load(text)
        if p.suffix == ".json":
            import json
            return json.loads(text)
        return text

    def prompt(self, **fields: Any) -> str:
        """The instructions with `{field}` placeholders filled in.

        Only the named fields are substituted; a brace the skill uses for
        anything else (JSON shapes appear throughout) is left alone.
        """
        out = self.instructions
        for k, v in fields.items():
            out = out.replace("{" + k + "}", str(v))
        return out


@lru_cache(maxsize=None)
def _load(name: str, root: str) -> Skill:
    d = Path(root) / name
    f = d / "SKILL.md"
    if not f.is_file():
        raise SkillNotFound(f"no skill {name!r} under {root}; have {available()}")
    meta, body = _split_frontmatter(f.read_text())
    declared = meta.get("name")
    if declared != name:
        raise ValueError(f"{f} declares name {declared!r} but sits in {name!r}")
    return Skill(name=name, description=(meta.get("description") or "").strip(),
                 instructions=body, path=d)


def load(name: str) -> Skill:
    """The skill by directory name, e.g. `load("split-into-scenes")`."""
    return _load(name, str(skills_root()))


def available() -> list[str]:
    root = skills_root()
    return sorted(p.name for p in root.iterdir()
                  if p.is_dir() and (p / "SKILL.md").is_file())
