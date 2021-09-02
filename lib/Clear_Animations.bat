@echo off

chcp 65001
cls

setlocal
:PROMPT
SET CONFIRM=S
SET /P CONFIRM=Confirmar a exclusão de todos os arquivos ([S]/N)? 

IF /I "%CONFIRM%" NEQ "S" GOTO NO
attrib +r +s *.bat
del /S /Q /A:-R *.*
attrib -r -s *.bat

:NO
endlocal