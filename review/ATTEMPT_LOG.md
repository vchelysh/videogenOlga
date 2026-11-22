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

## v5 selective scene repair

### Scene 01 take 01 — partially accepted

- Resolution: 576×1024; length: 124 frames; seed: 6122101.
- Accepted source window: frames 0-28.
- Rejected scope: frames 29-123, where candle flames progressively became decorative starburst rays.
- Repair: the accepted contiguous 29-frame window was deterministically resampled to 48 delivery frames with FILM.

### Scene 04 take 01 — rejected

- Resolution: 576×1024; length: 124 frames; seed: 6122104.
- Reason: the bright flash guide progressively bloomed even though the flash stayed attached.
- Decision: correct the guide to dark non-emissive plastic and regenerate.

### Scene 04 take 02 — accepted

- Resolution: 576×1024; length: 124 frames; seed: 6123113.
- Accepted source window: frames 15-62, mapped directly to delivery frames 145-192.

### Scene 03 interrupted recoveries — no output selected

- Prompt `a0823044-da9d-4f00-af3c-d6c92289ecb1` was interrupted by power loss immediately after start.
- Prompt `0dca17f2-00ea-45b2-85c0-5816876fac9b` was interrupted when the recovery session closed during model initialization.
- Neither prompt produced a saved scene master; both were discarded.

### Scene 03 take 01 — accepted production pass

- Resolution: 576×1024; length: 124 frames; seed: 6122103; prompt ID: `f533c611-3400-4f27-9a31-355b573e8b16`.
- Result: success after 12.0 minutes; ProRes 4444 source saved at `outputs/raw/v5/PhotoDay_H3_v5_scene03_take01_576x1024_124f.mov`.
- Source SHA-256: `D6685B8C327E016DC5395AF45E424F42E298CC8070BA46C7023ECDDA543D0DF9`.
- All 124 frames were reviewed; frames 0-47 were accepted without temporal interpolation and mapped to delivery frames 97-144.
- Acceptance: one continuous makeup shot, exactly three physical women, no photographer/camera, no internal cut or composition jump.

### v5 repaired sharp delivery — accepted

- The assembler was changed so scene 03 is a required input and the defective v4 range 97-144 cannot be reused silently.
- Final artifact: `outputs/PhotoDay_06-12_MINIMAX_H3_v5_REPAIRED_SHARP_1080x1920_FINAL.mp4`.
- Final SHA-256: `79562C826A47AD880E1E95A31B22E6ED0529025F37ACE7C6D0ADE941228DA4A3`.
- QC status: PASS; see `review/QC_REPORT_v5_REPAIRED_SHARP.md`.
