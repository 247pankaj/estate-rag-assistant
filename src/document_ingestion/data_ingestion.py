import os
from typing import Optional
import fitz
from utils.file_io import generate_session_id
from core.estate_exception import EstateRAGException
from logger import LOGGER as log


class EstateDocHandler:
    """
    EstateRAG: Handles saving and reading estate-related PDFs for analysis.
    Organizes files by session and ensures valid input format.
    """

    def __init__(self, data_dir: Optional[str] = None, session_id: Optional[str] = None):
        try:
            self.data_dir = data_dir or os.getenv(
                "ESTATE_DATA_STORAGE_PATH",
                os.path.join(os.getcwd(), "data", "document_analysis")
            )
            self.session_id = session_id or generate_session_id("estate_session")
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            log.info("EstateDocHandler initialized", extra={
                "session_id": self.session_id,
                "session_path": self.session_path
            })

        except Exception as e:
            log.error("Initialization failed in EstateDocHandler", extra={"error": str(e)})
            raise EstateRAGException("Failed to initialize EstateDocHandler", e) from e

    def save_pdf(self, uploaded_file) -> str:
        """
        Save uploaded estate PDF to session directory.
        """
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith(".pdf"):
                raise ValueError("Invalid file type. Only PDFs are allowed.")

            save_path = os.path.join(self.session_path, filename)
            with open(save_path, "wb") as f:
                if hasattr(uploaded_file, "read"):
                    f.write(uploaded_file.read())
                else:
                    f.write(uploaded_file.getbuffer())

            log.info("Estate PDF saved successfully", extra={
                "file": filename,
                "save_path": save_path,
                "session_id": self.session_id
            })

            return save_path

        except Exception as e:
            log.error("Failed to save estate PDF", extra={
                "error": str(e),
                "session_id": self.session_id
            })
            raise EstateRAGException(f"Failed to save estate PDF: {str(e)}", e) from e

    def read_pdf(self, pdf_path: str) -> str:
        """
        Reads an estate-related PDF file and extracts text content page by page.
        Returns the full text as a single string with page markers.
        """
        try:
            text_chunks = []

            with fitz.open(pdf_path) as doc:
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    page_text = page.get_text()
                    text_chunks.append(f"\n--- Page {page_num + 1} ---\n{page_text}")

            full_text = "\n".join(text_chunks)

            log.info("Estate PDF read successfully", extra={
                "pdf_path": pdf_path,
                "session_id": self.session_id,
                "total_pages": len(text_chunks)
            })

            return full_text

        except Exception as e:
            log.error("Failed to read estate PDF", extra={
                "error": str(e),
                "pdf_path": pdf_path,
                "session_id": self.session_id
            })
            raise EstateRAGException(f"Could not process estate PDF: {pdf_path}", e) from e
