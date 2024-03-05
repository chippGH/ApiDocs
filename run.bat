@echo off
SET mypath=%~dp0
cmd /k "cd /d %mypath%venv\Scripts & activate & cd /d %mypath:~0, -1% & waitress-serve --port 8080 --threads=8 app:app"