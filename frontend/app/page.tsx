'use client'

import { useAuth } from '@/hooks/useAuth'
import { AuthForm } from '@/components/auth/AuthForm'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { isSupabaseConfigured } from '@/lib/supabase'

export default function Home() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Agent Platform
          </h1>
          <p className="text-xl text-muted-foreground">
            Create content, generate images, and build digital assets with AI
          </p>
        </div>

        {!isSupabaseConfigured && (
          <div className="mb-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start gap-3">
              <span className="text-2xl">⚠️</span>
              <div className="flex-1">
                <h3 className="font-semibold text-yellow-900 mb-1">Setup Required</h3>
                <p className="text-sm text-yellow-800 mb-2">
                  Supabase is not configured. Authentication features won't work until you set up your environment variables.
                </p>
                <div className="text-xs text-yellow-700 bg-yellow-100 p-2 rounded font-mono">
                  <p>1. Create a Supabase account at https://supabase.com</p>
                  <p>2. Create a new project</p>
                  <p>3. Copy your project URL and anon key from Settings → API</p>
                  <p>4. Update frontend/.env.local with your keys</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <AuthForm />

        <div className="mt-16 grid md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-4xl mb-2">✍️</div>
            <h3 className="font-semibold mb-2">Content Generation</h3>
            <p className="text-sm text-muted-foreground">
              Create blog posts, social media content, and marketing copy with AI
            </p>
          </div>
          <div>
            <div className="text-4xl mb-2">🎨</div>
            <h3 className="font-semibold mb-2">Image Creation</h3>
            <p className="text-sm text-muted-foreground">
              Generate stunning images with Stable Diffusion and DALL-E
            </p>
          </div>
          <div>
            <div className="text-4xl mb-2">🚀</div>
            <h3 className="font-semibold mb-2">Digital Assets</h3>
            <p className="text-sm text-muted-foreground">
              Build link-in-bio pages and digital storefronts instantly
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
