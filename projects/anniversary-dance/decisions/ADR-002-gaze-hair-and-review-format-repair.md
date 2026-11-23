# ADR-002: repair gaze, hair stability and review packaging

- Status: Accepted
- Date: 2026-11-24

## Context

The first I2VA proof achieved recognizable identities, a readable slow dance and warm smiles, but the man appeared emotionally vacant during the opening seconds and both hairstyles showed temporal shimmer. The only initial ComfyUI output was ProRes/MOV, which was not playable in the user's normal viewer.

## Decision

1. Reject the first proof as a delivery source.
2. Define gaze and expression from the first live frame for both subjects.
3. Treat hairlines, hairstyle silhouettes, major curl/strand groups, glasses rims and face contours as locked temporal geometry.
4. Reduce head/body rotation and use first-plus-last-frame conditioning.
5. Test a non-Turbo 20-step base schedule at 576x768 before any upscale.
6. Preserve ProRes only as an optional mezzanine and always emit a validated H.264 MP4 review file.

## Consequences

- The repair run costs more time but directly tests the failure modes instead of hiding them with post-upscale sharpening.
- The accepted smiling proof frame 84 becomes the last-frame anchor; it is versioned and hashed.
- Temporal smoothing may be considered only after a native pass and only if it does not soften identity, eyes, glasses, hands or expression.
