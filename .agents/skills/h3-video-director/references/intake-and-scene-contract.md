# Intake and scene contract

Use a compact interview only for information that changes the result. Group questions so the user can answer quickly, and lead each one with a recommended default.

## Minimum intake

Ask at most five grouped questions on the first pass:

1. **Delivery:** platform, aspect ratio, duration, fps, resolution, safe areas. Recommend 9:16, 24 fps, and one 4–6 second generated shot when the user has no delivery spec.
2. **Cast and references:** exact physical subject count, identity priority, wardrobe, screen positions, and supplied image/video/audio references.
3. **Action:** one main action, observable start state, observable end state, intended cadence/easing, direction changes, and whether a cut is allowed.
4. **Camera and sound:** shot size, camera motion, dialogue/language, diegetic sound, music, and final hold.
5. **Constraints and execution:** elements to preserve/avoid, acceptance criteria, local hardware versus cloud, time budget, and permission for paid services or downloads.

Do not ask what the repository, attached files, or prior approved decisions already answer. If the user says “choose for me,” record a conservative recommendation rather than asking again.

## Readiness classes

- **Ready:** duration, subject count, action, start/end states, camera, and acceptance are explicit. Summarize and proceed.
- **Ready with assumptions:** gaps are low risk and the user delegated choice. Record assumptions and proceed.
- **Blocked by a material choice:** alternatives change identity, conditioning mode, cost, or edit structure. Ask the smallest possible question.
- **Infeasible as written:** explain the conflict and offer a technically feasible rewrite.

## Scene contract fields

Use [../assets/scene-contract.template.json](../assets/scene-contract.template.json) as the starting point.

- `scene_id`: stable identifier used everywhere.
- `intent`: what the audience must understand or feel.
- `duration_seconds`, `fps`, `aspect_ratio`: delivery contract.
- `mode`: one of `t2va`, `i2va`, `fl2va`, `ref2va`, or `multiframe_control`.
- `inputs.frame_anchors`: zero, one, or two boundary frames.
- `inputs.references`: labelled image/video/audio references for Ref2VA.
- `subjects`: exact physical people/creatures, stable IDs, screen position, identity and wardrobe locks, visible hand count.
- `props`: exact instance count, owner, hand, initial state, final state, and whether a handoff occurs.
- `timeline`: contiguous intervals from 0 to the full duration. Each interval has one visible beat and resulting state.
- `motion`: one physical path, cadence, easing, allowed body motion, locked contacts, direction changes, and native/interpolated delivery policy.
- `camera`: framing, motion type, amplitude, speed, and final framing.
- `audio`: dialogue, language, ambient sound, effects, music, and lip-sync requirement.
- `locks`: facts that must not change.
- `avoid`: concise, testable failure states; not a substitute for positive geometry.
- `acceptance`: statements that can be checked on frames or the final encode.
- `execution`: backend preference and permissions.

## Contract quality test

A different operator should be able to answer all of these without guessing:

- Who is physically present, where are they, and how many hands are visible?
- What changes during the shot, and what is unchanged?
- What single motion path connects the states, and do speed/direction remain continuous at every timeline boundary?
- Which body owns every visible hand and which hand owns every prop?
- What does the camera do and when does it stop?
- What exact state must be visible in the final half-second?
- What evidence decides pass or fail?

If not, the contract is not ready for generation.
