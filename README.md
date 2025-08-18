# 🤖 Jake Cosme's Personal RAG Chatbot - "The Recipe" Life Story AI

Welcome to Jake Cosme's personal AI chatbot! This RAG (Retrieval-Augmented Generation) chatbot is trained on "The Recipe" - Jake's inspiring life story and journey. Ask questions about Jake's experiences, insights, and wisdom.

## 🧠 What is this chatbot?

This is **Jake Cosme's Personal RAG Chatbot** trained on "The Recipe" - his life story book.

**RAG = Retrieval-Augmented Generation**
- **Retrieval**: Find relevant information from Jake's life story
- **Augmented**: Combine that information with AI knowledge  
- **Generation**: Create helpful answers about Jake's journey and insights

Think of it like having a conversation with Jake himself about his experiences, challenges, and the wisdom he's gained along the way!

## 📁 What's in this project?

### 1. `simple_rag_chatbot.py` - Your Main Chatbot
- **What it does:** Complete RAG chatbot you can chat with
- **What you'll learn:** How AI retrieves and uses information
- **Try it:** `python3 simple_rag_chatbot.py`

### 2. `document_processor.py` - Document Handler
- **What it does:** Reads and processes your documents
- **What you'll learn:** How AI "understands" text
- **Features:** Handles PDF, TXT, and other text files

### 3. `sample_documents/` - Jake's Documents
- **What it contains:** "The Recipe" - Jake Cosme's life story book and other documents
- **What you'll learn:** How Jake's experiences and insights are processed for AI conversations

### 4. `requirements.txt` - Required Libraries
- **What it does:** Lists all the AI libraries we need
- **Install with:** `pip install -r requirements.txt`

## 🚀 How to Set Up Your RAG Chatbot

### 🆓 **FREE VERSION (No API Keys Required!)**

**Don't want to pay for OpenAI?** Use our completely free version!

#### Quick Start (Free):
```bash
pip3 install -r requirements.txt
python3 free_rag_chatbot.py
```

**Free Version Features:**
- ✅ Completely free - no API keys needed
- ✅ Runs entirely on your computer
- ✅ Uses open-source sentence-transformers
- ✅ Same document processing capabilities
- ✅ Vector search and retrieval

**Want smarter AI responses?** Check out `UPGRADE_GUIDE.md` for free AI model options like Ollama and Hugging Face!

### 📤 **Upload Your Own Documents**

You can easily add your own documents to the chatbot:

#### Method 1: During Chat
```bash
python3 free_rag_chatbot.py
# Then type: upload /path/to/your/document.pdf
```

#### Method 2: Upload Helper Script
```bash
python3 upload_document.py /path/to/your/document.pdf
python3 free_rag_chatbot.py
```

#### Method 3: Copy to Sample Documents
```bash
cp /path/to/your/document.pdf sample_documents/
python3 free_rag_chatbot.py
```

**Supported file formats:** PDF, TXT, DOCX
**Large files:** The system handles large documents (100+ pages) by automatically chunking them for optimal search.

---

### 💰 **PREMIUM VERSION (OpenAI GPT)**

For the most advanced AI responses, use the OpenAI version:

#### Step 1: Install Required Libraries
```bash
pip3 install -r requirements.txt
pip3 install openai
```

#### Step 2: Add Your OpenAI API Key
1. Get an API key from OpenAI (openai.com)
2. Create a `.env` file in this folder
3. Add: `OPENAI_API_KEY=your_key_here`

#### Step 3: Add Your Documents
- Put any text files or PDFs in the `sample_documents/` folder
- The chatbot will learn from these documents

#### Step 4: Run Your Chatbot
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

### Sample Questions About Jake's Story:
- "Tell me about Jake's journey"
- "What is The Recipe about?"
- "What challenges did Jake face?"
- "What are Jake's key insights about life?"

### Advanced Questions (with upgraded models):
- "What lessons can I learn from Jake's experiences?"
- "How did Jake overcome obstacles in his life?"
- "What advice would Jake give about pursuing dreams?"
- "What are the main themes in The Recipe?"

## 🎉 What You're Experiencing

- **Personal AI Assistant**: Chat with an AI trained on Jake's life story
- **Semantic Search**: Find relevant parts of Jake's journey based on your questions
- **Life Insights**: Discover wisdom and lessons from Jake's experiences
- **Document Processing**: See how a 128-page book becomes searchable AI knowledge
- **RAG Architecture**: Experience the same technology used by ChatGPT and Claude

## 🔧 Customization Ideas

### Free Version Upgrades:
- **Install Ollama**: Get local LLM models (see `UPGRADE_GUIDE.md`)
- **Try Hugging Face models**: Various free AI models
- **Add more documents**: PDFs, Word docs, web pages
- **Create topic-specific chatbots**: Focus on specific subjects

### Advanced Features:
- Add a web interface
- Implement conversation memory
- Add document summarization
- Create multi-language support
- Export conversation history

**Remember:** You're building the same technology used by ChatGPT, Claude, and other AI assistants!

## 🎯 Next Steps

1. **Start with the free version**: `python3 free_rag_chatbot.py`
2. **Add your own documents**: Put files in `sample_documents/`
3. **Upgrade when ready**: Check `UPGRADE_GUIDE.md` for free AI models
4. **Experiment and learn**: This is professional-level AI technology!

**🚀 You're chatting with Jake Cosme's life story through cutting-edge AI technology!**
