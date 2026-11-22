# Task-specific production runbook

This file records reproducible project decisions. It is not a copy of hidden platform or system instructions.

1. Treat `references/PhotoDay_v1_motion_master.mp4` as the authoritative edit and motion target.
2. Do not split the H3 generation into independent two-second clips.
3. Do not add repeated guide frames inside a scene.
4. Use one continuous 243-frame generation with the same seed and boundary-guide schedule as v1.
5. Preserve scene order, camera movement, human timing and transition rhythm from v1.
6. Replace the male photographer with the woman in `inputs/photographer_identity_reference.jpg`; no man may remain in scenes 3 or 4.
7. Keep scene 5 hair naturally dark and detailed with no orange/white rim or crawling hotspot.
8. Generate natively at the proven 448×800 setting on the RTX 3070 8 GB, then use the documented super-resolution model and downsample to 1080×1920. The recommended v4 delivery reads the corrected lossless PNG frames, uses 100% RealESRGAN_x4plus and only the documented mild unsharp mask. The recorded 512×896 attempt exceeded VRAM before sampling. Do not use face restoration because it can change identity.
9. Serialize prompt, seed, model filenames, graph, software versions, upscaling model/hash, FFmpeg filters and QC reports.
10. Before delivery, compare all 240 delivery frames against v1 and the prior upscale, inspect the photographer in scenes 3/4, inspect full-resolution hair in scene 5, measure temporal high-frequency stability, and verify hands, glasses, tree stability, transitions, duration, frame rate, audio and black frames.
