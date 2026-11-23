# H3 structured prompt formats

Use stable subject and reference labels from the scene contract. Keep the prompt chronological and observable. Avoid literary backstory that cannot appear on screen.

## FL2VA family: T2VA, I2VA, first/last frame

Use three top-level sections:

1. `integrated_multimodal_description`
2. `overall_soundscape`
3. `non_diegetic_music`

Within the integrated description:

- state how supplied frame images anchor the shot, if any;
- establish composition, subjects, wardrobe, props, environment, lighting, and initial state;
- describe action onset, continuous development, settling, and the locked result;
- specify camera motion by type, meaningful amplitude, speed, and final framing;
- state identity, colour, object, count, and spatial locks.

## Face performance and temporal edge locks

For every visible face, specify a continuous state rather than only a late reaction:

- gaze target: partner, lens, prop, or a declared off-screen point;
- expression: neutral-but-engaged, restrained smile, concern, and so on;
- micro-performance: natural blink, eye refocus, cheek/eyebrow response, closed or speaking mouth;
- transition time: when the expression begins changing and when it settles.

If a subject must look emotionally present from the beginning, say so in the establish beat: “from the first live frame his eyes remain focused on his partner, with responsive eyelids and a faint warm micro-smile; never a fixed or vacant stare.” Do not postpone all facial direction to the settle beat.

For hair and other high-frequency features, name the fixed geometry: hairline, outer hairstyle silhouette, major curl/strand groups, glasses rims, face contour, and their allowed motion. When no motion is wanted, use a positive lock such as “the hairstyle moves as one stable shape with the head; individual strands and edges do not flutter, crawl, pulse, or regenerate frame to frame.”

For first-frame I2VA, use:

`first-frame anchor → action begins → continuous change → reaction/result → final hold`

For first/last-frame FL2VA, use:

`first state → physically plausible intermediate changes → only intended differences → exact last state`

Keep it one shot unless a timestamped cut is truly required. If cuts are required, number them and cover the full duration without overlap.

## Ref2VA

Use six sections:

1. `subject_definitions`: map each stable subject ID to reference labels.
2. `summary`: one-sentence dramatic and visual goal.
3. `retention_analysis`: state what identity, wardrobe, motion, camera, voice, style, or environment each reference contributes.
4. `detailed_description`: chronological visible action with composition, positions, environment, lighting, camera, sound, and explicit reference use.
5. `overall_soundscape`.
6. `non_diegetic_music`.

Use the same labels in every section. Do not refer to “the woman” if two women are present; use stable IDs such as `heroine`, `stylist`, and `photographer`.

## Timeline grammar

For a six-second shot:

- `0.0–1.0 s — establish`: prove counts, ownership, and starting pose.
- `1.0–2.0 s — prepare`: small anticipatory motion.
- `2.0–4.5 s — execute`: one main action with continuous geometry.
- `4.5–5.5 s — settle`: reaction and deceleration.
- `5.5–6.0 s — end-state lock`: no new action; hold the required result.

Intervals must cover the full duration with no gaps or overlaps. The state at the start of an interval must match the locked state from the prior interval.

The intervals describe one continuous motion envelope. State the physical path once, then give its ease-in, steady portion, deceleration, and hold. At every boundary preserve position, direction, and velocity; do not use a sequence of independent verbs that imply a pause and restart. Name every intentional reversal, normally no more than one in a short shot.

For natural human movement, state what is allowed to move together: weight shifts through hips and feet, shoulders follow the torso, elbows and joined hands travel with the shared body path, and the head follows with a small bounded lag. Use locks for identity, ownership and contact rather than freezing all joints.

Example continuity clause: `One uninterrupted low-frequency sway follows a single smooth path. It accelerates gradually from rest, keeps an even cadence through both timeline boundaries, then decelerates over one full second into the final hold; no pause, snap, catch-up jump or unplanned reversal.`

## Camera language

Always specify:

- movement type: locked, pan, tilt, dolly, truck, pedestal, crane, orbit, handheld, zoom;
- amplitude: none, subtle, small, medium, or an observable endpoint;
- speed/easing: static, slow, steady, accelerating, decelerating;
- subject relationship: keeps heroine centred, reveals photographer, ends on close-up;
- end state: camera settles and holds.

Avoid contradictory combinations such as “locked tripod” and “handheld drift.”

## Exclusions

Keep exclusions short and testable:

- no new physical person enters;
- exactly one instance of each glass;
- no cut or composition morph;
- no detached, duplicated, or ownerless hand;
- no light source blooms unless the contract allows a timed flash.
- no vacant gaze, frozen affect, hairline crawl, strand regeneration, or frame-to-frame edge shimmer.

Positive state and ownership descriptions come first.
