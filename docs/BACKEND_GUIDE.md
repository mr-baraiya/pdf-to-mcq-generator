# Backend Development Guide

## Project Overview

FastAPI-based REST API for generating Multiple Choice Questions from PDF documents using Ollama LLM. This guide covers architecture, endpoints, and development practices.

## Technologies

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **PyPDF2** - PDF text extraction
- **Ollama** - Local LLM inference
- **Pydantic** - Data validation
- **Python-multipart** - File upload handling

## Project Structure

```
backend/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore
└── src/
    ├── pdf/
    │   ├── __init__.py
    │   └── extractor.py      # PDF processing logic
    ├── llm/
    │   ├── __init__.py
    │   └── mcq_generator.py  # MCQ generation logic
    └── utils/
        ├── __init__.py
        └── blob_storage.py   # Vercel Blob integration
```

## Core Modules

### app.py - FastAPI Application

Main application file containing:

#### Setup
```python
app = FastAPI(title="PDF to MCQ Generator API", version="1.0.0")
app.add_middleware(CORSMiddleware, ...)  # CORS configuration
```

#### Data Models (Pydantic)

```python
class MCQRequest(BaseModel):
    text: str
    num_questions: int = 5

class MCQResponse(BaseModel):
    questions: list
    status: str
```

#### Endpoints

1. **GET /** - Health check
2. **POST /upload-pdf** - Upload and extract PDF
3. **POST /generate-mcqs** - Generate questions from text

### src/pdf/extractor.py - PDF Extraction

Handles PDF text extraction:

```python
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()
```

**Features:**
- Handles multi-page PDFs
- Error handling for corrupted files
- Returns clean text

**Limitations:**
- Scanned PDFs (images) won't extract text
- Complex layouts may have formatting issues

### src/llm/mcq_generator.py - MCQ Generation

Generates questions using Ollama:

```python
def generate_mcqs(text: str, num_questions: int = 5) -> list:
    """
    Generate MCQs using Ollama LLM
    """
    response = ollama.generate(
        model="mistral",
        prompt=prompt,
        stream=False,
    )
    questions = json.loads(response['response'])
    return questions
```

**Prompt Engineering:**
- Instructs model to output JSON
- Specifies question count
- Defines expected structure

**Error Handling:**
- Regex fallback for JSON parsing
- Graceful error messages

### src/utils/blob_storage.py - Vercel Blob Integration

Handles cloud storage of PDFs:

```python
async def upload_pdf_to_blob(file_content: bytes, filename: str) -> dict:
    """Upload PDF to Vercel Blob storage"""
    
async def download_pdf_from_blob(blob_url: str) -> bytes:
    """Download PDF from Vercel Blob"""
    
async def delete_pdf_from_blob(blob_url: str) -> bool:
    """Delete PDF from Vercel Blob"""
```

**Features:**
- Async upload/download operations
- Automatic authentication with token
- Error handling and logging
- Optional cloud storage (can be disabled)

For detailed Vercel Blob setup, see [docs/VERCEL_BLOB_SETUP.md](../VERCEL_BLOB_SETUP.md)

## API Endpoints

### 1. GET /

**Purpose:** Health check and version info

**Response:**
```json
{
  "message": "PDF to MCQ Generator API",
  "version": "1.0.0"
}
```

---

### 2. POST /upload-pdf

**Purpose:** Upload PDF and extract text

**Request:**
```
Content-Type: multipart/form-data
file: <PDF binary>
```

**Response (200):**
```json
{
  "filename": "document.pdf",
  "text": "Extracted text...",
  "status": "success"
}
```

**Error Responses:**
- 400: Invalid file type
- 500: Extraction error

**Implementation Flow:**
```
1. Receive file
2. Validate MIME type
3. Save temporarily
4. Extract text with PyPDF2
5. Clean up temp file
6. Return extracted text
```

---

### 3. POST /generate-mcqs

**Purpose:** Generate MCQs from text

**Request:**
```json
{
  "text": "Content to generate questions from",
  "num_questions": 5
}
```

**Response (200):**
```json
{
  "questions": [
    {
      "question": "What is X?",
      "options": {
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
      },
      "answer": "B"
    }
  ],
  "status": "success"
}
```

**Error Responses:**
- 500: MCQ generation error

**Implementation Flow:**
```
1. Validate request data
2. Build dynamic prompt
3. Call Ollama API
4. Parse JSON response
5. Handle parsing errors
6. Return structured MCQs
```

## Configuration

### Environment Variables (.env)

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for production)
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production:
```python
allow_origins=["https://yourdomain.com"],
```

## Development Setup

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
python app.py
```

Server starts at: `http://localhost:8000`

### Development with Auto-reload

```bash
pip install python-dotenv
python app.py --reload
```

Or use:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/

# Upload PDF
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@sample.pdf"

# Generate MCQs
curl -X POST http://localhost:8000/generate-mcqs \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "num_questions": 3}'
```

### Testing with Python

```python
import requests

# Test upload
files = {'file': open('sample.pdf', 'rb')}
response = requests.post('http://localhost:8000/upload-pdf', files=files)
print(response.json())

# Test MCQ generation
data = {'text': 'Sample text', 'num_questions': 3}
response = requests.post('http://localhost:8000/generate-mcqs', json=data)
print(response.json())
```

### Unit Testing with Pytest

```bash
pip install pytest pytest-asyncio httpx

# Create test_app.py
pytest test_app.py -v
```

Example test:
```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
```

## Extending the Backend

### Adding a New Endpoint

```python
@app.post("/your-endpoint")
async def your_endpoint(request: YourRequest):
    """Endpoint description"""
    try:
        result = process_data(request.data)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Creating a New Module

1. Create `src/your_module/` directory
2. Add `__init__.py`
3. Add implementation file
4. Import in `app.py`

### Integrating Different LLM Models

```python
# In mcq_generator.py
def generate_mcqs(text: str, num_questions: int = 5, model: str = "mistral"):
    response = ollama.generate(
        model=model,  # Support multiple models
        prompt=prompt,
        stream=False,
    )
```

## Performance & Optimization

### Request/Response Optimization

```python
# Limit text size
MAX_TEXT_SIZE = 50000  # characters

@app.post("/generate-mcqs")
async def generate_mcqs_endpoint(request: MCQRequest):
    if len(request.text) > MAX_TEXT_SIZE:
        raise HTTPException(400, "Text too large")
```

### Async Processing

```python
import asyncio

@app.post("/async-endpoint")
async def async_endpoint(request: Request):
    # Run CPU-intensive task in thread pool
    result = await asyncio.to_thread(cpu_intensive_function, request.data)
    return result
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def extract_text_cached(pdf_path: str) -> str:
    return extract_text_from_pdf(pdf_path)
```

## Error Handling

### Custom Error Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/generate-mcqs")
async def generate_mcqs_endpoint(request: MCQRequest):
    logger.info(f"Generating {request.num_questions} MCQs")
    try:
        # ... code ...
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(500, str(e))
```

## Deployment

### Local Production

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment-Specific Configuration

```python
import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    app.add_middleware(CORSMiddleware, allow_origins=["https://yourdomain.com"])
else:
    app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

## Common Issues & Solutions

### "Ollama connection refused"
- Ensure Ollama is running
- Check http://localhost:11434 is accessible
- Set correct OLLAMA_HOST in .env

### "Model not found"
```bash
ollama pull mistral
ollama list  # verify installed models
```

### "Slow MCQ generation"
- First request loads model (normal)
- Use stream=False for complete responses
- GPU acceleration available with `ollama --gpus 1`

### "Out of memory"
- Use smaller model: `ollama pull neural-chat`
- Limit concurrent requests
- Increase server RAM

## Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.debug(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
```

### FastAPI Debug Mode

```python
app = FastAPI(debug=True)
```

### Visit Docs
- OpenAPI (Swagger): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io)
