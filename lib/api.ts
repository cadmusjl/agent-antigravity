const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

export interface AgentRequest {
  task: string
  agent_type: 'content' | 'image' | 'link_in_bio' | 'storefront'
  parameters?: Record<string, any>
}

export interface VoiceRequest {
  audio_data: string
  agent_type: string
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(error.detail || 'Request failed')
    }

    return response.json()
  }

  // Agent endpoints
  async executeAgent(request: AgentRequest) {
    return this.request('/api/agents/execute', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async processVoice(request: VoiceRequest) {
    return this.request('/api/agents/voice', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async generateContent(topic: string, content_type = 'blog_post', tone = 'professional') {
    return this.request('/api/agents/content/generate', {
      method: 'POST',
      body: JSON.stringify({ topic, content_type, tone }),
    })
  }

  async generateImage(prompt: string, style = 'realistic', model = 'stable-diffusion') {
    return this.request('/api/agents/image/generate', {
      method: 'POST',
      body: JSON.stringify({ prompt, style, model }),
    })
  }

  async createLinkInBio(profile_data: any) {
    return this.request('/api/agents/link-in-bio/create', {
      method: 'POST',
      body: JSON.stringify(profile_data),
    })
  }

  async createStorefront(store_data: any) {
    return this.request('/api/agents/storefront/create', {
      method: 'POST',
      body: JSON.stringify(store_data),
    })
  }

  // Payment endpoints
  async createCheckoutSession(price_id: string, success_url: string, cancel_url: string): Promise<{ url: string }> {
    return this.request<{ url: string }>('/api/payments/create-checkout-session', {
      method: 'POST',
      body: JSON.stringify({ price_id, success_url, cancel_url }),
    })
  }

  async getPrices() {
    return this.request('/api/payments/prices')
  }
}

export const api = new ApiClient()
