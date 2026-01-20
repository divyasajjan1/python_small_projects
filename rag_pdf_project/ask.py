import os
from dotenv import load_dotenv
from importlib_resources import contents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from google import genai


DB_DIR = "chroma_db"

MODEL_NAME = "gemini-2.5-flash" 

SYSTEM_PROMPT = (
    "You are a PDF Q&A assistant. Answer ONLY using the provided context. "
    "If the answer is not in the context, reply exactly: Not found in the document."
)

def main():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

    #llm = genai.GenerativeModel(model_name="gemini-1.5")

    while True:
        q = input("\nAsk a question (or type exit): ").strip()
        if q.lower() in {"exit", "quit"}:
            break

        # 1) Retrieve relevant chunks
        docs = db.similarity_search(q, k=3)
        context = "\n\n---\n\n".join([d.page_content for d in docs])

        # 2) Ask LLM with context
        prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {q}"
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        print("\n✅ Answer:\n", response.text)

        print("\n📌 Sources:")
        for d in docs:
            print(d.metadata)

if __name__ == "__main__":
    main()
