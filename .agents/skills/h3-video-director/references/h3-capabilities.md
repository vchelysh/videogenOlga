# MiniMax H3 capability and mode selection

Use this file when choosing conditioning, duration, resolution, or a hardware profile. Re-discover live ComfyUI nodes and model files before execution; names and templates change faster than these directing rules.

## Stable capability envelope

- H3 generates at 24 fps and supports clips from 4 to 15 seconds with common landscape, portrait, and square aspect ratios.
- The FL2VA family accepts zero, one, or two frame images. This covers text-to-video, first-frame image-to-video, and first-plus-last-frame conditioning.
- The Ref2VA family accepts reference media. The published limit is up to 9 images, 3 videos, and 3 audio files, with no more than 12 references total.
- The open H3 Base release targets 768p. Context-IR prompt/context refinement and Regenerate-2K are separate hosted stages; do not claim a local Base graph includes them.
- Prompt/context expansion can materially affect quality. When Context-IR is unavailable, use the structured prompt and scene contract rather than a loose paragraph.
- A single request must use one conditioning family. Do not combine FL2VA frame anchors with Ref2VA references in one model call.

Sources:

- MiniMax model card: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/README.md
- Official ComfyUI H3 guide: https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- MiniMax base prompt guide: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md
- MiniMax reference prompt guide: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md

## Choose one mode

| Need | Mode | Use when | Main risk |
|---|---|---|---|
| Explore from prose | T2VA / FL2VA with no image | Composition and identity may vary | Weak continuity |
| Preserve the opening composition | I2VA / FL2VA with one image | The first state is authoritative | End state may drift |
| Reach a precise final state | FL2VA with first and last images | One continuous shot can plausibly connect both states | Forced morph if endpoints differ too much |
| Preserve identities, style, motion, camera, or voice from media | Ref2VA | Reference semantics matter more than fixed boundary pixels | Reference conflicts or label drift |
| Hold pose, edges, depth, or a masked region | ComfyUI multiframe/control workflow around H3 | Geometry is the dominant risk and the installed graph supports it | Overconstraint or unavailable nodes |

If two needs conflict, split the shot or protect the higher-risk invariant. For example, a precise glass handoff is usually safer as two shots or a first/last-frame shot than as first-frame-only animation with a long verbal prohibition list.

## Feasibility sequence

1. Convert delivery seconds to delivery frames: `seconds * fps`.
2. Check that requested H3 duration is within 4–15 seconds.
3. Confirm the graph's supported latent frame count; do not assume it equals delivery frames.
4. Define whether the generated clip is used in full or as one contiguous accepted window.
5. Check aspect ratio, native raster, VRAM, model precision, sampler, steps, and expected runtime on the current machine.
6. Prefer a short/native proof before an upscale or final encode.

## Hardware is project data

Never promote a successful setting from one GPU to a universal H3 recommendation. Read the project's environment record and live system stats. Record every proven raster, frame length, precision, sampler, step count, runtime, and OOM boundary in that project's environment or run manifest.

## Human-performance and temporal-detail risks

- A face can preserve identity yet still fail performance because its gaze target or affect was unspecified. For every visible subject, state an observable gaze target and expression from the first live frame, not only at the ending beat.
- Hair, hairlines, glasses, eyelashes, jewellery, and other high-frequency edges can shimmer even when sparse contact sheets look correct. Lock the outer silhouette and major detail groups in the prompt, then inspect adjacent native frames at 100% scale.
- When a Turbo/low-step proof shows temporal hair or face-edge instability, do not hide it with an upscale. First test a physically compatible first/last anchor pair, less head rotation and hair motion, native raster, and a non-Turbo/base schedule with the model's normal step range. Record the changed profile as a new run.
- Deflicker or temporal smoothing is a repair stage, not proof that the generation passed. Reject it if it softens identity, eyes, glasses, hands, or the intended expression.

## Motion-cadence risks

- H3's native 24 fps is fixed generation cadence. If the encoded file probes as 24 fps with monotonic timestamps and no duplicate/frozen frames, visible jerkiness is usually a generated trajectory problem rather than an MP4 problem.
- First/last conditioning can create endpoint pull: motion stays quiet, then accelerates as the model tries to reach an incompatible final pose. Compare landmark displacement, occlusion order, contacts, and background geometry before accepting an anchor pair.
- Hard timestamp blocks can produce stop-start motion when each beat reads as a new command. Define one motion path and require position, direction, and velocity to continue across beat boundaries with explicit ease-in and ease-out.
- Too many simultaneous locks can remove the degrees of freedom needed for natural full-body motion. Lock identity, ownership, contact and risky edges; positively declare the coordinated joints and torso motion that are allowed.
- Frame interpolation is optional delivery smoothing only after native trajectory/anatomy PASS. Read [motion-continuity.md](motion-continuity.md) before building or approving it.

## Reject or redesign when

- more than one major action must complete in a short shot;
- the requested start and end states cannot be connected physically;
- multiple hands cross, exchange props, or disappear behind an occluder without a clear ownership plan;
- a first-frame-only request requires an exact final grip, pose, or subject count;
- identity, camera, and motion references disagree;
- a visible person's gaze/expression is undefined for any beat, or the requested hair/head motion has no stable temporal reference;
- the local graph cannot fit and cloud/paid execution is not authorized.
