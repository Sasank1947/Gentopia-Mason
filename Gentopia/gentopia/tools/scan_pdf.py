import requests
import pdfplumber
from typing import AnyStr, Any, Type, Optional
from gentopia.tools.basetool import BaseTool
import os
from pydantic import BaseModel, Field


class PdfExtractorArgs(BaseModel):
    document_url: str = Field(..., description="URL or path to the PDF document")


class PdfTextExtractor(BaseTool):
    """Tool to extract text from a PDF file, supports local files and online URLs."""

    name = "pdf_text_extractor"
    description = ("A tool for reading PDF files and extracting the text content."
                   "Input should be the file path or URL of the PDF.")

    args_schema: Optional[Type[BaseModel]] = PdfExtractorArgs  # Ensure correct import of Optional and Type

    def _download_pdf(self, url: AnyStr) -> str:
        """Download PDF from a URL and save it locally."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                temp_filename = "temp_downloaded.pdf"
                with open(temp_filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                return temp_filename
            else:
                return None
        except Exception as e:
            return f"Failed to download PDF: {str(e)}"

    def _run(self, document_url: AnyStr) -> str:
        """Run the extraction logic."""
        try:
            # If the path is a URL, download the PDF first
            if document_url.startswith("http"):
                document_path = self._download_pdf(document_url)
                if document_path is None:
                    return "Failed to download the PDF."
            else:
                document_path = document_url  # Treat it as a local file path

            # Now read the PDF using pdfplumber
            full_text = ""
            with pdfplumber.open(document_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"  # Append each page's text

            # Cleanup the temporary file if it was downloaded
            if document_url.startswith("http") and os.path.exists(document_path):
                os.remove(document_path)

            return full_text.strip() if full_text else "No text found in PDF."

        except Exception as e:
            return f"Failed to read PDF: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    pdf_url = "https://arxiv.org/pdf/2407.02067"
    pdf_extractor = PdfTextExtractor()
    extracted_text = pdf_extractor._run(pdf_url)
    print(extracted_text)
