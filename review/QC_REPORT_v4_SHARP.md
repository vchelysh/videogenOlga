# Final QC report — PhotoDay v4 sharp upscale

Status: PASS

Final artifact: outputs/PhotoDay_06-12_MINIMAX_H3_v4_SHARP_1080x1920_FINAL.mp4

Native pre-upscale artifact: outputs/raw/PhotoDay_H3_v3_clean_FILM_448x800_10s.mp4

SHA-256: 0E8BED358D7F2D40F5B28B34AB39EFAA78AC9C08DD3357618D6A2BC890FF0835

## Technical validation

- 1080×1920 portrait, 24/1 fps, 240 frames, exactly 10.000000 seconds.
- H.264 High, yuv420p, measured video bitrate 28,789,951 bit/s.
- AAC-LC, 48 kHz, stereo, measured audio bitrate 193,309 bit/s.
- File size: 36,237,962 bytes.
- Full FFmpeg decode completed with zero reported errors.
- Black-frame scan found zero black segments.

## Upscale change

- Previous v3: 65% RealESRGAN_x4plus plus 35% direct Lanczos, CRF 16.
- Selected v4: 100% RealESRGAN_x4plus plus mild unsharp mask (radius 0.65, amount 75%, threshold 2), CRF 12, x264 tune film.
- v4 reads the corrected lossless source PNG frames directly, avoiding an extra decode of the native MP4.
- No face restoration, identity synthesis or temporal frame interpolation was added.

## Sharpness and temporal stability

- Mean full-frame Tenengrad edge energy: v3 1380.99; v4 2564.38; ratio 1.8569×.
- Mean full-frame Laplacian variance: v3 1358.73; v4 4164.78; ratio 3.0652×.
- Final-hair high-frequency energy increased from 0.002228 to 0.003162.
- Final-hair detail coefficient of variation remains low: v3 0.935%; v4 1.017%.
- Normalized adjacent-frame high-frequency change: v3 0.2377; v4 0.2805. The increase is consistent with the added edge detail; all 48 final portrait frames were visually checked for crawling texture.
- Full metrics and per-frame CSV: review/upscale_v4_final.

## Visual validation

- All five 48-frame scene sheets were reviewed: 240/240 delivery frames.
- Heroine, female photographer, other team members, hands, camera, glasses and scene geometry remain unchanged from approved v3.
- Fireplace carving, curtain edges, hair curl groups, jewelry, glass rims and piano reflections are visibly better defined.
- No new halos, ringing, plastic face restoration, black frames, text, logos or foreground obstruction were observed.
- Final brunette hair remains stable with no white/orange flare or progressive brightening.
- Encoded frame 210 was extracted from the final H.264 file and inspected at original 1080×1920 resolution.
