$files = @("server.py", "time_sync.py", "display.py", "wifi_manager.py", "sensor.py", "location_service.py", "config_manager.py", "main.py")

foreach ($file in $files){
  Write-Host "Uploading file $file to ESP..."
  python -m mpremote connect COM3 cp .\$file : *>$null
  Start-Sleep -Seconds 1.5
}

python -m mpremote connect COM3
