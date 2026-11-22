# V5 keyframe creation record

Built-in image generation/editing was used in identity-preserving edit mode. Generated masters are retained in `keyframes_v5`; each selected master was cropped to exact 9:16 and resized to 1080x1920 with Lanczos for H3 conditioning. No generated asset remains only in the Codex cache.

## Scene 01

Input role: `keyframes/scene_01.png` was the edit target and exact composition/identity anchor.

Prompt:

> Use case: precise-object-edit / identity-preserve. Asset type: opening keyframe for a premium 9:16 live-action Instagram video advertisement. Preserve this glamorous brunette heroine, her exact face, pose, hair, black gown, ivory fur, pearl jewelry, grand piano, Christmas tree, burgundy curtains, mirror and framing. Make only two surgical corrections: remove every starburst, flare, glowing streak and blown highlight from the pearl necklaces; pearls must have small stable realistic reflections with full bead detail; make every visible candle clearly lit with a small physically plausible warm flame and a subtle local glow. Heroine's face, eyes, lips, hairline and individual curl groups are tack-sharp and naturally textured; clean coherent facial boundaries; realistic skin pores; clean fur and hair edges; realistic hands and piano keys. Keep subject identity, body pose, hand placement, camera angle, crop, set geometry and color palette unchanged. No face redesign, smoothing, lens flare, glowing necklace, blown whites, jagged face edge, text, logo, watermark, extra objects or people.

Generated master: `keyframes_v5/scene_01_no_flare_master.png`

H3 guide: `keyframes_v5/scene_01_start.png`

## Scene 04

Input roles:

- `keyframes/scene_04.png`: edit target and exact composition/style anchor.
- `inputs/v5_issue_references/photographer_profile_reference_v5.png`: photographer identity reference only.

Prompt:

> Use case: compositing / identity-preserve. Asset type: keyframe for a premium 9:16 live-action Instagram video advertisement. Rebuild the edit target at high photorealistic quality while changing only the photographer in the background. Give the photographer the clearly recognizable facial identity from the profile reference. She wears a tailored black professional blazer, her blonde hair is neatly pulled back, and she is actively photographing the central brunette heroine. Her right eye is aligned directly with the camera viewfinder, her gaze follows through the viewfinder toward the heroine, the lens axis points directly at the heroine, both hands grip the camera naturally, and a compact rectangular speedlight is visibly and mechanically mounted on the camera hot shoe. The flash must not float, detach, or appear beside the camera. Preserve the exact portrait composition, three distinct foreground women, brunette heroine in the center, black formal outfits, three coupe glasses with champagne, black grand piano, ivory fireplace, burgundy velvet, decorated Christmas tree, warm Old Hollywood tungsten palette and elegant candid laughter. All four faces are crisply focused with clean natural facial boundaries; no smeared cheeks, torn or jagged face edges, fused profiles or waxy skin. All candle flames are visibly lit and physically plausible. No extra people, male photographer, text, logo, watermark, floating flash, detached camera parts, face morph, extra fingers, merged glasses or CGI look.

Generated master: `keyframes_v5/scene_04_identity_camera_master.png`

H3 guide: `keyframes_v5/scene_04_start.png`

### Scene 04 take-02 flash correction

Take 01 proved that the bright white flash panel in the first guide could overpower a textual no-flash instruction and progressively bloom. A second precise-object edit changed only that panel to dark unlit smoked plastic while retaining the attached speedlight body, camera, photographer identity and foreground composition.

Prompt:

> Change only the compact speedlight mounted on top of the photographer's camera: keep the speedlight physically and mechanically attached to the camera hot shoe in the exact same position, but make its front panel dark, unlit and non-emissive, with realistic dark smoked translucent plastic and a faint passive reflection. It is powered off and emits absolutely no light. Preserve everything else pixel-compositionally: all four women's identities and expressions, the blonde photographer's eye alignment with the viewfinder, her camera grip and lens direction, the three foreground women, champagne glasses, Christmas tree, fireplace, piano, crop, lighting, colors and background. No bright rectangle, white light, glow, bloom, detached flash, floating camera part, face change, hand change, extra object, text, logo or watermark.

Generated correction master: `keyframes_v5/scene_04_unlit_flash_master.png`

Take-02 H3 guide: `keyframes_v5/scene_04_start_v2_unlit_flash.png`

## Scene 03 corrective replacement

Input role: `outputs/source_frames_v5/source_00097.png` was the edit target and exact composition/identity anchor.

Reason: the v4 scene previously reused at delivery frames 97-144 already contained the obsolete dark-haired photographer in the rear center and changed internally from makeup to champagne. Replacing only scene 04 therefore left two different photographers and a visible jump. Scene 03 is now regenerated in full.

Prompt:

> Use case: precise-object-edit. Asset type: first keyframe for a photorealistic vertical luxury advertising video. Remove only the woman photographer standing in the rear center and remove her camera completely. Reconstruct that area as a natural unobstructed continuation of the black grand piano, warm candlelight and burgundy curtain already present in the room. Preserve exactly the seated brunette model's identity, face, expression, hairstyle, black satin dress, pearl necklaces, pose and proportions; the makeup artist on the left with glasses and brush near the model's cheek; the stylist on the right adjusting the pearl earring; foreground vanity, mirror, brushes, roses, decor; camera viewpoint, framing, Old Hollywood color grade and warm luxury lighting. Vertical 9:16, same framing. Exactly three physical people: seated model, makeup artist left, stylist right; no person in the background. Photorealistic natural skin texture, crisp anatomically correct faces, hands and hair edges, clean individual hair strands. All visible candle flames are small, natural and lit. Change only the rear photographer/camera area; no camera anywhere; no fourth physical person; no extra limbs or hands; no motion blur; no distorted faces; no glowing starbursts; no text, logos or watermark.

Generated master: `keyframes_v5/scene_03_no_photographer_master.png`

Rejected crop guide: `keyframes_v5/scene_03_start_v2_no_photographer.png` (incorrectly cropped too much from the bottom; never used for H3)

Accepted H3 guide: `keyframes_v5/scene_03_start_v3_no_photographer.png`

## Supplied issue references

- `inputs/v5_issue_references/scene01_face_candles_issue.png`
- `inputs/v5_issue_references/scene04_photographer_faces_issue.png`
- `inputs/v5_issue_references/photographer_profile_reference_v5.png`
