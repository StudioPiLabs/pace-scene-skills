# pace-scene-skills

The skills that break a screenplay down for [PACE](https://github.com/StudioPiLabs/pace-core):
how a script is cut into scenes, how a film's theme, world and genre decide the
way each stretch is shot, and where a beat begins.

They are data, not code. Each is a YAML file holding the criterion, the fields
it returns, the closed vocabulary it answers in, and what it does **not**
settle. `pace-core` reads them; nothing here imports anything.

They were lifted out of Python, where they had been living as prompt constants
and module-level tuples. That is the whole reason this repository exists: a
decomposition criterion that only exists inside a prompt string cannot be
read, versioned, or disagreed with by anyone who is not reading the source.

## The three levels

| level | skill | what decides the cut |
|---|---|---|
| scene | [`split_into_scenes`](skills/scene/split_into_scenes.yaml) | a change of location, time, or character constellation |
| film  | [`derive_shot_design`](skills/shot/derive_shot_design.yaml) | the film's stated theme, world and genre |
| beat  | [`segment_on_state_change`](skills/beat/segment_on_state_change.yaml) | a change of dramatic state, scored and thresholded |

They are not alternatives. A scene split gives the shot list its initial
granularity; the shot design says how each stretch of that list should be shot
and why; beat segmentation is a separate, finer cut that a panel can be built
from directly.

## What each one refuses to claim

This is the part worth reading before using them.

`split_into_scenes` carries a real boundary criterion, and its
`key_actions` field, which sets the initial shot count at one shot per action,
carries only a **definition**. Nothing in it says what makes two movements one
action rather than two, and it reads nothing from the world-state timeline. The
granularity is the model's, and where those cuts belong is not evaluated.

`derive_shot_design` returns an `intent` paragraph that is **never compiled
into an image prompt**. Compiling a director's note produces a picture of the
note: "watching them like a surveillance feed" draws a surveillance feed. The
prose is provenance, saying which reading of the theme a shot was built for.

`segment_on_state_change` is the only one with a decision rule, and it still
does not claim the cut is *right*. A partition holds by construction and any
sound merge rule preserves the transitions, so the usual counts cannot tell a
39-beat cut from a 26-beat one. Scoring that needs a human reference
segmentation.

## Using them

Read the YAML. Build the prompt or the rule from its fields, and return into
[`vocabulary.yaml`](skills/vocabulary.yaml) — a token outside those lists
produces a field the compilers cannot read.

A skill is only as typed as the vocabulary it answers in, so keep
`vocabulary.yaml` in step with the schema's enums in `pace-core`.

## License

Apache-2.0.
