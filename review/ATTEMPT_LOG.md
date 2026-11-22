# Render attempt log

## Attempt 1 — rejected automatically

- Resolution: 512×896
- Length: 243 frames
- Seed: 6122026
- Prompt ID: `7d80f903-3218-451d-9533-c808af711225`
- Result: CUDA out-of-memory before sampler step 1 after 9.4 minutes.
- Cause: the continuous 243-frame latent at 512×896 exceeded the physical 8 GB VRAM limit of the RTX 3070.
- Decision: no output was selected or delivered. Return to the exact proven v1 native resolution, 448×800, preserving the continuous workflow and improve delivery detail with conservative super-resolution.

This failure is retained so the package records why 512×896 must not be retried on this hardware with the current model stack.

## Attempt 2 — externally interrupted

- Resolution: 448×800
- Length: 243 frames
- Seed: 6122026
- Prompt ID: `3dc1f0f6-7a3f-4003-8f7b-7580823f02e9`
- Result: sampler reached 1/8 successfully, then the host execution session was reset before any video file was created.
- Decision: restart the exact same deterministic graph; no creative or technical setting was changed.

## Attempt 3 — successful production pass

- Resolution: 448×800
- Length: 243 frames
- Seed: 6122026
- Prompt ID: `9eee5c9b-f1b8-4d19-b6d5-decb5fe7a8f8`
- Graph: `workflow/minimax_h3_v3_api.json`
- Result: success after 40.7 minutes; 448×800, 243 frames, 24 fps.
- Raw output: `outputs/raw/PhotoDay_H3_v3_raw_448x800_10.125s.mp4`.
- QC decision: scenes 1–3 and final portrait accepted. Raw frames 167–191 were rejected because MiniMax created a white/gold transition bloom and scene morph.
- Repair: only clean scene-4 frames 144–166 were expanded to 48 frames with FILM; raw frames 167–191 were excluded. The final portrait was not interpolated.
- Delivery: Real-ESRGAN/Lanczos enhancement to 1080×1920, exactly 240 frames / 10.000 seconds.
