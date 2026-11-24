from pathlib import Path

from app.domain.enums import DocumentType
from app.infrastructure.extractors.base_extractor import BaseExtractor
from app.infrastructure.extractors.pdf_extractor import PdfExtractor
from app.infrastructure.extractors.spreadsheet_extractor import SpreadsheetExtractor

_BY_ENUM: dict[DocumentType, BaseExtractor] = {
    DocumentType.PDF: PdfExtractor(),
    DocumentType.XLSX: SpreadsheetExtractor(),
    DocumentType.CSV: SpreadsheetExtractor(),
}

_EXTRACTORS: list[BaseExtractor] = [PdfExtractor(), SpreadsheetExtractor()]


def get_extractor_by_type(document_type: DocumentType) -> BaseExtractor:
    extractor = _BY_ENUM.get(document_type)
    if extractor is None:
        raise ValueError(f"No extractor registered for '{document_type}'.")
    return extractor


def get_extractor(filename: str) -> BaseExtractor:
    ext = Path(filename).suffix.lower()
    for extractor in _EXTRACTORS:
        if ext in extractor.supported_extensions:
            return extractor
    raise ValueError(f"No extractor registered for '{ext}' files.")
