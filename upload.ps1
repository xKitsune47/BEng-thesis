$projectDir = Get-Location

Get-ChildItem -Filter *.py | ForEach-Object {
  $file = $_.Name
  Write-Host "Uploading file '$file' to ESP32..."
  python -m mpremote connect COM3 cp .\$file : *>$null
  Start-Sleep -Seconds 1.5
}

python -m mpremote connect COM3
