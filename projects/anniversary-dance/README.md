# Юбилейный танец пары

Project ID: `anniversary-dance`

## Замысел

Один непрерывный фотореалистичный кадр длительностью 158 кадров (6,58 с при 24 fps). Пара из исходной фотографии делает один небольшой медленный танцевальный шаг, мягко покачивается в закрытой позиции и заканчивает взглядом друг на друга и естественными улыбками. Хват рук, одежда, возраст и узнаваемость людей не меняются.

## Текущее состояние

- Финальный ролик принят пользователем: 1080x1440, H.264 MP4, 24 fps, 158 кадров, 6,583 с.
- Мужчина эмоционально включён с первых кадров; проблемное мерцание волос из первого proof устранено до приемлемого уровня.
- Нативный FL2VA v2 и RealESRGAN upscale сохранены как неизменяемые runs с manifests и хешами.
- Остаточная лёгкая рваность движения принята для этого релиза и подробно зафиксирована как урок для будущих проектов.
- Активный master: `workspace/runs/scene-01-upscale-realesrgan-x2-v1/outputs/scene-01-upscale-realesrgan-x2-v1_00001__delivery.mp4`.

## Главные документы

- `prompts/brief.md` — требования и допущения.
- `prompts/reference-plan-v1.md` — назначение всех фотографий и приоритеты идентичности.
- `prompts/scene-01-plan-v1.md` — сценарий и тайминг сцены.
- `prompts/scene-01-contract-v1.json` — проверяемый контракт H3.
- `workflow/PRODUCTION_PLAN_v1.md` — последовательность производства.
- `review/QC_CHECKLIST_v1.md` — критерии приёмки.
- `review/QC_REPORT_scene-01-repair-fl2va-v2.md` — финальная проверка, хеш master и анализ ритма движения.
- `decisions/ADR-003-motion-continuity-and-accepted-delivery.md` — решение о приёмке и стандарт плавности для будущих проектов.

## Проверка

```powershell
python ..\..\tools\validate_project.py .
python ..\..\.agents\skills\h3-video-director\scripts\validate_scene_contract.py .\prompts\scene-01-contract-v1.json
```

Generated media belongs in `workspace/` and is ignored by git. Prompts, contracts, workflows, manifests, decisions, and QC reports are source material and should be versioned.
