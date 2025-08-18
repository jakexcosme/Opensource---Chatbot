import os
import sys
from typing import List, Dict, Optional
from dotenv import load_dotenv
import openai
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from document_processor import DocumentProcessor

load_dotenv()

class SimpleRAGChatbot:
    """
    A beginner-friendly RAG (Retrieval-Augmented Generation) chatbot.
    
    This chatbot can answer questions using your own documents by:
    1. Finding relevant document chunks (Retrieval)
    2. Using those chunks to generate answers (Generation)
    """
    
    def __init__(self, documents_folder: str = "sample_documents"):
        """Initialize the RAG chatbot."""
        print("🤖 Initializing RAG Chatbot...")
        
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            print("❌ OpenAI API key not found!")
            print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
            sys.exit(1)
        
        openai.api_key = self.openai_api_key
        
        self.documents_folder = documents_folder
        self.doc_processor = DocumentProcessor()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.chroma_client = chromadb.Client()
        self.collection_name = "document_chunks"
        
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
            print("📚 Using existing document collection")
        except:
            self.collection = self.chroma_client.create_collection(self.collection_name)
            print("📚 Created new document collection")
        
        self.load_documents()
        
        self.conversation_history = []
        
        print("✅ RAG Chatbot ready!")
    
    def load_documents(self):
        """Load and process documents into the vector database."""
        print(f"\n📖 Loading documents from {self.documents_folder}...")
        
        document_chunks = self.doc_processor.process_documents(self.documents_folder)
        
        if not document_chunks:
            print("⚠️  No documents found! Add some documents to get started.")
            print(f"   Put .txt, .pdf, or .docx files in the '{self.documents_folder}' folder")
            return
        
        existing_count = self.collection.count()
        if existing_count > 0:
            print(f"📊 Found {existing_count} existing chunks in database")
            response = input("Do you want to reload documents? (y/n): ").lower()
            if response != 'y':
                return
            else:
                self.chroma_client.delete_collection(self.collection_name)
                self.collection = self.chroma_client.create_collection(self.collection_name)
        
        print("🔄 Creating embeddings for document chunks...")
        
        for i, chunk in enumerate(document_chunks):
            embedding = self.embedding_model.encode(chunk['content']).tolist()
            
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk['content']],
                metadatas=[{
                    'source': chunk['source'],
                    'chunk_id': chunk['chunk_id']
                }],
                ids=[f"chunk_{i}"]
            )
            
            if (i + 1) % 10 == 0:
                print(f"   Processed {i + 1}/{len(document_chunks)} chunks")
        
        print(f"✅ Successfully loaded {len(document_chunks)} document chunks!")
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Find the most relevant document chunks for a query.
        
        Args:
            query: User's question
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
        query_embedding = self.embedding_model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        relevant_chunks = []
        for i in range(len(results['documents'][0])):
            relevant_chunks.append({
                'content': results['documents'][0][i],
                'source': results['metadatas'][0][i]['source'],
                'chunk_id': results['metadatas'][0][i]['chunk_id'],
                'distance': results['distances'][0][i] if 'distances' in results else 0
            })
        
        return relevant_chunks
    
    def generate_answer(self, query: str, relevant_chunks: List[Dict]) -> str:
        """
        Generate an answer using OpenAI GPT and relevant document chunks.
        
        Args:
            query: User's question
            relevant_chunks: Relevant document chunks from retrieval
            
        Returns:
            Generated answer
        """
        context = "\n\n".join([
            f"Source: {chunk['source']}\nContent: {chunk['content']}"
            for chunk in relevant_chunks
        ])
        
        system_prompt = """You are a helpful AI assistant that answers questions based on provided documents. 
        
        Instructions:
        1. Use ONLY the information from the provided documents to answer questions
        2. If the documents don't contain relevant information, say so clearly
        3. Always cite which document(s) you used for your answer
        4. Be concise but comprehensive
        5. If asked about something not in the documents, explain that you can only answer based on the provided documents
        """
        
        user_prompt = f"""Based on the following documents, please answer this question: {query}

        Documents:
        {context}
        
        Question: {query}
        
        Answer:"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}"
    
    def chat(self, query: str) -> Dict[str, any]:
        """
        Main chat function that handles the complete RAG pipeline.
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        print(f"\n🔍 Searching for relevant information...")
        
        relevant_chunks = self.retrieve_relevant_chunks(query)
        
        if not relevant_chunks:
            return {
                'answer': "I couldn't find any relevant information in your documents to answer this question.",
                'sources': [],
                'chunks_used': 0
            }
        
        print(f"📄 Found {len(relevant_chunks)} relevant chunks")
        
        print("🤖 Generating answer...")
        answer = self.generate_answer(query, relevant_chunks)
        
        sources = list(set([chunk['source'] for chunk in relevant_chunks]))
        
        response = {
            'answer': answer,
            'sources': sources,
            'chunks_used': len(relevant_chunks),
            'relevant_chunks': relevant_chunks
        }
        
        self.conversation_history.append({
            'query': query,
            'response': response
        })
        
        return response
    
    def print_response(self, response: Dict[str, any]):
        """Pretty print the chatbot response."""
        print("\n" + "="*60)
        print("🤖 CHATBOT ANSWER:")
        print("="*60)
        print(response['answer'])
        print("\n" + "-"*60)
        print(f"📚 Sources used: {', '.join(response['sources'])}")
        print(f"📊 Chunks analyzed: {response['chunks_used']}")
        print("-"*60)
    
    def run_interactive_chat(self):
        """Run the interactive chat loop."""
        print("\n" + "="*60)
        print("🎉 Welcome to your RAG Chatbot!")
        print("="*60)
        print("Ask me anything about your documents!")
        print("Type 'quit' to exit, 'help' for commands")
        print("-"*60)
        
        while True:
            try:
                query = input("\n💬 You: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                
                elif query.lower() == 'help':
                    self.show_help()
                    continue
                
                elif query.lower() == 'sources':
                    self.show_sources()
                    continue
                
                elif query.lower() == 'history':
                    self.show_history()
                    continue
                
                elif not query:
                    print("Please enter a question!")
                    continue
                
                response = self.chat(query)
                self.print_response(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def show_help(self):
        """Show available commands."""
        print("\n📋 Available commands:")
        print("  help     - Show this help message")
        print("  sources  - Show loaded document sources")
        print("  history  - Show conversation history")
        print("  quit     - Exit the chatbot")
        print("\n💡 Example questions:")
        print("  - What is the main topic of the documents?")
        print("  - Summarize the key points")
        print("  - Tell me about [specific topic]")
    
    def show_sources(self):
        """Show information about loaded documents."""
        count = self.collection.count()
        print(f"\n📚 Document Database Info:")
        print(f"  Total chunks: {count}")
        
        if count > 0:
            sample = self.collection.get(limit=10)
            sources = set()
            for metadata in sample['metadatas']:
                sources.add(metadata['source'])
            
            print(f"  Documents loaded:")
            for source in sorted(sources):
                print(f"    - {source}")
    
    def show_history(self):
        """Show conversation history."""
        if not self.conversation_history:
            print("\n📝 No conversation history yet!")
            return
        
        print(f"\n📝 Conversation History ({len(self.conversation_history)} exchanges):")
        for i, exchange in enumerate(self.conversation_history[-5:], 1):  # Show last 5
            print(f"\n{i}. Q: {exchange['query'][:100]}...")
            print(f"   A: {exchange['response']['answer'][:100]}...")

def main():
    """Main function to run the RAG chatbot."""
    try:
        chatbot = SimpleRAGChatbot()
        
        chatbot.run_interactive_chat()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting chatbot: {str(e)}")
        print("\n💡 Make sure you have:")
        print("  1. Installed requirements: pip install -r requirements.txt")
        print("  2. Added OpenAI API key to .env file")
        print("  3. Added documents to sample_documents folder")

if __name__ == "__main__":
    main()
