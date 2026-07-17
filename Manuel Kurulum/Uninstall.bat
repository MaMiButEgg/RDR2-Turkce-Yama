@echo off
title RDR2 Turkce Yama Kaldirici

REM Programin bulundugu klasoru al
set "gamepath=%~dp0"

echo UYARI: Bu islem tum turkce yama dosyalarini silecektir!
echo Devam etmek icin ENTER tusuna basin, iptal etmek icin CTRL+C.
pause >nul

REM Dosyalari sil
del "%gamepath%rdr2-translator.asi" 2>nul
del "%gamepath%rdr2-translator.xml" 2>nul

echo Turkce yama basariyla kaldirildi!
pause
exit