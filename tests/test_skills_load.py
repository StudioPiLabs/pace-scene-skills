"""Every skill here loads, and says what a skill has to say.

These are the checks that would have caught the first version of this
repository, which invented its own YAML schema: nothing could load it, and the
one field that decides when a skill is used at all had nowhere to live.
"""
from __future__ import annotations

import re

import pytest

from pace_scene_skills import available, load, skills_root

NAMES = available()


def test_there_are_skills_to_load():
    assert NAMES, f"no SKILL.md found under {skills_root()}"


@pytest.mark.parametrize("name", NAMES)
def test_the_directory_name_is_the_skill_name(name):
    """An agent addresses a skill by its directory; frontmatter that says
    something else makes the two disagree about what was loaded."""
    assert load(name).name == name


@pytest.mark.parametrize("name", NAMES)
def test_the_name_is_kebab_case(name):
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)


@pytest.mark.parametrize("name", NAMES)
def test_the_description_states_when_to_use_it(name):
    """The description is the trigger. One that only says what the skill is
    leaves an agent no way to decide it applies here."""
    d = load(name).description
    assert d, "no description"
    assert len(d) <= 1024, f"{len(d)} characters"
    assert "Use when" in d, "description names no trigger"


@pytest.mark.parametrize("name", NAMES)
def test_the_instructions_survive_the_frontmatter_strip(name):
    body = load(name).instructions
    assert body.strip(), "empty body"
    assert not body.lstrip().startswith("---"), "frontmatter leaked into the body"
    assert body.lstrip().startswith("#"), "body does not open with a heading"


@pytest.mark.parametrize("name", NAMES)
def test_every_relative_link_resolves(name):
    s = load(name)
    for link in re.findall(r"\]\((?!https?:)([^)#]+)\)", s.instructions):
        assert (s.path / link).exists(), f"{name}: broken link {link}"


def test_the_vocabularies_are_closed_lists():
    v = load("derive-shot-design").reference("vocabulary.yaml")
    for key in ("shot_size", "angle", "camera_movement"):
        assert isinstance(v[key], list) and v[key], key
        assert len(set(v[key])) == len(v[key]), f"{key} repeats a value"


def test_the_segmenter_parameters_are_usable_as_numbers():
    """A weight or a threshold read as a string is a comparison that silently
    does the wrong thing."""
    p = load("segment-on-state-change").reference("parameters.yaml")
    assert all(isinstance(w, (int, float)) for w in p["weights"].values())
    assert 0 < p["thresholds"]["tau_low"] < p["thresholds"]["tau_high"] < 1
    assert set(p["measurable_from_ir"]) <= set(p["weights"])
    assert set(p["sufficient_alone"]) <= set(p["weights"])


def test_the_numbers_live_in_one_place():
    """SKILL.md points at parameters.yaml rather than restating it. A
    threshold written twice eventually disagrees with itself."""
    body = load("segment-on-state-change").instructions
    p = load("segment-on-state-change").reference("parameters.yaml")
    for value in list(p["weights"].values()) + list(p["thresholds"].values()):
        assert f"{value}" not in body, f"{value} is quoted in the prose as well"


def test_a_missing_skill_names_the_ones_that_exist():
    from pace_scene_skills import SkillNotFound

    with pytest.raises(SkillNotFound) as e:
        load("no-such-skill")
    assert "derive-shot-design" in str(e.value)
