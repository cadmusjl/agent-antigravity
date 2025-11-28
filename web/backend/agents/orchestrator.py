import base64
import tempfile
from typing import Dict, Any, Optional
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import openai
from config import settings
from agents.tools.content_generation import ContentGenerationTool
from agents.tools.image_creation import ImageCreationTool
from agents.tools.link_in_bio_builder import LinkInBioBuilderTool
from agents.tools.storefront_builder import StorefrontBuilderTool


class AgentOrchestrator:
    """Orchestrates AI agents using CrewAI and LangChain"""

    def __init__(self):
        # Initialize LLMs
        self.claude = None
        self.gpt4 = None

        if settings.ANTHROPIC_API_KEY:
            self.claude = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                api_key=settings.ANTHROPIC_API_KEY
            )

        if settings.OPENAI_API_KEY:
            self.gpt4 = ChatOpenAI(
                model="gpt-4o",
                api_key=settings.OPENAI_API_KEY
            )
            openai.api_key = settings.OPENAI_API_KEY

        # Initialize tools
        self.content_tool = ContentGenerationTool(self.claude or self.gpt4)
        self.image_tool = ImageCreationTool()
        self.link_in_bio_tool = LinkInBioBuilderTool(self.claude or self.gpt4)
        self.storefront_tool = StorefrontBuilderTool(self.claude or self.gpt4)

    def _get_llm(self, prefer_claude: bool = True):
        """Get the preferred LLM"""
        if prefer_claude and self.claude:
            return self.claude
        elif self.gpt4:
            return self.gpt4
        raise Exception("No LLM configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")

    def _create_agent(self, role: str, goal: str, backstory: str, tools: list = None):
        """Create a CrewAI agent"""
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=self._get_llm(),
            tools=tools or [],
            verbose=True
        )

    async def execute_task(
        self,
        task: str,
        agent_type: str,
        parameters: Dict[str, Any]
    ) -> Any:
        """Execute an agent task based on type"""

        if agent_type == "content":
            return await self._execute_content_generation(task, parameters)
        elif agent_type == "image":
            return await self._execute_image_generation(task, parameters)
        elif agent_type == "link_in_bio":
            return await self._execute_link_in_bio(task, parameters)
        elif agent_type == "storefront":
            return await self._execute_storefront(task, parameters)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

    async def _execute_content_generation(self, task: str, parameters: Dict[str, Any]):
        """Execute content generation task"""
        agent = self._create_agent(
            role="Content Marketing Specialist",
            goal="Create compelling marketing content that drives engagement",
            backstory="You are an expert content marketer with years of experience creating high-converting copy.",
            tools=[]
        )

        crew_task = Task(
            description=task,
            expected_output=f"High-quality {parameters.get('content_type', 'content')} with {parameters.get('tone', 'professional')} tone",
            agent=agent
        )

        crew = Crew(agents=[agent], tasks=[crew_task], verbose=True)
        result = crew.kickoff()

        return str(result)

    async def _execute_image_generation(self, task: str, parameters: Dict[str, Any]):
        """Execute image generation task"""
        prompt = task.replace("Generate image:", "").strip()
        style = parameters.get("style", "realistic")
        model = parameters.get("model", "stable-diffusion")

        return await self.image_tool.generate_image(prompt, style, model)

    async def _execute_link_in_bio(self, task: str, parameters: Dict[str, Any]):
        """Execute link-in-bio page creation"""
        agent = self._create_agent(
            role="Web Design Specialist",
            goal="Create beautiful and functional link-in-bio pages",
            backstory="You are a skilled web designer specializing in personal branding pages.",
            tools=[]
        )

        crew_task = Task(
            description=f"Create a link-in-bio page with the following data: {parameters}",
            expected_output="Complete link-in-bio page configuration with design and content",
            agent=agent
        )

        crew = Crew(agents=[agent], tasks=[crew_task], verbose=True)
        result = crew.kickoff()

        # Generate the actual page structure
        page_data = await self.link_in_bio_tool.build_page(parameters, str(result))

        return page_data

    async def _execute_storefront(self, task: str, parameters: Dict[str, Any]):
        """Execute storefront creation"""
        agent = self._create_agent(
            role="E-commerce Specialist",
            goal="Create professional digital storefronts",
            backstory="You are an expert in e-commerce design and conversion optimization.",
            tools=[]
        )

        crew_task = Task(
            description=f"Create a digital storefront with the following data: {parameters}",
            expected_output="Complete storefront configuration with products, design, and layout",
            agent=agent
        )

        crew = Crew(agents=[agent], tasks=[crew_task], verbose=True)
        result = crew.kickoff()

        # Generate the actual storefront structure
        storefront_data = await self.storefront_tool.build_storefront(parameters, str(result))

        return storefront_data

    async def transcribe_audio(self, audio_data: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key required for transcription")

        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        try:
            # Transcribe using Whisper
            with open(temp_audio_path, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        finally:
            # Clean up temporary file
            import os
            os.unlink(temp_audio_path)
