import os
import PyPDF2
from docx import Document
from typing import List, Dict
import re

class DocumentProcessor:
    """
    Processes different types of documents for RAG chatbot.
    Handles PDF, TXT, and DOCX files.
    """
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.pdf', '.docx']
    
    def load_documents(self, folder_path: str) -> List[Dict[str, str]]:
        """
        Load all supported documents from a folder.
        
        Args:
            folder_path: Path to folder containing documents
            
        Returns:
            List of dictionaries with 'content' and 'source' keys
        """
        documents = []
        
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} doesn't exist. Creating it...")
            os.makedirs(folder_path)
            return documents
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                extension = os.path.splitext(filename)[1].lower()
                
                if extension in self.supported_extensions:
                    try:
                        content = self._extract_text(file_path, extension)
                        if content.strip():  # Only add non-empty documents
                            documents.append({
                                'content': content,
                                'source': filename
                            })
                            print(f"✅ Loaded: {filename}")
                        else:
                            print(f"⚠️  Empty file: {filename}")
                    except Exception as e:
                        print(f"❌ Error loading {filename}: {str(e)}")
                else:
                    print(f"⚠️  Unsupported file type: {filename}")
        
        print(f"\n📚 Total documents loaded: {len(documents)}")
        return documents
    
    def _extract_text(self, file_path: str, extension: str) -> str:
        """Extract text from different file types."""
        
        if extension == '.txt':
            return self._extract_from_txt(file_path)
        elif extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension == '.docx':
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end < len(text):
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def process_documents(self, folder_path: str) -> List[Dict[str, str]]:
        """
        Complete document processing pipeline.
        
        Args:
            folder_path: Path to documents folder
            
        Returns:
            List of processed document chunks with metadata
        """
        documents = self.load_documents(folder_path)
        processed_chunks = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                processed_chunks.append({
                    'content': chunk,
                    'source': doc['source'],
                    'chunk_id': i
                })
        
        print(f"📄 Total chunks created: {len(processed_chunks)}")
        return processed_chunks

if __name__ == "__main__":
    processor = DocumentProcessor()
    
    sample_folder = "sample_documents"
    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)
        print(f"Created {sample_folder} folder. Add your documents there!")
    
    chunks = processor.process_documents(sample_folder)
    
    if chunks:
        print(f"\n📋 Sample chunk preview:")
        print(f"Source: {chunks[0]['source']}")
        print(f"Content: {chunks[0]['content'][:200]}...")
    else:
        print("\n💡 Add some documents to the sample_documents folder to test!")
