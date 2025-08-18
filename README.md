# 🤖 My First RAG Chatbot - AI Document Q&A System

Welcome to your first AI chatbot project! This RAG (Retrieval-Augmented Generation) chatbot can answer questions using your own documents.

## 🧠 What is RAG?

**RAG = Retrieval-Augmented Generation**
- **Retrieval**: Find relevant information from your documents
- **Augmented**: Combine that information with AI knowledge
- **Generation**: Create a helpful answer using an LLM

Think of it like having a super-smart assistant that can instantly read through all your documents and answer questions about them!

## 📁 What's in this project?

### 1. `simple_rag_chatbot.py` - Your Main Chatbot
- **What it does:** Complete RAG chatbot you can chat with
- **What you'll learn:** How AI retrieves and uses information
- **Try it:** `python3 simple_rag_chatbot.py`

### 2. `document_processor.py` - Document Handler
- **What it does:** Reads and processes your documents
- **What you'll learn:** How AI "understands" text
- **Features:** Handles PDF, TXT, and other text files

### 3. `sample_documents/` - Example Documents
- **What it contains:** Sample documents to test your chatbot
- **What you'll learn:** How different document types work with RAG

### 4. `requirements.txt` - Required Libraries
- **What it does:** Lists all the AI libraries we need
- **Install with:** `pip install -r requirements.txt`

## 🚀 How to Set Up Your RAG Chatbot

### Step 1: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 2: Add Your OpenAI API Key
1. Get an API key from OpenAI (openai.com)
2. Create a `.env` file in this folder
3. Add: `OPENAI_API_KEY=your_key_here`

### Step 3: Add Your Documents
- Put any text files or PDFs in the `sample_documents/` folder
- The chatbot will learn from these documents

### Step 4: Run Your Chatbot
```bash
python3 simple_rag_chatbot.py
```

## 🎯 How It Works (The Magic Explained!)

1. **Document Processing**: Your documents are split into chunks
2. **Embedding Creation**: Each chunk gets a "fingerprint" (vector)
3. **Vector Storage**: All fingerprints are stored in a database
4. **Question Processing**: Your question gets its own fingerprint
5. **Similarity Search**: Find document chunks similar to your question
6. **LLM Generation**: GPT uses the relevant chunks to answer

## 💡 Cool Features

- **Smart Document Search**: Finds the most relevant information
- **Context-Aware Answers**: Uses your specific documents
- **Multiple File Types**: Works with PDF, TXT, DOCX files
- **Conversation Memory**: Remembers your chat history
- **Source Citations**: Shows which documents were used

## 🤔 Questions to Ask Your Chatbot

- "What is the main topic of document X?"
- "Summarize the key points from my documents"
- "Find information about [specific topic]"
- "What does the document say about [question]?"

## 🎉 What You're Learning

- **Vector Embeddings**: How AI represents text as numbers
- **Semantic Search**: Finding meaning, not just keywords
- **LLM Integration**: Connecting to powerful AI models
- **Document Processing**: Handling different file types
- **RAG Architecture**: The foundation of modern AI assistants

## 🔧 Customization Ideas

- Add more document types (web pages, emails)
- Implement different embedding models
- Add a web interface
- Create specialized chatbots for different topics
- Add conversation export features

**Remember:** You're building the same technology used by ChatGPT, Claude, and other AI assistants!
