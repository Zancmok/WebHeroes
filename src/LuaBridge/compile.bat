@echo off
setlocal

REM =========================================
REM Build LuaBridge Linux .so using Docker
REM =========================================

REM Get the directory of this script
set SCRIPT_DIR=%~dp0
REM Remove trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

set IMAGE_NAME=luabridge-builder
set CONTAINER_NAME=luabridge-temp
set OUTPUT_FILE=LuaBridge.so

echo Changing to script directory: %SCRIPT_DIR%
cd /d "%SCRIPT_DIR%"

echo Building Docker image...
docker build -t %IMAGE_NAME% .

IF %ERRORLEVEL% NEQ 0 (
    echo Docker build failed!
    exit /b 1
)

echo Creating temporary container...
docker create --name %CONTAINER_NAME% %IMAGE_NAME%

IF %ERRORLEVEL% NEQ 0 (
    echo Container creation failed!
    exit /b 1
)

echo Copying %OUTPUT_FILE%...
docker cp %CONTAINER_NAME%:/build/%OUTPUT_FILE% "%SCRIPT_DIR%\..\WebHeroes\%OUTPUT_FILE%"

IF %ERRORLEVEL% NEQ 0 (
    echo Failed to copy output file!
    docker rm %CONTAINER_NAME%
    exit /b 1
)

echo Cleaning up...
docker rm %CONTAINER_NAME%

echo ========================================
echo Build complete: %OUTPUT_FILE%
echo ========================================

endlocal
pause
