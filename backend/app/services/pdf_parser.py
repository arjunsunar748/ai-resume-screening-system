import io
from typing import Union
from pypdf import PdfReader


class PDFParserService:
    """
    Production service for extracting clean text from uploaded PDF resumes.
    """

    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes) -> str:
        """
        Parses raw bytes from a PDF file upload and extracts plain text.

        Args:
            file_bytes (bytes): Raw binary content of the PDF file.

        Returns:
            str: Extracted plain text string.
        """
        if not file_bytes:
            return ""

        extracted_text = []

        try:
            # Load PDF from memory stream
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)

            # Iterate through all pages in the PDF document
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)

            full_text = "\n".join(extracted_text).strip()
            return full_text

        except Exception as e:
            print(f"[ERROR] Failed to extract text from PDF stream: {e}")
            raise ValueError("Invalid or corrupted PDF file.") from e


# Singleton instance
pdf_parser_service = PDFParserService()