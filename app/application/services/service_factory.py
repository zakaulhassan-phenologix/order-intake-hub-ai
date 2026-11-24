from app.domain.enums import DocumentType
from app.application.services.pdf_extraction import PdfExtractionService
from app.application.services.spreadsheet_extraction import SpreadsheetExtractionService

_SERVICES = {
    DocumentType.PDF: PdfExtractionService(),
    DocumentType.XLSX: SpreadsheetExtractionService(DocumentType.XLSX),
    DocumentType.CSV: SpreadsheetExtractionService(DocumentType.CSV),
}


def get_extraction_service(document_type: DocumentType):
    service = _SERVICES.get(document_type)
    if not service:
        raise ValueError(f"No service registered for '{document_type}'.")
    return service
