pushd %~dp0

copy /Y settings_aida64.py settings.py

python310 main.py

popd
