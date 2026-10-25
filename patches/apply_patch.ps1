param(
    [string]$TargetFile,
    [string]$StartMarker,
    [string]$EndMarker,
    [string]$PatchFile
)

$content = Get-Content $TargetFile -Raw

$patch = Get-Content $PatchFile -Raw

$pattern = "(?s)$StartMarker.*?$EndMarker"

$replacement = "$StartMarker`r`n$patch`r`n$EndMarker"

$content = [regex]::Replace(
    $content,
    $pattern,
    $replacement
)

Set-Content `
    -Path $TargetFile `
    -Value $content `
    -Encoding UTF8

Write-Host "Patch Applied Successfully"