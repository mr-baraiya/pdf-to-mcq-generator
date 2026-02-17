# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. CORS is enabled for all origins.

## Endpoints

### 1. Health Check

Get the API status.

**Request:**
```http
GET /
```

**Response (200):**
```json
{
  "message": "PDF to MCQ Generator API",
  "version": "1.0.0"
}
```

---

### 2. Upload PDF

Upload a PDF file and extract text from it.

**Request:**
```http
POST /upload-pdf
Content-Type: multipart/form-data

file: <PDF file>
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | PDF file to upload |

**Response (200):**
```json
{
  "filename": "sample.pdf",
  "text": "Extracted text from the PDF...",
  "status": "success"
}
```

**Error Response (400):**
```json
{
  "detail": "File must be a PDF"
}
```

**Error Response (500):**
```json
{
  "detail": "Error extracting text from PDF: ..."
}
```

---

### 3. Generate MCQs

Generate Multiple Choice Questions from text using Ollama LLM.

**Request:**
```http
POST /generate-mcqs
Content-Type: application/json

{
  "text": "Your text content here...",
  "num_questions": 5
}
```

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| text | string | Yes | - | Text to generate questions from |
| num_questions | integer | No | 5 | Number of questions to generate |

**Response (200):**
```json
{
  "questions": [
    {
      "question": "What is the capital of France?",
      "options": {
        "A": "London",
        "B": "Paris",
        "C": "Berlin",
        "D": "Madrid"
      },
      "answer": "B"
    }
  ],
  "status": "success"
}
```

**Error Response (500):**
```json
{
  "detail": "Error generating MCQs: ..."
}
```

---

## Example Usage

### With cURL

**Upload PDF:**
```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -F "file=@sample.pdf"
```

**Generate MCQs:**
```bash
curl -X POST "http://localhost:8000/generate-mcqs" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "num_questions": 5
  }'
```

### With Python (requests)

```python
import requests

# Upload PDF
files = {'file': open('sample.pdf', 'rb')}
response = requests.post('http://localhost:8000/upload-pdf', files=files)
text = response.json()['text']

# Generate MCQs
data = {
    'text': text,
    'num_questions': 5
}
response = requests.post('http://localhost:8000/generate-mcqs', json=data)
mcqs = response.json()['questions']
```

### With JavaScript (Fetch)

```javascript
// Upload PDF
const formData = new FormData();
formData.append('file', pdfFile);

const uploadResponse = await fetch('http://localhost:8000/upload-pdf', {
  method: 'POST',
  body: formData
});
const { text } = await uploadResponse.json();

// Generate MCQs
const mcqResponse = await fetch('http://localhost:8000/generate-mcqs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: text,
    num_questions: 5
  })
});
const { questions } = await mcqResponse.json();
```

---

## Interactive API Documentation

Once the API is running, visit:

```
http://localhost:8000/docs
```

This provides an interactive Swagger UI where you can test all endpoints directly.

---

## Troubleshooting

### "Ollama connection refused"
- Make sure Ollama is running: `ollama pull mistral`
- Check that Ollama is accessible at `http://localhost:11434`

### "Model not found"
- Pull the model: `ollama pull mistral`

### "CORS Error"
- CORS is enabled by default for all origins in development
- For production, update CORS settings in `backend/app.py`

### Slow MCQ Generation
- The first request may be slow as the model loads
- Subsequent requests should be faster
- Consider using a smaller model if performance is critical
