# Final QC report — PhotoDay v5 repaired sharp delivery

Status: PASS

Final artifact: `outputs/PhotoDay_06-12_MINIMAX_H3_v5_REPAIRED_SHARP_1080x1920_FINAL.mp4`

SHA-256: `79562C826A47AD880E1E95A31B22E6ED0529025F37ACE7C6D0ADE941228DA4A3`

## Defect repair

- The complete delivery range `97-144` (`4.000-5.999 s`) was replaced. No frame from the defective approved-v4 scene 03 remains in that range.
- Replacement source: `outputs/raw/v5/PhotoDay_H3_v5_scene03_take01_576x1024_124f.mov`, accepted zero-based source window `0-47` with no temporal interpolation.
- At delivery frame `121` (exactly 5.000 s), the image contains only the seated heroine, makeup artist and stylist; there is no photographer or camera.
- The correct female photographer appears once, at the intentional scene cut on delivery frame `145` (6.000 s). There is no obsolete photographer, duplicate identity, morph or intermediate composition.
- Assembly-boundary hashes prove frames `96` and `193` remain locked v4 material, while frames `97`, `121` and `144` are newly generated scene-03 material.

## Technical validation

- 1080×1920 portrait, 24/1 fps, 240/240 decoded video frames, exactly 10.000000 seconds.
- H.264 High, yuv420p, measured video bitrate 32,245,897 bit/s.
- AAC-LC, 48 kHz, stereo, measured audio bitrate 193,309 bit/s; 10.000000-second audio stream.
- File size: 40,557,895 bytes.
- Full FFmpeg video/audio decode completed with zero reported errors.
- Black-frame scan found zero black segments.
- The final upscale cache contains exactly 240 frames and was created in a new directory; the stopped 205-frame defective cache was not reused.

## Scene-03 generation and temporal validation

- MiniMax H3 prompt ID: `f533c611-3400-4f27-9a31-355b573e8b16`.
- Native source: ProRes 4444, yuv444p12le, 576×1024, 124 frames at 24 fps; full decode succeeded.
- Native source SHA-256: `D6685B8C327E016DC5395AF45E424F42E298CC8070BA46C7023ECDDA543D0DF9`.
- All 124 generated frames were reviewed on eight sequential contact sheets; selected frames `1`, `25`, `40` and `48` were inspected at original resolution.
- Selected delivery window motion mean/median/p95 after final encode: `7.6802 / 7.6851 / 8.2692` mean absolute luma delta.
- Largest internal scene-03 adjacent-frame delta was `8.3937`; there is no isolated spike or internal cut.
- The only large deltas around the repaired area occur at the intended edit boundaries: frame `96` at 4.000 s and frame `144` at 6.000 s.
- Scene-03 motion is `1.2953×` the v1 scene-03 mean, preserving the requested dynamic live-action feel.

## Upscale and locked-material validation

- Reused the approved v4 sharp profile unchanged: 100% RealESRGAN_x4plus, mild unsharp mask (radius 0.65, amount 75%, threshold 2), x264 CRF 12 / slow / tune film.
- No face restoration and no global temporal interpolation were used.
- Locked scene-02 frames `49`, `72` and `96` are SHA-256 identical to the approved v4 pre-encode sharp frames.
- Locked final-portrait frames `193`, `210` and `240` are SHA-256 identical to approved v4 pre-encode sharp frames, preserving the previously accepted hair detail and stability.

## Visual validation

- All five 48-frame final scene sheets were reviewed: 240/240 encoded delivery frames.
- Scene 03 remains one continuous beauty-preparation composition with exactly three physical women. The lower-right soft mirror reflection remains only the heroine's reflection and never becomes another person.
- Heroine identity, eyes, lips, hairline and curls remain coherent; makeup brush, earring and visible hands remain readable without face tearing or object penetration.
- Scene 04 contains one stable correct female photographer and attached camera; champagne glasses, hands, faces, Christmas tree and piano remain coherent.
- Final brunette hair remains unchanged from approved v4, without white/orange flare, progressive brightening or crawling hotspot.
- No text, logo, watermark, black frame, foreground wipe, extra person, exposure pulse or new ringing/halo was observed.

Motion CSVs and summary: `review/motion_metrics_v5_final/`.
