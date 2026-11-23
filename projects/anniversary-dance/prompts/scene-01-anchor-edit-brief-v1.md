# Scene 01 — anchor edit brief v1

## First anchor: cleanup only

Input: `workspace/anchors/prep/scene-01-first-crop-preview-v1.png`.

Create a clean photorealistic restoration of the same 3:4 photograph. Preserve the dancing couple exactly: their identities, age, hair, glasses, clothing, body proportions, pose, all four hands, every finger and all three contact points must remain unchanged. Remove only the background guests at frame left, directly behind the woman, and at frame right, plus the bright circular flash reflection behind the man. Reconstruct a dark warm restaurant interior with wood panels and softly out-of-focus furniture. Do not add any person, face, hand, mirror figure, text, logo, new light source or decorative object. Preserve the original flash-lit skin, warm brown-black background, floor geometry and natural photographic grain.

Output target: `workspace/anchors/scene-01-first-v1.png`, 1080×1440.

## Last anchor: identity-safe expression change

Input base: accepted `scene-01-first-v1.png`.

Use the four identity crops only for facial identity. Keep the exact same camera, crop, background, exposure, wardrobe, hair, glasses, shoulders, elbows, hands and dance grip. The woman raises her chin slightly and turns her face only a few degrees toward the man and camera, with a warm restrained smile. The man keeps looking at her and forms a soft closed-mouth smile. Preserve their age, face width, jaw, nose, eyes and natural skin texture. Do not copy the reference photos' clothing, cake, tray, balloons, blue window frames or table setting. Do not beautify, de-age, whiten teeth, enlarge eyes, change glasses or make either face symmetrical.

Output target: `workspace/anchors/scene-01-last-v1.png`, 1080×1440.

## Anchor acceptance

- Both anchors contain exactly the same two foreground bodies and the same four hands.
- A difference view outside the intended face/background masks shows no change to hands, clothing or body geometry.
- The final smiles are recognizable but calm; mouths do not look pasted on.
- First and last anchors are physically connectable by one small sway and step.
- Both images pass 100% zoom inspection before any video run.
