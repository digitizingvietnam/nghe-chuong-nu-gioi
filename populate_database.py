"""
populate_database.py

Pinecone vector database construction and update pipeline.

This script builds and maintains a Pinecone vector database for the RAG system.
It migrates data from the previous Chroma implementation to Pinecone with
improved metadata structure and namespace organization.

Pipeline:
1. Load structured data from CSV files
2. Convert rows into Document objects with metadata
3. Split documents into overlapping chunks
4. Generate embeddings for each chunk
5. Upsert embeddings into Pinecone with proper namespaces

Metadata structure:
- book-title: Title of the source book/publication
- page-number: Page number in the source
- author: Author name (blank if unknown)
- chapter: Chapter name/number (blank if unknown)

Requirements:
- OPENAI_API_KEY
- PINECONE_API_KEY
"""

import time
import argparse
import os
import pandas as pd
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from utils.embedding import get_embedding_function
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PINECONE_INDEX_NAME = "digitizing-vietnam"  # Shared index for all projects
PROJECT_NAMESPACE = "nghe-chuong-nu-gioi"  # Unique namespace for this project
DATA_PATH = "data"

embedding_function = get_embedding_function()
test_embedding = embedding_function.embed_query("test")
EMBEDDING_DIMENSION = len(test_embedding)


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true",
                        help="Delete all vectors in the namespace before uploading.")
    args = parser.parse_args()

    # Initialize Pinecone
    print("🔌 Connecting to Pinecone...")
    pc = initialize_pinecone()
    index = pc.Index(PINECONE_INDEX_NAME)

    if args.reset:
        print(f"✨ Clearing namespace '{PROJECT_NAMESPACE}'...")
        index.delete(namespace=PROJECT_NAMESPACE, delete_all=True)

    # Load and process documents
    print("📄 Loading documents...")
    documents = load_documents()
    print(f"📄 Loaded {len(documents)} documents.")

    print("✂️ Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks.")

    print("📝 Uploading to Pinecone...")
    upload_to_pinecone(index, chunks)

    end_time = time.time()
    print(f"✅ Total running time: {end_time - start_time:.2f} seconds")


def initialize_pinecone():
    """Initialize Pinecone client and create index if needed."""
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in .env file")

    pc = Pinecone(api_key=api_key)

    # Create index if it doesn't exist
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"📦 Creating new index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("✅ Index created successfully")
    else:
        print(f"✅ Using existing index '{PINECONE_INDEX_NAME}'")

    return pc


def load_documents():
    """Load CSV files and convert to Document objects with metadata."""
    documents = []

    for file_name in os.listdir(DATA_PATH):
        if not file_name.endswith(".csv"):
            continue

        file_path = os.path.join(DATA_PATH, file_name)
        try:
            df = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')

            for _, row in df.iterrows():
                # Extract metadata from CSV columns
                metadata = {
                    "book-title": row.get("Tên sách", row.get("Title", "")),
                    "page-number": str(row.get("Trang", row.get("Page", ""))),
                    "author": row.get("Tác giả", row.get("Author", "")),
                    "chapter": row.get("Chương", row.get("Chapter", "")),
                    "source": file_name
                }

                # Clean metadata: convert NaN to empty string
                metadata = {k: (v if pd.notna(v) else "")
                            for k, v in metadata.items()}

                # Get content from 'Nội dung' or the last column
                if 'Nội dung' in df.columns:
                    content = row.get('Nội dung', '')
                else:
                    content = row.iloc[-1]

                content = str(content) if pd.notna(content) else ""

                if content.strip():  # Only add non-empty content
                    document = Document(
                        page_content=content,
                        metadata=metadata
                    )
                    documents.append(document)

        except Exception as e:
            print(f"⚠️ Error loading {file_name}: {e}")
            continue

    return documents


def split_documents(documents: list[Document]):
    """Split documents into smaller chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = []
    for doc in tqdm(documents, desc="Splitting documents", unit="doc"):
        chunks.extend(text_splitter.split_documents([doc]))

    return chunks


def upload_to_pinecone(index, chunks: list[Document], batch_size=100):
    """Upload document chunks to Pinecone with embeddings."""
    embedding_function = get_embedding_function()

    # Prepare vectors
    vectors = []
    for i, chunk in enumerate(tqdm(chunks, desc="Generating embeddings", unit="chunk")):
        # Generate unique ID
        vector_id = f"{PROJECT_NAMESPACE}-{i}"

        # Get embedding
        embedding = embedding_function.embed_query(chunk.page_content)

        # Prepare metadata
        metadata = {
            "text": chunk.page_content,
            "book-title": chunk.metadata.get("book-title", ""),
            "page-number": chunk.metadata.get("page-number", ""),
            "author": chunk.metadata.get("author", ""),
            "chapter": chunk.metadata.get("chapter", ""),
            "source": chunk.metadata.get("source", "")
        }

        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": metadata
        })

        # Upload in batches
        if len(vectors) >= batch_size:
            index.upsert(vectors=vectors, namespace=PROJECT_NAMESPACE)
            vectors = []

    # Upload remaining vectors
    if vectors:
        index.upsert(vectors=vectors, namespace=PROJECT_NAMESPACE)

    print(
        f"✅ Uploaded {len(chunks)} vectors to namespace '{PROJECT_NAMESPACE}'")

    # Print stats
    stats = index.describe_index_stats()
    print(f"📊 Total vectors in index: {stats.total_vector_count}")
    if PROJECT_NAMESPACE in stats.namespaces:
        ns_count = stats.namespaces[PROJECT_NAMESPACE].vector_count
        print(f"📊 Vectors in '{PROJECT_NAMESPACE}': {ns_count}")


if __name__ == "__main__":
    main()
