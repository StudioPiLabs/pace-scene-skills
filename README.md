# pace-scene-skills

Five [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
that break a screenplay down **into a [PACE](https://github.com/StudioPiLabs/pace-core)
document**.

That is the thing to know about them. They do not return notes about a script;
they return typed fields in a schema a compiler reads, stages as 3D geometry,
renders, and then measures the result against. The vocabularies below are
closed because they are PACE's own enums: a token outside one of them is not a
loose answer, it is a field nothing downstream can read and a value the
delivered frame will not carry.

They were lifted out of Python, where they had been living as prompt constants
and module-level tuples. That is the other reason this repository exists: a
decomposition criterion that only exists inside a prompt string cannot be
read, versioned, or disagreed with by anyone who is not reading the source.

## The skills

| skill | decides | writes into the PACE document |
|---|---|---|
| [`split-into-scenes`](split-into-scenes/) | where a scene ends: a change of location, time, or character constellation | the scenes, and the `key_actions` that set the initial shot count |
| [`derive-shot-design`](derive-shot-design/) | how each stretch of the film is shot, from its stated theme, world and genre | `camera.creative_intent` and the `_design` provenance behind it |
| [`segment-on-state-change`](segment-on-state-change/) | where a beat begins: a change of dramatic state, scored and thresholded | the beats a panel is built from, each with the state before and after |
| [`extract-props`](extract-props/) | what a production has to source and hand to someone | `setup.props` |
| [`enrich-to-scine`](enrich-to-scine/) | the leaf fields a director left implicit | framing, lighting, action, emotion, eyeline, screen placement, backdrop |

They are not alternatives. A scene split gives the shot list its initial
granularity; the shot design says how each stretch of that list should be shot
and why; beat segmentation is a separate, finer cut that a panel can be built
from directly; the last two fill in what the first three leave null.

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

## Vocabularies that are not here

`enrich-to-scine` answers in the largest vocabulary of the five, and it is
**not** in this repository. Its caller generates an `ALLOWED VALUES` section
from the live PACE schema and appends it to the instructions, so that
vocabulary and the code that validates against it cannot drift apart. Freezing
a copy here would create exactly the split this repository exists to close.

The smaller closed lists that do not move with the schema are bundled:
`derive-shot-design/references/vocabulary.yaml` and
`extract-props/references/categories.yaml`.

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

`extract-props` and `enrich-to-scine` both prefer null to a guess. An invented
prop or an over-eager enum value is worse than an absent one: a null shows as
a gap, and a wrong value shows as a fact.

## License

Apache-2.0.
