# PhotoDay MiniMax H3 — v5 repaired sharp delivery

This package reproduces the approved dynamic revision and the final v5 repair. The complete `4.00-6.00 s` makeup scene was regenerated to remove the obsolete photographer and the composition jump reported around five seconds. The correct female photographer now appears once, at the intentional 6.00-second scene cut.

## Recommended repaired delivery

- Master: `outputs/PhotoDay_06-12_MINIMAX_H3_v5_REPAIRED_SHARP_1080x1920_FINAL.mp4`
- Native preview: `outputs/raw/v5/PhotoDay_v5_repaired_native_preview_576x1024_10s.mp4`
- Format: 1080×1920, 24 fps, 240 frames, exactly 10.000 seconds
- Video: H.264 High, yuv420p, x264 preset slow, tune film, CRF 12
- Audio: AAC-LC, 48 kHz, stereo, 192 kb/s
- SHA-256: `79562C826A47AD880E1E95A31B22E6ED0529025F37ACE7C6D0ADE941228DA4A3`
- QC report: `review/QC_REPORT_v5_REPAIRED_SHARP.md`
- Final manifest: `workflow/final_delivery_manifest_v5_repaired_sharp.json`

The repaired assembly mapping is exact: scene 01 replacement at frames `1-48`, locked v4 scene 02 at `49-96`, new scene-03 take-01 frames `0-47` at delivery frames `97-144`, accepted scene-04 take-02 frames `15-62` at `145-192`, and locked v4 final portrait at `193-240`.

## Previous v4 sharp baseline

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
- prompts/generation_spec_v5.json — accepted/rejected v5 takes, source windows and delivery mapping.
- prompts/postprocess_spec_v5.json — repaired source sequence and unchanged sharp delivery profile.
- AGENT_RUNBOOK.md — project-specific production and checking instructions; it intentionally contains no hidden platform instructions.
- PROJECT_CONTEXT.md — durable recovery state and continuation instructions.
- CONVERSATION_TRANSCRIPT.md and the recovery/continuation transcript files — user-visible task history without hidden reasoning or credentials.
- workflow/minimax_h3_v3_api.json — exported ComfyUI API graph.
- workflow/generation_manifest_v3.json — generation manifest and successful prompt ID.
- workflow/final_delivery_manifest_v3.json — final artifact metadata and hash.
- workflow/final_delivery_manifest_v4_sharp.json — sharp delivery metadata and hash.
- workflow/minimax_h3_v5_scene03_take01_api.json — exact repaired scene-03 graph.
- workflow/generation_manifest_v5_scene03_take01.json — prompt ID, seed, source hash and render metadata.
- workflow/source_assembly_manifest_v5.json — exact five-scene frame mapping.
- workflow/final_delivery_manifest_v5_repaired_sharp.json — repaired final artifact metadata and hash.
- ENVIRONMENT.md and MODELS.md — hardware, software, model paths and model hashes.
- SHA256SUMS.txt — hashes of packaged artifacts, excluding only temporary full-resolution frame caches.

The base concept frames before photographer/hair correction are retained under references/base_keyframes_before_v3_edits. The final corrected H3 guides are in keyframes. The supplied photographer reference is inputs/photographer_identity_reference.jpg.

## Core generation rule

The rejected v2 placed repeated guide images inside every two-second scene and suppressed movement. v3 uses one continuous 243-frame MiniMax H3 generation, with guides only at frames 0, 48, 96, 144, 192 and 242. Do not add dense internal anchors.

Native settings: 448×800, 243 frames, 24 fps, seed 6122026, eight MiniMax H3 turbo steps. A 512×896 attempt exceeded the RTX 3070 8 GB VRAM before sampling, so the proven native resolution was retained and enhanced conservatively after generation.

## Reproduction commands

Run these from the package root after starting ComfyUI with the environment recorded in ENVIRONMENT.md.

### v5 repaired delivery

1. Generate the replacement makeup scene:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\run_minimax_h3_scene_v5.py --scene 03 --take 1 --poll-seconds 20
~~~

2. Assemble the exact 240-frame repaired source sequence. This command makes scene 03 mandatory and prevents accidental reuse of the defective v4 frames `97-144`:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\assemble_v5_source_frames.py --scene01-frame-dir .\outputs\raw\v5\scene01_selected_film_48f --scene03 .\outputs\raw\v5\PhotoDay_H3_v5_scene03_take01_576x1024_124f.mov --scene04 .\outputs\raw\v5\PhotoDay_H3_v5_scene04_take02_576x1024_124f.mov --scene03-start 0 --scene04-start 15 --output-dir .\outputs\source_frames_v5_repaired
~~~

3. Build the native review preview, then run the unchanged v4 sharp upscale profile into a new cache:

~~~powershell
ffmpeg -y -framerate 24 -start_number 1 -i .\outputs\source_frames_v5_repaired\source_%05d.png -i .\references\PhotoDay_v1_motion_master.mp4 -map 0:v:0 -map 1:a:0? -frames:v 240 -t 10 -vf "scale=576:1024:force_original_aspect_ratio=increase:flags=lanczos,crop=576:1024" -c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 .\outputs\raw\v5\PhotoDay_v5_repaired_native_preview_576x1024_10s.mp4
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\upscale_and_encode.py --input .\outputs\raw\v5\PhotoDay_v5_repaired_native_preview_576x1024_10s.mp4 --output .\outputs\PhotoDay_06-12_MINIMAX_H3_v5_REPAIRED_SHARP_1080x1920_FINAL.mp4 --audio-from .\references\PhotoDay_v1_motion_master.mp4 --source-frame-dir .\outputs\source_frames_v5_repaired --frame-dir .\outputs\upscaled_frames_v5_repaired_final --model C:\Users\Vadim\ComfyUI\models\upscale_models\RealESRGAN_x4plus.pth --sr-blend 1.0 --unsharp-radius 0.65 --unsharp-percent 75 --unsharp-threshold 2 --crf 12 --preset slow --tune film
~~~

4. Rebuild final motion metrics and checksums:

~~~powershell
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\compare_motion.py --video .\references\PhotoDay_v1_motion_master.mp4 --label v1 --video .\outputs\PhotoDay_06-12_MINIMAX_H3_v4_SHARP_1080x1920_FINAL.mp4 --label v4_sharp --video .\outputs\PhotoDay_06-12_MINIMAX_H3_v5_REPAIRED_SHARP_1080x1920_FINAL.mp4 --label v5_repaired --output-dir .\review\motion_metrics_v5_final
C:\Users\Vadim\ComfyUI\.venv\Scripts\python.exe .\scripts\write_checksums.py
~~~

### Base v3/v4 reproduction

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

The recommended v5 master inherits the approved v4 sharp profile unchanged: 100% RealESRGAN_x4plus detail, a mild deterministic unsharp mask (radius 0.65, amount 75%, threshold 2), and a CRF 12 x264 film encode. It reads the repaired lossless source PNG sequence directly into a new cache. The previous v3 master used a softer 65% Real-ESRGAN / 35% Lanczos blend and remains available for comparison. No face restoration is used. In v5, FILM is limited to the accepted scene-01 window; scene 03 uses direct source frames `0-47`, scene 04 uses direct source frames `15-62`, and the final portrait is never interpolated.
