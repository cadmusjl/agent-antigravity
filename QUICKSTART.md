# Quick Start Guide

## Setup in 5 Minutes

### 1. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Configure Environment Variables

**Backend** - Create `backend/.env`:
```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
STRIPE_SECRET_KEY=sk_test_your-key
```

**Frontend** - Create `frontend/.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Essential API Keys

### Required (Get Started)
1. **Supabase** (Free): https://supabase.com
   - Create a project
   - Copy URL and anon key from Settings > API

2. **OpenAI** (Paid): https://platform.openai.com
   - Get API key from API Keys section
   - Used for GPT-4 and Whisper

### Optional (Enhanced Features)
3. **Anthropic** (Paid): https://console.anthropic.com
   - Get API key for Claude 3

4. **Replicate** (Paid): https://replicate.com
   - Get API token for Stable Diffusion

5. **Stripe** (Free in test mode): https://stripe.com
   - Get test keys from Developers > API Keys

## Testing Without Full Setup

### Minimum Setup (Auth Only)
If you just want to test the auth system:
- Only set up Supabase keys
- Comment out AI features in code

### Content Generation Only
- OpenAI or Anthropic API key
- Supabase for auth

### Full Features
- All API keys above

## Common Issues

**Backend won't start?**
- Check Python version: `python --version` (need 3.13+)
- Install missing packages: `pip install -r requirements.txt`

**Frontend build errors?**
- Check Node version: `node --version` (need 22+)
- Clear cache: `rm -rf .next node_modules && npm install`

**Can't connect to backend?**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/config.py`

**Supabase auth not working?**
- Verify URL and anon key in both .env files
- Check Supabase project is active

## Next Steps

1. Sign up at http://localhost:3000
2. Try content generation in Dashboard > AI Agents
3. Test voice input (requires microphone permission)
4. Explore the API at http://localhost:8000/docs

## Getting Help

- Check README.md for detailed documentation
- Review backend/main.py for API endpoints
- Frontend components in frontend/components/

Enjoy building with AI! 🚀
