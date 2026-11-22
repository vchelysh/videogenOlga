# PhotoDay H3 project context

This file is the durable, user-visible recovery state for the PhotoDay video project. Update it after every accepted generation, assembly, QC decision, and delivery. It intentionally excludes hidden platform instructions, private reasoning, credentials, and raw tool logs.

## Recovery identity

- Active working directory: `C:\Users\Vadim\Downloads\PhotoDay_H3_v3_Dynamic_Reproducible`
- Earlier complete baseline package: `C:\Users\Vadim\Downloads\PhotoDay_H3_Reproducible_v2`
- Recovered Codex thread ID: `01a1ff14-0f52-7382-899b-5f54bc2f1ef9`
- Original local rollout: `C:\Users\Vadim\.codex\sessions\2026\11\21\rollout-2026-11-21T19-07-47-01a1ff14-0f52-7382-899b-5f54bc2f1ef9.jsonl`
- User-visible transcript exported to: `CONVERSATION_TRANSCRIPT.md`
- Git remote: `https://github.com/vchelysh/videogenOlga.git`
- Recovery event: power loss on 2026-11-22 while MiniMax H3 scene 03 take 01 had just started.

Current recovery-session directives from the user:

- Continue the interrupted video generation and repair.
- Serialize the durable context into text files.
- Work from this repository and push it to the GitHub remote above.
- Do not put images or videos in Git; keep them locally in the working tree.

## User objective

Produce a premium, photorealistic, 10-second vertical Instagram advertisement for a New Year Photo Day on 06.12. The result must feel like continuous generated live-action footage rather than a slideshow.

Narrative timing:

1. `0.00-2.00`: glamorous brunette heroine beside the grand piano.
2. `2.00-4.00`: decorated Old Hollywood Christmas interior.
3. `4.00-6.00`: makeup artist and stylist finish the heroine's look.
4. `6.00-8.00`: champagne/laughter/photo-session moment with the correct photographer.
5. `8.00-10.00`: final close portrait beside the piano.

Non-negotiable requirements:

- 9:16, exactly 10.000 seconds, 24 fps, 240 delivery frames.
- Old Hollywood cinematic luxury; warm tungsten light, burgundy, black, ivory, restrained gold.
- Realistic restrained motion, stable identities, coherent hands, hair, glasses, candles, tree, and architecture.
- No text, logo, watermark, fabric wipe, lens obstruction, face morph, extra person, malformed hands, or exposure pulse.
- The obsolete/male/wrong photographer must not remain.
- The supplied female photographer identity is required where the photographer is intentionally present.
- Final portrait hair must remain naturally dark and detailed, without a white/orange rim, hotspot, or crawling highlight.

Canonical project-specific requirements remain in `AGENT_RUNBOOK.md`, `prompts/source_brief.md`, and the generation/postprocess specifications.

## Version history and current repair

- v1 is the authoritative motion/edit target retained under `references/`.
- v2 is the earlier reproducible package. It is complete, but the later work was moved into this v3/v4/v5 package.
- v3 used one continuous 243-frame MiniMax H3 generation at 448x800 and repaired a rejected transition.
- v4 is the sharp 1080x1920 delivery using RealESRGAN_x4plus and mild deterministic unsharp masking.
- v5 selectively replaces weak scenes at 576x1024 while retaining accepted v4 material.

The user found a critical defect around five seconds in the first v5 assembly: the obsolete crooked photographer was still visible inside the old scene-03 source, followed by a composition/person jump when the corrected photography scene appeared. The correct fix is to replace all of scene 03, not merely patch the nominal 6-8 second scene boundary.

## Accepted and locked v5 material

- Scene 01: take 01, clean source frames 0-28, temporally resampled with FILM to 48 frames. The later candle-starburst portion is rejected.
- Scene 02: retain approved v4 lossless frames 49-96.
- Scene 03: regenerate completely from the clean no-photographer keyframe; acceptance is still pending.
- Scene 04: take 02, accepted contiguous source frames 15-62. Take 01 is rejected because the flash guide bloomed.
- Scene 05: retain approved v4 lossless frames 193-240.

The v5 specification is `prompts/generation_spec_v5.json`.

## Scene 03 state at power loss

Saved inputs:

- `keyframes_v5/scene_03_no_photographer_master.png`
- `keyframes_v5/scene_03_start_v3_no_photographer.png`
- `prompts/scene03_video_prompt_v5.txt`
- `scripts/run_minimax_h3_scene_v5.py`
- `workflow/minimax_h3_v5_scene03_take01_api.json`
- `workflow/generation_manifest_v5_scene03_take01.json`

The clean keyframe contains exactly the seated heroine, makeup artist, and stylist. The obsolete photographer and camera were removed. The shot prompt requires one continuous beauty-preparation shot, no photographer, no camera, no fourth physical person, no internal transition, and no composition jump.

The interrupted ComfyUI prompt ID was `a0823044-da9d-4f00-af3c-d6c92289ecb1`. It had only reached the initial queued/running state (`0.0 min`) when power was lost. No scene-03 output video was saved, and ComfyUI history cannot be relied on after the restart. Resubmit the deterministic take using the saved graph, keyframe, prompt, seed, and model manifest.

The existing `outputs/upscaled_frames_v5_sharp/upscaled_00001.png` through approximately `upscaled_00205.png` belong to the superseded assembly that still contained the defective old scene 03. They are stale and must not be treated as a final delivery cache.

## Technical generation state

Scene 03 take 01 settings:

- Native resolution: 576x1024.
- Length: 124 frames at 24 fps.
- Seed: 6122103.
- Steps: 8.
- Sampler/scheduler: `res_multistep` / `simple`.
- Denoise: 1.0.
- UNet: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`.
- Text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`.
- VAE: `minimax_h3_video_vae_int8_convrot.safetensors`.
- Turbo LoRA: `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`, strength 1.0.
- Conditioning: first frame only; do not introduce dense internal guide frames.

ComfyUI launch command:

```powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe C:\Users\Vadim\ComfyUI\main.py --lowvram --listen 127.0.0.1 --port 8188 --disable-auto-launch
```

Scene resubmission command from the repository root:

```powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\run_minimax_h3_scene_v5.py --scene 03 --take 1 --poll-seconds 20
```

## Required continuation sequence

1. Snapshot the text/code/config state in Git before new GPU work.
2. Start ComfyUI and verify the API at `http://127.0.0.1:8188`.
3. Resubmit scene 03 take 01 and preserve its output under `outputs/raw/v5/`.
4. Decode and inspect every source frame. Reject identity drift, soft/torn faces, bad hands, extra person/reflection, candle artifacts, internal cut, or composition jump.
5. Choose one contiguous clean scene-03 window and produce exactly 48 delivery frames. Use deterministic FILM resampling only if a shorter clean window must be expanded.
6. Update `prompts/generation_spec_v5.json` with accepted take/window/resampling facts.
7. Extend `scripts/assemble_v5_source_frames.py` so scene 03 replaces delivery frames 97-144. The current pre-recovery script still copies old base frames 97-144 and is not sufficient.
8. Assemble exactly 240 v5 source frames with this mapping: scene 01 replacement, locked scene 02, new scene 03, accepted scene 04, locked scene 05.
9. Re-run the established v4 sharp upscale profile: RealESRGAN_x4plus at full SR blend, unsharp radius 0.65 / amount 75 / threshold 2, 1080x1920, H.264 High, CRF 12, preset slow, tune film, approved AAC audio.
10. Perform frame-by-frame and technical QC, especially 4-8 seconds, transitions, photographer identity, heroine face/hair, hands, candles, duration, frame count, audio, decode, and black frames.
11. Update this file, manifests, README/QC reports/checksums, and commit the final text/code/config state.

## Repository policy

This directory is the working repository. Media remains physically present but is intentionally not versioned:

- Ignore all video formats.
- Ignore all image formats, including source photos, keyframes, decoded frame caches, upscaled frames, and review contact sheets.
- Track code, PowerShell/Python scripts, prompts, Markdown documentation, JSON workflow/manifests, CSV metrics, environment/model manifests, and checksums.
- Track `PROJECT_CONTEXT.md` and `CONVERSATION_TRANSCRIPT.md` so a fresh agent can reconstruct the task without the original Codex database.
- Never commit credentials or tokens.

## Recovery rule

After any interruption, read this file first, then `AGENT_RUNBOOK.md`, `prompts/generation_spec_v5.json`, and the latest QC/manifest files. Verify actual artifacts on disk before resuming; a queued prompt ID or partial frame cache is not proof of completion.
