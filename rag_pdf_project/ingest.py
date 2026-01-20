import fitz  # PyMuPDF

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PDF_PATH = "data/sample.pdf"
DB_DIR = "chroma_db"

def load_pdf_with_pymupdf(path: str):
    doc = fitz.open(path)
    docs = []
    for i in range(len(doc)):
        text = doc[i].get_text("text")  # robust text extraction
        docs.append(Document(page_content=text, metadata={"page": i + 1, "source": path}))
    return docs

def main():
    # 1) Load PDF (NO PyPDF used here)
    docs = load_pdf_with_pymupdf(PDF_PATH)

    # Safety: if PDF is scanned, text might be empty
    non_empty = sum(1 for d in docs if d.page_content.strip())
    if non_empty == 0:
        raise RuntimeError("PDF text is empty (likely scanned image PDF). Use OCR (Fix 3 below).")

    # 2) Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3) Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4) Store in Chroma
    db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_DIR)
    db.persist()

    print(f"✅ Ingest complete. Pages loaded: {len(docs)}, non-empty pages: {non_empty}, chunks: {len(chunks)}")
    print(f"✅ Vector DB saved at: {DB_DIR}")

if __name__ == "__main__":
    main()
