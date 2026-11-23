# Motion continuity and natural movement

Use this reference when motion looks jerky, frozen-then-bursting, mechanically timed, or merely low-frame-rate. H3 generates at 24 fps; a valid 24 fps encode can still look rough because the generated poses do not follow a smooth trajectory.

## Diagnose before choosing a repair

| Symptom | Likely cause | Correct response |
|---|---|---|
| Pose holds, then jumps several pixels | Freeze/burst generation or conflicting locks | Regenerate with a simpler action and one continuous motion envelope |
| Motion accelerates near the end | First/last anchors are too different; endpoint pull | Replace or reduce the last-anchor difference before regenerating |
| Hands, face, or body topology changes between frames | Structural generation failure | Regenerate; interpolation must not invent the missing anatomy |
| Trajectory is continuous but looks stroboscopic at 24 fps | Delivery cadence rather than structural failure | Optionally interpolate an accepted native take to 48 fps |
| Hair or fine edges sparkle while the body path is smooth | High-frequency temporal instability | Use the temporal-detail repair path; do not treat it as cadence |

Confirm codec, fps, timestamps, frame count, and duplicate/frozen frames first. Encoding does not repair a bad pose path, and a nominal 24 fps file is not proof of smooth motion.

### Periodic-cadence diagnostic

If spikes, flashes, or freeze/burst pairs recur at an exact frame interval, do not assume the prompt is the only cause. Record the ComfyUI version and commit, exact checkpoint and VAE filenames, acceleration/attention backend, sampler, scheduler, frame count, and whether the cadence exists in native or lossless output.

Then make the smallest diagnostic A/B that the budget allows: same build and seed with one simple constant pan or slow subject motion, followed by one checkpoint/runtime variable at a time. A regular cadence can expose an implementation, precision, temporal-lattice, or decode issue that interpolation merely conceals.

Public reports illustrate why this remains a diagnostic, not a universal rule:

- a MiniMax H3 issue reports 17-frame periodic instability on specific full INT8/BF16 checkpoints while the pruned checkpoint was unaffected;
- a Wan2GP issue reports a 24-frame panning stutter, but its author explicitly says the same test did not stutter in ComfyUI.

Neither report proves the cause of a new clip. Match the build, checkpoint, cadence, and reproduction before applying any proposed code change.

## Design one motion envelope

Record this before prompting:

- `path`: one physical trajectory, such as one forward weight transfer or one clockwise four-degree turn;
- `cadence`: slow continuous, steady, rhythmic, or intentionally punctuated;
- `ease_in_seconds` and `ease_out_seconds`: long enough to avoid a still-to-motion pop;
- `direction_changes`: normally zero for a short generated shot; one only when the reversal is the action;
- `allowed_body_motion`: the joints and torso axes that move together;
- `locked_contacts`: ownership/contact invariants that remain fixed;
- `delivery_motion`: native 24 fps or optional interpolation after native acceptance.

Use the timeline to expose stages of this same curve. At every boundary, say that position, direction, and speed continue without a pause, reset, snap, or reversal. Give the settle enough time to decelerate rather than requesting a sudden final hold.

For a gentle six-second human action, a conservative starting shape is:

- 0.0–0.75 s: subpixel breathing and gradual acceleration from rest;
- 0.75–4.75 s: one low-frequency action at nearly constant cadence;
- 4.75–5.75 s: gradual deceleration with no new action;
- final 0.75–1.0 s: stable end-state hold with breathing only.

This is a starting profile, not a universal timing rule. Preserve the user's intended rhythm.

## Avoid overconstraint

Natural movement needs degrees of freedom. A prompt that freezes heads, hands, shoulders, hair, camera, background, and contacts while also asking for a turn can force the model into pose holds and catch-up jumps.

- Lock identity, ownership, contact, and dangerous edges.
- Declare small coordinated motion for shoulders, elbows, wrists, hips, and weight transfer instead of saying they never move.
- Keep head rotation small when identity is important, but allow the head to follow the torso with a bounded lag.
- Put the desired opening gaze/expression into the first anchor when possible; forcing a neutral source face to smile in 0.25 seconds creates an avoidable facial acceleration.

## First/last-anchor compatibility

Before FL2VA, compare the anchors at identical crop and scale. Reject or redesign when the last anchor changes background geometry, contact ownership, occlusion order, limb lengths, or large face/body landmarks. A generated frame selected only because it has a good smile can be a poor last anchor if its pose is midway through another motion.

Prefer an endpoint that differs in one intended state: a small expression change, a small pose displacement, or a prop result. If the action needs a large path, split the scene or use an appropriate motion reference instead of making the final frame pull the whole clip into place.

## Sampling and prompt changes

- Use Turbo/low-step runs to explore composition and rough motion, not as the final temporal-quality baseline when they show shimmer or freeze/burst cadence.
- A base/non-Turbo schedule can improve temporal detail, but steps alone do not fix contradictory motion instructions or incompatible anchors.
- Change one variable family per immutable run: motion wording, anchor pair, sampler/steps, or postprocess. Otherwise the cause of improvement is unknowable.

## Controlled motion experiments

Treat motion quality as an experiment, not as a lucky seed.

1. Establish a base/non-Turbo baseline at a native or already proven resolution before adding acceleration LoRAs, caching, interpolation, or restoration.
2. Render a small seed grid, normally three to five candidates, with the contract, anchors, prompt, sampler, and resolution held constant.
3. Rank native candidates on trajectory, dynamic degree, identity, anatomy, contact ownership, temporal flicker, and prompt adherence. Do not select the smoothest clip if it is merely more static.
4. Change one variable family, repeat the same seed set when practical, and record the comparison in the manifest or QC report.
5. Promote a speedup or postprocess to the reusable default only after it wins on repeated representative scenes, including people, hands, hair, fine edges, and occlusions.

Community reports repeatedly recommend starting complex reference/keyframe work with the full model, comparing multiple candidates, and introducing Turbo or other speedups only after a baseline exists. Treat that as useful operational evidence, not as a model guarantee.

## Continuation and multi-clip motion

A single carried last frame preserves appearance but contains no velocity. For a seamless continuation, prefer a supported video/motion-context path that conditions on a short tail of the preceding clip; keep the last frame as an endpoint or identity/composition reference only when the mode gives it that role.

- Discover the live Ref2VA, guide, or motion-context capability before planning this route. Do not assume a community workflow matches the installed H3 build.
- Start with roughly 0.5-2.0 seconds of preceding motion context, then trim overlap after QC. This is an experiment range reported by users, not an H3 guarantee.
- If the continuation still drifts, use a motivated cut, camera sweep, foreground occlusion, or short separately generated bridge instead of hiding a broken join with interpolation.
- Do not add unverified masking nodes, latent-injection forks, smooth-motion LoRAs, or third-party models to the factory default without authorization and a controlled A/B evaluation.

## Optional frame interpolation

Interpolate only after the native take passes anatomy, identity, ownership, and trajectory QC. Interpolation is appropriate for continuous 24 fps motion that still looks stroboscopic; it is not a repair for pose jumps, contact changes, duplicate limbs, or endpoint pull.

When live ComfyUI discovery shows `FrameInterpolationModelLoader`, `FrameInterpolate`, and a local FILM/RIFE model, a 2× pass can create a 48 fps review candidate. Keep the accepted native file, version the interpolated run separately, and verify output timestamps, frame count, duration, and audio sync. Do not silently return the interpolated result to 24 fps, because that usually discards the smoothness benefit.

ComfyUI's core node produces `(input_frames - 1) * multiplier + 1` frames. An exact-duration delivery therefore needs an explicit timestamp or tail-frame policy rather than assuming that `2× frames` encoded at `2× fps` is duration-identical.

Inspect interpolated adjacent frames around hands, glasses, mouths, hair, occlusions, and direction changes. Reject double edges, rubber fingers, face blends, or geometry that exists only in synthetic in-between frames.

## Motion QC evidence

Review at normal speed and 0.5× speed, then inspect frame strips around every beat boundary and the largest motion changes. A useful diagnostic reports normalized adjacent-frame luma deltas and the locations of spikes/freezes; it supports visual review but never replaces it. Use `scripts/analyze_motion.py` when `ffmpeg` is available.

Score these dimensions separately before issuing one verdict:

- `trajectory_smoothness`: velocity and acceleration remain coherent rather than freezing and bursting;
- `dynamic_degree`: the requested action has enough visible amplitude and did not become static to gain smoothness;
- `temporal_flicker`: texture, lighting, hair, and fine edges do not pulse independently of the action;
- `subject_integrity`: faces, limbs, clothing, and contact ownership remain structurally coherent;
- `background_consistency`: scene geometry and bystanders do not morph or jump;
- `action_adherence`: direction, cadence, timing, expression, and end state follow the scene contract.

This separation follows the useful principle in VBench: motion smoothness, dynamic degree, temporal flicker, subject consistency, and background consistency are different evaluation dimensions. A single adjacent-frame-difference score cannot replace them.

## Evidence hierarchy and research basis

Use recommendations in this order:

1. official MiniMax mode and prompt documentation;
2. live node/model discovery plus a reproducible local A/B test;
3. peer-reviewed methods and public benchmark definitions;
4. repeated community reports, explicitly labeled as anecdotal;
5. isolated presets, LoRA recipes, or workflow claims only as hypotheses to test.

Primary references:

- MiniMax H3 base prompt guide, especially the FL2VA requirement to describe the motion path between anchors: <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md>
- ComfyUI core frame-interpolation implementation: <https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_frame_interpolation.py>
- VBench multidimensional video evaluation: <https://github.com/Vchitect/VBench>
- FILM and RIFE frame-interpolation papers: <https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136670244.pdf> and <https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136740608.pdf>

Community signals to revisit, not blindly adopt:

- official-guide-first prompting and one continuous FL2VA path: <https://www.reddit.com/r/StableDiffusion/comments/1vtnhvj/psa_proper_prompt_structure_really_matters_in_h3/>
- motion-context continuation instead of carrying only one still frame: <https://www.reddit.com/r/StableDiffusion/comments/1vqicp8/anyone_found_any_tricks_for_avoiding_degradation/>
- full-model baseline, candidate grids, and short bridge generation for difficult joins: <https://www.reddit.com/r/comfyui/comments/1xdbmts/minimah_h3_video_continuation_workflow_that/>
- checkpoint-specific 17-frame instability report: <https://github.com/MiniMax-AI/MiniMax-H3/issues/85>
- runtime-specific 24-frame panning-stutter report: <https://github.com/deepbeepmeep/WanGP/issues/2279>
