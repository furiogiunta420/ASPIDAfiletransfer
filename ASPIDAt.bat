@echo off
title Aspida File Transfer Server
color d
setlocal EnableDelayedExpansion 


:loop
cls
color d 





:::                                         ___   ___        __                                               
:::                              .'|=|`.   |   |=|_.'   .'|=|  |    .'|   .'|=|`.     .'|=|`.                 
:::                            .'  | |  `. `.  |      .'  | |  |  .'  | .'  | |  `. .'  | |  `.               
:::                            |   |=|   |   `.|=|`.  |   |=|.'   |   | |   | |   | |   |=|   |               
:::                            |   | |   |  ___  |  `.|   |       |   | |   | |  .' |   | |   |               
:::                            |___| |___|  `._|=|___||___|       |___| |___|=|.'   |___| |___|               
:::                                                                                                           
:::                                               ___                         ___                             
:::                                          .'|=|_.'   .'|   .'|        .'|=|_.'                             
:::                                        .'  |  ___ .'  | .'  |      .'  |  ___                             
:::                                        |   |=|_.' |   | |   |      |   |=|_.'                             
:::                                        |   |      |   | |   |  ___ |   |  ___                             
:::                                        |___|      |___| |___|=|_.' |___|=|_.'                             
:::                                                                                                           
:::              ___  ___   ___        __                     ___   ___   ___        ___        ___        __ 
:::             `._|=|   |=|_.'   .'|=|  |   .'|=|`.     .'| |   | |   |=|_.'   .'|=|_.'   .'|=|_.'   .'|=|  |
:::                  |   |      .'  | |  | .'  | |  `. .'  |\|   | `.  |      .'  |  ___ .'  |  ___ .'  | |  |
:::                  |   |      |   |=|.'  |   |=|   | |   | |   |   `.|=|`.  |   |=|_.' |   |=|_.' |   |=|.' 
:::                  `.  |      |   |  |`. |   | |   | |   | |  .'  ___  |  `.|   |      |   |  ___ |   |  |`.
:::                    `.|      |___|  |_| |___| |___| |___| |.'    `._|=|___||___|      |___|=|_.' |___|  |_|
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
echo ------------------------------------------------------------------------------------------------------------------------
echo Type 1 to start the server
echo.
echo Type 5 to read the instructions
echo.
echo Type 9 to exit 
echo ------------------------------------------------------------------------------------------------------------------------
echo.

set /p olii=

if /I "!olii!"=="1" goto kala
if /I "!olii!"=="5" goto insi 
if /I "!olii!"=="9" goto endi 

goto loop 



:kala 
cls 
python file_server.py 
goto loop











:insi 
cls
echo Go to your phone or laptop browser that is on the same network
echo.
echo and type in the credentials given to your when you run the server
echo.
echo Transfered files should be saved to received_files
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Type 9 to go back
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.

set /p mana=

if /I "!mana!"=="9" goto loop 


goto insi 

:endi 

set /a rand=%RANDOM% %% 6 + 1 
cls
color 0!rand!
echo Goodbye...
timeout /t 1 >nul 
exit 


