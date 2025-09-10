import sys
from dotenv import load_dotenv
import pandas as pd
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from utils.model_loader import ModelLoader
from logger import LOGGER as log
from core.estate_exception import EstateRAGException
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import SummaryResponse, PromptType


class EstateDocumentComparatorLLM:
    """
    EstateRAG: Compares two estate-related documents using LLM and returns structured differences.
    """
    def __init__(self):
        try:
            load_dotenv()
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            self.prompt = PROMPT_REGISTRY[PromptType.ESTATE_DOCUMENT_COMPARISON.value]
            self.chain = self.prompt | self.llm | self.fixing_parser

            log.info("EstateDocumentComparatorLLM initialized", extra={"model": str(self.llm)})

        except Exception as e:
            log.error("Initialization failed in EstateDocumentComparatorLLM", extra={"error": str(e)})
            raise EstateRAGException("Failed to initialize EstateDocumentComparatorLLM", e) from e

    def compare_documents(self, combined_docs: str) -> pd.DataFrame:
        """
        Compares two estate documents and returns a DataFrame of page-wise changes.
        """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions()
            }

            log.info("Invoking estate document comparison chain")
            response = self.chain.invoke(inputs)

            log.info("Comparison chain invoked successfully", extra={
                "response_preview": str(response)[:200]
            })

            return self._format_response(response)

        except Exception as e:
            log.error("Error during estate document comparison", extra={"error": str(e)})
            raise EstateRAGException("Error comparing estate documents", e) from e

    def _format_response(self, response_parsed: List[dict]) -> pd.DataFrame:
        """
        Converts parsed response into a pandas DataFrame.
        """
        try:
            df = pd.DataFrame(response_parsed)
            return df
        except Exception as e:
            log.error("Error formatting comparison response", extra={"error": str(e)})
            raise EstateRAGException("Error formatting comparison response", e) from e
