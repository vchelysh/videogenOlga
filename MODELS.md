# Model inventory

## MiniMax H3 generation

Official model repository: `https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main`

| Component | File | ComfyUI folder |
|---|---|---|
| Video model | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | `models/diffusion_models/` |
| Text encoder | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | `models/text_encoders/` |
| Video VAE | `minimax_h3_video_vae_int8_convrot.safetensors` | `models/vae/` |
| Audio VAE | `minimax_h3_audio_vae_fp32.safetensors` | `models/vae/` |
| Turbo LoRA | `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` | `models/loras/` |

The exact generation graph, model filenames, seed and parameters are stored in
`workflow/generation_manifest_v3.json` and `workflow/minimax_h3_v3_api.json`.

## Delivery upscale

- Model: `RealESRGAN_x4plus.pth`
- Upstream project: `https://github.com/xinntao/Real-ESRGAN`
- Official release URL: `https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth`
- Local path: `C:/Users/Vadim/ComfyUI/models/upscale_models/RealESRGAN_x4plus.pth`
- Size: `67040989` bytes
- SHA-256: `4FA0D38905F75AC06EB49A7951B426670021BE3018265FD191D2125DF9D682F1`

The previous v3 delivery used 65% Real-ESRGAN detail blended with 35% direct
Lanczos resize. The recommended v4 sharp delivery uses the same verified x4plus
model at 100%, followed by a mild deterministic unsharp mask. No face
restoration is used because it can alter identity.

### Alternative official upscale models tested for v4

| Model | Size | SHA-256 | Decision |
|---|---:|---|---|
| RealESRGAN_x2plus.pth | 67061725 | 49FAFD45F8FD7AA8D31AB2A22D14D91B536C34494A5CFE31EB5D89C2FA266ABB | Rejected: cleaner than Lanczos but softer than x4plus on hair and architecture. |
| realesr-general-x4v3.pth | 4885111 | 8DC7EDB9AC80CCDC30C3A5DCA6616509367F05FBC184AD95B731F05BECE96292 | Rejected: high edge score but more painterly skin and edge shaping. |
| realesr-general-wdn-x4v3.pth | 4885111 | 1641F8C4464B9F097C9FDDA5589273713F67CF59F3D909E0BD688F0CEE269DCA | Retained only as a test dependency; not selected for the final master. |

## Transition cleanup

- Model: `film_net_fp16.safetensors`
- Official ComfyUI model URL: `https://huggingface.co/Comfy-Org/frame_interpolation/resolve/main/frame_interpolation/film_net_fp16.safetensors`
- Local path: `C:/Users/Vadim/ComfyUI/models/frame_interpolation/film_net_fp16.safetensors`
- Size: `68882302` bytes
- SHA-256: `F226E51375DC839D4B40E5C3D63DA560DD1EA1C962364EC78F5ADF2D05DB05C0`

FILM is applied only to clean scene-4 source frames after QC rejected the
generated flash/morph. It is not used on the final portrait and is not used to
raise the delivery frame rate.
