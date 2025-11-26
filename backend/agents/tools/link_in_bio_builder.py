from typing import Dict, Any, List


class LinkInBioBuilderTool:
    """Tool for building link-in-bio pages"""

    def __init__(self, llm):
        self.llm = llm

    async def build_page(
        self,
        profile_data: Dict[str, Any],
        ai_suggestions: str = ""
    ) -> Dict[str, Any]:
        """Build a link-in-bio page configuration"""

        # Generate AI-enhanced bio if not provided
        bio = profile_data.get("bio", "")
        if not bio and profile_data.get("name"):
            bio_prompt = f"""Create a compelling bio for a link-in-bio page:
Name: {profile_data.get('name')}
Profession: {profile_data.get('profession', 'Professional')}
Interests: {profile_data.get('interests', '')}

Write a short, engaging bio (2-3 sentences):"""

            if hasattr(self.llm, 'ainvoke'):
                response = await self.llm.ainvoke(bio_prompt)
                bio = response.content
            else:
                response = self.llm.invoke(bio_prompt)
                bio = response.content

        # Generate link descriptions if not provided
        links = profile_data.get("links", [])
        enhanced_links = []

        for link in links:
            if not link.get("description"):
                desc_prompt = f"""Create a short, compelling description (one sentence) for this link:
Title: {link.get('title')}
URL: {link.get('url')}"""

                if hasattr(self.llm, 'ainvoke'):
                    response = await self.llm.ainvoke(desc_prompt)
                    description = response.content.strip()
                else:
                    response = self.llm.invoke(desc_prompt)
                    description = response.content.strip()

                link["description"] = description

            enhanced_links.append(link)

        # Generate theme suggestions
        theme = profile_data.get("theme", {})
        if not theme:
            theme = {
                "primary_color": "#6366f1",
                "secondary_color": "#8b5cf6",
                "background_color": "#ffffff",
                "text_color": "#1f2937",
                "font": "Inter",
                "style": "modern"
            }

        page_data = {
            "profile": {
                "name": profile_data.get("name", ""),
                "bio": bio,
                "avatar_url": profile_data.get("avatar_url", ""),
                "profession": profile_data.get("profession", ""),
            },
            "links": enhanced_links,
            "social_links": profile_data.get("social_links", []),
            "theme": theme,
            "seo": {
                "title": f"{profile_data.get('name', 'Profile')} - Links",
                "description": bio[:160],
                "og_image": profile_data.get("avatar_url", "")
            }
        }

        return page_data

    async def suggest_improvements(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest improvements for an existing page"""
        prompt = f"""Analyze this link-in-bio page and suggest improvements:

Profile: {page_data.get('profile', {})}
Links: {len(page_data.get('links', []))} links
Theme: {page_data.get('theme', {})}

Provide specific suggestions for:
1. Bio improvement
2. Link organization
3. Visual design
4. User engagement"""

        if hasattr(self.llm, 'ainvoke'):
            response = await self.llm.ainvoke(prompt)
            suggestions = response.content
        else:
            response = self.llm.invoke(prompt)
            suggestions = response.content

        return {"suggestions": suggestions, "original_data": page_data}
