import os
import sys
from model.models import Metadata
from utils.model_loader import ModelLoader
from core.estate_exception import EstateRAGException
from logger import LOGGER as log
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY 

class EstateDocumentAnalyzer:
    """
    EstateRAG Assistant: Analyzes estate-related documents using a pre-trained LLM.
    Extracts structured metadata and summaries with robust error handling and logging.
    """
    def __init__(self):
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # Estate metadata parser
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            # EstateRAG-specific prompt key
            self.prompt = PROMPT_REGISTRY["estate_document_analysis"]

            log.info("EstateDocumentAnalyzer initialized successfully")

        except Exception as e:
            log.error(f"Initialization failed in EstateDocumentAnalyzer: {e}")
            raise EstateRAGException("Failed to initialize EstateDocumentAnalyzer", sys)

    def analyze_document(self, document_text: str) -> dict:
        """
        Analyze estate document text and extract structured metadata and summary.
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            log.info("Estate metadata analysis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            log.info("Estate metadata extraction successful", extra={"keys": list(response.keys())})
            return response

        except Exception as e:
            log.error("Estate metadata analysis failed", extra={"error": str(e)})
            raise EstateRAGException("Estate metadata extraction failed", sys)
