# Reproduction environment

- OS: Windows
- GPU: NVIDIA GeForce RTX 3070, 8192 MiB VRAM
- NVIDIA driver: 621.14
- System RAM: 32 GB
- ComfyUI root: `C:/Users/Vadim/ComfyUI`
- ComfyUI version: 0.46.0
- ComfyUI git commit: `f99de883d5e65317c7f4a4b617b5aa7936622029`
- ComfyUI launch mode: `--lowvram --listen 127.0.0.1 --port 8188 --disable-auto-launch`
- Python: 3.12.4
- PyTorch: 2.11.0+cu128
- PyAV: 19.0.2
- NumPy: 2.5.4
- Pillow: 13.0.0
- spandrel: 0.4.2
- FFmpeg: 9.0 full build
- Generation frame rate: 24 fps
- Native generation: 448×800, 243 frames, one continuous graph
- Delivery: 1080×1920, 240 frames, exactly 10.000 seconds

The first 512×896 continuous attempt exceeded the physical 8 GB VRAM limit before sampler step 1. The exact failure and prompt ID are retained in `review/ATTEMPT_LOG.md`.
