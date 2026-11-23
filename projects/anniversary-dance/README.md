# Юбилейный танец пары

Project ID: `anniversary-dance`

## Замысел

Один непрерывный фотореалистичный кадр длительностью 158 кадров (6,58 с при 24 fps). Пара из исходной фотографии делает один небольшой медленный танцевальный шаг, мягко покачивается в закрытой позиции и заканчивает взглядом друг на друга и естественными улыбками. Хват рук, одежда, возраст и узнаваемость людей не меняются.

## Текущее состояние

- Исходная танцевальная фотография и две дополнительные фотографии пары скопированы в игнорируемый `workspace/`.
- Из дополнительных фотографий подготовлены четыре identity-кропа: по два на каждого человека.
- Выбран режим MiniMax H3 FL2VA с первым и последним кадрами.
- Сценарий, scene contract, prompt draft, ownership ledger, generation spec и QC-план готовы к проверке.
- Генерация ещё не запускалась. ComfyUI во время последнего preflight не был запущен.

## Главные документы

- `prompts/brief.md` — требования и допущения.
- `prompts/reference-plan-v1.md` — назначение всех фотографий и приоритеты идентичности.
- `prompts/scene-01-plan-v1.md` — сценарий и тайминг сцены.
- `prompts/scene-01-contract-v1.json` — проверяемый контракт H3.
- `workflow/PRODUCTION_PLAN_v1.md` — последовательность производства.
- `review/QC_CHECKLIST_v1.md` — критерии приёмки.

## Проверка

```powershell
python ..\..\tools\validate_project.py .
python ..\..\.agents\skills\h3-video-director\scripts\validate_scene_contract.py .\prompts\scene-01-contract-v1.json
```

Generated media belongs in `workspace/` and is ignored by git. Prompts, contracts, workflows, manifests, decisions, and QC reports are source material and should be versioned.
