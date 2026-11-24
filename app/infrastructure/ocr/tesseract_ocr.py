import io
import logging
import os
from pathlib import Path
import shutil

from app.core.config import settings

logger = logging.getLogger(__name__)

# Fallback path for Windows installation
_DEFAULT_WIN_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _get_tesseract():
    try:
        import pytesseract
        cmd = settings.tesseract_cmd or os.getenv("TESSERACT_CMD")
        if not cmd:
            if Path(_DEFAULT_WIN_PATH).exists():
                cmd = _DEFAULT_WIN_PATH
            else:
                cmd = shutil.which("tesseract") or "tesseract"
        pytesseract.pytesseract.tesseract_cmd = cmd
        return pytesseract
    except ImportError:
        logger.warning("pytesseract package is not installed.")
        return None


def ocr_image_bytes(image_bytes: bytes, lang: str = "eng") -> str:
    pytesseract = _get_tesseract()
    if not pytesseract:
        return ""
    try:
        from PIL import Image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as exc:
        logger.warning("Tesseract OCR execution failed: %s", exc)
        return ""
