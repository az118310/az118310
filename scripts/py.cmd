@echo off
setlocal

set "PY=%USERPROFILE%\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

if not exist "%PY%" (
    set "PY=%USERPROFILE%\.workbuddy\binaries\python\versions\3.13.12\python.exe"
)

if not exist "%PY%" (
    echo [ERROR] Python environment not found.
    exit /b 1
)

endlocal & "%PY%" %*
