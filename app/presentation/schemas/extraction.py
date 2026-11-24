from typing import Any

from pydantic import BaseModel, Field

from app.domain.enums import DocumentType, ExtractionStatus, OCREngine


class ExtractionRequest(BaseModel):
    document_type: DocumentType


class TableData(BaseModel):
    rows: list[list[str]] = Field(default_factory=list)
    row_count: int = 0
    col_count: int = 0

    @classmethod
    def from_raw(cls, raw: list[list[str]]) -> "TableData":
        return cls(
            rows=raw,
            row_count=len(raw),
            col_count=max((len(r) for r in raw), default=0),
        )


class ExtractionResult(BaseModel):
    filename: str
    document_type: DocumentType
    status: ExtractionStatus
    ocr_engine: OCREngine = OCREngine.NONE
    page_count: int = 0
    text: str = ""
    tables: list[TableData] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    ocr_images_found: int = 0
    ocr_images_success: int = 0
    ocr_images_failed: int = 0
