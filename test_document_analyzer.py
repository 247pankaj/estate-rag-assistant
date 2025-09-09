from pathlib import Path
from src.document_ingestion.data_ingestion  import EstateDocHandler
from src.document_analyzer.data_analysis import EstateDocumentAnalyzer
from core.estate_exception import EstateRAGException

# Path to the estate PDF you want to test
PDF_PATH = r"/Users/pankaj/Desktop/AI/estate-rag-assistant/data/General provisions - Dutch rental agreement.pdf"

# Dummy file wrapper to simulate uploaded file
class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()

def test_estate_document_analysis():
    try:
        print("🔍 Starting estate PDF ingestion...")
        dummy_pdf = DummyFile(PDF_PATH)

        handler = EstateDocHandler(session_id="test_estate_analysis")
        saved_path = handler.save_pdf(dummy_pdf)
        print(f"✅ PDF saved at: {saved_path}")

        text_content = handler.read_pdf(saved_path)
        print(f"📄 Extracted text length: {len(text_content)} characters\n")

        print("🧠 Starting metadata analysis...")
        analyzer = EstateDocumentAnalyzer()
        analysis_result = analyzer.analyze_document(text_content)

        print("\n📊 === METADATA ANALYSIS RESULT ===")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")

    except EstateRAGException as e:
        print(f"❌ EstateRAG test failed: {e}")

if __name__ == "__main__":
    test_estate_document_analysis()
