from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from agents.orchestrator import AgentOrchestrator

router = APIRouter()
orchestrator = AgentOrchestrator()


class AgentRequest(BaseModel):
    task: str
    agent_type: str  # "content", "image", "link_in_bio", "storefront"
    parameters: Optional[Dict[str, Any]] = None


class VoiceRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    agent_type: str


@router.post("/execute")
async def execute_agent_task(request: AgentRequest):
    """Execute an AI agent task"""
    try:
        result = await orchestrator.execute_task(
            task=request.task,
            agent_type=request.agent_type,
            parameters=request.parameters or {}
        )
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice")
async def process_voice_input(request: VoiceRequest):
    """Process voice input and execute agent task"""
    try:
        # Transcribe audio using Whisper
        transcript = await orchestrator.transcribe_audio(request.audio_data)

        # Execute the task based on the transcript
        result = await orchestrator.execute_task(
            task=transcript,
            agent_type=request.agent_type,
            parameters={}
        )

        return {
            "success": True,
            "transcript": transcript,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/content/generate")
async def generate_content(
    topic: str,
    content_type: str = "blog_post",
    tone: str = "professional"
):
    """Generate marketing content"""
    try:
        result = await orchestrator.execute_task(
            task=f"Generate {content_type} about {topic}",
            agent_type="content",
            parameters={"content_type": content_type, "tone": tone}
        )
        return {"success": True, "content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image/generate")
async def generate_image(
    prompt: str,
    style: str = "realistic",
    model: str = "stable-diffusion"
):
    """Generate AI image"""
    try:
        result = await orchestrator.execute_task(
            task=f"Generate image: {prompt}",
            agent_type="image",
            parameters={"style": style, "model": model}
        )
        return {"success": True, "image_url": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/link-in-bio/create")
async def create_link_in_bio(
    profile_data: Dict[str, Any]
):
    """Create a link-in-bio page"""
    try:
        result = await orchestrator.execute_task(
            task="Create link-in-bio page",
            agent_type="link_in_bio",
            parameters=profile_data
        )
        return {"success": True, "page_data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/storefront/create")
async def create_storefront(
    store_data: Dict[str, Any]
):
    """Create a digital storefront"""
    try:
        result = await orchestrator.execute_task(
            task="Create digital storefront",
            agent_type="storefront",
            parameters=store_data
        )
        return {"success": True, "storefront_data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
