@echo off
setlocal EnableDelayedExpansion

set "subnet=192.168.0"
set "timeout=1"

:ping_loop
for /L %%i in (1,1,254) do (
    set "ip=!subnet!.%%i"
    ping !ip! -n 1 -w !timeout! >nul
    if !errorlevel! equ 0 (
        echo !ip! is reachable
    ) else (
        echo !ip! is unreachable
    )
)

goto ping_loop