# RAG Intelligence System

An AI-powered document Q&A system with chatbot interface.

## Features

- **Document Upload**: Upload PDF, TXT, or MD files
- **AI Question Answering**: Ask questions about your uploaded documents using RAG (Retrieval Augmented Generation)
- **Chat Interface**: Modern chatbot UI with orange & white theme
- **Markdown Support**: Bot responses support markdown formatting (bold, code, lists, etc.)

## Tech Stack

- **Backend**: Flask (Python)
- **AI/ML**: LangChain, OpenAI/Azure OpenAI, ChromaDB (Vector Store)
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: AWS S3
- **Charting**: Matplotlib

## Project Structure

```
AWS-RAG_Intelligence-System/
├── app/
│   ├── main.py              # Flask backend API
│   ├── config.py           # Configuration
│   ├── models/
│   │   └── vector_store.py  # ChromaDB vector store
│   ├── services/
│   │   ├── llm_service.py    # LLM service
│   │   └── storage_service.py # AWS S3 storage
│   └── templates/
│       ├── index.html    # Chat UI
│      
├── chromedb/             # Vector database
├── .env                 # Environment variables
├── requirements.txt      # Python dependencies
└── README.md
```

## How It Works

### 1. Document Upload Flow

```
User uploads PDF/TXT file
        ↓
Flask receives file (POST /upload)
        ↓
Document processed with PyPDFLoader/TextLoader
        ↓
Text split into chunks (RecursiveCharacterTextSplitter)
        ↓
Chunks stored in ChromaDB vector store
        ↓
File saved to AWS S3
        ↓
Success response to user
```

### 2. Question Answering Flow

```
User sends question in chat
        ↓
Question sent to /query endpoint
        ↓
Similar documents retrieved from vector store
        ↓
Question + context sent to LLM (Azure OpenAI)
        ↓
LLM generates response
        ↓
Markdown-formatted response displayed in chat
```

### 3. Chart Generation Flow

```
User selects chart type & enters data
        ↓
Data sent to /api/plot-data endpoint
        ↓
Matplotlib generates chart
        ↓
Chart returned as base64 image
        ↓
Displayed in UI
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit `.env` file:

```env
# AWS
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_STORAGE_BUCKET_NAME = "your_bucket"

# Azure OpenAI
Azure_OPENAI_ENDPOINT = "https://your-resource.cognitiveservices.azure.com/"
Azure_OPENAI_KEY = "your_key"
Azure_OPENAI_DEPLOYMENT = "gpt-4"
```

### 3. Run the Application

```bash
python app/main.py
# OR
flask run
```

The app runs on `http://localhost:5000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|------------|
| `/` | GET | Chat UI |
| `/upload` | POST | Upload documents |
| `/query` | POST | Ask questions |

## Frontend Features

- **Chat Interface**: Orange & white themed chatbot
- **File Upload**: Attach PDF/TXT files
- **Markdown Rendering**: Bold, italic, code, lists, etc.
- **Typing Indicator**: Shows while AI is "thinking"
- **Toast Notifications**: Success/error messages
- **Responsive Design**: Works on mobile & desktop

## Supported File Types

- PDF (.pdf)
- Text (.txt)
- Markdown (.md)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name |
| `Azure_OPENAI_ENDPOINT` | Azure OpenAI endpoint |
| `Azure_OPENAI_KEY` | Azure OpenAI API key |
| `Azure_OPENAI_DEPLOYMENT` | Model deployment name |
| `Azure_EMBEDDING_KEY` | Embedding API key |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Send message |
| Shift + Enter | New line |

## License

MIT