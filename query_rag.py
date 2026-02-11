"""
Invoice RAG Query System using ChromaDB + Gemini
"""
import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict


class InvoiceRAG:
    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "invoices_collection",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """Initialize Invoice RAG system"""
        load_dotenv()
        
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel('gemini-2.5-flash')
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)
        
        # Connect to ChromaDB
        print(f"Connecting to ChromaDB: {db_path}")
        client = chromadb.PersistentClient(path=db_path)
        self.collection = client.get_collection(name=collection_name)
        
        print(f"Invoice RAG ready! ({self.collection.count()} invoices indexed)")
    
    def retrieve(self, query: str, n_results: int = 5) -> Dict:
        """Retrieve relevant invoices from vector DB"""
        query_embedding = self.embedder.encode(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        return results
    
    def format_retrieved_context(self, results: Dict) -> str:
        """Format retrieved invoices for LLM"""
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        context_parts = []
        for i, (doc, meta) in enumerate(zip(documents, metadatas), 1):
            context_parts.append(f"--- Invoice {i} ({meta['file_name']}) ---\n{doc}")
        
        return "\n\n".join(context_parts)
    
    def generate_answer(self, query: str, n_results: int = 5) -> str:
        """Full RAG pipeline for invoice queries"""
        print(f"\nQuery: {query}")
        
        # Retrieve relevant invoices
        results = self.retrieve(query, n_results)
        
        documents = results['documents'][0]
        if not documents:
            return "No relevant invoices found in the database."
        
        print(f"Retrieved {len(documents)} relevant invoices")
        
        # Format context
        context = self.format_retrieved_context(results)
        
        # Build prompt
        prompt = f"""You are an invoice analysis assistant. Answer questions based on the invoice data provided.

Invoice Data:
{context}

Question: {query}

Provide a clear, concise answer based on the invoice information above. If the answer requires specific amounts or dates, include them in your response.

Answer:"""
        
        # Generate answer
        print("Generating answer with Gemini...")
        response = self.llm.generate_content(prompt)
        
        return response.text
    
    def chat(self):
        """Interactive chat interface"""
        print("\n" + "="*60)
        print("Invoice RAG System (type 'quit' to exit)")
        print("="*60)
        print("\nExample queries:")
        print("  - What is the total amount for invoice X?")
        print("  - Which invoices are from company Y?")
        print("  - Show me invoices from January 2023")
        print("  - What are the highest value invoices?")
        print("="*60)
        
        while True:
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            try:
                answer = self.generate_answer(query)
                print(f"\nAssistant: {answer}")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def search_invoices(self, query: str, n_results: int = 5) -> List[Dict]:
        """Return structured invoice data (for programmatic use)"""
        results = self.retrieve(query, n_results)
        
        invoices = []
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            invoices.append({
                'file_name': meta['file_name'],
                'content': doc,
                'source_index': meta['source_index']
            })
        
        return invoices


if __name__ == "__main__":
    # Initialize system
    rag = InvoiceRAG(
        db_path="./chroma_db",
        collection_name="invoices_collection",
        embedding_model="all-MiniLM-L6-v2"
    )
    
    # Start interactive chat
    rag.chat()
    
    # OR: Single query
    # answer = rag.generate_answer("What invoices are from Acme Corp?")
    # print(answer)
    
    # OR: Get structured results
    # invoices = rag.search_invoices("invoices over $1000")
    # print(json.dumps(invoices, indent=2))