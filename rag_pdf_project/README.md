# RAG PDF Project

This project is a simple **Retrieval-Augmented Generation (RAG)** application that allows users to query information from PDF documents using embeddings and a large language model.

## What it does
- Loads PDF documents
- Splits text into chunks
- Generates embeddings for semantic search
- Retrieves relevant chunks based on a user query
- Uses an LLM to generate answers grounded in the PDF content

## Tech Stack
- Python
- LangChain
- Google Gemini (for embeddings and generation)
- Vector store for similarity search

## How to run
1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt ```

3. Run the main script to query PDFs

## Use case

This project demonstrates how RAG can be used for:

Document Q&A

Knowledge retrieval from PDFs

Building LLM-powered assistants over private data

## Notes

Designed as a learning and portfolio project

Focuses on clarity and core RAG concepts rather than production setup

