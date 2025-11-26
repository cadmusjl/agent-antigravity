# Setup Instructions - Fix the Errors

## Issues Fixed

✅ **Fixed NextAuth middleware error** - Replaced with Supabase-compatible middleware
✅ **Fixed Supabase environment error** - Created .env.local with placeholders
✅ **Added graceful error handling** - App will start even without API keys
✅ **Added helpful warnings** - Clear messages about what's missing

## Current Status

The app will now **start without errors**, but you need to configure your API keys for full functionality.

## Quick Fix - Get the App Running

The app should now start successfully:

```bash
cd frontend
npm run dev
```

You'll see the landing page at http://localhost:3000 with a warning banner about Supabase configuration.

## Step-by-Step Setup

### 1. Set Up Supabase (Required for Auth)

**a) Create a Supabase Account**
- Go to https://supabase.com
- Click "Start your project"
- Sign up with GitHub/email

**b) Create a New Project**
- Click "New Project"
- Choose an organization (create one if needed)
- Fill in:
  - Project name: `ai-agent-platform` (or any name)
  - Database password: (save this securely)
  - Region: Choose closest to you
- Click "Create new project"
- Wait 2-3 minutes for setup

**c) Get Your API Keys**
- Once project is ready, go to Settings (gear icon)
- Click "API" in the left sidebar
- You'll see:
  - **Project URL**: `https://xxxxx.supabase.co`
  - **anon public key**: `eyJhbGc...` (long string)

**d) Update Frontend Environment**

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-actual-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...your-actual-anon-key...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-publishable-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**e) Restart the Dev Server**

```bash
# Stop the server (Ctrl+C)
npm run dev
```

The warning banner should now disappear, and auth will work!

### 2. Set Up Backend API Keys (Required for AI Features)

**a) Get OpenAI API Key**
- Go to https://platform.openai.com
- Sign up/login
- Go to API Keys section
- Click "Create new secret key"
- Copy the key (starts with `sk-`)
- **Note**: This requires adding a payment method ($5-10 minimum)

**b) Get Anthropic API Key (Optional but Recommended)**
- Go to https://console.anthropic.com
- Sign up/login
- Go to API Keys
- Create a new key
- Copy the key (starts with `sk-ant-`)

**c) Get Replicate API Token (Optional - for image generation)**
- Go to https://replicate.com
- Sign up/login
- Go to Account → API Tokens
- Copy your token

**d) Update Backend Environment**

Edit `backend/.env`:

```env
# Required
OPENAI_API_KEY=sk-your-actual-openai-key
SUPABASE_URL=https://your-actual-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-role-key

# Optional but recommended
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key
REPLICATE_API_TOKEN=r8_your-actual-replicate-token

# Optional
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
STABILITY_API_KEY=sk-your-stability-key

# App config
SECRET_KEY=your-random-secret-key-for-jwt
```

**e) Start the Backend**

```bash
cd backend
python main.py
```

### 3. Set Up Stripe (Optional - for payments)

**a) Create Stripe Account**
- Go to https://stripe.com
- Sign up for an account

**b) Get Test API Keys**
- Go to Developers → API Keys
- Toggle to "Test mode" (top right)
- Copy:
  - **Publishable key**: `pk_test_...`
  - **Secret key**: `sk_test_...`

**c) Update Environment Files**

Frontend `.env.local`:
```env
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-key
```

Backend `.env`:
```env
STRIPE_SECRET_KEY=sk_test_your-key
```

## Testing the Setup

### 1. Test Frontend (Without Backend)

```bash
cd frontend
npm run dev
```

Visit http://localhost:3000
- ✅ Page loads without errors
- ✅ No warning banner (if Supabase configured)
- ✅ Can try to sign up (will work with Supabase)

### 2. Test Backend

```bash
cd backend
python main.py
```

Visit http://localhost:8000/docs
- ✅ API documentation loads
- ✅ Can see all endpoints

### 3. Test Full Integration

With both frontend and backend running:

1. **Test Auth:**
   - Go to http://localhost:3000
   - Click "Sign Up" tab
   - Create an account
   - Should redirect to dashboard

2. **Test Content Generation:**
   - In dashboard, go to "AI Agents" tab
   - Select "Content" tab
   - Enter a topic
   - Click "Generate Content"
   - Should see AI-generated content

3. **Test Image Generation:**
   - Select "Images" tab
   - Enter a prompt
   - Click "Generate Image"
   - Should see generated image

## Minimum Setup for Testing

If you just want to see the app running:

**Minimum Required:**
- ✅ Supabase URL + key (for auth only)
- ✅ No backend needed initially

**Add AI Features:**
- ✅ OpenAI API key (for content + images via DALL-E)

**Full Features:**
- ✅ All the above
- ✅ Anthropic key (better content with Claude)
- ✅ Replicate token (better images with Stable Diffusion)
- ✅ Stripe keys (for payments)

## Common Issues

### "Module not found: next-auth/jwt"
✅ **Fixed!** The middleware now uses Supabase instead of NextAuth.

### "supabaseUrl is required"
✅ **Fixed!** The app now uses placeholder values and shows a helpful warning.

### Frontend won't start
```bash
# Clear cache and reinstall
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Backend won't start
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
python main.py
```

### Auth not working
- Check that Supabase keys are correctly set in `.env.local`
- Keys should NOT have quotes around them
- Restart the dev server after changing .env

### AI features not working
- Check that OpenAI/Anthropic keys are set in `backend/.env`
- Make sure backend is running on port 8000
- Check browser console for errors

## Cost Estimates

### Free Tier (Testing)
- Supabase: Free (up to 500MB database)
- Stripe: Free (test mode)
- **Total: $0/month**

### With AI (Light Usage)
- OpenAI: ~$5-10/month
- Anthropic: ~$5-10/month
- Replicate: ~$5/month
- **Total: ~$15-25/month**

## Next Steps

1. ✅ Get app running with Supabase
2. ✅ Add OpenAI key for AI features
3. ✅ Test content and image generation
4. ✅ (Optional) Add Stripe for payments
5. ✅ (Optional) Deploy to production

## Getting Help

- Check the browser console for errors
- Check the terminal for backend errors
- Read QUICKSTART.md for quick reference
- Read README.md for full documentation

## Success Checklist

- [ ] Frontend starts without errors
- [ ] Can see landing page
- [ ] Supabase warning banner gone (after setup)
- [ ] Can sign up for account
- [ ] Backend API docs load at /docs
- [ ] Can generate content
- [ ] Can generate images
- [ ] Dashboard shows all features

You're all set! 🚀
