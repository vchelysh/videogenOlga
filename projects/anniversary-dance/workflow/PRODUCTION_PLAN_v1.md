# Production plan v1

## 1. Reference gate

- Сохранить исходные файлы неизменными и сверить SHA-256 с `reference-pack-v1.json`.
- Использовать четыре лицевых кропа только для идентичности/выражения.
- Получить подтверждение на очистку фоновых гостей и на территорию использования H3 output.

## 2. Anchor gate

- Подготовить first anchor по `scene-01-anchor-edit-brief-v1.md`.
- Проверить в 100% масштабе лица, очки, четыре кисти, запястья, локти, ткань и отсутствие новых фигур.
- Из принятого first anchor подготовить last anchor с минимальным изменением лиц.
- Сделать difference-проверку: вне масок фона и лица геометрия пары должна совпадать.
- Не запускать видео, пока оба якоря не имеют PASS.

## 3. Live ComfyUI preflight

- Подключить уже запущенный ComfyUI или отдельно согласовать headless start.
- Запустить `tools/comfy_preflight.py --json`.
- Проверить live `MiniMaxH3ImageToVideo`, loader inputs и точные имена моделей через `/object_info`.
- Проверить VRAM/RAM/disk, наличие официального H3 template и поддержку двух frame anchors.
- Клонировать template; сохранить GUI JSON в ComfyUI Workflows и API JSON в immutable run directory проекта.

## 4. Proof ladder

1. `scene-01_v001_take01`: 480×640, 158 кадров, 8 steps.
2. Просмотреть все кадры, а не только contact sheet.
3. Если движение/лица/руки структурно неверны — исправить anchor/contract, создать v002; не лечить длинным negative prompt.
4. При хорошем дизайне проверить ещё один seed, если первый take имеет локальный stochastic defect.

## 5. Native production

- Продвигать только proof с PASS.
- Render 576×768, 158 кадров, тот же prompt/anchors/settings и новый записанный seed.
- Сохранить prompt ID, seed, hashes, API/GUI graph и model filenames до ожидания результата.
- При обрыве polling сначала проверить history по prompt ID.

## 6. Native QC

- Полный просмотр 158 кадров.
- Отдельные crops: лицо женщины, лицо мужчины, совместный хват, рука на плече, рука на талии, очки, края одежды.
- Особо проверить соседние кадры вокруг 17-кадровых VAE boundaries на brightness dip/stutter.
- Принять только один непрерывный take; не собирать танец из разрозненных кадров.

## 7. Upscale A/B

- A: Lanczos до 1080×1440 + мягкий unsharp; приоритет идентичности и стабильности.
- B: RealESRGAN x4plus с консервативным blend около 65%, затем downscale до 1080×1440.
- Не использовать face restoration.
- Сравнить лицо/волосы/очки/ткань в движении; более резкий стоп-кадр не выигрывает автоматически.

## 8. Assembly and delivery

- Сохранить 158 кадров без retime и interpolation.
- По решению пользователя оставить видео немым или добавить отдельный лицензированный медленный вальс с короткими fades.
- Проверить encoded master: 1080×1440, 24 fps, 158 кадров, 6,583333 с, yuv420p, отсутствие black/frozen frames.
- Записать final manifest, SHA-256 и QC verdict.
