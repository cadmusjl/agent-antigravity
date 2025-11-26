'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface PricingPlan {
  id: string
  name: string
  price: number
  interval: string
  features: string[]
  popular?: boolean
}

const plans: PricingPlan[] = [
  {
    id: 'starter',
    name: 'Starter',
    price: 29,
    interval: 'month',
    features: [
      '100 AI generations/month',
      'Content & image creation',
      'Basic templates',
      'Email support'
    ]
  },
  {
    id: 'pro',
    name: 'Professional',
    price: 79,
    interval: 'month',
    popular: true,
    features: [
      'Unlimited AI generations',
      'All content & image tools',
      'Link-in-bio builder',
      'Storefront builder',
      'Priority support',
      'Custom branding'
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 199,
    interval: 'month',
    features: [
      'Everything in Pro',
      'Dedicated account manager',
      'Custom AI training',
      'API access',
      'White-label solution',
      'SLA guarantee'
    ]
  }
]

export function PricingCard() {
  const [loading, setLoading] = useState<string | null>(null)

  const handleSubscribe = async (priceId: string) => {
    setLoading(priceId)

    try {
      const { url } = await api.createCheckoutSession(
        priceId,
        `${window.location.origin}/dashboard?success=true`,
        `${window.location.origin}/dashboard?canceled=true`
      )

      if (url) {
        window.location.href = url
      }
    } catch (error) {
      console.error('Subscription error:', error)
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
      {plans.map((plan) => (
        <Card key={plan.id} className={plan.popular ? 'border-blue-500 shadow-lg' : ''}>
          <CardHeader>
            {plan.popular && (
              <Badge className="w-fit mb-2" variant="default">
                Most Popular
              </Badge>
            )}
            <CardTitle>{plan.name}</CardTitle>
            <CardDescription>
              <span className="text-3xl font-bold text-foreground">${plan.price}</span>
              <span className="text-muted-foreground">/{plan.interval}</span>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {plan.features.map((feature, index) => (
                <li key={index} className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span className="text-sm">{feature}</span>
                </li>
              ))}
            </ul>
          </CardContent>
          <CardFooter>
            <Button
              className="w-full"
              variant={plan.popular ? 'default' : 'outline'}
              onClick={() => handleSubscribe(plan.id)}
              disabled={loading === plan.id}
            >
              {loading === plan.id ? 'Loading...' : 'Get Started'}
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
