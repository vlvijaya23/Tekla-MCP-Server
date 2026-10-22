@echo off

cd /d C:\tekla-mcp

python -m PyInstaller ^
--clean ^
--onefile ^
--windowed ^
--name TeklaAIModeler ^
product\app.py

pause