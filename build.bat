
del .\dist\gui\* /f /q /s
conda activate py31016 && ^
echo building frontend ... && ^
cd .\src\frontend\ && ^
pnpm run build && ^
xcopy .\dist ..\..\dist\gui /E && ^
cd ..\..\ && ^
echo packaging app ... && ^
pyinstaller .\AIBOT.spec && ^
pause
