# QC — scene-01-proof-i2v-v1

- Verdict: REGENERATE
- Reviewed: 2026-11-24
- Prompt ID: 72c7230b-e7c6-4188-9306-5728df7b7061
- Source: workspace/runs/scene-01-proof-i2v-v1/outputs/scene-01-proof-i2v-v1_00001_.mov
- Review MP4: workspace/runs/scene-01-proof-i2v-v1/outputs/scene-01-proof-i2v-v1_review.mp4
- Source hash: CBAF03AEECEE47881123925ACB2729787DB48D2CAC5452355583CEC2607A349B
- Review MP4 hash: 245EE17CF920CC6DA501D4421E33291F8D5BCF1781EDEF4E9DCAFED48D099A16

## Technical checks

- PASS: 480x640, 24 fps, 158 frames, 6.583333 seconds.
- PASS: H.264 review encode is yuv420p and playable as MP4.
- PASS: couple identity, slow-dance action, mutual smiles and joined-hand contact read correctly in sampled frames.

## Rejection reasons

- FAIL: partner_man has an under-directed neutral interval at the beginning and appears to look into empty space instead of maintaining an emotionally engaged target.
- FAIL: visible frame-to-frame shimmer/crawl affects both hairstyles, especially the outer hair edges and fine texture.
- FAIL: the source's background guests acquire some generated motion and one central background face becomes more recognizable late in the clip.

## Repair decision

- Switch from first-frame-only I2VA to FL2VA using the accepted source crop and proof frame 84 as a physically compatible smiling endpoint.
- Give both faces a gaze/expression timeline beginning in the first live frames.
- Lock hairline, hairstyle silhouette, major curl/strand groups, glasses rims and face edges as temporal geometry.
- Reduce shared body rotation from eight to four degrees.
- Test native 576x768 with a non-Turbo 20-step base schedule before any upscale.
- Always create and review H.264 MP4 alongside any ProRes/MOV mezzanine.
