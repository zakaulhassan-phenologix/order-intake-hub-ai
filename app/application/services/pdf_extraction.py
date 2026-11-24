from app.domain.enums import DocumentType, ExtractionStatus, OCREngine
from app.infrastructure.extractors.pdf_extractor import PdfExtractor
from app.presentation.schemas.extraction import ExtractionResult, TableData


class PdfExtractionService:
    def __init__(self):
        self.extractor = PdfExtractor()

    async def extract(self, file_bytes: bytes, filename: str) -> ExtractionResult:
        doc = await self.extractor.extract(file_bytes, filename)
        warnings = []
        ocr_engine = OCREngine.TESSERACT if doc.ocr_images_found > 0 else OCREngine.NONE

        if doc.ocr_images_failed > 0:
            warnings.append(f"{doc.ocr_images_failed} image(s) or scanned page(s) could not be read by OCR.")

        status = ExtractionStatus.SUCCESS if doc.text or doc.tables else ExtractionStatus.FAILED

        return ExtractionResult(
            filename=filename,
            document_type=DocumentType.PDF,
            status=status,
            ocr_engine=ocr_engine,
            page_count=doc.page_count,
            text=doc.text,
            tables=[TableData.from_raw(t) for t in doc.tables],
            metadata=doc.metadata,
            warnings=warnings,
            ocr_images_found=doc.ocr_images_found,
            ocr_images_success=doc.ocr_images_success,
            ocr_images_failed=doc.ocr_images_failed,
        )

