# Repository instructions

- Keep the repository root project-agnostic. Project-specific prompts, workflows, reviews, decisions, scripts, and media belong under `projects/<id>/`.
- Do not create a top-level `prompts/`, `workflow/`, `review/`, or film-specific `scripts/` directory.
- Read the target project's `project.json` before acting. Historical transcripts do not override the active release or decision records.
- Use the repo-scoped `h3-video-director` skill for MiniMax H3 design, prompting, generation, repair, or QC.
- Establish a scene contract and observable acceptance criteria before a costly generation.
- Discover live ComfyUI nodes/models before building or running a graph. Agent Kit and MCP are optional executors; do not install third-party components, large models, or paid/cloud services without authorization.
- Preserve accepted runs and caches. A changed prompt, workflow, model setting, assembly, or upscale profile gets a new version and manifest.
- Review native frames before upscaling, and review the final encoded master before delivery.
- Every video review or delivery handoff must include a broadly compatible H.264 MP4 (`yuv420p`, `+faststart`) with verified dimensions, fps, frame count, and duration. A ProRes/MOV mezzanine may be preserved, but it must never be the only user-facing review file.
- For shots with visible people, define each subject's gaze target and expression from the first live frame through the final hold. Treat vacant gaze, frozen affect, hairline shimmer, and frame-to-frame hair/edge flicker as explicit QC failures unless the scene contract intentionally allows them.
