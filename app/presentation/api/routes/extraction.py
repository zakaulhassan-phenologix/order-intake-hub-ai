from fastapi import APIRouter, Form, UploadFile

from app.domain.enums import DocumentType
from app.application.services.service_factory import get_extraction_service
from app.presentation.schemas.extraction import ExtractionResult
from app.presentation.schemas.response_schema import ResponseSchema

router = APIRouter()
_MAX_FILE_BYTES = 10 * 1024 * 1024


@router.post("/document", response_model=ResponseSchema[ExtractionResult])
async def extract_document(
    file: UploadFile,
    document_type: DocumentType = Form(...),
):
    if not file.filename:
        return ResponseSchema.error("No filename provided.")

    file_bytes = await file.read()

    if not file_bytes:
        return ResponseSchema.error("Uploaded file is empty.")

    if len(file_bytes) > _MAX_FILE_BYTES:
        return ResponseSchema.error("File exceeds 10 MB limit.")

    try:
        service = get_extraction_service(document_type)
        result = await service.extract(file_bytes, file.filename)
    except Exception as exc:
        return ResponseSchema.error(str(exc))

    return ResponseSchema.success(data=result, message=f"Extraction completed with status: {result.status}")
