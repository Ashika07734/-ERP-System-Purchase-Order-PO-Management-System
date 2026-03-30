"""
ERP PO Management System — AI Service
Generate marketing descriptions using Google Gemini or OpenAI.
Optional MongoDB logging of AI responses.
"""

import os
from datetime import datetime, timezone
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # "gemini" or "openai"

# ── MongoDB Logging (optional) ───────────────────────────
_mongo_client = None
_mongo_collection = None


def _get_mongo_collection():
    """Lazy-initialise the MongoDB collection for AI logs."""
    global _mongo_client, _mongo_collection
    if _mongo_collection is not None:
        return _mongo_collection

    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        return None

    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
        db_name = os.getenv("MONGODB_DB_NAME", "erp_ai_logs")
        _mongo_collection = _mongo_client[db_name]["ai_descriptions"]
        return _mongo_collection
    except Exception:
        return None


def _log_to_mongo(product_name: str, description: str):
    """Log AI-generated description to MongoDB."""
    try:
        col = _get_mongo_collection()
        if col is not None:
            col.insert_one({
                "product_name": product_name,
                "generated_description": description,
                "timestamp": datetime.now(timezone.utc),
            })
    except Exception:
        pass  # Non-critical — silently skip


async def generate_description_gemini(product_name: str, category: str) -> str:
    """Generate a marketing description using Google Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback_description(product_name, category)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            f"Write a professional 2-sentence marketing description for "
            f"the product '{product_name}' in the category '{category}'. "
            f"Keep it concise, compelling, and suitable for a B2B product catalog."
        )

        response = model.generate_content(prompt)
        description = response.text.strip()
        _log_to_mongo(product_name, description)
        return description
    except Exception as e:
        return _fallback_description(product_name, category)


async def generate_description_openai(product_name: str, category: str) -> str:
    """Generate a marketing description using OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_description(product_name, category)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = (
            f"Write a professional 2-sentence marketing description for "
            f"the product '{product_name}' in the category '{category}'. "
            f"Keep it concise, compelling, and suitable for a B2B product catalog."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.7,
        )
        description = response.choices[0].message.content.strip()
        _log_to_mongo(product_name, description)
        return description
    except Exception as e:
        return _fallback_description(product_name, category)


async def generate_description(product_name: str, category: str = "General") -> str:
    """Route to the configured AI provider."""
    if AI_PROVIDER == "openai":
        return await generate_description_openai(product_name, category)
    return await generate_description_gemini(product_name, category)


def _fallback_description(product_name: str, category: str) -> str:
    """Return a template description when AI APIs are unavailable."""
    return (
        f"Introducing {product_name} — a premium-grade {category.lower()} solution "
        f"engineered for reliability and performance. "
        f"Trusted by industry leaders for demanding operational environments."
    )
