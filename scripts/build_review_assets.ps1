param(
    [Parameter(Mandatory = $true)]
    [string]$V3Video,
    [string]$PackageRoot = 'C:\Users\Vadim\Downloads\PhotoDay_H3_v3_Dynamic_Reproducible'
)

$ErrorActionPreference = 'Stop'
$V1Video = Join-Path $PackageRoot 'references\PhotoDay_v1_motion_master.mp4'
$ReviewDir = Join-Path $PackageRoot 'review\v1_v3_comparison'
New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null

foreach ($Required in @($V1Video, $V3Video)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "Missing required video: $Required"
    }
}

& ffmpeg -hide_banner -loglevel warning -y `
    -i $V1Video -i $V3Video `
    -filter_complex '[0:v]scale=540:960:flags=lanczos[v1];[1:v]scale=540:960:flags=lanczos[v3];[v1][v3]hstack=inputs=2[out]' `
    -map '[out]' -an -t 10 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p `
    (Join-Path $ReviewDir 'v1_left_v3_right_10s.mp4')

& ffmpeg -hide_banner -loglevel warning -y `
    -i $V3Video -vf 'fps=2,scale=288:512:flags=lanczos,tile=5x4' -frames:v 1 `
    (Join-Path $ReviewDir 'v3_full_timeline_2fps.jpg')

for ($Scene = 1; $Scene -le 5; $Scene++) {
    $Start = ($Scene - 1) * 2
    $Output = Join-Path $ReviewDir ("scene_{0:D2}_v1_left_v3_right_6fps.jpg" -f $Scene)
    & ffmpeg -hide_banner -loglevel warning -y `
        -ss $Start -t 2 -i $V1Video -ss $Start -t 2 -i $V3Video `
        -filter_complex '[0:v]fps=6,scale=180:320:flags=lanczos[v1];[1:v]fps=6,scale=180:320:flags=lanczos[v3];[v1][v3]hstack=inputs=2[pair];[pair]tile=6x2[out]' `
        -map '[out]' -frames:v 1 $Output
}

& ffmpeg -hide_banner -loglevel warning -y `
    -ss 4 -t 4 -i $V3Video -vf 'fps=6,scale=180:320:flags=lanczos,tile=6x4' -frames:v 1 `
    (Join-Path $ReviewDir 'female_photographer_all_4s_to_8s_6fps.jpg')

& ffmpeg -hide_banner -loglevel warning -y `
    -ss 8 -t 2 -i $V3Video -vf 'fps=12,scale=180:320:flags=lanczos,tile=6x4' -frames:v 1 `
    (Join-Path $ReviewDir 'final_hair_all_8s_to_10s_12fps.jpg')

$FullFrameQcDir = Join-Path $PackageRoot 'review\full_frame_qc'
New-Item -ItemType Directory -Force -Path $FullFrameQcDir | Out-Null
for ($Scene = 1; $Scene -le 5; $Scene++) {
    $Start = ($Scene - 1) * 2
    $Output = Join-Path $FullFrameQcDir ("scene_{0:D2}_all_48_frames.jpg" -f $Scene)
    & ffmpeg -hide_banner -loglevel warning -y `
        -ss $Start -t 2 -i $V3Video `
        -vf 'scale=135:240:flags=lanczos,tile=8x6' -frames:v 1 $Output
}

Write-Output "Review assets written to $ReviewDir"
