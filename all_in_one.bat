@echo off

:run

if "%~x1" == "" (
    if "%1" == "" (
        goto end
    ) else (
        set mode=%1
        call :mode_all
    )
) else ( 
    set mode=%~x1
    call :mode
)

goto :end

:mode_all
echo mode: %mode%
@echo on
for %%i in (*.%mode%) do python %mode%.py %%i
@echo off
goto :eof

:mode
echo mode: %mode%
@echo on
for %%i in (%*) do python %mode:~1%.py %%i
@echo off
goto :eof

:end

pause