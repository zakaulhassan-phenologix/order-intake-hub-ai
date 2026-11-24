from app.domain.enums import DocumentType, ExtractionStatus, OCREngine
from app.infrastructure.extractors.spreadsheet_extractor import SpreadsheetExtractor
from app.presentation.schemas.extraction import ExtractionResult, TableData


class SpreadsheetExtractionService:
    def __init__(self, document_type: DocumentType):
        self.document_type = document_type
        self.extractor = SpreadsheetExtractor()

    async def extract(self, file_bytes: bytes, filename: str) -> ExtractionResult:
        doc = await self.extractor.extract(file_bytes, filename)
        status = ExtractionStatus.SUCCESS if doc.text or doc.tables else ExtractionStatus.FAILED

        return ExtractionResult(
            filename=filename,
            document_type=self.document_type,
            status=status,
            ocr_engine=OCREngine.NONE,
            page_count=doc.page_count,
            text=doc.text,
            tables=[TableData.from_raw(t) for t in doc.tables],
            metadata=doc.metadata,
            warnings=[],
            ocr_images_found=0,
            ocr_images_success=0,
            ocr_images_failed=0,
        )
