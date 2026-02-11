"""
Build ChromaDB vector database from invoice chunks
"""
import json
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from pathlib import Path


def build_invoice_vectordb(
    chunks_file: str = "data/chunks.json",
    db_path: str = "./chroma_db",
    collection_name: str = "invoices_collection",
    embedding_model: str = "all-MiniLM-L6-v2",
    batch_size: int = 32
):
    """
    Build ChromaDB from invoice chunks
    """
    print(f"Building invoice vector database...")
    
    # Load chunks
    print(f"Loading chunks from {chunks_file}")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"Total invoices: {len(chunks)}")
    
    # Initialize embedding model
    print(f"Loading embedding model: {embedding_model}")
    embedder = SentenceTransformer(embedding_model)
    
    # Initialize ChromaDB
    print(f"Initializing ChromaDB at {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    
    # Delete collection if exists
    try:
        client.delete_collection(name=collection_name)
        print("Deleted existing collection")
    except:
        pass
    
    # Create collection
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Process in batches
    print(f"⚡ Generating embeddings and storing in ChromaDB...")
    
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i+batch_size]
        
        ids = [chunk["id"] for chunk in batch]
        texts = [chunk["text"] for chunk in batch]
        
        # Prepare metadata (ChromaDB doesn't support nested dicts well)
        metadatas = []
        for chunk in batch:
            meta = {
                "file_name": chunk["metadata"]["file_name"],
                "source_index": chunk["metadata"]["source_index"],
                "has_image": chunk["metadata"]["has_image"]
            }
            metadatas.append(meta)
        
        # Generate embeddings
        embeddings = embedder.encode(texts, show_progress_bar=False)
        
        # Add to ChromaDB
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )
    
    print(f"\nInvoice vector database built successfully!")
    print(f"Location: {db_path}")
    print(f"Collection: {collection_name}")
    print(f"Total invoices indexed: {collection.count()}")
    
    return collection


if __name__ == "__main__":
    build_invoice_vectordb(
        chunks_file="data/chunks.json",
        db_path="./chroma_db",
        collection_name="invoices_collection",
        embedding_model="all-MiniLM-L6-v2",
        batch_size=32
    )