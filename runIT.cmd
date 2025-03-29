@ECHO OFF

CD /D %~dp0

COPY /Y %APPDATA%\GHISLER\wi*.ini .\

PYTHON.exe inicopy3.py

COPY /Y %APPDATA%\GHISLER\wincmd_large.ini %APPDATA%\GHISLER\wincmd_large.ini.bak
COPY /Y .\wincmd_large.ini %APPDATA%\GHISLER\

START "" "%ProgramFiles%\totalcmd\TOTALCMD64.EXE" /i=%APPDATA%\GHISLER\wincmd_large.ini
