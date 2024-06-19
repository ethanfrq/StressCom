@echo off
setlocal EnableDelayedExpansion

set "script_path="
set /p script_path="Entrez le chemin complet du script Python (.py) : "

set "exe_name="
set /p exe_name="Entrez le nom du fichier executable de sortie (sans extension) : "

echo Verification de l'installation de PyInstaller...
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller n'est pas installe. Installation en cours...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Echec de l'installation de PyInstaller. Verifiez votre installation de Python et pip.
        exit /b 1
    ) else (
        echo PyInstaller a ete installe avec succes.
    )
) else (
    echo PyInstaller est deja installe.
)

echo Creation de l'executable...
pyinstaller --onefile --name %exe_name% "%script_path%" >nul 2>&1

set "bar=."
for /L %%i in (1,1,50) do (
    set /p "=." <nul
    ping -n 2 127.0.0.1 >nul 2>&1
)
echo.

if exist "dist\%exe_name%.exe" (
    echo L'executable a ete cree avec succes : dist\%exe_name%.exe
) else (
    echo Echec de la creation de l'executable. Verifiez les logs pour plus de details.
)

echo Affichage des logs...
type "dist\%exe_name%.exe"
echo.

pause
