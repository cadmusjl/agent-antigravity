@echo off
echo ========================================
echo   Environment Setup Helper
echo ========================================
echo.
echo This script will help you set up your environment files.
echo You'll need to have your API keys ready.
echo.
pause

REM Setup Backend .env
echo.
echo Setting up BACKEND environment file...
echo.
cd backend

if exist .env (
    echo .env file already exists in backend folder.
    echo Do you want to overwrite it? (Y/N)
    set /p overwrite=
    if /i not "%overwrite%"=="Y" goto frontend_setup
)

echo Creating backend/.env from .env.example...
copy .env.example .env

echo.
echo ========================================
echo IMPORTANT: Edit backend/.env file now
echo ========================================
echo.
echo Open: %cd%\.env
echo.
echo You need to replace these placeholders:
echo   - OPENAI_API_KEY
echo   - ANTHROPIC_API_KEY
echo   - SUPABASE_URL
echo   - SUPABASE_KEY
echo   - SUPABASE_SERVICE_KEY
echo   - SECRET_KEY
echo   - STRIPE_SECRET_KEY
echo   - And optionally: REPLICATE_API_TOKEN, STABILITY_API_KEY
echo.
echo See USER_ACTION_ITEMS.md for detailed instructions on getting these keys.
echo.
pause

REM Setup Frontend .env.local
:frontend_setup
echo.
echo Setting up FRONTEND environment file...
echo.
cd ..\frontend

if exist .env.local (
    echo .env.local file already exists in frontend folder.
    echo Do you want to overwrite it? (Y/N)
    set /p overwrite2=
    if /i not "%overwrite2%"=="Y" goto done
)

echo Creating frontend/.env.local from .env.example...
copy .env.example .env.local

echo.
echo ========================================
echo IMPORTANT: Edit frontend/.env.local file now
echo ========================================
echo.
echo Open: %cd%\.env.local
echo.
echo You need to replace these placeholders:
echo   - NEXT_PUBLIC_SUPABASE_URL
echo   - NEXT_PUBLIC_SUPABASE_ANON_KEY
echo   - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
echo   - NEXT_PUBLIC_API_URL (update after deploying backend)
echo.
echo See USER_ACTION_ITEMS.md for detailed instructions.
echo.
pause

:done
cd ..
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your API keys
echo 2. Edit frontend\.env.local with your API keys
echo 3. Run 'start-backend.bat' to test backend
echo 4. Run 'start-frontend.bat' to test frontend
echo 5. Follow USER_ACTION_ITEMS.md for production deployment
echo.
pause
