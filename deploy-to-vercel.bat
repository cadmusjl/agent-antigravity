@echo off
echo ========================================
echo   Deploying Frontend to Vercel
echo ========================================
echo.

REM Check if vercel CLI is installed
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo Failed to install Vercel CLI
        pause
        exit /b 1
    )
)

echo Navigating to frontend directory...
cd frontend

echo.
echo Checking environment variables...
if not exist .env.local (
    echo WARNING: .env.local not found!
    echo Please create .env.local with your environment variables
    echo See .env.example for reference
    pause
    exit /b 1
)

echo.
echo Starting Vercel deployment...
echo Follow the prompts to deploy your application
echo.
vercel --prod

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy your Vercel URL
echo 2. Update NEXT_PUBLIC_API_URL in Vercel dashboard once backend is deployed
echo 3. Update ALLOWED_ORIGINS in backend to include your Vercel URL
echo.
pause
