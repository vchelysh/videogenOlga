# Anatomy, contact, and continuity

Use this whenever a scene contains people, hands, held objects, body contact, handoffs, occlusion, or reflective surfaces.

## Ownership ledger

Create one row for every visible hand and important prop:

| ID | Owner | Side | Emerges from | Screen path | Contact/prop | Start state | End state | Occlusion |
|---|---|---|---|---|---|---|---|---|
| hand_stylist_r | stylist | right | stylist right sleeve | upper-right to earring | heroine earring | open fingers | light pinch | never behind head |

Rules:

- A person has at most one left and one right hand.
- Every visible hand must have an unbroken readable path to the correct wrist, forearm, elbow, and body.
- Every prop instance has one owner at every moment.
- A handoff needs a timed ownership transition: owner A holds → both touch briefly → owner B holds → owner A releases.
- A hand may enter or leave frame only through a declared edge or occluder.
- Do not place a hand against furniture or another body if the connecting arm will be hidden in an ambiguous way.
- Reflections are not extra physical people or extra props; state whether a reflection is visible.

## Complexity budget

Count risk before generation:

- +1 per visible face;
- +1 per visible hand;
- +2 per hand touching a face, hair, jewellery, glass, tool, or another hand;
- +2 per handoff;
- +2 per mirror/reflection;
- +2 per crossing limb path;
- +1 per moving camera axis;
- +1 per cut or transformation.

A high score is a design warning, not a model setting. Reduce it by hiding nonessential hands, locking the camera, removing a handoff, splitting the shot, or using stronger structural conditioning.

## Prompt order

1. State the physical subject count and screen positions.
2. State each visible hand and its body connection.
3. State each prop owner and grip.
4. State the minimal motion in chronological order.
5. State the final locked geometry.
6. Add concise failure exclusions.

Prefer “the frame-right stylist's single visible right hand extends continuously from her right sleeve and lightly touches the earring” over “no extra hands.” Use both only when needed.

## Keyframe preflight

Reject a keyframe before video generation if it already contains:

- ambiguous or duplicated wrists/fingers;
- an arm hidden behind an object with no readable owner;
- a prop whose grip could belong to two people;
- two nearly identical people that may merge;
- a reflection that reads as another subject;
- a start state incompatible with the requested motion.

Video conditioning tends to preserve and amplify defects already baked into the anchor.

## Continuity between generated shots

Record and compare:

- character ID, wardrobe, hair, accessories, and face reference;
- gaze target and expression state at the cut boundary and throughout every held beat;
- hairline, outer hairstyle silhouette, major curl/strand groups, glasses rims, and face contour in adjacent frames, not only selected stills;
- prop count, owner, fill level, orientation, and screen side;
- lighting direction, colour temperature, exposure, and practical lights;
- camera height, lens feel, framing, and movement;
- final state of the prior shot versus first state of the next.

Use the last accepted frame as evidence, not memory or the prompt alone.
