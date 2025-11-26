from typing import Optional


class ContentGenerationTool:
    """Tool for generating marketing content using LLMs"""

    def __init__(self, llm):
        self.llm = llm

    async def generate_content(
        self,
        topic: str,
        content_type: str = "blog_post",
        tone: str = "professional",
        length: str = "medium"
    ) -> str:
        """Generate marketing content"""

        prompts = {
            "blog_post": f"""Write a comprehensive blog post about {topic}.
Tone: {tone}
Length: {length}

Include:
- Engaging headline
- Introduction
- Main points with subheadings
- Conclusion
- Call to action""",

            "social_media": f"""Create engaging social media content about {topic}.
Tone: {tone}
Include:
- Attention-grabbing hook
- Key message
- Relevant hashtags
- Call to action""",

            "email": f"""Write a marketing email about {topic}.
Tone: {tone}
Include:
- Subject line
- Personalized greeting
- Value proposition
- Benefits
- Clear call to action""",

            "product_description": f"""Write a compelling product description for {topic}.
Tone: {tone}
Include:
- Key features
- Benefits
- Unique selling points
- Call to action"""
        }

        prompt = prompts.get(content_type, prompts["blog_post"])

        if hasattr(self.llm, 'ainvoke'):
            response = await self.llm.ainvoke(prompt)
            return response.content
        else:
            response = self.llm.invoke(prompt)
            return response.content

    async def refine_content(self, content: str, feedback: str) -> str:
        """Refine existing content based on feedback"""
        prompt = f"""Refine the following content based on this feedback:

Feedback: {feedback}

Content:
{content}

Provide the improved version:"""

        if hasattr(self.llm, 'ainvoke'):
            response = await self.llm.ainvoke(prompt)
            return response.content
        else:
            response = self.llm.invoke(prompt)
            return response.content
