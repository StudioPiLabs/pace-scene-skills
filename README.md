# pace-scene-skills

Three [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
that break a screenplay down for [PACE](https://github.com/StudioPiLabs/pace-core):
where a scene ends, how a film's theme, world and genre decide the way each
stretch is shot, and where a beat begins.

They were lifted out of Python, where they had been living as prompt constants
and module-level tuples. That is the whole reason this repository exists: a
decomposition criterion that only exists inside a prompt string cannot be
read, versioned, or disagreed with by anyone who is not reading the source.

## The skills

| skill | level | what decides the cut |
|---|---|---|
| [`split-into-scenes`](split-into-scenes/) | scene | a change of location, time, or character constellation |
| [`derive-shot-design`](derive-shot-design/) | film | the film's stated theme, world and genre |
| [`segment-on-state-change`](segment-on-state-change/) | beat | a change of dramatic state, scored and thresholded |

They are not alternatives. A scene split gives the shot list its initial
granularity; the shot design says how each stretch of that list should be shot
and why; beat segmentation is a separate, finer cut that a panel can be built
from directly.

## Installing

Each directory is a complete skill. Copy the ones you want into a skills
directory your agent reads:

```bash
git clone https://github.com/StudioPiLabs/pace-scene-skills
cp -r pace-scene-skills/derive-shot-design ~/.claude/skills/
```

`~/.claude/skills/` makes a skill available everywhere; `.claude/skills/`
inside a project scopes it to that project.

## Reading them from a program

A program that compiles a skill into an LLM call should get the same text an
agent would follow, from the same file, rather than keeping its own copy in a
string constant.

```bash
pip install git+https://github.com/StudioPiLabs/pace-scene-skills
```

```python
from pace_scene_skills import load

s = load("derive-shot-design")
s.instructions                    # the SKILL.md body, frontmatter stripped
s.reference("vocabulary.yaml")    # parsed, from references/

load("segment-on-state-change").reference("parameters.yaml")["thresholds"]
# {'tau_high': 0.55, 'tau_low': 0.2}
```

Set `PACE_SKILLS_PATH` to read from a checkout instead of the installed copy.

## What each one refuses to claim

This is the part worth reading before using them.

`split-into-scenes` carries a real boundary criterion, and its `key_actions`
field, which sets the initial shot count at one shot per action, carries only
a **definition**. Nothing in it says what makes two movements one action
rather than two, and it reads nothing from a world-state timeline. The
granularity is the model's, and where those cuts belong is not evaluated.

`derive-shot-design` returns an `intent` paragraph that is **never compiled
into an image prompt**. Compiling a director's note produces a picture of the
note: "watching them like a surveillance feed" draws a surveillance feed. The
prose is provenance, saying which reading of the theme a shot was built for.

`segment-on-state-change` is the only one with a decision rule, and it still
does not claim the cut is *right*. A partition holds by construction and any
sound merge rule preserves the transitions, so the usual counts cannot tell a
39-beat cut from a 26-beat one. Scoring that needs a human reference
segmentation.

## License

Apache-2.0.
