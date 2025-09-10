from pydantic import BaseModel, RootModel
from typing import List, Union
from enum import Enum

class Metadata(BaseModel):
    """
    Structured metadata extracted from estate-related documents.
    """
    summary: List[str]
    title: str
    author: List[str]
    date_created: str
    last_modified_date: str
    publisher: str
    language: str
    page_count: Union[int, str]
    sentiment_tone: str

class ChangeFormat(BaseModel):
    """
    Represents a change detected on a specific page of the document.
    """
    page: str
    changes: str

class SummaryResponse(RootModel[List[ChangeFormat]]):
    """
    Root model for a list of page-level changes in estate documents.
    """
    pass

class PromptType(str, Enum):
    """
    Enum for prompt types used in EstateRAG Assistant.
    """
    ESTATE_DOCUMENT_ANALYSIS = "estate_document_analysis",
    ESTATE_DOCUMENT_COMPARISON="estate_document_comparison"
