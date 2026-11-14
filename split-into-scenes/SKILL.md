---
name: split-into-scenes
description: >-
  Cuts a screenplay into the scenes of a PACE document, on a stated boundary
  rule grounded in explicit headings and continuous place/time, and
  returns each scene as typed PACE fields including the key_actions list that
  sets the initial shot granularity. Use when breaking a script or treatment into scenes, building
  a shot list or storyboard breakdown from a screenplay, or when asked how
  many scenes or shots a script contains.
license: Apache-2.0
---

# Split a screenplay into scenes

You are a script supervisor. Break the script into individual scenes.

The output is a **PACE document**: these are typed fields a compiler reads and
stages, not notes about the script.

## The boundary rule

A scene is continuous action in one place and time. Preserve explicit source
scene headings and their order, including numbered headings. Two separate
headings remain separate even when their location and time labels agree.
Do not split a headed scene merely because someone enters, leaves, speaks,
or becomes the focus. An offscreen voice does not establish physical presence.

For a treatment without headings, propose boundaries at changes of place or
time supported by the text. Do not invent headings to satisfy a desired count.
Mark an uncertain boundary in `source_notes` with its supporting quote.

A processing chunk is not a scene. When the caller identifies a fragment of
one explicit scene, return one scene fragment under that heading; do not
create a new scene at either edge or complete events from a later passage.

A change of *focused action* is **not** a scene boundary. An action change
inside one location at one time is a shot boundary, and it is handled by
`key_actions` below.

## What to return for each scene

| field | type | note |
|---|---|---|
| `scene_number` | int | 1-indexed |
| `heading` | str | preserve the explicit source heading; propose one only for unheaded prose |
| `interior_exterior` | `INT` \| `EXT` \| `INT/EXT` \| null | use the source; null if unknown |
| `location_raw` | str | location as it appears in the text |
| `time_of_day` | str | night, morning, dusk, afternoon |
| `characters_present` | list[str] | physically present agents, including unnamed groups; lowercase IDs |
| `dialogue` | list[object] | every spoken line in source order: `{"speaker": "id", "text": "verbatim speech", "on_screen": bool, "after_action": int \| null}` |
| `summary` | str | one sentence |
| `story_beat` | str | 1-3 word arc tag: opening / first connection / climax |
| `story_text` | str | the verbatim text passages that fall in this scene |
| `implied_shot_count` | int | rough estimate of shots needed to cover the scene |
| `key_actions` | list[str] | the discrete physical actions that drive the scene |
| `action_evidence` | list[object] | parallel to `key_actions`: `{"quote": "exact source substring"}` for each action |
| `axis` | object \| null | the line of action: `{"between": ["id", "id"]}`, the two present characters the scene's main exchange runs between; null without one |
| `coverage` | list[object] | the shots that cover the scene, in order (see below) |
| `source_notes` | list[object] | `{"kind": "footnote"\|"camera_direction"\|"sound"\|"continuity"\|"uncertainty", "quote": "exact source substring"}` |
| `era` | str \| null | period; null if unknowable |
| `region` | str \| null | place/setting; null if unknowable |
| `culture` | str \| null | short snake_case cultural/visual context tag |

Infer `era` / `region` / `culture` from the scene's own content: period cues,
place names, characters, props. Do **not** assume any specific film. A model
that recognises the film answers from the film instead of from the text.

Return ONE JSON object: `{"scenes": [...]}`. No prose, no markdown fences.
`key_actions` contains strings, never nested objects. Keep quotes in the
parallel `action_evidence` array. For example, given `Mira kneels.`, return
`"key_actions": ["Mira kneels"], "action_evidence": [{"quote": "Mira kneels."}]`.

## Preserve the event and its evidence

Write each action with its performer, concrete action and target when stated.
Keep source order and distinct participants: one person falling and another
catching them are not two people standing. Carry state changes forward until
the text changes them. A conditional plan, remembered event or spoken claim
is not automatically an action happening now. Do not turn dialogue into a
physical event or assume that every scene character appears in every shot.
Every spoken line goes in `dialogue`, once, verbatim and in source order,
with its speaker's ID from `characters_present` (or the offscreen speaker's
lowercase ID). `on_screen` is false for O.S., V.O., O.C., phone and recalled
speech. `after_action` is the 0-based index of the last `key_actions` entry
before the line in the source, or null when the line comes before every action.
A line that runs across several actions keeps the index of the action it
starts after; do not split or repeat it. Include an offscreen speaker in
`characters_present` only if separate action text establishes physical
presence in that scene. A crowd or unnamed attackers still count as agents;
do not replace them with an offscreen named speaker.

Copy evidence quotes character for character from the supplied passage; do
not combine separated lines or repair the author's wording. Quote occurrence
supports provenance, not proof that the extracted claim is correct. Keep
interpretation provisional and omit unsupported claims.

Preserve supplied footnotes, parenthetical directions and production notes
as quoted `source_notes`, including relevant camera, sound and continuity
instructions. Do not invent a footnote to explain a guess.

PDF page numbers and running headers are document furniture, not footnotes or
story actions. A footnote quote must contain the note's substantive text,
not merely its numeric marker. Camera directions belong in `source_notes`,
not in physical `key_actions`; preserve explicit black/title beats separately.
Notes can describe an intended shot or offscreen sound without establishing either in the
finished film. Script names help identify candidates; film visibility and
script-to-edit alignment require separate evidence.

Keep camera proposals and thematic interpretation separate from source
observations. A starter shot per action is an authoring scaffold, not a
recovered edit, measured duration or verified camera setup. Use the same
rules for English and Chinese source text without translating quoted evidence.

## Cover each scene with shots

`coverage` proposes the shots, in screen order. Each entry is one shot:

`{"actions": [int], "lines": [int], "shot_size": str|null, "angle": str|null, "position": str|null,
"camera_side": "A"|"B"|null, "crosses_axis": bool, "focus": "id"|null, "speaker": "id"|null,
"eyeline_to": "id"|null, "basis": "exact source substring"}`

- `actions` are 0-based `key_actions` indices the shot shows, in order. Every action is in at least one shot;
  an exchange may cover one action with several shots.
- `lines` are 0-based `dialogue` indices spoken in the shot. Every line is in exactly one shot, in source order.
- Split an exchange by turns, as shot and reverse shot on the speaker (or on a listener whose reaction is the
  point). Do not put a whole exchange between two people in one shot unless the text asks for a two-shot.
- `shot_size` is one of `establishing`, `wide`, `full`, `medium`, `medium_close_up`, `close_up`,
  `extreme_close_up`; `angle` one of `eye_level`, `high`, `low`, `overhead`; `position` one of `front`,
  `three_quarter`, `profile`, `ots`, `behind`. Choose them from what the audience must read in the shot: an entrance or a
  new place is wide or full, a spoken turn medium_close_up, a reaction or a decision close_up, a prop or a figure that carries
  the story (a phone balance, a key) extreme_close_up.
- `focus` is the one thing the audience reads: a present character's ID, or a prop named in the text.
  `speaker` is the character speaking in the shot (null for a silent shot). `eyeline_to` is who or what they look at.
- `camera_side` keeps the camera on one side of `axis`: shots of the exchange stay on `A` unless the text moves the
  camera or a character across the line; then set `crosses_axis` and quote why in `basis`.
- `basis` quotes the source text the choices rest on. Use null for any value the text gives no ground for;
  never fill one value everywhere.

These are proposals for a director to review, not a recovered edit.

## What this skill does not settle

`coverage` proposes the shots; without it `key_actions` sets the initial shot granularity, one shot and one
starter panel per action. Neither is a **decision rule**: nothing in it
says what makes two movements one action rather than two, so that granularity
is the model's. It also reads nothing from a world-state timeline, which is
what separates it from `segment-on-state-change`. Where the cuts belong at
this level is not evaluated here.

If you need a decomposition with a decision rule behind it, use
`segment-on-state-change`. If you need to know how each stretch of the film
should be shot, use `derive-shot-design`.
