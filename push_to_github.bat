@echo off
echo Adding files...
git add -A

echo Committing...
git commit -m "Fix: Downgrade Next.js/React and rename package to 'web' for Netlify compatibility"

echo Pushing to GitHub...
git push origin main

echo.
echo Done!
