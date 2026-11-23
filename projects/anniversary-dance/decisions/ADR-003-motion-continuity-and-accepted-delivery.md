# ADR-003: accept delivery and productionize motion-continuity QC

- Status: Accepted
- Date: 2026-11-24

## Context

The v2 FL2VA repair fixed the opening male gaze and materially reduced hair instability. The RealESRGAN delivery passed technical and visual review and the user accepted it. A later frame-difference analysis found a mild periodic freeze/burst cadence in both the H.264 review MP4 and the ProRes mezzanine, so the remaining jerkiness is not an MP4-container problem.

The prompt strongly locked heads, hands, hair, camera and background while requesting a coordinated step and turn. The last anchor was chosen from a prior generated clip primarily for its smile. These choices protected identity and contacts but may have reduced the degrees of freedom available to form a natural trajectory. Public reports also show checkpoint- and runtime-specific periodic artifacts, but no report proves the cause of this run.

## Decision

1. Accept `scene-01-upscale-realesrgan-x2-v1_00001__delivery.mp4` as the project master and preserve the native and upscale runs.
2. Do not alter the accepted master with interpolation, temporal denoise, or another generative repair.
3. Add a reusable motion envelope to future scene contracts: path, cadence, easing, direction changes, allowed coordinated body motion, locked contacts, and delivery cadence.
4. Treat FL2VA anchors as boundary states that must be compatible in pose, contact, occlusion, geometry and intended velocity; a good expression alone is insufficient.
5. Use a base/non-Turbo native baseline and a controlled three-to-five-seed grid before promoting acceleration or post-processing to a default.
6. Score motion smoothness, dynamic degree, temporal flicker, subject integrity, background consistency and action adherence separately.
7. Treat exact periodic frame cadences as a possible runtime/checkpoint/decode clue. Record the full reproduction matrix and test one variable at a time.
8. Allow optional FILM/RIFE interpolation only after the native clip passes structural QC, as a separate immutable run with exact-duration and audio-sync checks.

## Consequences

- The accepted project remains stable and immediately usable.
- Future scenes will spend more effort on motion design and small controlled candidate grids, reducing expensive blind repairs.
- Smoothness can no longer be improved by making a clip static or by hiding structural errors with interpolation.
- Community workflows, LoRAs and code patches remain hypotheses until authorized and validated against representative local scenes.
