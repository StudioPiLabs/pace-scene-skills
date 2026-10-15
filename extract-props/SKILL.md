---
name: extract-props
description: >-
  Reads a scene breakdown and returns every physical prop in it as PACE prop
  entries, with a category from a closed list and a short visual anchor. Use
  when building a prop list or prop registry from a script or breakdown, when
  a shot needs to know what objects are in it, or when asked which props a
  production has to source.
license: Apache-2.0
---

# Extract the props from a scene breakdown

You are a production designer. Read the scene breakdown and extract every
physical PROP that characters carry, place, hold, or that the camera lingers
on.

Each one becomes a PACE `setup.props` entry, which is staged as geometry and
named in a compiled prompt, so an invented prop is an object that gets built.

## What counts as a prop

A prop is anything the production has to **source and hand to someone**:
objects characters carry, place or hold, and the garments they wear. The
boundary is sourcing, not what appears in the frame.

Garments are props here, under `wearable`. They are not a character's
description. A costume written as a sentence on a character cannot be compared
across a cut, because there is no identifier for two shots to disagree about;
written as an entry with an id and states, a change of costume between two
shots of one scene is a fact something can report.

Do **not** include:

- architectural fixtures (lights, doors, windows, walls) — those belong to the
  location bible
- vegetation, bodies of water, large buildings — those are part of the
  location

Each of those has a home already. A prop list that swallows them produces
duplicates that then disagree with each other.

## What to return for each prop

| field | note |
|---|---|
| `id` | stable lowercase identifier with underscores, e.g. `phone`, `coffee_cup` |
| `name` | human-readable label |
| `category` | one of the category vocabulary |
| `anchor` | 6-15 word prompt fragment describing the prop visually |
| `size_m` | rough `[width, depth, height]` in metres |
| `linked_scenes` | list of `scene_id` values that reference this prop |
| `continuity_states` | optional dict; named states the prop can be in (open/closed, lit/dark, clean/soiled) |
| `worn_by` | for a `wearable` garment, the `character_id` who wears it |
| `production_notes` | optional one-sentence note about why the prop matters |

Give a garment the id `<character_id>_costume`, and
`<character_id>_costume_<name>` when a character has more than one, and set
`worn_by`. A shot then references it through `setup.subjects[].costume_id`
rather than restating the sentence or listing it in `setup.props`.

`category` is closed. It lives in
[references/categories.yaml](references/categories.yaml); a value outside that
list produces a field nothing downstream can read.

`id` is the key everything else resolves against, so it has to be stable
across scenes: the same object named twice under two ids becomes two props,
sourced twice and dressed differently.

Return ONE JSON object: `{"props": [...]}`. Output JSON only, no prose, no
markdown fences.
