@echo off
echo Clearing GitHub credentials from Windows Credential Manager...

cmdkey /delete:git:https://github.com
cmdkey /delete:legacyGeneric:target=git:https://github.com

echo.
echo Credentials cleared!
echo.
echo Now, please run 'push_to_github.bat' again.
echo You should be prompted to sign in.
pause
