import httpx

from app.config import settings


class AIServiceError(RuntimeError):
    pass


async def _chat_openai(prompt: str) -> tuple[str, str, str]:
    if not settings.openai_api_key:
        raise AIServiceError("OPENAI_API_KEY is missing")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "You are an ERP assistant for wholesale grocery operations."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, headers=headers, json=payload)

    if res.status_code >= 400:
        raise AIServiceError(f"OpenAI request failed: {res.text}")

    data = res.json()
    content = data["choices"][0]["message"]["content"]
    return "openai", settings.openai_model, content


async def _chat_gemini(prompt: str) -> tuple[str, str, str]:
    if not settings.gemini_api_key:
        raise AIServiceError("GEMINI_API_KEY is missing")

    model = settings.gemini_model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    params = {"key": settings.gemini_api_key}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are an ERP assistant for wholesale grocery operations. "
                            f"User request: {prompt}"
                        )
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, params=params, json=payload)

    if res.status_code >= 400:
        raise AIServiceError(f"Gemini request failed: {res.text}")

    data = res.json()
    candidates = data.get("candidates", [])
    text = ""
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "\n".join(part.get("text", "") for part in parts).strip()

    if not text:
        raise AIServiceError("Gemini returned an empty response")

    return "gemini", model, text


async def generate_ai_response(prompt: str) -> tuple[str, str, str]:
    local_fallback = (
        "local",
        "offline",
        (
            "Local preview response: "
            f"I read your request about '{prompt}'. "
            "The live provider was unavailable, so I returned this offline response instead."
        ),
    )

    provider = settings.ai_provider.strip().lower()
    if provider not in {"openai", "gemini"}:
        return local_fallback

    if provider == "gemini":
        if not settings.gemini_api_key:
            return local_fallback
        try:
            return await _chat_gemini(prompt)
        except AIServiceError:
            return local_fallback

    if not settings.openai_api_key:
        return local_fallback

    try:
        return await _chat_openai(prompt)
    except AIServiceError:
        return local_fallback
