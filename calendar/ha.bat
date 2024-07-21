@echo off
setlocal

:: Thực hiện check_calendar.py và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'python' -ArgumentList 'check_calendar.py' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.py: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.exe và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'check_calendar.exe' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.exe: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.exe và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'check_calendar.exe' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.exe: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.py và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'python' -ArgumentList 'check_calendar.py' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.py: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.py và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'python' -ArgumentList 'check_calendar.py' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.py: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.exe và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'check_calendar.exe' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.exe: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.exe và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'check_calendar.exe' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.exe: ' + $duration.TotalSeconds + ' giay'); }"

:: Thực hiện check_calendar.py và đo thời gian
powershell -Command "& { $start = Get-Date; Start-Process -FilePath 'python' -ArgumentList 'check_calendar.py' -NoNewWindow -Wait; $end = Get-Date; $duration = $end - $start; [Console]::WriteLine('Thoi gian thuc hien check_calendar.py: ' + $duration.TotalSeconds + ' giay'); }"


pause
