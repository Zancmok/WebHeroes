title WebHeroes
echo off
cls
py -m pip install -r ./requirements.txt
:run
cls
py -B src/main.py
set /p input=Restart(y/n)?
if /i "%input%" == "y" goto run
