# Environment — anniversary-dance

Состояние зафиксировано 2026-11-24. Это плановый профиль; новый ролик ещё не генерировался.

## Машина

- Windows, NVIDIA GeForce RTX 3070, 8 GB VRAM.
- 32 GB system RAM.
- ComfyUI source checkout: `C:/Users/Vadim/ComfyUI`.
- ComfyUI 0.46.0, Python 3.12.4, PyTorch 2.11.0+cu128.
- Launch profile: `--lowvram --listen 127.0.0.1 --port 8188 --disable-auto-launch`.

## Доступный H3 stack

- `minimax_h3_fl2va_pruned_int8_convrot.safetensors`.
- `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`.
- `minimax_h3_video_vae_int8_convrot.safetensors`.
- `minimax_h3_audio_vae_fp32.safetensors`.
- `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`.
- Core node `MiniMaxH3ImageToVideo` поддерживает первый и последний кадры.
- Ref2VA checkpoint не зафиксирован как установленный; этот проект от него не зависит.

## Доказанный и плановый профили

PhotoDay на этой же машине доказал профиль 576×1024, 124 кадра, 8 turbo steps, `res_multistep` + `simple`, около 11 минут на принятом take.

План anniversary-dance: 576×768, 158 кадров, 8 turbo steps. Его pixel-frame budget равен 69 894 144 против 73 138 176 у доказанного профиля, то есть примерно на 4,4% ниже. Это обоснование вероятной вместимости, а не доказанный результат; first+last conditioning всё равно требует отдельного proof-run.

## Backend state

Последний `tools/comfy_preflight.py --json` нашёл официальный local MCP, Agent Kit MCP и direct API route, но `http://127.0.0.1:8188` не отвечал. Перед генерацией нужно запустить или подключить ComfyUI, затем заново проверить live nodes, model filenames, VRAM и свободное место.

## Лицензионный gate

Локальные MiniMax H3 weights имеют территориальные ограничения, распространяющиеся и на outputs. До запуска пользователь должен подтвердить предполагаемую территорию просмотра/пересылки либо выбрать другой генератор.
