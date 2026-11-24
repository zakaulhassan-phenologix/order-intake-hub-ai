from pathlib import Path

from app.infrastructure.extractors.base_extractor import BaseExtractor

# Register extractors here as you implement them, e.g.:
# from app.infrastructure.extractors.pdf_extractor import PdfExtractor
# _EXTRACTORS: list[BaseExtractor] = [PdfExtractor(), SpreadsheetExtractor(), ...]
_EXTRACTORS: list[BaseExtractor] = []


def get_extractor(filename: str) -> BaseExtractor:
    """Pick the right extractor from the file extension."""
    ext = Path(filename).suffix.lower()
    for extractor in _EXTRACTORS:
        if ext in extractor.supported_extensions:
            return extractor
    raise ValueError(f"No extractor registered for '{ext}' files")
