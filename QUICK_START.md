# Quick Start - Get to Production in 60 Minutes

This is the fastest path to get your AI Agent SaaS Platform live in production.

---

## ⏱️ Timeline

- **15 min:** Get API keys
- **10 min:** Set up environment
- **10 min:** Set up database
- **15 min:** Deploy backend
- **10 min:** Deploy frontend
- **5 min:** Final configuration

**Total: ~60 minutes**

---

## Step 1: Get API Keys (15 min)

### Required (Must have):
1. **Supabase** (Free): https://supabase.com
   - Sign up → New Project → Copy URL and keys

2. **Stripe** (Free): https://stripe.com
   - Sign up → Get test keys from dashboard

3. **OpenAI** (Paid): https://platform.openai.com/api-keys
   - Sign up → Add payment method → Create API key

### Optional (Can add later):
4. **Anthropic** (Paid): https://console.anthropic.com
5. **Replicate** (Paid): https://replicate.com

---

## Step 2: Set Up Environment (10 min)

### Option A: Automatic (Easiest)
```bash
cd C:\Users\jason\agent-saas-platform
.\setup-environment.bat
```
Follow prompts and fill in your API keys.

### Option B: Manual

**Backend:** Create `backend\.env`:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbG...
SUPABASE_SERVICE_KEY=eyJhbG...
SECRET_KEY=<generate-random-64-chars>
STRIPE_SECRET_KEY=sk_test_...
ALLOWED_ORIGINS=["http://localhost:3000"]
DEBUG=false
```

**Frontend:** Create `frontend\.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Step 3: Set Up Database (10 min)

1. Go to your Supabase dashboard
2. Click **SQL Editor** → **New query**
3. Copy all contents from `backend\database_schema.sql`
4. Paste and click **Run**
5. ✅ Done! Tables created.

---

## Step 4: Deploy Backend (15 min)

### Railway (Recommended)

1. **Push to GitHub:**
```bash
cd C:\Users\jason\agent-saas-platform
git init
git add .
git commit -m "Initial commit"
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/agent-saas-platform.git
git push -u origin main
```

2. **Deploy to Railway:**
   - Go to https://railway.app
   - Sign up/Login
   - New Project → Deploy from GitHub
   - Select your repo
   - Select `backend` folder as root
   - Add all environment variables from `backend\.env`
   - Deploy!

3. **Copy your Railway URL:** `https://xxx.railway.app`

---

## Step 5: Deploy Frontend (10 min)

### Vercel (Recommended)

**Method 1: CLI (Fastest)**
```bash
npm install -g vercel
cd C:\Users\jason\agent-saas-platform\frontend
vercel login
vercel --prod
```

**Method 2: Dashboard**
1. Go to https://vercel.com
2. New Project → Import from GitHub
3. Select your repo
4. Set Root Directory: `frontend`
5. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
   - `NEXT_PUBLIC_API_URL` (your Railway URL)
6. Deploy!

---

## Step 6: Final Configuration (5 min)

### 1. Update Backend CORS
In Railway dashboard:
- Go to Variables
- Update `ALLOWED_ORIGINS` to include your Vercel URL:
  ```
  ["https://your-project.vercel.app"]
  ```
- Redeploy

### 2. Set Up Stripe Webhook
1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://your-backend.railway.app/api/payments/webhook`
3. Select events: `checkout.session.completed`, `customer.subscription.*`
4. Copy webhook secret
5. Add to Railway: `STRIPE_WEBHOOK_SECRET=whsec_...`
6. Redeploy

### 3. Update Frontend API URL (if needed)
In Vercel dashboard:
- Settings → Environment Variables
- Update `NEXT_PUBLIC_API_URL` to your Railway URL
- Redeploy

---

## ✅ Test Your Deployment

1. **Frontend:** Open your Vercel URL
2. **Sign up** for a new account
3. **Create an agent**
4. **Run a test task**
5. **Try Stripe checkout** (use test card: 4242 4242 4242 4242)

---

## 🎉 You're Live!

Your URLs:
- **Frontend:** https://your-project.vercel.app
- **Backend:** https://your-backend.railway.app
- **API Docs:** https://your-backend.railway.app/docs

---

## Next Steps

1. **Add custom domain** (optional)
2. **Switch Stripe to live mode** (when ready for real payments)
3. **Set up monitoring** (Sentry, UptimeRobot)
4. **Add more AI providers** (Anthropic, Replicate)
5. **Customize branding**

---

## Need Help?

- **Detailed Guide:** See `DEPLOYMENT_GUIDE.md`
- **Action Items:** See `USER_ACTION_ITEMS.md`
- **Check Status:** Run `.\check-deployment-readiness.bat`

---

## Common Issues

**"CORS Error"**
→ Check `ALLOWED_ORIGINS` in backend includes your frontend URL

**"Supabase Error"**
→ Verify database schema is set up and RLS policies are enabled

**"API Key Invalid"**
→ Check for extra spaces in `.env` files

**"Webhook Failed"**
→ Ensure webhook URL is correct and backend is accessible

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| Vercel (Frontend) | Free |
| Railway (Backend) | $5/month |
| Supabase (Database) | Free |
| Stripe (Payments) | 2.9% + $0.30 per transaction |
| OpenAI (Usage) | ~$0.03 per 1K tokens |
| **Total Fixed:** | **$5/month** |

---

**Ready to deploy? Start with Step 1! ⬆️**
