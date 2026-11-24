from fastapi import APIRouter

from app.presentation.schemas.response_schema import ApiResponse

router = APIRouter()


@router.get("/health", response_model=ApiResponse[dict])
async def health():
    return ApiResponse.success(data={"service": "order-intake-ai"}, message="Healthy")
