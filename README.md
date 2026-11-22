# PhotoDay MiniMax H3 v3 generation — v4 sharp delivery

This package reproduces the approved dynamic revision: retain the movement, pacing and continuous-shot architecture of v1; replace the male photographer with the supplied woman; repair the final hair light; and deliver a clean 1080×1920 master.

## Recommended sharp delivery

- Master: outputs/PhotoDay_06-12_MINIMAX_H3_v4_SHARP_1080x1920_FINAL.mp4
- Native pre-upscale master: outputs/raw/PhotoDay_H3_v3_clean_FILM_448x800_10s.mp4
- Format: 1080×1920, 24 fps, 240 frames, exactly 10.000 seconds
- Video: H.264 High, yuv420p, x264 preset slow, tune film, CRF 12
- Audio: AAC-LC, 48 kHz, stereo, 192 kb/s
- SHA-256: 0E8BED358D7F2D40F5B28B34AB39EFAA78AC9C08DD3357618D6A2BC890FF0835
- QC report: review/QC_REPORT_v4_SHARP.md

## Previous softer delivery

- Master: outputs/PhotoDay_06-12_MINIMAX_H3_v3_DYNAMIC_1080x1920_FINAL.mp4
- Format: 1080×1920, 24 fps, 240 frames, exactly 10.000 seconds
- Video: H.264 High, yuv420p, CRF 16 source encode
- Audio: AAC-LC, 48 kHz, stereo, 192 kb/s
- SHA-256: D277D9B5D7DAF0EDE2EC3FFD470079C0651CF14522B603E2C6DA54AFE8C87E01
- QC report: review/QC_REPORT.md

## Reproducibility contents

- prompts/source_brief.md — original brief and non-negotiable revision requirements.
- prompts/keyframe_prompts_v3.md — exact image-generation and v3 correction prompts.
- prompts/video_prompt_v3.txt — exact MiniMax H3 prompt.
- prompts/generation_spec_v3.json — seed, model names, resolution, timing and guide schedule.
- prompts/transition_cleanup_spec_v3.json — exact rejected frame range and FILM repair.
- prompts/postprocess_spec_v3.json — exact upscale and delivery encode settings.
- prompts/postprocess_spec_v4_sharp.json — selected sharper upscale and CRF 12 encode settings.
- AGENT_RUNBOOK.md — project-specific production and checking instructions; it intentionally contains no hidden platform instructions.
- workflow/minimax_h3_v3_api.json — exported ComfyUI API graph.
- workflow/generation_manifest_v3.json — generation manifest and successful prompt ID.
- workflow/final_delivery_manifest_v3.json — final artifact metadata and hash.
- workflow/final_delivery_manifest_v4_sharp.json — sharp delivery metadata and hash.
- ENVIRONMENT.md and MODELS.md — hardware, software, model paths and model hashes.
- SHA256SUMS.txt — hashes of packaged artifacts, excluding only temporary full-resolution frame caches.

The base concept frames before photographer/hair correction are retained under references/base_keyframes_before_v3_edits. The final corrected H3 guides are in keyframes. The supplied photographer reference is inputs/photographer_identity_reference.jpg.

## Core generation rule

The rejected v2 placed repeated guide images inside every two-second scene and suppressed movement. v3 uses one continuous 243-frame MiniMax H3 generation, with guides only at frames 0, 48, 96, 144, 192 and 242. Do not add dense internal anchors.

Native settings: 448×800, 243 frames, 24 fps, seed 6122026, eight MiniMax H3 turbo steps. A 512×896 attempt exceeded the RTX 3070 8 GB VRAM before sampling, so the proven native resolution was retained and enhanced conservatively after generation.

## Reproduction commands

Run these from the package root after starting ComfyUI with the environment recorded in ENVIRONMENT.md.

1. Generate the continuous H3 source:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\run_minimax_h3_photoday_v3.py
~~~

2. Remove only the rejected scene-4 morph/bloom and write the corrected 240 source frames:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\clean_transition_film.py --input .\outputs\raw\PhotoDay_H3_v3_raw_448x800_10.125s.mp4 --output .\outputs\raw\PhotoDay_H3_v3_clean_FILM_448x800_10s.mp4 --frame-dir .\outputs\upscaled_frames
~~~

3. Enhance and encode the recommended sharp 1080×1920 master directly from the lossless corrected source frames:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\upscale_and_encode.py --input .\outputs\raw\PhotoDay_H3_v3_clean_FILM_448x800_10s.mp4 --output .\outputs\PhotoDay_06-12_MINIMAX_H3_v4_SHARP_1080x1920_FINAL.mp4 --source-frame-dir .\outputs\upscaled_frames --frame-dir .\outputs\upscaled_frames_v4_sharp --model C:\Users\Vadim\ComfyUI\models\upscale_models\RealESRGAN_x4plus.pth --sr-blend 1.0 --unsharp-radius 0.65 --unsharp-percent 75 --unsharp-threshold 2 --crf 12 --preset slow --tune film
~~~

4. Rebuild comparison/QC assets and checksums:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_review_assets.ps1 -V3Video .\outputs\PhotoDay_06-12_MINIMAX_H3_v3_DYNAMIC_1080x1920_FINAL.mp4
powershell -ExecutionPolicy Bypass -File .\scripts\build_v4_upscale_review.ps1
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\compare_upscale_v3_v4.py
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\compare_motion.py --video .\references\PhotoDay_v1_motion_master.mp4 --label v1 --video .\references\PhotoDay_v2_rejected_static.mp4 --label v2 --video .\outputs\PhotoDay_06-12_MINIMAX_H3_v3_DYNAMIC_1080x1920_FINAL.mp4 --label v3_final_1080 --output-dir .\review\motion_metrics_final
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\write_checksums.py
~~~

## Post-processing policy

The recommended v4 master uses 100% RealESRGAN_x4plus detail, a mild deterministic unsharp mask (radius 0.65, amount 75%, threshold 2), and a CRF 12 x264 film encode. It reads the corrected lossless PNG sequence directly, avoiding another decode of the native MP4. The previous v3 master used a softer 65% Real-ESRGAN / 35% Lanczos blend and remains available for comparison. No face restoration is used. FILM remains limited to the documented scene-4 repair and is never applied to the final portrait.
