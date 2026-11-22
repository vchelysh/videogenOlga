# Exact keyframe prompt record

The prompt bodies below are copied from the generation calls. File paths are normalized to this package so the sequence can be rebuilt. The base frames are retained in references/base_keyframes_before_v3_edits; final H3 guide frames are in keyframes.

## 0. Clean the promotional poster

Input:

- inputs/original_photos/photo_2026-11-21_18-52-29 (2).jpg

Output:

- references/base_keyframes_before_v3_edits/clean_poster.png

Prompt:

Edit the supplied promotional poster into a clean photorealistic vertical first-frame reference for an AI video. Remove all typography, labels, buttons, icons, watermarks, and logos completely. Keep the same glamorous woman, face, auburn hair, white fur stole, black dress, pearl jewelry, grand piano, candles, Christmas tree bokeh, warm amber Old Hollywood lighting, pose, composition, and luxurious atmosphere. Do not add any text. Preserve the woman and piano accurately; only remove the graphic text and UI-like elements. 9:16 portrait.

## 1. Base scene 01

Inputs:

- references/base_keyframes_before_v3_edits/clean_poster.png
- inputs/original_photos/photo_2026-11-21_18-52-30.jpg

Prompt:

Use case: ads-marketing. Asset type: first cinematic keyframe for a 9:16 Instagram photo-day advertisement. Create a brand-new photorealistic vertical scene using Image 1 only as the heroine/wardrobe/mood reference and Image 2 only as a structural reference for the real black grand piano. Scene 1, 0–2 seconds, concept 'the poster comes alive': the same glamorous adult brunette heroine sits beside a glossy black grand piano in a luxurious Old Hollywood New Year interior, ivory faux-fur stole over a refined black satin evening dress, layered pearls. Her right fingertips lightly touch the piano keys as she turns her gaze toward the camera; a small warm golden highlight runs across the pearls. Decorated Christmas tree, many steady candles, dark burgundy velvet, champagne coupe subtly in the background. Medium portrait, 35mm cinematic lens, graceful asymmetrical composition, realistic anatomy and hands, editorial luxury photography, warm tungsten light, deep blacks, restrained gold and burgundy palette, real skin texture, sophisticated and aspirational. No text, no logos, no watermark, no poster layout, no fabric covering the lens, no excessive glow, no deformed fingers, no duplicate person, no uncanny face.

## 2. Base scene 02

Inputs:

- inputs/original_photos/photo_2026-11-21_18-52-29 (3).jpg
- inputs/original_photos/photo_2026-11-21_18-52-30 (2).jpg
- inputs/original_photos/photo_2026-11-21_18-52-30.jpg

Prompt:

Use case: ads-marketing. Asset type: second cinematic keyframe for a 9:16 Instagram photo-day advertisement. Create a brand-new photorealistic visualization of the same real venue transformed for an elegant New Year photo day. Use Image 1 as the reference for the tree-and-curtain corner, Image 2 for the ornate historic fireplace, and Image 3 for the real black grand piano and room proportions; preserve recognizable architectural cues but redesign the decor at premium editorial quality. Scene 2, 2–4 seconds, concept 'the venue is revealed': a small polished gold-and-pearl Christmas ornament near the left foreground catches the same warm highlight from the previous scene, while the camera view opens onto an ornate ivory fireplace with a gentle real fire, a tall richly decorated tree, burgundy velvet drapes, steady candles and the edge of the black grand piano. No people. Clear depth layers and a graceful visual path through the room, wide vertical interior composition, 24mm cinematic lens, Old Hollywood luxury, warm tungsten light, deep blacks, burgundy, ivory and restrained gold, realistic materials and coherent architecture, sophisticated hotel-editorial photography. No text, no logos, no watermark, no fabric or curtain covering the lens, no giant foreground object, no warped furniture, no flickering or surreal lights, no excessive decorations.

## 3. Base scene 03

Inputs:

- references/base_keyframes_before_v3_edits/scene_01.png
- inputs/original_photos/photo_2026-11-21_18-52-30.jpg
- inputs/photographer_identity_reference.jpg

Prompt:

Use case: ads-marketing. Asset type: third cinematic keyframe for a 9:16 Instagram photo-day advertisement. Create a brand-new photorealistic behind-the-scenes luxury fashion moment. Image 1 is the identity, face, hair, wardrobe palette and visual-continuity reference for the adult brunette heroine; keep her clearly recognizable. Image 2 is only a structural reference for the real black grand piano and venue. Image 3 is only a beauty-editorial styling reference, not a different identity. Scene 3, 4–6 seconds, concept 'three professionals create one portrait': the heroine sits gracefully at a classic vanity mirror beside the grand piano, now without the fur covering her shoulders. A female makeup artist at frame left makes one precise final brush stroke near the heroine’s cheek; a female stylist at frame right delicately fastens one pearl drop earring. In the large mirror reflection, a professional photographer in an elegant dark suit raises a camera, ready to capture the shot. The heroine meets her own reflection with a subtle confident smile. Make all four roles immediately readable, with natural professional body language and no crowding. Layered mirror composition, medium close-up, 50mm cinematic lens, warm candlelight with soft flattering key light, burgundy velvet, glossy black piano and small golden practical lights, Old Hollywood editorial realism, refined behind-the-scenes energy, realistic skin and hands. No text, no logos, no watermark, no extra people, no duplicated limbs, no brushes crossing the eyes, no distorted mirror, no fabric blocking the view, no uncanny faces.

## 4. Base scene 04

Inputs:

- references/base_keyframes_before_v3_edits/scene_03.png
- references/base_keyframes_before_v3_edits/scene_02.png

Prompt:

Use case: ads-marketing. Asset type: fourth cinematic keyframe for a 9:16 Instagram photo-day advertisement. Create a brand-new photorealistic candid celebration that continues directly from Image 1. Preserve the same adult brunette heroine in the center and the same two adult female professionals from Image 1 as recognizable people; they are now relaxed together immediately after the portrait setup, not a random crowd. Image 2 is the location and Christmas decor reference. Scene 4, 6–8 seconds, concept 'the team becomes the memory': beside the glossy black grand piano, the heroine and the two women share one spontaneous warm laugh while gently clinking three elegant coupe glasses of champagne at chest height. Their eyes naturally connect with each other, not all staring at camera. The heroine still wears black satin and layered pearls; the two professionals wear tailored black evening suits with subtle individual jewelry. A soft camera flash blooms in the far background as if the photographer catches the candid moment. Medium group shot, 35mm cinematic lens, dynamic triangular composition, clean separation between faces and hands, warm candles and Christmas tree bokeh, Old Hollywood celebration, real skin texture, natural smiles, premium fashion-event photography, restrained burgundy-gold-black palette. No text, no logos, no watermark, no extra people, no duplicated faces, no merged glasses, no malformed fingers, no open-mouth caricature laughter, no fabric in front of lens, no confetti, no surreal champagne splash.

## 5. Base scene 05

Inputs:

- references/base_keyframes_before_v3_edits/scene_01.png
- references/base_keyframes_before_v3_edits/scene_04.png

Prompt:

Use case: ads-marketing. Asset type: fifth and final cinematic keyframe for a 9:16 Instagram photo-day advertisement. Create a brand-new photorealistic hero portrait that feels like the finished photograph from the event. Preserve the same adult brunette heroine’s identity, hair, black satin dress and pearl styling from Images 1 and 2. Scene 5, 8–10 seconds, concept 'the memory becomes the portrait': intimate chest-up close-up beside the glossy rim of the black grand piano. The heroine has turned slightly over one shoulder toward the lens, ivory faux-fur draped elegantly over only one shoulder, one hand resting naturally on the piano edge, direct confident eye contact and the faintest satisfied smile. A champagne coupe rests safely out of focus on the piano behind her. Warm candle flames and the Christmas tree dissolve into refined golden bokeh; a subtle fading camera-flash halo defines her hair, suggesting the final photograph has just been taken. 85mm portrait lens, shallow but believable depth of field, premium Old Hollywood beauty editorial, warm sculpted light, deep black background, burgundy and restrained gold accents, natural skin texture, immaculate eyes, realistic hand and pearls, quiet luxurious finish with room for a clean fade to black. No text, no logos, no watermark, no finger on lips, no copied pose from the reference, no wet hair, no fabric covering the lens, no extra people, no warped piano, no deformed hand, no plastic skin, no excessive glow.

## 6. v3 correction — scene 03 photographer identity

Inputs:

- references/base_keyframes_before_v3_edits/scene_03.png
- inputs/photographer_identity_reference.jpg

Output:

- keyframes/scene_03.png

Prompt:

Use case: compositing / identity-preserve
Asset type: vertical 9:16 photorealistic advertising-video keyframe.
Input images: Image 1 is the edit target and base composition. Image 2 is the identity reference for the female photographer.
Primary request: In Image 1, replace the male photographer in the upper background with the adult woman from Image 2. She is now the professional photographer, wearing a tailored black suit, slicked-back brown hair, and her distinctive long sculptural gold earrings. Show enough of her face for the identity to be recognizable; she holds a professional mirrorless camera just below eye level and is about to raise it.
Important duplicate prevention: the foreground stylist on the right currently resembles Image 2. Change only that stylist's identity to a clearly different adult woman with a refined short dark-blonde bob, subtle small gold studs, and the same black tailored outfit; keep her exact pose and action of fastening the heroine's pearl earring.
Hair quality: render the brunette heroine's curls as natural, high-detail individual strands with realistic volume and smooth tonal transitions; controlled soft amber edge light only, no white halo, no crispy outline, no glowing frizz.
Invariants: preserve the heroine's face, body, pose, black satin dress, pearls and expression; preserve the makeup artist on the left, her pose and cheek-brush action; preserve the mirror composition, grand piano, burgundy curtains, candles, vanity objects, framing, perspective and Old Hollywood warm lighting. Do not add or remove people.
Constraints: photorealistic premium fashion campaign, anatomically correct hands, coherent reflections, no text, no logos, no watermark.
Avoid: duplicated faces, duplicate identity, male photographer, face drift, plastic skin, malformed fingers, blown highlights, direct flash halo, CGI look.

## 7. v3 correction — scene 04 photographer identity and flash

Inputs:

- references/base_keyframes_before_v3_edits/scene_04.png
- inputs/photographer_identity_reference.jpg

Output:

- keyframes/scene_04.png

Prompt:

Use case: compositing / identity-preserve
Asset type: vertical 9:16 photorealistic advertising-video keyframe.
Input images: Image 1 is the edit target and base composition. Image 2 is the identity reference for the female photographer.
Primary request: In Image 1, replace only the male photographer in the upper background with the adult woman from Image 2. She is the professional photographer, recognizable as Image 2, wearing a tailored black suit, slicked-back brown hair and her distinctive long sculptural gold earrings. She holds a professional mirrorless camera at eye level, photographing the moment.
Important duplicate prevention: the foreground woman on the right currently resembles Image 2. Change only her identity to the same clearly different stylist established for the companion backstage scene: an elegant adult woman with a refined short dark-blonde bob, subtle small gold studs and black tailored outfit. Preserve her exact pose, smile and champagne glass.
Lighting correction: move the camera flash slightly to the side and make it softly diffused. It must not sit directly behind the heroine's head and must not create a white halo, blown hair edge or overexposed face.
Hair quality: the heroine's brunette curls have realistic individual strands, natural curl clusters, refined specular detail and smooth amber tonal transitions, with no glowing outline or crunchy frizz.
Invariants: preserve the heroine's face, body, joyful expression, black dress, pearls, seated pose and champagne glass; preserve the foreground woman on the left, all three glass positions, hands, piano, fireplace, Christmas tree, burgundy curtains, composition, camera perspective and warm Old Hollywood palette. Keep exactly four women total: three foreground women plus the female photographer in the background. No men.
Constraints: premium photorealistic fashion campaign, anatomically correct hands, physically plausible glassware, no text, no logos, no watermark.
Avoid: duplicate identity, male photographer, extra people, merged glasses, malformed hands, face drift, plastic skin, direct flash halo, blown highlights, strobing lights, CGI look.

## 8. v3 correction — scene 05 hair and rim light

Input:

- references/base_keyframes_before_v3_edits/scene_05.png

Output:

- keyframes/scene_05.png

Prompt:

Use case: identity-preserve / lighting correction
Asset type: final vertical 9:16 close-up keyframe for a premium Old Hollywood photo-day commercial.
Input images: Image 1 is the edit target.
Primary request: Correct only the heroine's hair rendering and the back/rim lighting. Re-render her brunette curls as luxurious natural hair with clean individual strands, believable curl clusters, realistic fine flyaways, rich brown tonal variation and soft specular detail. Replace the harsh white hotspot behind the upper-left side of her hair with a broad, controlled warm amber rim light that gently separates the curls from the background.
Invariants: preserve the heroine's exact identity, facial structure, gaze, expression, skin texture, body, pose, hands, black satin dress, pearls, ivory fur, earrings, piano, Christmas bokeh, candles, champagne coupe, framing, depth of field and warm color palette. Change nothing except hair detail and the excessive backlight.
Constraints: photorealistic editorial beauty photography, refined cinematic highlight roll-off, no text, no logos, no watermark.
Avoid: white halo, glowing hair outline, blown highlight, orange neon edge, crispy frizz, painted hair, plastic strands, face drift, beauty-filter skin, extra fingers, CGI appearance.

## 9. Video prompt and graph

The exact MiniMax H3 video prompt is stored verbatim in prompts/video_prompt_v3.txt and embedded in workflow/minimax_h3_v3_api.json. Seed, guide frames and model names are stored in prompts/generation_spec_v3.json.
