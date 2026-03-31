Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipPath = $args[0]
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)

$slides = $zip.Entries | Where-Object { $_.FullName -match 'ppt/slides/slide\d+\.xml' } | Sort-Object FullName
Write-Host "Number of slides: $($slides.Count)"

foreach ($slide in $slides) {
    Write-Host "`n=== $($slide.FullName) ==="
    $reader = New-Object System.IO.StreamReader($slide.Open())
    $content = $reader.ReadToEnd()
    $reader.Close()
    $texts = [regex]::Matches($content, '<a:t>([^<]+)</a:t>') | ForEach-Object { $_.Groups[1].Value.Trim() } | Where-Object { $_ -ne '' }
    $texts | ForEach-Object { Write-Host $_ }
}
$zip.Dispose()
