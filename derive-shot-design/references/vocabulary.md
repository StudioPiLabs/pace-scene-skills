# Closed vocabularies

Every value `derive-shot-design` returns comes from these lists. They are the
compilers' own enum values, so a token outside them produces a field nothing
downstream can read. A skill is only as typed as the vocabulary it answers in.

## `shot_size`

```
extreme_close_up   close_up   medium_close_up   medium
medium_full        full       wide              extreme_wide
```

## `angle`

```
eye_level   low_angle   high_angle   overhead   dutch
```

## `camera_movement`

```
static   handheld   steadicam   crane_up   crane_down
push_in  pull_out   tracking
```

Rig behaviour and framing moves are different fields. A rig (`handheld`,
`steadicam`, `tripod`) belongs to the trajectory's `gear`; a framing move
(`push_in`, `crane_up`, `tracking`) belongs to `movement_3d`. Both names
appear above because a corpus already stored `handheld` where it is not a
legal value and lost it to a `tripod` default. Say which one you mean.

## The film's own top matter

`derive-shot-design` reads three of these. They are the treatment's own
headings, and the author's sentence under each is what to pass through
verbatim.

| field | heading |
|---|---|
| genre | 题材 |
| source | 核心溯源 |
| worldview | 世界观设定 |
| theme | 核心主题 |
