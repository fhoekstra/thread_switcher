pushd %~dp0

cp settings_aida64.py settings.py

python310 main.py

popd

pause