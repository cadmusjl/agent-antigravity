@echo off
echo ========================================
echo   Deployment Readiness Check
echo ========================================
echo.

set errors=0

REM Check backend .env
echo Checking backend configuration...
if not exist backend\.env (
    echo [X] backend\.env file NOT FOUND
    echo     Create it using: setup-environment.bat
    set /a errors+=1
) else (
    echo [OK] backend\.env file exists

    REM Check for placeholder values
    findstr /C:"your_openai_api_key_here" backend\.env >nul 2>nul
    if %errorlevel% equ 0 (
        echo [!] WARNING: Found placeholder values in backend\.env
        echo     Update with real API keys before deploying
        set /a errors+=1
    ) else (
        echo [OK] No obvious placeholders found in backend\.env
    )
)

echo.
echo Checking frontend configuration...
if not exist frontend\.env.local (
    echo [X] frontend\.env.local file NOT FOUND
    echo     Create it using: setup-environment.bat
    set /a errors+=1
) else (
    echo [OK] frontend\.env.local file exists

    REM Check for placeholder values
    findstr /C:"your-project.supabase.co" frontend\.env.local >nul 2>nul
    if %errorlevel% equ 0 (
        echo [!] WARNING: Found placeholder values in frontend\.env.local
        echo     Update with real values before deploying
        set /a errors+=1
    ) else (
        echo [OK] No obvious placeholders found in frontend\.env.local
    )
)

echo.
echo Checking dependencies...

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Node.js NOT FOUND
    echo     Install from: https://nodejs.org
    set /a errors+=1
) else (
    echo [OK] Node.js found
)

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Python NOT FOUND
    echo     Install from: https://python.org
    set /a errors+=1
) else (
    echo [OK] Python found
)

REM Check if frontend dependencies installed
if not exist frontend\node_modules (
    echo [!] WARNING: Frontend dependencies not installed
    echo     Run: cd frontend && npm install
    set /a errors+=1
) else (
    echo [OK] Frontend dependencies installed
)

REM Check if backend dependencies installed
python -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo [!] WARNING: Backend dependencies may not be installed
    echo     Run: cd backend && pip install -r requirements.txt
    set /a errors+=1
) else (
    echo [OK] Backend dependencies appear to be installed
)

echo.
echo Checking deployment tools...

REM Check Vercel CLI
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Vercel CLI not installed (optional for deployment)
    echo     Install with: npm install -g vercel
) else (
    echo [OK] Vercel CLI found
)

echo.
echo ========================================
if %errors% equ 0 (
    echo   STATUS: READY FOR DEPLOYMENT
    echo ========================================
    echo.
    echo You can now:
    echo   1. Deploy frontend: run deploy-to-vercel.bat
    echo   2. Deploy backend: follow USER_ACTION_ITEMS.md
    echo.
) else (
    echo   STATUS: NOT READY - %errors% issue(s) found
    echo ========================================
    echo.
    echo Please fix the issues above before deploying.
    echo See USER_ACTION_ITEMS.md for detailed setup instructions.
    echo.
)

pause
