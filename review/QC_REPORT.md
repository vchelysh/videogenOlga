# Final QC report — PhotoDay H3 v3

Status: PASS

Final artifact: outputs/PhotoDay_06-12_MINIMAX_H3_v3_DYNAMIC_1080x1920_FINAL.mp4

SHA-256: D277D9B5D7DAF0EDE2EC3FFD470079C0651CF14522B603E2C6DA54AFE8C87E01

## Technical validation

- 1080×1920 portrait, square pixels, no geometric stretching.
- 24/1 fps, 240 video frames, exactly 10.000000 seconds.
- H.264 High, yuv420p, measured video bitrate 10,847,444 bit/s.
- AAC-LC, 48 kHz, stereo, measured audio bitrate 193,309 bit/s.
- FFmpeg full decode completed with no reported errors.
- File size: 13,809,828 bytes.
- No black frames found in the reviewed 240-frame sequence.

## Visual validation

- All five 48-frame scene sheets were reviewed at delivery resolution; evidence is in review/full_frame_qc.
- Scenes 3 and 4 contain the supplied female photographer with slicked-back brown hair, sculptural gold earrings, black tailored suit and mirrorless camera. No male photographer remains.
- Scene 3 preserves active professional movement instead of the rejected v2 frozen-photo behavior.
- Scene 4 contains natural laughter and champagne-glass movement. Raw H3 frames 167–191, which contained a frame-covering white/gold morph, are absent from the final master.
- Scene 5 was checked across all 48 frames. Brunette curls retain controlled brown highlights and dark edges; no progressive white/orange hair halo or frame-covering exposure bloom is present.
- Scene-5 mean luminance stays within 61.13–61.50 and p99 luminance within 198–199 across the checked sequence.
- No fabric wipe, foreground obstruction, generated caption, logo or watermark was observed.
- Full-resolution spot checks: delivery frames 110 (team/photographer), 160 (celebration/photographer) and 210 (final hair portrait).

## Motion regression check

Mean frame-difference ratios against approved v1:

| Scene | v2 / v1 | final v3 / v1 | Result |
|---|---:|---:|---|
| 1 | 1.004 | 1.069 | Preserved |
| 2 | 0.128 | 1.021 | Restored |
| 3 | 0.131 | 0.549 | Clearly active; restrained team actions |
| 4 | 0.286 | 0.509 | Active and clean after local transition repair |
| 5 | 1.015 | 0.501 | Intentional subtle portrait motion and blink |

Only six adjacent delivery frames are near-identical; these are the intentional final settle frames, approximately 0.25 seconds. Motion metrics and per-frame CSV files are stored under review/motion_metrics_final.

## Repair and enhancement scope

- MiniMax H3 raw generation remains unchanged for scenes 1–3 and the final portrait.
- FILM is used only to retime clean scene-4 source frames 144–166 to 48 frames. Rejected raw frames 167–191 are never used.
- Final portrait frames are never interpolated.
- RealESRGAN_x4plus at 65% is blended with 35% Lanczos and delivered at 1080×1920.
- No face restoration is used, preventing identity drift.
