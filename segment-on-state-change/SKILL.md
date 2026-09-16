---
name: segment-on-state-change
description: >-
  Cuts an ordered event list into beats at a change of dramatic state, scoring
  six boundary features against thresholds and treating one strong signal as
  sufficient on its own. Use when a decomposition needs a decision rule rather
  than a judgment call, when each unit must carry the world state before and
  after it, or when a downstream stage has to be handed a claim it can be
  checked against.
license: Apache-2.0
---

# Segment an event list into beats at a change of state

A beat is the smallest unit in which the world changes. Each one is a triple
`(state_before, transition, state_after)`.

Read the state from a **world-state timeline**, not from the beat's own
events. That is the property that stops a later beat quietly restoring what an
earlier one changed.

The gain over asking a model to split the scene itself is not a better cut but
a **checkable** one: a returned list of beats carries nothing to hold a later
stage to, whereas a beat that names the state before and after gives whatever
is built from it a claim that can be discharged and read back.

## The six boundary features

Each is scored on `[0, 1]` over an adjacent pair of events. The weights, the
thresholds and the signals strong enough to split on their own are in
[references/parameters.yaml](references/parameters.yaml); read it rather than
working from a number quoted in prose.

| feature | source |
|---|---|
| `state_change` | the IR; whether the later event carries one |
| `focus_shift` | the IR; whether the actor differs |
| `goal_shift` | adjudicator model |
| `spatial_shift` | **unmeasurable** where events carry no location |
| `reveal` | adjudicator model |
| `importance_delta` | the IR |

Leave a feature unmeasured rather than inventing it. `spatial_shift` has no
source when events carry no location of their own, and estimating it from
text distance would be a guess wearing a weight.

## The score

Renormalise over what was actually measured, so the score stays on `[0, 1]`
and a corpus missing one feature does not silently become unable to reach the
split threshold.

```
S = sum(w_g * f_g for g in measured) / sum(w_g for g in measured)
```

## The decision

```
SPLIT       if any feature reaches its sufficient-alone threshold,
            or S >= thresholds.tau_high
MERGE       if S <= thresholds.tau_low
ADJUDICATE  otherwise
```

A merge and an unresolved adjudication both keep the events together, because
over-splitting produces beats with no state change in them, and those have
nothing to depict.

The single-signal clause is a measured choice, not a preference. Under the
weighted sum alone, 40 of 41 adjudicated pairs merged; admitting one strong
signal took one film from 26 beats to 39.

## What this skill does not settle

Where the boundaries belong. A partition holds by construction, and any sound
merge rule preserves the transitions, so neither of the usual counts
distinguishes a 39-beat cut from a 26-beat or a 79-beat one. Scoring that
takes a human reference segmentation and a measure such as WindowDiff or
`P_k`, against an inter-annotator ceiling.
