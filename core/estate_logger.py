import os
import logging
from datetime import datetime
import structlog


class EstateRAGLogger:
    """
    Structured logger for EstateRAG Assistant.
    Logs to both console and timestamped file in JSON format.
    """

    def __init__(self, log_dir: str = "logs"):
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.log_file_path = os.path.join(self.logs_dir, f"estate_rag_{timestamp}.log")

        self._configure_logging()

    def _configure_logging(self):
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[console_handler, file_handler]
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self, name: str = "EstateRAG"):
        return structlog.get_logger(name)
