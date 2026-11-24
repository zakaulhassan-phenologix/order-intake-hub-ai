from fastapi import APIRouter

from app.presentation.schemas.response_schema import ApiResponse

router = APIRouter()


@router.get("/ping", response_model=ApiResponse[dict])
async def ping():
    return ApiResponse.success(data={"module": "matching"}, message="matching route ready")
