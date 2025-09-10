import io
from pathlib import Path
from src.document_ingestion.data_ingestion import EstateDocumentIngestion
from src.document_compare.document_comparator import EstateDocumentComparatorLLM

def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())

def test_estate_document_comparison():
    ref_path = Path("/Users/pankaj/Desktop/AI/estate-rag-assistant/data/rental_agreement_n.pdf")
    act_path = Path("/Users/pankaj/Desktop/AI/estate-rag-assistant/data/Lease.pdf")

    class FakeUpload:
        def __init__(self, file_path: Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()

        def getbuffer(self):
            return self._buffer

    comparator = EstateDocumentIngestion()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_documents()
    comparator.clean_old_sessions(keep_latest=3)

    print("\nCombined Text Preview (First 1000 chars):\n")
    print(combined_text[:1000])

    llm_comparator = EstateDocumentComparatorLLM()
    df = llm_comparator.compare_documents(combined_text)

    print("\nComparison DataFrame:\n")
    print(df)

if __name__ == "__main__":
    test_estate_document_comparison()
