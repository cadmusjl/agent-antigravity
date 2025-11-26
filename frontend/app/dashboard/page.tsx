'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { AgentInterface } from '@/components/dashboard/AgentInterface'
import { PricingCard } from '@/components/payments/PricingCard'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function Dashboard() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/')
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

  if (!user) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold mb-2">Welcome back!</h1>
          <p className="text-muted-foreground">
            Use AI agents to create amazing content and digital assets
          </p>
        </div>

        <Tabs defaultValue="agents" className="w-full">
          <TabsList>
            <TabsTrigger value="agents">AI Agents</TabsTrigger>
            <TabsTrigger value="pricing">Pricing</TabsTrigger>
            <TabsTrigger value="stats">Statistics</TabsTrigger>
          </TabsList>

          <TabsContent value="agents" className="space-y-4">
            <AgentInterface />
          </TabsContent>

          <TabsContent value="pricing" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Upgrade Your Plan</CardTitle>
                <CardDescription>
                  Choose a plan that fits your needs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <PricingCard />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="stats" className="space-y-4">
            <div className="grid md:grid-cols-3 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>Content Generated</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-4xl font-bold">0</p>
                  <p className="text-sm text-muted-foreground">this month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Images Created</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-4xl font-bold">0</p>
                  <p className="text-sm text-muted-foreground">this month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Digital Assets</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-4xl font-bold">0</p>
                  <p className="text-sm text-muted-foreground">created</p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}
