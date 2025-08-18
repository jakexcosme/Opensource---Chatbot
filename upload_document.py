#!/usr/bin/env python3
"""
📤 Document Upload Helper for Free RAG Chatbot
Simple script to upload documents to your RAG chatbot.
"""

import sys
import os
from free_rag_chatbot import FreeRAGChatbot

def main():
    if len(sys.argv) != 2:
        print("📤 Document Upload Helper")
        print("Usage: python3 upload_document.py <file_path>")
        print("Example: python3 upload_document.py ~/Documents/my_book.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print("🚀 Initializing RAG Chatbot for document upload...")
    try:
        chatbot = FreeRAGChatbot()
        
        print(f"\n📤 Uploading: {os.path.basename(file_path)}")
        success = chatbot.add_uploaded_document(file_path)
        
        if success:
            print("\n🎉 Upload complete! Your document is now part of the knowledge base.")
            print("💬 Run 'python3 free_rag_chatbot.py' to start chatting about your document!")
        else:
            print("\n❌ Upload failed. Please check the file format and try again.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you've installed all requirements: pip3 install -r requirements.txt")

if __name__ == "__main__":
    main()
