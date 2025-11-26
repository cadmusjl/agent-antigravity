# Complete Production Deployment Guide

This technical guide complements `USER_ACTION_ITEMS.md` with detailed implementation steps.

---

## 🗂️ Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Environment Configuration](#environment-configuration)
3. [Database Setup (Supabase)](#database-setup)
4. [Backend Deployment Options](#backend-deployment)
5. [Frontend Deployment (Vercel)](#frontend-deployment)
6. [Domain & SSL Configuration](#domain-ssl)
7. [Monitoring & Logging](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Users     │────────▶│   Frontend   │────────▶│   Backend   │
│  (Browser)  │         │  (Next.js)   │         │  (FastAPI)  │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                         │
                               │                         │
                               ▼                         ▼
                        ┌──────────────┐         ┌─────────────┐
                        │   Supabase   │         │  AI APIs    │
                        │  (Database)  │         │ (OpenAI/    │
                        │   + Auth     │         │  Anthropic) │
                        └──────────────┘         └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │    Stripe    │
                        │  (Payments)  │
                        └──────────────┘
```

**Technology Stack:**
- Frontend: Next.js 16 (React) + Tailwind CSS
- Backend: FastAPI (Python) + Uvicorn
- Database: PostgreSQL (via Supabase)
- Authentication: Supabase Auth
- Payments: Stripe
- AI: OpenAI GPT-4, Anthropic Claude
- Hosting: Vercel (Frontend), Railway/Render (Backend)

---

## Environment Configuration

### Backend Environment Variables

File: `backend/.env`

```env
# App Configuration
APP_NAME="AI Agent SaaS Platform"
APP_VERSION="1.0.0"
DEBUG=false                              # MUST be false in production

# AI Model API Keys
OPENAI_API_KEY=sk-...                    # From platform.openai.com/api-keys
ANTHROPIC_API_KEY=sk-ant-...            # From console.anthropic.com
REPLICATE_API_TOKEN=r8_...              # From replicate.com/account/api-tokens
STABILITY_API_KEY=sk-...                # Optional: stability.ai

# Supabase Configuration
SUPABASE_URL=https://xxx.supabase.co    # Project Settings > API
SUPABASE_KEY=eyJhbG...                  # Anon public key
SUPABASE_SERVICE_KEY=eyJhbG...          # Service role key (keep secret!)

# JWT Configuration
SECRET_KEY=<64-char-random-string>       # Generate securely!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Configuration
STRIPE_SECRET_KEY=sk_live_...           # Use test keys for testing
STRIPE_WEBHOOK_SECRET=whsec_...         # Set up after deployment

# CORS - Your production frontend URL
ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

### Frontend Environment Variables

File: `frontend/.env.local` (local) or Vercel Dashboard (production)

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...  # Use pk_test_ for testing

# Backend API
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Important Notes:**
- Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Never put secret keys in `NEXT_PUBLIC_` variables
- Use test keys during development, live keys in production

---

## Database Setup

### Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Click "New Project"
3. Fill in:
   - Project name: `agent-saas-platform`
   - Database password: (generate strong password)
   - Region: Choose closest to your users
4. Wait 2-3 minutes for provisioning

### Step 2: Run Database Schema

1. Go to your project dashboard
2. Click "SQL Editor" in left sidebar
3. Click "New query"
4. Copy entire contents of `backend/database_schema.sql`
5. Paste and click "Run"
6. Verify success message

### Step 3: Configure Authentication

1. Go to "Authentication" > "Providers"
2. Enable Email provider (enabled by default)
3. Optional: Enable OAuth providers (Google, GitHub, etc.)
4. Go to "Authentication" > "Email Templates"
5. Customize confirmation and password reset emails
6. Go to "Authentication" > "URL Configuration"
7. Set:
   - Site URL: `https://yourdomain.com`
   - Redirect URLs: `https://yourdomain.com/auth/callback`

### Step 4: Configure Storage (Optional)

If you need file uploads:

1. Go to "Storage" in left sidebar
2. Create a new bucket: `user-uploads`
3. Set policies:
   ```sql
   -- Allow authenticated users to upload
   CREATE POLICY "Allow authenticated uploads"
   ON storage.objects FOR INSERT
   TO authenticated
   WITH CHECK (bucket_id = 'user-uploads');

   -- Allow users to read own files
   CREATE POLICY "Allow users to read own files"
   ON storage.objects FOR SELECT
   TO authenticated
   USING (bucket_id = 'user-uploads' AND auth.uid()::text = (storage.foldername(name))[1]);
   ```

---

## Backend Deployment

### Option 1: Railway (Recommended)

**Pros:** Simple, auto-scaling, good pricing
**Cost:** $5/month minimum

**Deployment Steps:**

1. Push your code to GitHub:
```bash
cd C:\Users\jason\agent-saas-platform
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/agent-saas-platform.git
git push -u origin main
```

2. Go to https://railway.app
3. Sign up / Log in
4. Click "New Project"
5. Select "Deploy from GitHub repo"
6. Authorize GitHub and select your repository
7. Railway will detect Python and use `railway.json` config
8. Add environment variables:
   - Click "Variables" tab
   - Add all variables from `backend/.env`
   - Or import from file

9. Click "Deploy"
10. Copy your deployment URL: `https://your-app.railway.app`

**Custom Domain (Optional):**
1. In Railway project, go to "Settings"
2. Click "Generate Domain" or add custom domain
3. Follow DNS configuration instructions

### Option 2: Render

**Pros:** Free tier available, simple setup
**Cost:** Free (with limitations) or $7/month

**Deployment Steps:**

1. Go to https://render.com
2. Sign up / Log in
3. Click "New +" > "Web Service"
4. Connect GitHub repository
5. Configure:
   - Name: `agent-saas-backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `backend/.env`
7. Click "Create Web Service"
8. Copy deployment URL

**Note:** Free tier spins down after inactivity (requires 30s to wake up)

### Option 3: Docker + Any Cloud

The `backend/Dockerfile` is ready for deployment to any cloud:

**Build and test locally:**
```bash
cd backend
docker build -t agent-saas-backend .
docker run -p 8000:8000 --env-file .env agent-saas-backend
```

**Deploy to:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Apps
- DigitalOcean App Platform
- Fly.io

### Health Check Endpoint

All platforms should use: `/health`

This returns:
```json
{"status": "healthy"}
```

---

## Frontend Deployment

### Deploy to Vercel (Recommended)

**Pros:** Optimized for Next.js, automatic SSL, CDN, zero config
**Cost:** Free (hobby) or $20/month (Pro)

**Method 1: Using Vercel CLI (Easiest)**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd C:\Users\jason\agent-saas-platform\frontend
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Link to existing project? N
# - Project name? agent-saas-platform
# - Which directory? ./ (press Enter)
# - Override settings? N

# Deploy to production
vercel --prod
```

**Method 2: Using Vercel Dashboard**

1. Go to https://vercel.com
2. Click "Add New..." > "Project"
3. Import your GitHub repository
4. Vercel auto-detects Next.js
5. Configure:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.next` (auto-detected)
6. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
   - `NEXT_PUBLIC_API_URL`
7. Click "Deploy"

**Method 3: Using provided script**

```bash
.\deploy-to-vercel.bat
```

### Post-Deployment Configuration

1. **Update Backend CORS:**
   - Add your Vercel URL to backend `ALLOWED_ORIGINS`
   - Format: `["https://your-project.vercel.app"]`
   - Redeploy backend

2. **Custom Domain (Optional):**
   - In Vercel dashboard, go to "Settings" > "Domains"
   - Add your domain: `yourdomain.com`
   - Follow DNS configuration:
     - A Record: `76.76.21.21`
     - CNAME: `cname.vercel-dns.com`
   - Wait for DNS propagation (up to 48 hours, usually minutes)

3. **Configure Redirects:**
   Add to `frontend/vercel.json`:
   ```json
   {
     "redirects": [
       {
         "source": "/",
         "has": [{"type": "host", "value": "www.yourdomain.com"}],
         "destination": "https://yourdomain.com",
         "permanent": true
       }
     ]
   }
   ```

---

## Domain & SSL Configuration

### SSL Certificates

Both Vercel and Railway provide automatic SSL certificates (Let's Encrypt).

**For Vercel:**
- Automatic for all deployments
- Custom domains get SSL within minutes

**For Railway:**
- Automatic for generated domains
- Custom domains: follow Railway's DNS instructions

### DNS Configuration

**If using custom domain:**

1. Purchase domain from:
   - Namecheap
   - GoDaddy
   - Google Domains
   - Cloudflare

2. Configure DNS:

**Frontend (Vercel):**
```
Type    Name    Value
A       @       76.76.21.21
CNAME   www     cname.vercel-dns.com
```

**Backend (Railway):**
```
Type    Name        Value
CNAME   api         your-app.railway.app
```

Then access:
- Frontend: `https://yourdomain.com`
- Backend: `https://api.yourdomain.com`

---

## Stripe Webhook Configuration

After deploying backend:

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter webhook URL:
   ```
   https://your-backend.railway.app/api/payments/webhook
   ```
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Click "Add endpoint"
6. Copy "Signing secret" (starts with `whsec_`)
7. Add to backend environment as `STRIPE_WEBHOOK_SECRET`
8. Redeploy backend

### Test Webhook

```bash
stripe listen --forward-to localhost:8000/api/payments/webhook

# In another terminal:
stripe trigger checkout.session.completed
```

---

## Monitoring & Logging

### Backend Monitoring

**Option 1: Built-in Platform Logs**
- Railway: View logs in dashboard
- Render: View logs in dashboard

**Option 2: Sentry (Recommended)**

1. Sign up at https://sentry.io
2. Create new project (Python/FastAPI)
3. Install SDK:
```bash
pip install sentry-sdk[fastapi]
```

4. Add to `backend/main.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

5. Add `SENTRY_DSN` to environment variables

### Frontend Monitoring

**Vercel Analytics (Built-in):**
- Automatically enabled
- View in Vercel dashboard

**Sentry for Frontend:**

1. Install:
```bash
npm install @sentry/nextjs
```

2. Run setup wizard:
```bash
npx @sentry/wizard@latest -i nextjs
```

3. Add `NEXT_PUBLIC_SENTRY_DSN` to environment

### Uptime Monitoring

**UptimeRobot (Free):**

1. Sign up at https://uptimerobot.com
2. Add monitors:
   - Frontend: `https://yourdomain.com`
   - Backend: `https://your-backend.railway.app/health`
3. Set up alerts (email, SMS, Slack)

---

## Security Checklist

- [ ] All `.env` files in `.gitignore`
- [ ] Strong JWT `SECRET_KEY` (64+ characters)
- [ ] Supabase RLS policies enabled
- [ ] CORS restricted to production domains only
- [ ] `DEBUG=false` in production backend
- [ ] HTTPS everywhere (no HTTP)
- [ ] Stripe webhook signature verification enabled
- [ ] Rate limiting configured (consider adding to FastAPI)
- [ ] Database backups enabled (Supabase does this automatically)
- [ ] Monitoring and alerting set up

---

## Performance Optimization

### Backend

1. **Enable Caching:**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Add Redis caching for frequent queries
```

2. **Database Connection Pooling:**
Already configured in Supabase client

3. **Async Operations:**
Already using `async/await` in FastAPI

### Frontend

1. **Image Optimization:**
Next.js automatically optimizes images with `next/image`

2. **Code Splitting:**
Automatically handled by Next.js

3. **CDN:**
Vercel provides global CDN automatically

---

## Troubleshooting

### Common Issues

**Issue: CORS Error**
```
Access to fetch at 'backend-url' from origin 'frontend-url' has been blocked by CORS policy
```
**Solution:**
- Check `ALLOWED_ORIGINS` in backend `.env`
- Must include your frontend URL exactly
- Restart backend after changes

**Issue: Supabase Connection Failed**
```
Failed to initialize Supabase client
```
**Solution:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check project is not paused (Supabase pauses inactive free projects)
- Verify RLS policies allow your operations

**Issue: Stripe Webhook Failing**
```
No signatures found matching the expected signature for payload
```
**Solution:**
- Verify `STRIPE_WEBHOOK_SECRET` is correct
- Check webhook URL is exactly: `https://your-backend/api/payments/webhook`
- Ensure backend is publicly accessible

**Issue: API Keys Invalid**
```
Invalid API key provided
```
**Solution:**
- Check for extra spaces or quotes in `.env` file
- Verify key is still active in provider dashboard
- Ensure you're using correct key type (secret vs publishable)

### Debug Mode

**Enable temporarily for troubleshooting:**

Backend `.env`:
```
DEBUG=true
```

This will show detailed error messages. **Disable in production!**

### Test Endpoints

```bash
# Backend health
curl https://your-backend.railway.app/health

# Backend API status
curl https://your-backend.railway.app/

# Test authentication
curl -X POST https://your-backend.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

---

## Scaling Considerations

### When to Scale

Monitor these metrics:
- Response time > 1 second
- CPU usage > 80%
- Memory usage > 80%
- Error rate > 1%

### How to Scale

**Horizontal Scaling (Multiple Instances):**
- Railway: Auto-scales with Pro plan
- Render: Add more instances in settings
- Docker: Use orchestration (Kubernetes, ECS)

**Vertical Scaling (Bigger Instance):**
- Railway: Upgrade RAM/CPU in settings
- Render: Choose larger instance type

**Database Scaling:**
- Supabase Pro: Connection pooling, read replicas
- Consider moving to dedicated Postgres for > 10k users

---

## Backup & Recovery

### Database Backups

**Supabase (Automatic):**
- Free tier: Daily backups (7 day retention)
- Pro tier: Point-in-time recovery

**Manual Backup:**
```bash
# Backup database
pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql

# Restore
psql -h db.xxx.supabase.co -U postgres -d postgres < backup.sql
```

### Code Backups

Use Git:
```bash
git push origin main  # Push to GitHub
```

Consider multiple remotes:
```bash
git remote add gitlab https://gitlab.com/user/repo.git
git push gitlab main
```

---

## Cost Optimization

### Free Tier Limits

| Service | Free Tier | When to Upgrade |
|---------|-----------|----------------|
| Vercel | 100GB bandwidth | > 1000 visitors/day |
| Railway | $5 credit/month | Using > 4GB RAM |
| Supabase | 500MB database | > 500MB data |
| Render | 750 hours/month | Need 100% uptime |

### Cost Reduction Tips

1. **Use Cloudflare** (free CDN/caching)
2. **Optimize images** (reduce bandwidth)
3. **Cache API responses** (reduce compute)
4. **Use connection pooling** (reduce DB connections)
5. **Implement rate limiting** (prevent abuse)

---

## Next Steps After Deployment

1. **Set up analytics** (Google Analytics, Plausible)
2. **Configure error tracking** (Sentry)
3. **Set up uptime monitoring** (UptimeRobot)
4. **Create documentation** for users
5. **Set up CI/CD** (GitHub Actions)
6. **Implement backup strategy**
7. **Plan scaling strategy**
8. **Get feedback** from beta users

---

## Support & Resources

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Next.js Docs:** https://nextjs.org/docs
- **Stripe Docs:** https://stripe.com/docs

---

**Last Updated:** 2025-10-29
**Version:** 1.0.0
