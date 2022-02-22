pushd %~dp0

copy /Y settings_aida64.py settings.py

py main.py

popd
