python -OO -m PyInstaller -y --clean -F -n FactorioModPackSwapper --uac-admin --version-file file_version_info.txt main.py
copy .\dist\FactorioModPackSwapper.exe .