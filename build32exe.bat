@echo off
title TSC Editor+ Lite - Builder
setlocal enabledelayedexpansion

:: ============================================================
:: CONFIGURACIÓN
:: ============================================================
:: Ruta de Python 32 bits (ajusta si es necesario)
set PYTHON_CMD=py -3.13-32

:: Nombre del ejecutable
set EXE_NAME=TSC Editor+ Lite

:: Versión
set VERSION=2.0

:: Archivo de icono (relativo a la raíz)
set ICON_FILE=icon-lite.ico

:: Archivo de notas para antivirus
set NOTICE_FILE=Antivirus Notice.txt

:: Carpeta donde se instalan las dependencias locales (si usas auto-instalador)
set LIBS_DIR=libs

:: ============================================================
:: INICIO
:: ============================================================
echo ==================================================
echo   TSC Editor+ Lite - Builder v%VERSION%
echo ==================================================
echo.

:: Verificar PyInstaller
echo Verificando PyInstaller...
%PYTHON_CMD% -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no encontrado. Instalando...
    %PYTHON_CMD% -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: No se pudo instalar PyInstaller.
        pause
        exit /b 1
    )
)

:: Limpiar builds anteriores
echo Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del /q *.spec 2>nul

:: Construir argumentos --add-data para recursos
set ADD_DATA_ARGS=--add-data "faces;faces" --add-data "tsc_editor;tsc_editor"

:: Añadir archivos JSON de configuración si existen
if exist "settings.json" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "settings.json;."
if exist "custom_commands.json" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "custom_commands.json;."
if exist "command_colors.json" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "command_colors.json;."
if exist "FaceAnimation.json" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "FaceAnimation.json;."
if exist "Gemini Icon.png" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "Gemini Icon.png;."

:: Añadir la carpeta libs (dependencias locales) si existe
if exist "%LIBS_DIR%" set ADD_DATA_ARGS=%ADD_DATA_ARGS% --add-data "%LIBS_DIR%;libs"

:: Construir argumentos --hidden-import
set HIDDEN_ARGS=--hidden-import ttkbootstrap --hidden-import PIL --hidden-import pywinstyles

:: Opcional: si usas pillow, pywinstyles, etc., forzarlos
set HIDDEN_ARGS=%HIDDEN_ARGS% --hidden-import PIL._tkinter_finder

:: Generar el ejecutable
echo.
echo Generando ejecutable (esto puede tardar)...
%PYTHON_CMD% -m PyInstaller --onedir --windowed --noupx --name "%EXE_NAME%" --icon "%ICON_FILE%" %ADD_DATA_ARGS% %HIDDEN_ARGS% main.py

if errorlevel 1 (
    echo ERROR: Falló la generación.
    pause
    exit /b 1
)

:: Copiar el aviso de antivirus si existe
if exist "%NOTICE_FILE%" (
    echo Copiando %NOTICE_FILE%...
    copy "%NOTICE_FILE%" "dist\%EXE_NAME%\" >nul
) else (
    echo AVISO: No se encontró %NOTICE_FILE%.
)

:: Crear ZIP
echo.
echo Creando ZIP para distribución...
set ZIP_NAME=TSC-Editor-RCL-%VERSION%.zip
powershell -Command "Compress-Archive -Path 'dist\%EXE_NAME%\*' -DestinationPath '%ZIP_NAME%' -Force"
if errorlevel 1 (
    echo ERROR: No se pudo crear el ZIP.
) else (
    echo ZIP creado: %ZIP_NAME%
)

echo.
echo ==================================================
echo   Proceso completado.
echo   Ejecutable en: dist\%EXE_NAME%\
echo   ZIP: %ZIP_NAME%
echo ==================================================
pause