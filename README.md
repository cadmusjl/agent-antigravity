# AI Agent SaaS Platform

A full-stack AI-powered SaaS platform for content creation, image generation, and building digital assets. Built with Next.js, FastAPI, and multiple AI models (Claude 3, GPT-4, Stable Diffusion).

## 🚀 Ready to Deploy?

**Get to production fast:**
- **[QUICK_START.md](QUICK_START.md)** - Deploy in 60 minutes
- **[USER_ACTION_ITEMS.md](USER_ACTION_ITEMS.md)** - Your complete deployment checklist
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Detailed technical guide

**Helper Scripts:**
- `setup-environment.bat` - Automatic environment setup
- `check-deployment-readiness.bat` - Verify you're ready to deploy
- `deploy-to-vercel.bat` - One-click frontend deployment

## Features

- **Content Generation**: Create blog posts, social media content, emails, and product descriptions using Claude 3 and GPT-4
- **Image Generation**: Generate AI images with Stable Diffusion and DALL-E
- **Link-in-Bio Builder**: Create beautiful link-in-bio pages with AI assistance
- **Storefront Builder**: Build complete digital storefronts powered by AI
- **Multi-modal Interface**: Text and voice input support (Whisper integration)
- **Authentication**: Secure auth with Supabase
- **Payments**: Stripe integration for subscriptions
- **Beautiful UI**: Modern interface with shadcn/ui and Framer Motion

## Tech Stack

### Frontend
- **Next.js 16** with App Router
- **TypeScript**
- **TailwindCSS**
- **shadcn/ui** components
- **Framer Motion** for animations
- **Supabase** for auth and database
- **Stripe** for payments

### Backend
- **FastAPI** (Python)
- **CrewAI** for agent orchestration
- **LangChain** and **LangGraph** for AI workflows
- **Multiple AI Models**:
  - Anthropic Claude 3 (Sonnet)
  - OpenAI GPT-4o
  - Stable Diffusion XL
  - OpenAI Whisper (voice)

### Database & Services
- **Supabase** (PostgreSQL + Auth)
- **Stripe** for payments
- **Replicate** for image generation

## Quick Start

### Prerequisites

- Node.js 22+ and npm
- Python 3.13+
- Supabase account
- API keys for:
  - OpenAI
  - Anthropic
  - Replicate
  - Stability AI (optional)
  - Stripe

### 1. Clone and Setup

```bash
cd agent-saas-platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local and add your API keys
```

### 4. Environment Variables

#### Backend (.env)

```env
# AI Model API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
REPLICATE_API_TOKEN=your_replicate_token
STABILITY_API_KEY=your_stability_key

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Stripe
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

# JWT
SECRET_KEY=your_secret_key_change_in_production
```

#### Frontend (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Run the Application

#### Start Backend

```bash
cd backend
python main.py
# API will run on http://localhost:8000
```

#### Start Frontend

```bash
cd frontend
npm run dev
# App will run on http://localhost:3000
```

## Usage

1. **Sign Up**: Create an account at http://localhost:3000
2. **Generate Content**: Navigate to the AI Agents tab and select Content
3. **Create Images**: Use the Images tab to generate AI images
4. **Voice Input**: Click the microphone icon to use voice commands
5. **Upgrade Plan**: Visit the Pricing tab to subscribe

## Project Structure

```
agent-saas-platform/
├── frontend/                 # Next.js frontend
│   ├── app/                 # App router pages
│   │   ├── page.tsx        # Landing page
│   │   └── dashboard/      # Dashboard pages
│   ├── components/          # React components
│   │   ├── auth/           # Auth components
│   │   ├── dashboard/      # Dashboard components
│   │   ├── payments/       # Stripe components
│   │   └── ui/             # shadcn/ui components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities
│   │   ├── api.ts         # API client
│   │   └── supabase.ts    # Supabase client
│   └── package.json
│
└── backend/                 # FastAPI backend
    ├── main.py             # FastAPI entry point
    ├── config.py           # Configuration
    ├── requirements.txt    # Python dependencies
    ├── api/                # API routes
    │   ├── auth.py        # Authentication
    │   ├── agents.py      # Agent endpoints
    │   └── payments.py    # Stripe integration
    └── agents/             # AI agent logic
        ├── orchestrator.py # Agent orchestrator
        └── tools/          # Agent tools
            ├── content_generation.py
            ├── image_creation.py
            ├── link_in_bio_builder.py
            └── storefront_builder.py
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/signin` - Sign in
- `POST /api/auth/signout` - Sign out
- `GET /api/auth/user` - Get current user

### AI Agents
- `POST /api/agents/execute` - Execute generic agent task
- `POST /api/agents/voice` - Process voice input
- `POST /api/agents/content/generate` - Generate content
- `POST /api/agents/image/generate` - Generate image
- `POST /api/agents/link-in-bio/create` - Create link-in-bio page
- `POST /api/agents/storefront/create` - Create storefront

### Payments
- `POST /api/payments/create-checkout-session` - Create Stripe session
- `POST /api/payments/create-portal-session` - Customer portal
- `GET /api/payments/prices` - Get pricing plans
- `POST /api/payments/webhook` - Stripe webhooks

## Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run type-check   # Run TypeScript checks
```

### Backend Development

```bash
cd backend
uvicorn main:app --reload  # Auto-reload on changes
```

## Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel
```

### Backend

Deploy to any Python hosting service:
- Railway
- Render
- AWS Lambda
- Google Cloud Run

## Features Roadmap

- [x] Content generation
- [x] Image generation
- [x] Voice input
- [x] Authentication
- [x] Stripe integration
- [ ] Link-in-bio builder UI
- [ ] Storefront builder UI
- [ ] User analytics dashboard
- [ ] Template marketplace
- [ ] Team collaboration
- [ ] API rate limiting
- [ ] Advanced image editing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For support, email support@example.com or open an issue on GitHub.

## Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- AI powered by [Anthropic Claude](https://anthropic.com/), [OpenAI](https://openai.com/), and [Stability AI](https://stability.ai/)
- Agent framework by [CrewAI](https://crewai.com/) and [LangChain](https://langchain.com/)
