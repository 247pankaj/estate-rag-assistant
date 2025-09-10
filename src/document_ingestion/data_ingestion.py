import os
from typing import Optional
import shutil
from pathlib import Path
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
        


class EstateDocumentIngestion:
    """
    EstateRAG: Handles saving, reading, and combining estate-related PDFs for comparison.
    Organizes documents by session with versioning and cleanup support.
    """

    def __init__(self, base_dir: str = "data/document_compare", session_id: Optional[str] = None):
        try:
            self.base_dir = Path(base_dir)
            self.session_id = session_id or generate_session_id("estate_compare")
            self.session_path = self.base_dir / self.session_id
            self.session_path.mkdir(parents=True, exist_ok=True)

            log.info("EstateDocumentIngestion initialized", extra={
                "session_path": str(self.session_path),
                "session_id": self.session_id
            })

        except Exception as e:
            log.error("Failed to initialize EstateDocumentIngestion", extra={"error": str(e)})
            raise EstateRAGException("Initialization error in EstateDocumentIngestion", e) from e

    def save_uploaded_files(self, reference_file, actual_file):
        """
        Saves reference and actual estate PDFs to the session directory.
        """
        try:
            ref_path = self.session_path / reference_file.name
            act_path = self.session_path / actual_file.name

            for fobj, out_path in ((reference_file, ref_path), (actual_file, act_path)):
                if not fobj.name.lower().endswith(".pdf"):
                    raise ValueError("Only PDF files are allowed.")
                with open(out_path, "wb") as f:
                    if hasattr(fobj, "read"):
                        f.write(fobj.read())
                    else:
                        f.write(fobj.getbuffer())

            log.info("Estate PDFs saved", extra={
                "reference": str(ref_path),
                "actual": str(act_path),
                "session_id": self.session_id
            })

            return ref_path, act_path

        except Exception as e:
            log.error("Error saving estate PDFs", extra={
                "error": str(e),
                "session_id": self.session_id
            })
            raise EstateRAGException("Error saving estate documents", e) from e

    def read_pdf(self, pdf_path: Path) -> str:
        """
        Reads an estate PDF and extracts page-wise text.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")

                parts = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        parts.append(f"\n--- Page {page_num + 1} ---\n{text}")

            log.info("Estate PDF read successfully", extra={
                "file": str(pdf_path),
                "pages": len(parts)
            })

            return "\n".join(parts)

        except Exception as e:
            log.error("Error reading estate PDF", extra={
                "file": str(pdf_path),
                "error": str(e)
            })
            raise EstateRAGException("Error reading estate PDF", e) from e

    def combine_documents(self) -> str:
        """
        Combines all estate PDFs in the session into a single text block.
        """
        try:
            doc_parts = []

            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix.lower() == ".pdf":
                    content = self.read_pdf(file)
                    doc_parts.append(f"Document: {file.name}\n{content}")

            combined_text = "\n\n".join(doc_parts)

            log.info("Estate documents combined", extra={
                "count": len(doc_parts),
                "session_id": self.session_id
            })

            return combined_text

        except Exception as e:
            log.error("Error combining estate documents", extra={
                "error": str(e),
                "session_id": self.session_id
            })
            raise EstateRAGException("Error combining estate documents", e) from e

    def clean_old_sessions(self, keep_latest: int = 3):
        """
        Deletes older estate document sessions, keeping only the latest N.
        """
        try:
            sessions = sorted([f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True)
            for folder in sessions[keep_latest:]:
                shutil.rmtree(folder, ignore_errors=True)
                log.info("Old estate session deleted", extra={"path": str(folder)})

        except Exception as e:
            log.error("Error cleaning old estate sessions", extra={"error": str(e)})
            raise EstateRAGException("Error cleaning old estate sessions", e) from e
