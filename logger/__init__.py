from .estate_logger import EstateRAGLogger
# Create and expose the shared logger instance
LOGGER = EstateRAGLogger().get_logger("EstateRAG")