---
name: h3-video-director
description: Direct and productionize MiniMax H3 / Hailuo 3 video scenes from rough ideas through requirements, mode selection, structured prompts, ComfyUI workflows, manifests, and frame-level QC. Use when a user asks to design, prompt, generate, repair, or review an H3 video; when an H3 request is underspecified; or when hands, identity, props, camera, transitions, audio, references, duration, or execution backend must be made reliable.
---

# H3 Video Director

Turn an idea into a testable scene before spending generation time. Work in the user's language.

## Route the task

1. Locate the nearest project configuration, scene contract, generation spec, references, and prior QC. Do not treat an old prompt as the current requirement when a newer decision record exists.
2. Decide whether the user wants advice, a prompt/contract, a workflow, a generation run, a repair, or QC. Do not run generation for an advice-only request.
3. If material requirements are missing, run the compact intake in [references/intake-and-scene-contract.md](references/intake-and-scene-contract.md). Ask only questions whose answers change the graph, composition, cost, or acceptance test. Offer a recommended default for every question.
4. Write or update a scene contract. Validate JSON contracts with:

   ```text
   python scripts/validate_scene_contract.py <contract.json>
   ```

5. Select an H3 conditioning mode and feasible render profile using [references/h3-capabilities.md](references/h3-capabilities.md). Separate model capability from the current machine's proven profile.
6. For people, hands, held objects, contact, or handoffs, complete the ownership ledger in [references/anatomy-and-continuity.md](references/anatomy-and-continuity.md) before writing the prompt.
7. For any visible action, define one continuous motion envelope and diagnose smoothing options with [references/motion-continuity.md](references/motion-continuity.md).
8. Write the mode-specific structured prompt using [references/prompt-formats.md](references/prompt-formats.md).
9. Select and preflight the execution backend using [references/comfy-execution.md](references/comfy-execution.md). When this repository is available, run `python tools/comfy_preflight.py --json` first. Discover live nodes, models, templates, and limits; never infer them from a frozen list. If a requested Comfy backend is absent, follow the tested installation and repair procedure in that reference. Install only after explicit authorization, then verify the MCP handshake and record the machine profile before a costly run.
10. Generate a low-cost proof, inspect it, then promote an accepted take. Apply the gates in [references/qc-gates.md](references/qc-gates.md).

## Requirement gate

Do not finalize a scene while any of these are ambiguous and materially relevant:

- delivery duration, aspect ratio, frame rate, platform, or safe areas;
- subject count, identity references, wardrobe, screen position, and allowed visibility;
- one causal action and its observable start and end states;
- one continuous motion path, intended cadence, direction changes, ease-in/ease-out, and whether delivery above 24 fps is allowed;
- camera motion, cuts, transition ownership, and final hold;
- every visible hand, contact, prop owner, and handoff;
- dialogue, language, sound, music, and lip-sync expectations;
- each visible subject's gaze target and expression state at establish, action, settle, and final hold;
- hair silhouette, hairline, glasses, facial-edge, and other high-frequency temporal locks when people are visible;
- elements that must remain unchanged and explicit acceptance criteria;
- local versus cloud execution, available hardware, time, and paid-service permission.

If the user delegates a choice, choose a technically conservative default and record it as an assumption. If the prompt is already explicit, summarize it and proceed without repeating the interview.

## Directing rules

- Prefer one causal action beat per generated shot. Split a dense scene before adding more prompt clauses.
- Describe chronology as observable states: establish, prepare, execute, settle, end-state lock.
- Treat those beats as labels on one motion curve, not separate commands. Specify velocity continuity across boundaries, bounded acceleration, cadence, and the number of intentional direction changes; avoid stop-start verbs unless a stop is visible and required.
- Do not lock every body part while asking for a full-body action. Lock ownership and high-risk geometry, then state which joints, torso axes, and contacts are allowed to move together.
- For first/last-frame work, reject an endpoint that requires a late pose pull, large landmark displacement, new occlusion, or a changed contact. Prefer the smallest endpoint difference that proves the required result.
- State positive geometry and ownership before exclusions. A negative list cannot repair an impossible composition.
- Use stable subject IDs across contract, prompt, references, graph, manifest, and QC.
- Lock counts: physical people, visible faces, visible hands per person, and instances of important props.
- Keep camera motion purposeful and bounded by type, amplitude, speed, and end state.
- Give every visible face an observable performance from the first live frame: gaze target, eyelid activity, facial tension, and smile/neutral state. Do not leave an unspecified neutral interval that the model can fill with a vacant stare.
- Treat hair and face edges as geometry, not only identity descriptors. Lock the hairline, outer silhouette, major curl or strand groups, glasses edges, and their permitted motion; if no wind or head turn is intended, say they remain fixed frame to frame.
- Use first/last frame or structured references when the final state matters; do not rely on a first frame alone for a precise handoff or ownership change.
- Never mix frame-conditioning and reference-conditioning modes in one H3 model call. Split the operation or choose the mode that protects the highest-risk requirement.
- Treat prompt expansion, graph settings, seed, model files, references, output, and QC verdict as one versioned run.

## Execution and mutation policy

- A direct request to generate authorizes an appropriate local proof run after preflight. Do not ask for redundant confirmation.
- Ask before installing third-party Agent Kit components, downloading large models, using a paid/cloud run, or changing credentials unless the user explicitly authorized it.
- Do not install a backend merely because it is optional. If the direct local API already satisfies the task, keep working unless the user requested the MCP/Agent Kit integration or it is necessary for the requested operation.
- After installing a Codex skill or MCP server, state that a new Codex session is required to load it. In the current session, use the installed command-line client or direct HTTP API for verification instead of pretending newly registered tools are already attached.
- Prefer a dedicated virtual environment for the official `comfy-mcp`. For Agent Kit, install the knowledge, templates, and MCP driver with its optional in-graph Claude nodes skipped unless the user explicitly needs them; those nodes change the production ComfyUI checkout and require a restart.
- Never commit secrets. Do not place API keys in workflow JSON, manifests, prompts, or logs.
- Save both the canvas-readable workflow and runnable API workflow when the backend supports both.
- Preserve the archival/mezzanine output when useful, but always create and validate an H.264 MP4 (`yuv420p`, `+faststart`) for user review. Do not hand off MOV/ProRes as the only playable artifact.
- Use immutable run directories or unique run IDs. Never silently overwrite an accepted workflow or take.
- After an interrupted submission, query queue/history by prompt or job ID before resubmitting.

## Required handoff

For a prompt or plan, return:

1. requirement brief and assumptions;
2. selected H3 mode, render profile, and rejected alternatives;
3. scene contract and ownership ledger;
4. structured H3 prompt;
5. reference/ComfyUI graph plan;
6. acceptance checklist and known risks.

For a completed run, additionally record:

- workflow and manifest paths;
- seed, model files, hashes when available, dimensions, frames, fps, and duration;
- reference hashes and exact selected source window;
- QC evidence, accepted limitations, and final artifact hash.
- paths and hashes for both the mezzanine, when retained, and the required review MP4.

Do not call a result final merely because generation or encoding completed.
