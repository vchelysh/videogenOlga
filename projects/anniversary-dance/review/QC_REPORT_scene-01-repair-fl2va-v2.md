# QC — scene-01-repair-fl2va-v2 and upscale v1

- Verdict: PASS — USER ACCEPTED, WITH DOCUMENTED MOTION-CADENCE LIMITATION
- Reviewed: 2026-11-24
- Native prompt ID: `10eadec2-0385-4226-acd0-f4ac0f5f5485`
- Native mezzanine: `workspace/runs/scene-01-repair-fl2va-v2/outputs/scene-01-repair-fl2va-v2_00001_.mov`
- Native review MP4: `workspace/runs/scene-01-repair-fl2va-v2/outputs/scene-01-repair-fl2va-v2_00001__review.mp4`
- Accepted delivery MP4: `workspace/runs/scene-01-upscale-realesrgan-x2-v1/outputs/scene-01-upscale-realesrgan-x2-v1_00001__delivery.mp4`
- Accepted delivery SHA-256: `6539824B1A7F688192C92794331B1072334D6800AD176B2E1811FE7D401114D4`

## Technical checks

- PASS: native review is H.264 MP4, yuv420p, 576x768, 24 fps, 158 frames, 6.583333 seconds.
- PASS: native mezzanine is ProRes 4444-class video at the same 24 fps, 158-frame timing.
- PASS: delivery is H.264 MP4, yuv420p, 1080x1440, 24 fps, 158 frames, 6.583333 seconds.
- PASS: RealESRGAN x2 plus exact Lanczos resize preserves the accepted timing and does not introduce a new diffusion pass or face restoration.

## Visual checks

- PASS: the man is emotionally engaged from the opening; the vacant early gaze from proof v1 is repaired.
- PASS: both identities, age, glasses, clothing and joined-hand ownership remain recognizable and coherent.
- PASS: hair silhouettes and fine edges are materially more stable than proof v1; no delivery-blocking hair shimmer was found in the final review.
- PASS: the couple completes one readable, restrained dance movement and ends warmly.
- PASS: the user explicitly accepted the 1080x1440 MP4 on 2026-11-24.

## Motion-cadence evidence

The accepted result still contains a mild freeze/burst cadence visible in motion analysis and perceived by the user as some jerkiness. This is a documented limitation for future improvement, not a rejection of the accepted delivery.

Normalized adjacent-frame luma diagnostics:

| Artifact | Mean | Median | P95 | Max | Diagnostic freezes | Diagnostic spikes |
|---|---:|---:|---:|---:|---:|---:|
| proof v1 review MP4 | 3.204 | 3.100 | 5.055 | 7.275 | 0 | 1 |
| repair v2 review MP4 | 3.826 | 3.780 | 7.547 | 9.492 | 14 | 1 |
| repair v2 ProRes mezzanine | 3.871 | 3.825 | 7.674 | 9.620 | 13 | 1 |
| final 1080x1440 delivery MP4 | 3.723 | 3.674 | 7.313 | 9.263 | 14 | 1 |

The ProRes source contains the same alternating high/low differences around several one-second boundaries, for example frames 23-27 and later groups near frames 47-51, 95-99 and 119-123. Therefore the cadence is not introduced solely by the H.264 MP4 delivery encode.

This measurement is diagnostic only. It does not identify a unique cause and includes real subject/background motion. The likely contributors are the generated trajectory, strong prompt locks, FL2VA endpoint pull, and/or a periodic runtime/checkpoint/decode behavior. Similar public cadence reports exist, but none matches this exact ComfyUI build and reproduction closely enough to claim a confirmed implementation bug.

## Reproduction record

- ComfyUI: 0.46.0, git `f99de883d5e65317c7f4a4b617b5aa7936622029`
- Backend: local ComfyUI API, Windows, RTX 3070 8 GB, `--lowvram`
- Model: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- Video VAE: `minimax_h3_video_vae_int8_convrot.safetensors`
- Schedule: 20 steps, `res_multistep`, `simple`, no Turbo LoRA
- Seed: `24112402`
- Motion evidence: `workspace/runs/motion-analysis/v1-proof.json`, `v2-repair.json`, `v2-mezzanine.json`, and `final-delivery.json`

## Future-action decision

- Keep this accepted 24 fps delivery unchanged.
- For new scenes, define one continuous motion envelope, reduce contradictory locks, preflight first/last-anchor compatibility, and compare a three-to-five-seed base-model grid.
- When an exact periodic cadence appears, compare native/lossless output and run a minimal constant-motion diagnostic before changing prompt, checkpoint, runtime, or decode path.
- Consider FILM/RIFE 2x interpolation only after native anatomy, identity, ownership and trajectory pass. Version it separately and reject synthetic face, hand, hair or occlusion errors.
