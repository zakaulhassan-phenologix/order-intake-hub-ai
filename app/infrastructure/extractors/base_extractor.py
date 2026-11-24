from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExtractedDocument:
    text: str = ""
    tables: list[list[list[str]]] = field(default_factory=list)
    page_count: int = 0
    source_type: str = ""
    needs_ocr: bool = False
    metadata: dict = field(default_factory=dict)
    ocr_images_found: int = 0
    ocr_images_success: int = 0
    ocr_images_failed: int = 0


class BaseExtractor(ABC):
    supported_extensions: tuple[str, ...] = ()

    @abstractmethod
    async def extract(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        ...
