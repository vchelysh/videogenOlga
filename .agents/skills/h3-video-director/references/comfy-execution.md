# ComfyUI and Agent Kit execution

The director skill owns requirements, scene design, prompt structure, manifests, and QC. Comfy tooling owns live discovery, graph validation, queueing, and output retrieval. These layers are complementary.

## Discover the available layer

Use the first available route that meets the task:

1. **Official local Comfy MCP:** preferred structured executor when installed. Call `server_info` first, then discover templates, nodes, and models; validate before `run_workflow`; fetch outputs by prompt ID.
2. **Installed ComfyUI-Agent-Kit:** optional third-party local knowledge and MCP layer. Read its `comfyui`, `minimax-h3`, and machine profile instructions when present. Reuse its live hardware/template discovery, but keep this skill's scene contract and QC gates. Discover its current tool surface before calling it: in `comfyui-mcp` 0.52.206 the retired `health_check` name became `get_system_stats` with `{"action":"health"}`.
3. **Direct local ComfyUI HTTP API:** dependable fallback. Check `/system_stats` and `/object_info`, submit to `/prompt`, monitor queue/history, and copy outputs only after successful completion.
4. **Official Comfy Cloud MCP or Comfy Agent:** use only when available and the user authorized cloud/paid execution.

Official Comfy MCP is distinct from the built-in Comfy Agent. The local MCP server is available for external coding agents; the in-app Comfy Agent is generally available in Comfy Cloud, while local Desktop support is documented as forthcoming.

The community ComfyUI-Agent-Kit is also distinct from both. It can install local skills, model recipes, templates, and an MCP driver for Codex, but it is third-party software. Do not install or update it without permission.

Sources:

- Official Comfy MCP: https://docs.comfy.org/agent-tools/mcp
- Official in-app Comfy Agent: https://docs.comfy.org/agent-tools/in-app-agent
- Community Agent Kit: https://github.com/SlavaSexton/ComfyUI-Agent-Kit

## Preflight

Before a slow job:

1. Confirm which backend is active and where it will execute.
2. Read live GPU/VRAM, ComfyUI version, installed nodes, models, and free output space.
3. Search for a current official/template graph before building one from scratch.
4. Clone or version a template; never overwrite an accepted workflow.
5. Confirm every node class and input against live `object_info` or backend validation.
6. Confirm model filenames exist; do not rely on a stale manifest.
7. Check prompt mode matches graph family: FL2VA versus Ref2VA.
8. Save a canvas-readable workflow and runnable API workflow.
9. Submit once, record prompt/job ID immediately, and monitor that job.

## Install or repair missing backends

Only enter this section when the user explicitly requested the integration or already authorized installation. Installing either backend changes user-level state outside the repository. Resolve and verify the exact ComfyUI path first. Never install into the production ComfyUI Python environment merely for convenience.

### Official local Comfy MCP

Requirements: Python 3.10+, an existing ComfyUI checkout, and Codex CLI. On Windows, use a dedicated virtual environment:

```powershell
$ComfyRoot = (Resolve-Path 'C:\path\to\ComfyUI').Path
$McpVenv = Join-Path $env:LOCALAPPDATA 'comfy-mcp'
python -m venv $McpVenv
& "$McpVenv\Scripts\python.exe" -m pip install --upgrade pip
& "$McpVenv\Scripts\python.exe" -m pip install 'comfy-cli>=1.14.0' comfy-mcp
& "$McpVenv\Scripts\comfy.exe" set-default $ComfyRoot --where local

$Codex = (Get-Command codex.cmd -ErrorAction Stop).Source
& $Codex mcp add comfy-mcp `
  --env "COMFY_BIN=$McpVenv\Scripts\comfy.exe" `
  -- "$McpVenv\Scripts\comfy-mcp.exe"
```

On Linux/macOS, use the same isolation pattern with `python3 -m venv ~/.local/share/comfy-mcp`, executables under `bin/`, and the same `codex mcp add` shape. If the server name already exists, inspect it with `codex mcp get comfy-mcp`; remove and recreate it only when its resolved command or `COMFY_BIN` is stale.

Verify before proceeding:

```powershell
& "$McpVenv\Scripts\comfy.exe" --json which
& "$McpVenv\Scripts\comfy.exe" --json system-stats
codex.cmd mcp get comfy-mcp
```

After the next Codex session loads the server, call `server_info`, discover live nodes/models, then `validate_workflow` before a costly `run_workflow`.

### Community ComfyUI-Agent-Kit

Requirements: Git, Python, Node.js/npm, Codex CLI, about 1 GB free for the template clone, and a running or known ComfyUI checkout. Review the upstream installer before every first install because it is third-party code.

Windows:

```powershell
$ComfyRoot = (Resolve-Path 'C:\path\to\ComfyUI').Path
$KitRoot = 'C:\Users\<user>\Tools\ComfyUI-Agent-Kit'
git clone https://github.com/SlavaSexton/ComfyUI-Agent-Kit.git $KitRoot
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$KitRoot\install.ps1" `
  -Agents codex -ComfyUIPath $ComfyRoot -SkipNodes
```

Linux/macOS:

```bash
git clone https://github.com/SlavaSexton/ComfyUI-Agent-Kit.git "$HOME/Tools/ComfyUI-Agent-Kit"
bash "$HOME/Tools/ComfyUI-Agent-Kit/install.sh" --agents codex --comfyui-path /path/to/ComfyUI --skip-nodes
```

`-SkipNodes` / `--skip-nodes` is the default for this director skill. The omitted Anthropic/Claude prompt nodes are only useful when an unattended graph must call an LLM internally; they are not required when Codex writes the H3 prompt. Install them separately only after reviewing their dependencies, credentials, and the required ComfyUI restart.

The upstream installer registers `comfyui-mcp`, installs user skills under `~/.agents/skills/`, and clones the official workflow templates. For a robust Codex registration, prefer absolute Node and package entry paths and set both `COMFYUI_URL` and `COMFYUI_PATH`. On Windows, resolve them with `npm.cmd prefix -g` and `Get-Command node.exe`; the package entry is `node_modules\comfyui-mcp\dist\index.js`. Inspect an existing `comfyui` entry before replacing it.

Run the Agent Kit bootstrap once: read its installed `BOOTSTRAP.md`, query the live server, and fill its preserved `machine.md` with real paths, hardware, model roots, workflow directory, template index, and launch command. Do not copy machine-specific paths into this repository.

### Verification and session boundary

Run the repository preflight again and inspect both registrations:

```powershell
python .\tools\comfy_preflight.py --json
codex.cmd mcp list
```

For a zero-cost end-to-end local smoke test, official `comfy-cli` provides `comfy run-cli --no-pause --no-show-agent`; it runs a tiny no-model workflow. Open the produced image before declaring the backend ready. A fresh Codex session is still required before newly installed MCP tools and user skills appear in the agent tool list. Until then, use Agent Kit's `comfy_client.alive()` or direct HTTP for verification.

## Agent Kit integration contract

If ComfyUI-Agent-Kit is present:

- read its machine profile instead of guessing paths or VRAM;
- use its hardware-aware selection and template index for candidate discovery;
- use its H3 knowledge as a second check against the official model card;
- keep project-owned prompts, contracts, manifests, and decisions inside the repository;
- persist built/run graphs in both the ComfyUI workflow directory and the project run directory;
- do not let an Agent Kit update rewrite project-specific decisions.

If it is absent, continue with official MCP or direct API. Absence is not a blocker.

## Run identity

Create a unique run ID such as `scene03_v007_take02`. The run directory should contain:

- scene contract and prompt snapshot;
- reference paths and hashes;
- GUI and API workflow JSON;
- model/sampler/seed/render settings;
- prompt/job ID and timestamps;
- raw output and selected source interval;
- QC report and verdict.

After interruption, query history using the recorded ID. Never resubmit merely because polling stopped.

## Security and cost

- Never store API keys or OAuth tokens in git.
- Treat partner nodes and cloud generation as potentially paid even from a local graph.
- Ask before installing nodes, models, Agent Kit, MCP servers, or large template libraries unless installation was explicitly requested.
- Report expected download size, VRAM fit, and execution location before a material install or paid run.
