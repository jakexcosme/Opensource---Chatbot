#!/usr/bin/env python3
"""
🚀 Easy Launcher for Free RAG Chatbot
Simple script to run your free RAG chatbot with error checking.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'sentence_transformers',
        'chromadb',
        'numpy',
        'PyPDF2',
        'docx'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n💡 Install with: pip3 install -r requirements.txt")
        return False
    
    return True

def check_documents():
    """Check if sample documents exist."""
    docs_dir = "sample_documents"
    if not os.path.exists(docs_dir):
        print(f"📁 Creating {docs_dir} directory...")
        os.makedirs(docs_dir)
        print("⚠️  No documents found. Add some .txt, .pdf, or .docx files to the sample_documents folder!")
        return False
    
    files = [f for f in os.listdir(docs_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
    if not files:
        print("⚠️  No supported documents found in sample_documents folder!")
        print("💡 Add some .txt, .pdf, or .docx files to get started.")
        return False
    
    print(f"📚 Found {len(files)} document(s) ready to use!")
    return True

def main():
    """Main launcher function."""
    print("🤖 Free RAG Chatbot Launcher")
    print("=" * 40)
    
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed!")
    
    print("\n📖 Checking documents...")
    check_documents()
    
    print("\n🚀 Starting Free RAG Chatbot...")
    print("=" * 40)
    
    try:
        from free_rag_chatbot import main as chatbot_main
        chatbot_main()
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting chatbot: {e}")
        print("💡 Try running: python3 free_rag_chatbot.py")

if __name__ == "__main__":
    main()
