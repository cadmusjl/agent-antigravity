'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { VoiceInput } from './VoiceInput'

export function AgentInterface() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const [contentTask, setContentTask] = useState({ topic: '', type: 'blog_post', tone: 'professional' })
  const [imageTask, setImageTask] = useState({ prompt: '', style: 'realistic' })

  const handleContentGeneration = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.generateContent(contentTask.topic, contentTask.type, contentTask.tone)
      setResult(response)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleImageGeneration = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.generateImage(imageTask.prompt, imageTask.style)
      setResult(response)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleVoiceInput = async (transcript: string, audioData: string) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.processVoice({
        audio_data: audioData,
        agent_type: 'content'
      })
      setResult(response)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>AI Agent Interface</CardTitle>
          <CardDescription>
            Use AI agents to generate content, create images, and build digital assets
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="content" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="content">Content</TabsTrigger>
              <TabsTrigger value="image">Images</TabsTrigger>
              <TabsTrigger value="link">Link-in-Bio</TabsTrigger>
              <TabsTrigger value="store">Storefront</TabsTrigger>
            </TabsList>

            <TabsContent value="content" className="space-y-4">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Topic</Label>
                  <Input
                    placeholder="Enter your topic..."
                    value={contentTask.topic}
                    onChange={(e) => setContentTask({ ...contentTask, topic: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Content Type</Label>
                    <select
                      className="w-full h-10 px-3 rounded-md border border-input bg-background"
                      value={contentTask.type}
                      onChange={(e) => setContentTask({ ...contentTask, type: e.target.value })}
                    >
                      <option value="blog_post">Blog Post</option>
                      <option value="social_media">Social Media</option>
                      <option value="email">Email</option>
                      <option value="product_description">Product Description</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <Label>Tone</Label>
                    <select
                      className="w-full h-10 px-3 rounded-md border border-input bg-background"
                      value={contentTask.tone}
                      onChange={(e) => setContentTask({ ...contentTask, tone: e.target.value })}
                    >
                      <option value="professional">Professional</option>
                      <option value="casual">Casual</option>
                      <option value="friendly">Friendly</option>
                      <option value="persuasive">Persuasive</option>
                    </select>
                  </div>
                </div>
                <Button onClick={handleContentGeneration} disabled={loading || !contentTask.topic}>
                  {loading ? 'Generating...' : 'Generate Content'}
                </Button>
              </div>

              <div className="pt-4">
                <VoiceInput onTranscript={handleVoiceInput} disabled={loading} />
              </div>
            </TabsContent>

            <TabsContent value="image" className="space-y-4">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Image Prompt</Label>
                  <Textarea
                    placeholder="Describe the image you want to create..."
                    value={imageTask.prompt}
                    onChange={(e) => setImageTask({ ...imageTask, prompt: e.target.value })}
                    rows={4}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Style</Label>
                  <select
                    className="w-full h-10 px-3 rounded-md border border-input bg-background"
                    value={imageTask.style}
                    onChange={(e) => setImageTask({ ...imageTask, style: e.target.value })}
                  >
                    <option value="realistic">Realistic</option>
                    <option value="artistic">Artistic</option>
                    <option value="minimalist">Minimalist</option>
                    <option value="vibrant">Vibrant</option>
                    <option value="professional">Professional</option>
                  </select>
                </div>
                <Button onClick={handleImageGeneration} disabled={loading || !imageTask.prompt}>
                  {loading ? 'Generating...' : 'Generate Image'}
                </Button>
              </div>
            </TabsContent>

            <TabsContent value="link" className="space-y-4">
              <div className="text-center py-8">
                <h3 className="text-lg font-semibold mb-2">Link-in-Bio Builder</h3>
                <p className="text-muted-foreground mb-4">
                  Create beautiful link-in-bio pages with AI assistance
                </p>
                <Badge variant="secondary">Coming Soon</Badge>
              </div>
            </TabsContent>

            <TabsContent value="store" className="space-y-4">
              <div className="text-center py-8">
                <h3 className="text-lg font-semibold mb-2">Storefront Builder</h3>
                <p className="text-muted-foreground mb-4">
                  Build complete digital storefronts powered by AI
                </p>
                <Badge variant="secondary">Coming Soon</Badge>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-600">{error}</p>
          </CardContent>
        </Card>
      )}

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Result</CardTitle>
          </CardHeader>
          <CardContent>
            {result.content && (
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap">{result.content}</pre>
              </div>
            )}
            {result.image_url && (
              <img src={result.image_url} alt="Generated" className="max-w-full rounded-lg" />
            )}
            {result.result && (
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap">{JSON.stringify(result.result, null, 2)}</pre>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
