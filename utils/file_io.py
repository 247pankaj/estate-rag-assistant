from datetime import datetime, timezone
import uuid
from core.estate_exception import EstateRAGException
from logger import LOGGER as log


# Supported file types for estate document processing
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def generate_session_id(prefix: str = "estate_session") -> str:
    """
    Generates a unique session ID using UTC timestamp and UUID.
    Useful for organizing estate document sessions.
    """
    try:
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        session_id = f"{prefix}_{timestamp}_{unique_id}"
        
        log.info("Generated session ID", extra={"session_id": session_id})
        return session_id

    except Exception as e:
        log.error("Failed to generate session ID", extra={"error": str(e)})
        raise EstateRAGException("Error generating session ID", e) from e