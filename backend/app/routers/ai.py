from fastapi import APIRouter, Depends, HTTPException

from app.ai_service import AIServiceError, generate_ai_response
from app.dependencies import get_current_user
from app.models import User
from app.schemas import AIChatRequest, AIChatResponse


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(
    payload: AIChatRequest,
    _user: User = Depends(get_current_user),
):
    try:
        provider, model, message = await generate_ai_response(payload.prompt)
        return AIChatResponse(provider=provider, model=model, response=message)
    except AIServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
