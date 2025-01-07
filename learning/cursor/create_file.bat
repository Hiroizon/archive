@echo off
chcp 932
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
echo. > %year%-%month%-%day%.txt
echo %year%-%month%-%day%.txtを作成しました。
