@echo off
title TimeTrackerT2 v2.0 - Build Automatico
color 0A

echo.
echo ==========================================
echo    TIMETRACKERT2 V2.0 - AUTO BUILD
echo ==========================================
echo.
echo Questo script preparera' automaticamente:
echo - Versione vergine senza dati personali
echo - Eseguibile unico (.exe) 
echo - Pacchetto pronto per la distribuzione
echo.
echo I tuoi dati personali verranno preservati!
echo.
pause
echo.

echo Avvio processo di build...
python scripts\auto_build.py

echo.
echo ==========================================
echo           BUILD COMPLETATO!
echo ==========================================
echo.
echo Controlla la cartella 'release' per il pacchetto finale.
echo L'eseguibile e' pronto per la distribuzione!
echo.
pause