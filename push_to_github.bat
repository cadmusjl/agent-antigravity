@echo off
echo Cleaning up...
if exist .git\index.lock del .git\index.lock

echo Adding files...
git add -A

echo Committing...
git commit -m "Restructure project to root for Netlify deployment"

echo Setting remote...
git remote remove origin
git remote add origin https://github.com/cadmusjl/agent-antigravity.git

echo Pushing to GitHub (Force Overwrite)...
echo.
echo IMPORTANT: A login window may appear. Please sign in!
echo.
:: Using --force to overwrite the existing 'test' file/history on remote
git push -f origin main

echo.
echo Done! Please check the output above for any errors.
pause
