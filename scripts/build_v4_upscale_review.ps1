param(
    [string]$PackageRoot = 'C:\Users\Vadim\Downloads\PhotoDay_H3_v3_Dynamic_Reproducible'
)

$ErrorActionPreference = 'Stop'
$V3 = Join-Path $PackageRoot 'outputs\PhotoDay_06-12_MINIMAX_H3_v3_DYNAMIC_1080x1920_FINAL.mp4'
$V4 = Join-Path $PackageRoot 'outputs\PhotoDay_06-12_MINIMAX_H3_v4_SHARP_1080x1920_FINAL.mp4'
$ReviewDir = Join-Path $PackageRoot 'review\upscale_v4_final'
New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null

foreach ($Required in @($V3, $V4)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "Missing required video: $Required"
    }
}

$compareArgs = @(
    '-hide_banner', '-loglevel', 'warning', '-y',
    '-i', $V3, '-i', $V4,
    '-filter_complex', '[0:v]scale=540:960:flags=lanczos[v3];[1:v]scale=540:960:flags=lanczos[v4];[v3][v4]hstack=inputs=2[out]',
    '-map', '[out]', '-an', '-t', '10',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
    (Join-Path $ReviewDir 'v3_left_v4_right_10s.mp4')
)
& ffmpeg @compareArgs
if ($LASTEXITCODE -ne 0) { throw 'v3/v4 comparison encode failed' }

for ($Scene = 1; $Scene -le 5; $Scene++) {
    $Start = ($Scene - 1) * 2
    $Output = Join-Path $ReviewDir ("v4_scene_{0:D2}_all_48_frames.jpg" -f $Scene)
    $sceneArgs = @(
        '-hide_banner', '-loglevel', 'warning', '-y',
        '-ss', $Start, '-t', '2', '-i', $V4,
        '-vf', 'scale=135:240:flags=lanczos,tile=8x6',
        '-frames:v', '1', $Output
    )
    & ffmpeg @sceneArgs
    if ($LASTEXITCODE -ne 0) { throw "scene $Scene contact sheet failed" }
}

$hairArgs = @(
    '-hide_banner', '-loglevel', 'warning', '-y',
    '-ss', '8', '-t', '2', '-i', $V3,
    '-ss', '8', '-t', '2', '-i', $V4,
    '-filter_complex', '[0:v]fps=12,scale=180:320:flags=lanczos[v3];[1:v]fps=12,scale=180:320:flags=lanczos[v4];[v3][v4]hstack=inputs=2[pair];[pair]tile=6x4[out]',
    '-map', '[out]', '-frames:v', '1',
    (Join-Path $ReviewDir 'final_hair_v3_left_v4_right_12fps.jpg')
)
& ffmpeg @hairArgs
if ($LASTEXITCODE -ne 0) { throw 'hair comparison sheet failed' }

Write-Output "v4 review assets written to $ReviewDir"
