@echo off
:LOOP
for /f %%i in (.\threadlist.txt) do Powershell "ForEach($PROCESS in GET-PROCESS prime95) { $PROCESS.ProcessorAffinity=%%i}" | ping -n 10 127.0.0.1
GOTO LOOP
