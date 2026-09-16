---
name: split-into-scenes
description: >-
  Cuts a screenplay into scenes on a stated boundary rule (a change of
  location, time-of-day, or character constellation) and returns each scene
  as typed fields, including the key_actions list that sets the initial shot
  granularity. Use when breaking a script or treatment into scenes, building
  a shot list or storyboard breakdown from a screenplay, or when asked how
  many scenes or shots a script contains.
license: Apache-2.0
---

# Split a screenplay into scenes

You are a script supervisor. Break the script into individual scenes.

## The boundary rule

A scene = continuous action in ONE location at ONE time-of-day with ONE set
of characters. A scene change occurs whenever location, time, OR all
characters leave / enter.

A change of *focused action* is **not** a scene boundary. An action change
inside one location at one time is a shot boundary, and it is handled by
`key_actions` below.

## What to return for each scene

| field | type | note |
|---|---|---|
| `scene_number` | int | 1-indexed |
| `heading` | str | `INT./EXT. LOCATION - TIME OF DAY`, uppercase |
| `interior_exterior` | `INT` \| `EXT` | |
| `location_raw` | str | location as it appears in the text |
| `time_of_day` | str | night, morning, dusk, afternoon |
| `characters_present` | list[str] | lowercase |
| `summary` | str | one sentence |
| `story_beat` | str | 1-3 word arc tag: opening / first connection / climax |
| `story_text` | str | the verbatim text passages that fall in this scene |
| `implied_shot_count` | int | rough estimate of shots needed to cover the scene |
| `key_actions` | list[str] | the discrete physical actions that drive the scene |
| `era` | str \| null | period; null if unknowable |
| `region` | str \| null | place/setting; null if unknowable |
| `culture` | str \| null | short snake_case cultural/visual context tag |

Infer `era` / `region` / `culture` from the scene's own content: period cues,
place names, characters, props. Do **not** assume any specific film. A model
that recognises the film answers from the film instead of from the text.

Return ONE JSON object: `{"scenes": [...]}`. No prose, no markdown fences.

## What this skill does not settle

`key_actions` sets the initial shot granularity, one shot and one starter
panel per action. It is a **definition, not a decision rule**: nothing in it
says what makes two movements one action rather than two, so that granularity
is the model's. It also reads nothing from a world-state timeline, which is
what separates it from `segment-on-state-change`. Where the cuts belong at
this level is not evaluated here.

If you need a decomposition with a decision rule behind it, use
`segment-on-state-change`. If you need to know how each stretch of the film
should be shot, use `derive-shot-design`.
