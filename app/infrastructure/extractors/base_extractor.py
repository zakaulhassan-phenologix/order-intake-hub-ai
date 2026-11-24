from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExtractedDocument:
    """What every extractor returns, regardless of file type."""

    text: str = ""
    tables: list[list[list[str]]] = field(default_factory=list)
    page_count: int = 0
    source_type: str = ""
    needs_ocr: bool = False  # True when the file is scanned / image only
    metadata: dict = field(default_factory=dict)


class BaseExtractor(ABC):
    """Contract for all file extractors."""

    supported_extensions: tuple[str, ...] = ()

    @abstractmethod
    async def extract(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        ...
