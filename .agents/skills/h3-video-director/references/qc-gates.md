# H3 quality gates

Generation success is not acceptance. Apply gates in order so expensive work happens only after cheap failures are removed.

## Gate 0 — contract

- Requirements and assumptions are explicit.
- H3 mode matches the references and endpoint requirement.
- Timeline covers the full duration.
- A motion envelope defines one path, cadence, allowed body motion, direction changes, and ease-in/ease-out; timeline beats preserve velocity continuity.
- Subject, hand, and prop counts are fixed.
- Every visible subject has a gaze target and expression state for every beat, including the first live frames.
- Hairline, hairstyle silhouette, glasses, and other high-frequency temporal locks are explicit when visible.
- Acceptance checks can be observed or measured.

## Gate 1 — anchors and graph

- Every keyframe passes anatomy, ownership, identity, and prop-count inspection at full resolution.
- Start and end anchors are physically compatible.
- For first/last conditioning, anchor comparison shows no unexplained large landmark displacement, contact change, new occlusion, or background-geometry change that would cause endpoint pull.
- Workflow validates against live nodes and model files.
- Seed, model names, prompt hash, reference hashes, dimensions, frames, fps, and duration are captured before execution.

## Gate 2 — native proof

Review the raw/native output before upscaling:

- scrub every frame for hands, faces, props, reflections, flashes, black frames, and composition jumps;
- inspect face, hand, high-contrast edge, text, jewellery, glass, and foliage/tree ROIs;
- inspect adjacent-frame face and hair crops at 100% scale; reject vacant gaze, frozen affect, hairline crawl, strand regeneration, edge pulsing, and shimmer even when identity still reads correctly;
- verify the first live second separately: eyes must have the intended target and responsive micro-expression instead of waiting blankly for a later beat;
- review motion at normal speed and 0.5×; reject freeze-then-burst cadence, pose catch-up, unplanned reversals, or abrupt speed changes at timeline boundaries;
- inspect adjacent-frame strips around every beat boundary and the largest motion-delta spikes; metrics may locate problems but never override visual anatomy/trajectory review;
- verify there is one contiguous acceptable window of the required length;
- reject a take with a hidden mid-shot morph even if sparse contact sheets look good;
- compare start/end states against the scene contract.

Do not start a costly upscale until the source sequence passes.

## Gate 3 — assembly

- Scene ranges cover the delivery timeline with no gaps, overlaps, or off-by-one errors.
- Locked scenes are byte/frame identical when the contract says unchanged.
- Cuts occur on intended frames.
- Audio mapping and duration match.
- User-approved exceptions, such as a flash, are recorded as explicit decisions.

## Gate 4 — upscale

- Compare native, upscaled, and encoded ROI crops.
- Check temporal high-frequency variance: a sharper still can produce worse shimmer.
- Inspect face details, hair, tree needles, jewellery, glass edges, and background texture.
- Use one immutable cache per upscale profile; never reuse a stale frame directory.
- Prefer native high-resolution generation or model-native regeneration when available and identity-safe.
- If using per-frame GAN upscaling, keep denoise/restoration conservative and test temporal stability before choosing sharpness.

## Gate 5 — final encode

Verify:

- container, codec, pixel format, width, height, fps, frame count, and exact duration;
- audio stream, sample rate, channels, sync, and intended loudness;
- no black/frozen/corrupt frames;
- final encoded output, not just the PNG sequence, passes visual review;
- a user-facing H.264 MP4 with yuv420p and +faststart exists and is the file actually reviewed; a MOV/ProRes mezzanine alone is not a valid handoff;
- SHA-256, byte size, source mapping, and QC verdict are recorded.

If an interpolated delivery is requested, version it separately from the accepted native take. Verify its actual fps, timestamps, frame count, duration and audio sync, then inspect synthetic in-between frames at hands, faces, hair, glasses, occlusions and direction changes. Interpolation does not turn a structurally jerky native take into PASS.

## Verdicts

- **PASS:** all hard requirements pass.
- **PASS WITH ACCEPTED LIMITATION:** a named limitation is visible, understood, and explicitly accepted.
- **REPAIR:** defect is localized and a bounded repair plan exists.
- **REGENERATE:** identity, anatomy, ownership, motion, or composition is structurally wrong.

Never bury a known defect under “looks good overall.” Record it with scope, severity, and the user's decision.
