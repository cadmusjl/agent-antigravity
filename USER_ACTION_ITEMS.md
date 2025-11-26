# YOUR ACTION ITEMS - Production Deployment Checklist

This document contains the **manual steps YOU need to complete** to deploy the AI Agent SaaS Platform to production. Follow these steps in order.

---

## 📋 PHASE 1: GET API KEYS & ACCOUNTS (30-60 minutes)

### 1. Create Supabase Account & Project
**What:** Database, authentication, and storage for your platform
**Where:** https://supabase.com
**How:**
1. Sign up for a free account at https://supabase.com
2. Click "New Project"
3. Choose organization (or create new one)
4. Name your project: "agent-saas-platform" (or your choice)
5. Choose a database password (SAVE THIS!)
6. Select region closest to your users
7. Wait for project to provision (~2 minutes)

**What to copy:**
- Go to: Project Settings > API
- Copy `Project URL` → You'll need this as `SUPABASE_URL`
- Copy `anon public` key → You'll need this as `SUPABASE_ANON_KEY`
- Copy `service_role` key → You'll need this as `SUPABASE_SERVICE_KEY` (keep secret!)

**Cost:** Free tier (up to 500MB database, 50,000 monthly active users)

---

### 2. Create OpenAI Account & API Key
**What:** Powers AI agents with GPT models
**Where:** https://platform.openai.com
**How:**
1. Sign up at https://platform.openai.com/signup
2. Add payment method (required for API access)
3. Go to: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Name it: "agent-saas-production"
6. Copy the key (starts with `sk-...`)
7. SAVE IT NOW - you can't view it again!

**What to copy:**
- API Key → You'll need this as `OPENAI_API_KEY`

**Cost:** Pay-as-you-go (GPT-4: ~$0.03/1K tokens, GPT-3.5: ~$0.002/1K tokens)

---

### 3. Create Anthropic Account & API Key
**What:** Powers AI agents with Claude models
**Where:** https://console.anthropic.com
**How:**
1. Sign up at https://console.anthropic.com
2. Go to: Settings > API Keys
3. Click "Create Key"
4. Name it: "agent-saas-production"
5. Copy the key (starts with `sk-ant-...`)

**What to copy:**
- API Key → You'll need this as `ANTHROPIC_API_KEY`

**Cost:** Pay-as-you-go (Claude 3.5: ~$0.003/1K tokens)

---

### 4. Create Stripe Account & API Keys
**What:** Payment processing for subscriptions
**Where:** https://stripe.com
**How:**
1. Sign up at https://stripe.com
2. Complete business verification (required for live mode)
3. Go to: https://dashboard.stripe.com/apikeys
4. **For Testing:**
   - Copy "Publishable key" (starts with `pk_test_...`)
   - Click "Reveal test key" for Secret key (starts with `sk_test_...`)
5. **For Production (after testing):**
   - Toggle to "Live mode" in Stripe dashboard
   - Copy Live "Publishable key" (starts with `pk_live_...`)
   - Copy Live "Secret key" (starts with `sk_live_...`)

**What to copy:**
- Publishable Key → You'll need this as `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- Secret Key → You'll need this as `STRIPE_SECRET_KEY`

**Webhook Setup (do this after deployment):**
1. Go to: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter: `https://your-backend-domain.com/api/payments/webhook`
4. Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
5. Copy the Webhook signing secret → You'll need this as `STRIPE_WEBHOOK_SECRET`

**Cost:** 2.9% + $0.30 per transaction

---

### 5. Create Replicate Account & API Token (Optional)
**What:** AI image generation models
**Where:** https://replicate.com
**How:**
1. Sign up at https://replicate.com
2. Go to: https://replicate.com/account/api-tokens
3. Copy your API token

**What to copy:**
- API Token → You'll need this as `REPLICATE_API_TOKEN`

**Cost:** Pay-as-you-go (varies by model, ~$0.002-0.01 per image)

---

### 6. Generate JWT Secret Key
**What:** Secure token for user authentication
**Where:** Your computer
**How:**
```bash
# On Windows (PowerShell):
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# OR use an online generator:
# https://generate-secret.vercel.app/64
```

**What to copy:**
- Generated string → You'll need this as `SECRET_KEY`

**Cost:** Free

---

## 📝 PHASE 2: CONFIGURE ENVIRONMENT VARIABLES (15 minutes)

### Backend Environment Variables

1. Navigate to `C:\Users\jason\agent-saas-platform\backend`
2. Create a file named `.env` (no extension before the dot)
3. Open it and paste this template:

```env
# App Configuration
APP_NAME="AI Agent SaaS Platform"
APP_VERSION="1.0.0"
DEBUG=false

# AI Model API Keys
OPENAI_API_KEY=sk-...your-openai-key...
ANTHROPIC_API_KEY=sk-ant-...your-anthropic-key...
REPLICATE_API_TOKEN=r8_...your-replicate-token...
STABILITY_API_KEY=sk-...your-stability-key...(optional)

# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbG...your-anon-key...
SUPABASE_SERVICE_KEY=eyJhbG...your-service-key...

# JWT Configuration
SECRET_KEY=your-64-character-random-secret-from-step-6
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...or-sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...(get this after deployment)

# CORS - Add your production domain
ALLOWED_ORIGINS=["https://yourdomain.com","http://localhost:3000"]
```

4. Replace ALL placeholder values with your actual keys from Phase 1

---

### Frontend Environment Variables

1. Navigate to `C:\Users\jason\agent-saas-platform\frontend`
2. Create/edit `.env.local` file
3. Paste this template:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...your-anon-key...

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...or-pk_live_...

# Backend API - UPDATE THIS AFTER DEPLOYING BACKEND
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Replace placeholder values with your actual keys
5. **IMPORTANT:** You'll update `NEXT_PUBLIC_API_URL` after deploying the backend (Phase 3)

---

## 🗄️ PHASE 3: SET UP SUPABASE DATABASE (10 minutes)

### Create Database Tables

1. Go to your Supabase project dashboard
2. Click "SQL Editor" in left sidebar
3. Click "New query"
4. Paste the SQL schema from `backend/database_schema.sql` (if it exists)
   - OR use the schema in `DEPLOYMENT_GUIDE.md`
5. Click "Run"
6. Verify tables were created: Go to "Table Editor" tab

### Enable Row Level Security (RLS)

1. In Supabase dashboard, go to "Authentication" > "Policies"
2. For each table, enable RLS and add appropriate policies
3. See `DEPLOYMENT_GUIDE.md` for specific policy configurations

---

## 🚀 PHASE 4: DEPLOY TO PRODUCTION (30 minutes)

### Option A: Deploy Frontend to Vercel (Recommended - Easiest)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy frontend:
```bash
cd C:\Users\jason\agent-saas-platform\frontend
vercel
```

4. Follow prompts:
   - Link to existing project? **No**
   - Project name? **agent-saas-platform** (or your choice)
   - Which directory? **Press Enter** (current directory)
   - Override settings? **No**

5. Add environment variables in Vercel dashboard:
   - Go to: https://vercel.com/dashboard
   - Select your project
   - Go to Settings > Environment Variables
   - Add each variable from your `.env.local`:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
     - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
     - `NEXT_PUBLIC_API_URL` (update this after backend deployment)

6. Copy your Vercel URL: `https://your-project.vercel.app`

**Cost:** Free tier (100GB bandwidth, unlimited deployments)

---

### Option B: Deploy Backend to Railway (Recommended for Backend)

1. Sign up at https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo" (or "Empty Project")
4. Connect your GitHub account (if using GitHub)
   - Push your code to GitHub first
   - OR use Railway CLI for local deploy

**Using Railway Dashboard:**
1. Click "New" > "GitHub Repo"
2. Select your repository
3. Select `backend` folder as root directory
4. Add environment variables:
   - Click "Variables" tab
   - Add all variables from your backend `.env` file
5. Railway will auto-detect Python and deploy
6. Copy your Railway URL: `https://your-app.railway.app`

**Cost:** $5/month (includes $5 credit)

---

### Alternative Backend Deployment Options

**Option C: Render.com**
- Free tier available (spins down after inactivity)
- Good for testing
- https://render.com

**Option D: Heroku**
- $7/month minimum
- Very reliable
- https://heroku.com

**Option E: AWS/GCP/Azure**
- Most control but requires more setup
- Use provided Docker configurations

---

## 🔗 PHASE 5: CONNECT FRONTEND TO BACKEND (5 minutes)

1. After backend is deployed, copy your backend URL
2. Update frontend environment variable:
   - **Vercel:**
     - Go to Vercel dashboard > Settings > Environment Variables
     - Update `NEXT_PUBLIC_API_URL` to your backend URL
     - Redeploy: `vercel --prod`
   - **Local .env.local:**
     - Update `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`

3. Update backend CORS:
   - In backend `.env` file (or Railway environment variables)
   - Update `ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]`
   - Redeploy backend

---

## ✅ PHASE 6: FINALIZE STRIPE WEBHOOK (5 minutes)

1. Go to Stripe Dashboard: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter URL: `https://your-backend.railway.app/api/payments/webhook`
4. Select events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Click "Add endpoint"
6. Copy the "Signing secret" (starts with `whsec_...`)
7. Add to backend environment:
   - Railway: Add `STRIPE_WEBHOOK_SECRET` variable
   - Redeploy backend

---

## 🧪 PHASE 7: TEST YOUR PRODUCTION DEPLOYMENT (15 minutes)

### Test Checklist:
- [ ] Frontend loads at your Vercel URL
- [ ] Can create a new account
- [ ] Can login
- [ ] Backend API responds (check: `https://your-backend.railway.app/health`)
- [ ] Can create an AI agent
- [ ] Can run an AI agent task
- [ ] Stripe checkout works (use test card: 4242 4242 4242 4242)
- [ ] Webhook receives Stripe events

---

## 📊 PHASE 8: SET UP MONITORING (Optional but Recommended)

### 1. Set up Sentry for Error Tracking
- Sign up at https://sentry.io
- Add Sentry DSN to environment variables
- Install Sentry SDK in frontend and backend

### 2. Set up Uptime Monitoring
- Use UptimeRobot (free): https://uptimerobot.com
- Monitor both frontend and backend URLs
- Get alerts if site goes down

---

## 🎉 YOU'RE DONE!

Your production URLs:
- **Frontend:** https://your-project.vercel.app
- **Backend:** https://your-backend.railway.app

---

## 📞 NEED HELP?

**Common Issues:**
1. **"CORS Error"** - Check `ALLOWED_ORIGINS` in backend .env includes your frontend URL
2. **"API Key Invalid"** - Double-check keys in environment variables (no quotes, no extra spaces)
3. **"Database Error"** - Verify Supabase credentials and that tables are created
4. **"Webhook Not Working"** - Check webhook URL is correct and endpoint is accessible

**Quick Test Commands:**
```bash
# Test backend health
curl https://your-backend.railway.app/health

# Test backend API
curl https://your-backend.railway.app/api/health
```

---

## 💰 TOTAL ESTIMATED MONTHLY COSTS

| Service | Free Tier | Paid Plan |
|---------|-----------|-----------|
| Vercel (Frontend) | ✅ Free | $20/month (Pro) |
| Railway (Backend) | $5 credit/month | $5-20/month |
| Supabase | ✅ Free (500MB) | $25/month (Pro) |
| OpenAI | Pay-per-use | ~$10-100/month |
| Anthropic | Pay-per-use | ~$10-100/month |
| Stripe | Transaction fees only | 2.9% + $0.30/transaction |
| Replicate | Pay-per-use | ~$5-50/month |

**Estimated Starting Cost:** $5-20/month + usage-based AI costs

---

## 🔐 SECURITY CHECKLIST BEFORE LAUNCH

- [ ] All `.env` files are in `.gitignore` (never commit secrets!)
- [ ] Using strong JWT SECRET_KEY (64+ random characters)
- [ ] Stripe is in live mode (not test mode)
- [ ] Supabase RLS policies are enabled
- [ ] CORS only allows your production domain
- [ ] DEBUG=false in production backend
- [ ] Using HTTPS everywhere (no HTTP)
