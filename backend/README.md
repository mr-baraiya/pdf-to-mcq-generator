# Backend - PDF to MCQ Generator API

This is the backend API for the PDF to MCQ Generator application, built with FastAPI.

## Directory Structure

```
backend/
├── api/                    # Main API package
│   ├── config.py          # Configuration settings
│   ├── handlers.py        # Request handlers
│   ├── index.py          # Main FastAPI application
│   ├── models.py         # Pydantic models
│   ├── routes.py         # API routes
│   ├── llm/              # LLM integration
│   ├── pdf/              # PDF processing
│   └── utils/            # Utility functions
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
└── .env                  # Environment variables (not in git)
```

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

3. **Run the development server:**
   ```bash
   python -m uvicorn index:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

See `.env.example` for required environment variables:
- `OLLAMA_HOST`: Ollama API host (for local LLM)
- `OLLAMA_MODEL`: Ollama model name
- `GROQ_API_KEY`: Groq API key (for cloud AI)
- `GEMINI_API_KEY`: Google Gemini API key
- `FRONTEND_URL`: Frontend URL for CORS
- `VERCEL_BLOB_READ_WRITE_TOKEN`: Vercel Blob storage token
- `VERCEL_BLOB_STORE_ID`: Vercel Blob store ID

## API Endpoints

### Core Endpoints
- `GET /` - Health check endpoint
- `POST /upload-pdf` - Upload PDF file and extract text
- `GET /ai-status` - Check which AI models are available

### MCQ Generation Endpoints (Choose Your Model!)

**Auto Fallback (Recommended):**
- `POST /generate-mcqs` - Automatic fallback (Ollama → Groq → Gemini)

**Specific Models:**
- `POST /generate-mcqs-ollama` - Use local Ollama (free & private)
- `POST /generate-mcqs-groq` - Use Groq API (fast cloud)
- `POST /generate-mcqs-gemini` - Use Gemini API (advanced)

**Why multiple endpoints?**
Frontend developers can now choose which AI model to use, giving users control over:
- Privacy (local Ollama)
- Speed (Groq)
- Quality (Gemini)
- Cost (free local vs API)

See **[API_ENDPOINTS.md](API_ENDPOINTS.md)** for detailed documentation and frontend integration examples.

## Deployment

The backend can be deployed to Vercel using the included `vercel.json` configuration.

```bash
vercel deploy
```
