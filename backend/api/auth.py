from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from config import settings

router = APIRouter()


def get_supabase() -> Client:
    """Get Supabase client"""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def sign_up(request: SignUpRequest, supabase: Client = Depends(get_supabase)):
    """Sign up a new user"""
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
                }
            }
        })
        return {
            "message": "User created successfully",
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signin")
async def sign_in(request: SignInRequest, supabase: Client = Depends(get_supabase)):
    """Sign in an existing user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        return {
            "message": "Signed in successfully",
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/signout")
async def sign_out(supabase: Client = Depends(get_supabase)):
    """Sign out the current user"""
    try:
        supabase.auth.sign_out()
        return {"message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user")
async def get_user(supabase: Client = Depends(get_supabase)):
    """Get current user"""
    try:
        user = supabase.auth.get_user()
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
