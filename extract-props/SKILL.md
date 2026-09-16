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

A prop is a **portable object**, distinct from architectural fixtures and
wardrobe. The boundary is what the production has to source and hand to
someone, not what appears in the frame.

Do **not** include:

- architectural fixtures (lights, doors, windows, walls) — those belong to the
  location bible
- wardrobe and clothing — those belong to the character records
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
| `continuity_states` | optional dict; named states the prop can be in (open/closed, lit/dark) |
| `production_notes` | optional one-sentence note about why the prop matters |

`category` is closed. It lives in
[references/categories.yaml](references/categories.yaml); a value outside that
list produces a field nothing downstream can read.

`id` is the key everything else resolves against, so it has to be stable
across scenes: the same object named twice under two ids becomes two props,
sourced twice and dressed differently.

Return ONE JSON object: `{"props": [...]}`. Output JSON only, no prose, no
markdown fences.
