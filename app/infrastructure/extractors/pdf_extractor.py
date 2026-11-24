import asyncio
import io
import logging

import fitz

from app.infrastructure.extractors.base_extractor import BaseExtractor, ExtractedDocument
from app.infrastructure.ocr.tesseract_ocr import ocr_image_bytes

logger = logging.getLogger(__name__)

_MIN_TEXT_CHARS = 30
_DPI = 300


class PdfExtractor(BaseExtractor):
    supported_extensions: tuple[str, ...] = (".pdf",)

    async def extract(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        pdf = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")
        text_parts: list[str] = []
        tables: list[list[list[str]]] = []
        needs_ocr = False
        ocr_images_found = 0
        ocr_images_success = 0
        ocr_images_failed = 0

        for page in pdf:
            page_text = page.get_text("text").strip()

            # Scanned page fallback: render to image and run OCR
            if len(page_text) < _MIN_TEXT_CHARS:
                needs_ocr = True
                ocr_images_found += 1
                try:
                    pix = page.get_pixmap(dpi=_DPI)
                    ocr_res = await asyncio.to_thread(ocr_image_bytes, pix.tobytes("png"))
                    if ocr_res:
                        text_parts.append(ocr_res)
                        ocr_images_success += 1
                    else:
                        ocr_images_failed += 1
                except Exception:
                    ocr_images_failed += 1
            else:
                text_parts.append(page_text)

                # Process embedded images on text-layer pages
                for img in page.get_images(full=True):
                    try:
                        base_img = pdf.extract_image(img[0])
                        if base_img["width"] >= 150 and base_img["height"] >= 150:
                            ocr_images_found += 1
                            img_text = await asyncio.to_thread(ocr_image_bytes, base_img["image"])
                            if img_text:
                                text_parts.append(img_text)
                                ocr_images_success += 1
                            else:
                                ocr_images_failed += 1
                    except Exception:
                        ocr_images_failed += 1

            # Extract tables if present
            if hasattr(page, "find_tables"):
                try:
                    for tbl in page.find_tables().tables:
                        rows = tbl.extract()
                        tables.append([
                            [str(cell) if cell is not None else "" for cell in row]
                            for row in rows
                        ])
                except Exception:
                    logger.warning("Table extraction failed on page %d.", page.number + 1)

        metadata = {
            "filename": filename,
            "page_count": len(pdf),
            "table_count": len(tables),
            "encrypted": pdf.is_encrypted,
            "title": pdf.metadata.get("title", ""),
            "author": pdf.metadata.get("author", ""),
        }

        result = ExtractedDocument(
            text="\n\n".join(text_parts),
            tables=tables,
            page_count=len(pdf),
            source_type="pdf",
            needs_ocr=needs_ocr,
            metadata=metadata,
            ocr_images_found=ocr_images_found,
            ocr_images_success=ocr_images_success,
            ocr_images_failed=ocr_images_failed,
        )
        pdf.close()
        return result
