from pathlib import Path
from typing import Optional

from PyPDF2 import PdfReader

from utils.logger import get_logger


logger = get_logger(__name__)


def extract_text_from_pdf(path: str | Path) -> str:
    """Extract raw text from a PDF file.

    This implementation handles text-based PDFs via PyPDF2. For image-based
    PDFs (scanned resumes), you can extend this to use OCR (e.g. Tesseract).
    """

    pdf_path = Path(path)
    if not pdf_path.is_file():
        logger.warning("PDF file not found: %s", pdf_path)
        return ""

    text_parts: list[str] = []

    try:
        reader = PdfReader(str(pdf_path))
        for page_num, page in enumerate(reader.pages):
            try:
                page_text: Optional[str] = page.extract_text()
            except Exception as page_err:  # noqa: BLE001
                logger.error("Failed to extract text from page %s of %s: %s", page_num, pdf_path, page_err)
                page_text = None

            if page_text:
                text_parts.append(page_text)
    except Exception as err:  # noqa: BLE001
        logger.error("Error reading PDF %s: %s", pdf_path, err)
        return ""

    full_text = "\n".join(text_parts)
    if not full_text.strip():
        logger.warning("No text extracted from PDF: %s (may require OCR)", pdf_path)

    return full_text
