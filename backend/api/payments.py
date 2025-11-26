from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import stripe
from config import settings

router = APIRouter()

# Initialize Stripe
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str


class CreatePortalSessionRequest(BaseModel):
    customer_id: str
    return_url: str


@router.post("/create-checkout-session")
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """Create a Stripe checkout session"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": request.price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=request.success_url,
            cancel_url=request.cancel_url,
        )
        return {"sessionId": session.id, "url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-portal-session")
async def create_portal_session(request: CreatePortalSessionRequest):
    """Create a Stripe customer portal session"""
    try:
        session = stripe.billing_portal.Session.create(
            customer=request.customer_id,
            return_url=request.return_url,
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        if not settings.STRIPE_WEBHOOK_SECRET:
            raise HTTPException(status_code=500, detail="Webhook secret not configured")

        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # Handle successful payment
            print(f"Payment successful for session: {session.id}")

        elif event["type"] == "customer.subscription.updated":
            subscription = event["data"]["object"]
            # Handle subscription update
            print(f"Subscription updated: {subscription.id}")

        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            # Handle subscription cancellation
            print(f"Subscription cancelled: {subscription.id}")

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/prices")
async def get_prices():
    """Get available pricing plans"""
    try:
        prices = stripe.Price.list(active=True)
        return {"prices": prices.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
