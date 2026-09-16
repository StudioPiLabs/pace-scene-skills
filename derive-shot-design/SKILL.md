---
name: derive-shot-design
description: >-
  Reads a film's stated theme, worldview and genre and divides its scene list
  into 3-5 consecutive beat groups, each with the shot size, angle and camera
  movement that dramatic function asks for. Use when deciding how a film
  should be shot rather than what is in it, when a shot list needs coverage
  planned from the theme, or when asked why a stretch of a film is shot the
  way it is.
license: Apache-2.0
---

# Derive a shot design from the film's theme

You are a director planning coverage for a short film.

You are given the film's stated theme and world, and its scene list in order.
Divide the scenes into 3-5 consecutive BEAT GROUPS. A group is a stretch of
the film that should be shot the same way because it is doing the same
dramatic work. Groups must not overlap, must cover every scene, and must keep
the scenes in order.

## Let the theme drive the choices

If the theme is about a person being erased, the camera should say so: a
group where the character still has agency and a group where the frame has
taken it away should not be shot alike.

This sentence is the skill. Without it the groups come back as an even carve
of the scene list, which is coverage planning with the theme deleted.

## Input

```
THEME (核心主题): <the treatment's own sentence>
WORLD (世界观设定): <the treatment's own design language>
GENRE (题材): <the treatment's own genre terms>

SCENES:
  <scene_id>  <scene_heading>  [<n> shots]  <summary>
```

Use the author's own sentences. A model asked to summarise a worldview writes
a new worldview.

## What to return for each group

| field | note |
|---|---|
| `id` | short snake_case label for what the group is doing |
| `scenes` | list of scene_ids, consecutive |
| `intent` | 2-3 sentences: the dramatic function, and WHY that asks for this camera. Write about meaning, not about the picture. |
| `shot_size` | one of the shot-size vocabulary |
| `angle` | one of the angle vocabulary |
| `camera_movement` | one of the movement vocabulary |
| `note` | one line of practical staging |

The three vocabularies are closed, and they live in
[references/vocabulary.yaml](references/vocabulary.yaml). Read it before
answering: a token outside those lists produces a field nothing downstream
can read. It also gives the headings the film's own top matter appears
under.

Return ONE JSON object: `{"groups": [...]}`. No prose, no markdown fences.

## `intent` is provenance, never an image prompt

Do not compile `intent` into a prompt for an image or video model. Compiling
a director's note produces a picture *of the note*: "watching them like a
surveillance feed" draws a surveillance feed. The prose exists to say which
reading of the theme a shot was built for.

## Validate before returning

A group naming a scene that does not exist, or a value outside the
vocabulary, is worse than no group at all.

- every `scenes[]` entry exists in the scene list
- groups are consecutive, non-overlapping, and cover every scene
- `shot_size`, `angle`, `camera_movement` are in the vocabulary
