from typing import Dict, Any, List


class StorefrontBuilderTool:
    """Tool for building digital storefronts"""

    def __init__(self, llm):
        self.llm = llm

    async def build_storefront(
        self,
        store_data: Dict[str, Any],
        ai_suggestions: str = ""
    ) -> Dict[str, Any]:
        """Build a digital storefront configuration"""

        # Generate store description if not provided
        description = store_data.get("description", "")
        if not description:
            desc_prompt = f"""Create a compelling store description:
Store Name: {store_data.get('name')}
Category: {store_data.get('category', 'General')}
Products: {len(store_data.get('products', []))} products

Write an engaging store description (2-3 sentences):"""

            if hasattr(self.llm, 'ainvoke'):
                response = await self.llm.ainvoke(desc_prompt)
                description = response.content
            else:
                response = self.llm.invoke(desc_prompt)
                description = response.content

        # Enhance product descriptions
        products = store_data.get("products", [])
        enhanced_products = []

        for product in products:
            if not product.get("description"):
                prod_prompt = f"""Create a compelling product description:
Product Name: {product.get('name')}
Price: ${product.get('price', 0)}
Category: {product.get('category', '')}

Write an engaging product description highlighting features and benefits:"""

                if hasattr(self.llm, 'ainvoke'):
                    response = await self.llm.ainvoke(prod_prompt)
                    prod_description = response.content
                else:
                    response = self.llm.invoke(prod_prompt)
                    prod_description = response.content

                product["description"] = prod_description

            # Generate SEO-friendly URL slug
            if not product.get("slug"):
                product["slug"] = product.get("name", "").lower().replace(" ", "-")

            enhanced_products.append(product)

        # Generate theme and layout
        theme = store_data.get("theme", {})
        if not theme:
            theme = {
                "primary_color": "#2563eb",
                "secondary_color": "#7c3aed",
                "background_color": "#ffffff",
                "text_color": "#111827",
                "accent_color": "#f59e0b",
                "font": "Inter",
                "style": "modern-ecommerce"
            }

        # Configure payment and shipping
        settings = {
            "payment_methods": store_data.get("payment_methods", ["card", "digital_wallet"]),
            "shipping_methods": store_data.get("shipping_methods", [
                {"name": "Standard", "price": 5.99, "delivery_days": "5-7"},
                {"name": "Express", "price": 12.99, "delivery_days": "2-3"}
            ]),
            "currency": store_data.get("currency", "USD"),
            "tax_rate": store_data.get("tax_rate", 0.0)
        }

        storefront_data = {
            "store": {
                "name": store_data.get("name", ""),
                "description": description,
                "logo_url": store_data.get("logo_url", ""),
                "category": store_data.get("category", ""),
                "owner_id": store_data.get("owner_id", "")
            },
            "products": enhanced_products,
            "collections": self._organize_collections(enhanced_products),
            "theme": theme,
            "settings": settings,
            "seo": {
                "title": f"{store_data.get('name', 'Store')} - Shop Now",
                "description": description[:160],
                "og_image": store_data.get("logo_url", "")
            },
            "features": {
                "cart_enabled": True,
                "wishlist_enabled": True,
                "reviews_enabled": True,
                "search_enabled": True,
                "filters_enabled": True
            }
        }

        return storefront_data

    def _organize_collections(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Organize products into collections by category"""
        collections = {}

        for product in products:
            category = product.get("category", "General")
            if category not in collections:
                collections[category] = {
                    "name": category,
                    "slug": category.lower().replace(" ", "-"),
                    "products": []
                }
            collections[category]["products"].append(product["id"] if "id" in product else product["name"])

        return list(collections.values())

    async def generate_marketing_copy(self, storefront_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate marketing copy for the storefront"""
        prompt = f"""Create marketing copy for this e-commerce store:

Store Name: {storefront_data['store']['name']}
Description: {storefront_data['store']['description']}
Products: {len(storefront_data['products'])} items

Generate:
1. Homepage headline
2. Featured product tagline
3. About us section
4. Newsletter signup text"""

        if hasattr(self.llm, 'ainvoke'):
            response = await self.llm.ainvoke(prompt)
            copy = response.content
        else:
            response = self.llm.invoke(prompt)
            copy = response.content

        return {"marketing_copy": copy}

    async def optimize_product_listings(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize product listings for SEO and conversion"""
        optimized = []

        for product in products:
            opt_prompt = f"""Optimize this product listing for SEO and conversions:

Name: {product.get('name')}
Description: {product.get('description', '')}
Price: ${product.get('price', 0)}

Provide:
1. SEO-optimized title
2. Meta description
3. Key selling points (3-5 bullet points)"""

            if hasattr(self.llm, 'ainvoke'):
                response = await self.llm.ainvoke(opt_prompt)
                optimization = response.content
            else:
                response = self.llm.invoke(opt_prompt)
                optimization = response.content

            product["seo_optimization"] = optimization
            optimized.append(product)

        return optimized
