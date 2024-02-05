@echo off
setlocal EnableDelayedExpansion

set "subnet=192.168.0"
set "timeout=1"
set "maxSize=65500"

:ping_loop
for /L %%i in (1,1,254) do (
    set "ip=!subnet!.%%i"
    ping !ip! -n 1 -w !timeout! -l !maxSize! >nul
    if !errorlevel! equ 0 (
        echo !ip! is reachable
    ) else (
        echo !ip! is unreachable
    )
)

goto ping_loop