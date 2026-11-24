from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    XLSX = "xlsx"
    CSV = "csv"


class ExtractionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class OCREngine(str, Enum):
    NONE = "none"
    TESSERACT = "tesseract"
    PADDLE = "paddle"
    VISION_LLM = "vision_llm"
