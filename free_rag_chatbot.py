#!/usr/bin/env python3
"""
🤖 Free RAG Chatbot - No API Keys Required!
Uses open-source models that run locally on your computer.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
    import numpy as np
    from document_processor import DocumentProcessor
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("📦 Please install with: pip3 install -r requirements.txt")
    sys.exit(1)

class JakeCosmeRAGChatbot:
    """
    Jake Cosme's Personal RAG Chatbot - trained on "The Recipe" life story.
    Uses completely free, open-source models. No API keys required!
    """
    
    def __init__(self, documents_dir: str = "sample_documents"):
        """Initialize the free RAG chatbot."""
        print("🚀 Initializing Jake Cosme's RAG Chatbot...")
        print("📖 Trained on 'The Recipe' - Jake Cosme's life story")
        print("📚 This may take a moment to download models the first time...")
        
        print("🔄 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded!")
        
        print("🔄 Setting up vector database...")
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"description": "Jake Cosme's life story and documents"}
        )
        print("✅ Vector database ready!")
        
        self.documents_dir = documents_dir
        self.doc_processor = DocumentProcessor()
        self.load_documents()
        
        self.response_templates = {
            "greeting": [
                "Hello! I'm Jake Cosme's personal RAG chatbot, trained on 'The Recipe' - his life story.",
                "Hi there! Ask me anything about Jake Cosme's journey, experiences, or insights from 'The Recipe'.",
                "Welcome! I'm ready to help you explore Jake Cosme's life story and wisdom."
            ],
            "no_context": [
                "I couldn't find information about that in Jake's story or documents.",
                "That question doesn't seem to match any content from 'The Recipe' or Jake's documents.",
                "I don't have information about that in Jake Cosme's current document collection."
            ]
        }
        
        print("🎉 Jake Cosme's RAG Chatbot is ready!")
        print("📖 Ask me about Jake's life story, experiences, and insights from 'The Recipe'!")
        print("💡 Note: This uses a simple response system. For advanced AI responses,")
        print("   you can upgrade to use Ollama or Hugging Face models (see instructions).")
    
    def load_documents(self):
        """Load and process documents into the vector database."""
        if not os.path.exists(self.documents_dir):
            print(f"📁 Creating documents directory: {self.documents_dir}")
            os.makedirs(self.documents_dir)
            return
        
        print(f"📖 Loading documents from {self.documents_dir}...")
        
        existing_docs = self.collection.get()
        existing_count = len(existing_docs['ids']) if existing_docs['ids'] else 0
        
        if existing_count > 0:
            print(f"📚 Found {existing_count} existing document chunks in database")
            return
        
        documents = self.doc_processor.load_documents(self.documents_dir)
        
        if not documents:
            print("⚠️  No documents found. Add some .txt, .pdf, or .docx files to the sample_documents folder!")
            return
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for doc in documents:
            doc_name = doc['source']
            content = doc['content']
            chunks = self.doc_processor.chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_name}_chunk_{i}"
                all_chunks.append(chunk)
                all_metadatas.append({
                    "source": doc_name,
                    "chunk_index": i,
                    "chunk_length": len(chunk)
                })
                all_ids.append(chunk_id)
        
        if all_chunks:
            print(f"🔄 Creating embeddings for {len(all_chunks)} chunks...")
            embeddings = self.embedding_model.encode(all_chunks).tolist()
            
            self.collection.add(
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            
            print(f"✅ Successfully processed {len(documents)} documents into {len(all_chunks)} chunks!")
    
    def add_uploaded_document(self, file_path: str, source_name: str = None) -> bool:
        """
        Add a single uploaded document to the vector database.
        
        Args:
            file_path: Path to the uploaded file
            source_name: Optional custom name for the document
            
        Returns:
            True if successful, False otherwise
        """
        print(f"📤 Processing uploaded file: {os.path.basename(file_path)}")
        
        document = self.doc_processor.process_single_file(file_path, source_name)
        if not document:
            return False
            
        existing_docs = self.collection.get()
        if existing_docs['ids']:
            existing_sources = [meta['source'] for meta in existing_docs['metadatas']]
            if document['source'] in existing_sources:
                print(f"⚠️  Document '{document['source']}' already exists in database")
                response = input("Do you want to replace it? (y/n): ").lower()
                if response != 'y':
                    return False
                existing_ids = [id for id, meta in zip(existing_docs['ids'], existing_docs['metadatas']) 
                              if meta['source'] == document['source']]
                if existing_ids:
                    self.collection.delete(ids=existing_ids)
                    print(f"🗑️  Removed {len(existing_ids)} existing chunks")
        
        chunks = self.doc_processor.chunk_text(document['content'])
        print(f"📄 Created {len(chunks)} chunks from document")
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document['source']}_chunk_{i}"
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": document['source'],
                "chunk_index": i,
                "chunk_length": len(chunk)
            })
            all_ids.append(chunk_id)
        
        print(f"🔄 Creating embeddings for {len(all_chunks)} chunks...")
        embeddings = self.embedding_model.encode(all_chunks).tolist()
        
        self.collection.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        print(f"✅ Successfully added '{document['source']}' to knowledge base!")
        print(f"   Total chunks in database: {self.collection.count()}")
        return True

    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant document chunks."""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                search_results.append({
                    'content': results['documents'][0][i],
                    'source': results['metadatas'][0][i]['source'],
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
        
        return search_results
    
    def generate_response(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """Generate a response using the retrieved context."""
        if not context_chunks:
            return np.random.choice(self.response_templates["no_context"])
        
        response_parts = []
        response_parts.append(f"Based on your documents, here's what I found about '{query}':\n")
        
        for i, chunk in enumerate(context_chunks[:2], 1):
            source = chunk['source']
            content = chunk['content'][:300] + "..." if len(chunk['content']) > 300 else chunk['content']
            
            response_parts.append(f"\n📄 From {source}:")
            response_parts.append(f"{content}")
        
        if len(context_chunks) > 2:
            response_parts.append(f"\n💡 Found {len(context_chunks)} total relevant sections in your documents.")
        
        return "\n".join(response_parts)
    
    def chat(self, query: str) -> str:
        """Main chat function."""
        if not query.strip():
            return "Please ask me a question about your documents!"
        
        greeting_words = ['hello', 'hi', 'hey', 'greetings']
        if any(word in query.lower() for word in greeting_words):
            return np.random.choice(self.response_templates["greeting"])
        
        context_chunks = self.search_documents(query)
        
        response = self.generate_response(query, context_chunks)
        
        return response

def main():
    """Main function to run the chatbot."""
    print("🤖 Welcome to Jake Cosme's Personal RAG Chatbot!")
    print("=" * 60)
    print("📖 Trained on 'The Recipe' - Jake Cosme's Life Story")
    print("💰 No API keys required - completely free!")
    print("🏠 Runs entirely on your local computer")
    print("💡 Ask about Jake's journey, experiences, and insights")
    print("=" * 60)
    
    try:
        chatbot = JakeCosmeRAGChatbot()
        
        print("\n💬 Chat started! Type 'quit', 'exit', or 'bye' to end.")
        print("🔍 Try asking: 'Tell me about Jake's journey' or 'What is The Recipe about?'")
        print("📤 To upload a file, type: 'upload /path/to/your/file.pdf'")
        print("-" * 60)
        
        while True:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Thanks for exploring Jake Cosme's story! Goodbye!")
                break
            
            if not user_input:
                continue
            
            if user_input.lower().startswith('upload '):
                file_path = user_input[7:].strip()
                if file_path:
                    success = chatbot.add_uploaded_document(file_path)
                    if success:
                        print("🎉 File uploaded successfully! You can now ask questions about it.")
                    else:
                        print("❌ Failed to upload file. Please check the file path and format.")
                else:
                    print("❌ Please provide a file path. Example: upload /path/to/your/book.pdf")
                continue
            
            print("\n🤖 Chatbot: ", end="")
            response = chatbot.chat(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you've installed all requirements: pip3 install -r requirements.txt")

if __name__ == "__main__":
    main()
