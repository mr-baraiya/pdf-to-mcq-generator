# API Endpoints Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://your-backend.vercel.app
```

---

## Available Endpoints

### 1. Health Check
**GET** `/`

Check if API is running.

**Response:**
```json
{
  "message": "PDF to MCQ Generator API",
  "version": "1.0.0"
}
```

---

### 2. Upload PDF
**POST** `/upload-pdf`

Upload a PDF file and extract text.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file (form field: `file`)

**Response:**
```json
{
  "filename": "sample.pdf",
  "text": "Extracted text content...",
  "blob_url": "https://vercel-blob-url.com/...",
  "status": "success"
}
```

**Errors:**
- `400`: Not a PDF file
- `500`: Upload or extraction failed

---

### 3. Check AI Models Status
**GET** `/ai-status`

Check which AI models are available and configured.

**Response:**
```json
{
  "ollama": {
    "available": true,
    "url": "http://localhost:11434",
    "model": "llama3.2",
    "description": "Local LLM - Free & Private"
  },
  "groq": {
    "available": true,
    "model": "llama-3.3-70b-versatile",
    "description": "Cloud LLM - Fast inference"
  },
  "gemini": {
    "available": true,
    "model": "gemini-pro",
    "description": "Google AI - Advanced understanding"
  },
  "recommended": "ollama"
}
```

**Use this endpoint to:**
- Show available AI models in UI
- Disable buttons for unavailable models
- Show recommended model to user

---

### 4. Ollama Installation Status
**GET** `/ollama-status`

Check if Ollama is installed and get installation instructions.

**Response:**
```json
{
  "os": "linux",
  "installed": false,
  "running": false,
  "can_auto_install": true,
  "installation_instructions": {
    "description": "Install Ollama on Linux",
    "auto_install_available": true,
    "manual_command": "curl -fsSL https://ollama.com/install.sh | sh",
    "steps": [
      "Run: curl -fsSL https://ollama.com/install.sh | sh",
      "Start Ollama: ollama serve",
      "Pull a model: ollama pull llama3.2"
    ]
  },
  "model": "llama3.2",
  "host": "http://localhost:11434"
}
```

**Use this endpoint to:**
- Check if Ollama needs to be installed
- Show installation instructions to users
- Display OS-specific setup steps
- Determine if auto-install is available

---

### 5. Auto-Install Ollama
**POST** `/ollama-install`

Automatically install Ollama (Linux only).

**Response (Already Installed):**
```json
{
  "success": true,
  "message": "Ollama is already installed",
  "installed": true,
  "running": false
}
```

**Response (Installation Success):**
```json
{
  "success": true,
  "message": "Ollama installed successfully! Please start it with: ollama serve"
}
```

**Response (Non-Linux OS):**
```json
{
  "success": false,
  "message": "Auto-install not available for macos",
  "installation_instructions": {
    "description": "Install Ollama on macOS",
    "auto_install_available": false,
    "manual_command": "Download from https://ollama.com/download",
    "steps": [...]
  }
}
```

**Important:**
- Only works on Linux systems (Ubuntu in dev container)
- Takes 2-5 minutes to complete
- Requires internet connection
- macOS/Windows users get manual instructions

**UI Recommendation:**
```javascript
// Show install button only if can_auto_install is true
if (status.os === 'linux' && !status.installed) {
  showInstallButton();
}
```

---

### 6. Start Ollama Service
**POST** `/ollama-start`

Start the Ollama service if it's installed but not running.

**Response (Success):**
```json
{
  "success": true,
  "message": "Ollama service started"
}
```

**Response (Already Running):**
```json
{
  "success": true,
  "message": "Ollama is already running"
}
```

**Errors:**
- `500`: Failed to start Ollama or Ollama not installed

**Use this when:**
- Ollama is installed but `/ai-status` shows it's not available
- User wants to start Ollama without terminal commands
- After installing Ollama with `/ollama-install`

---

## MCQ Generation Endpoints

### 7. Auto Fallback (Recommended for most users)
**POST** `/generate-mcqs`

Automatically tries models in order: **Ollama → Groq → Gemini**

**Request:**
```json
{
  "text": "Your extracted PDF text here...",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [
    {
      "question": "What is the capital of France?",
      "options": ["London", "Paris", "Berlin", "Madrid"],
      "answer": "Paris"
    }
  ],
  "status": "success"
}
```

**When to use:** 
- Default option for users
- Best reliability (automatic fallback)
- No model selection needed

---

### 8. Ollama Only (Local & Free)
**POST** `/generate-mcqs-ollama`

Uses **local Ollama** LLM only. No API costs!

**Request:**
```json
{
  "text": "Your text here...",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [...],
  "status": "success"
}
```

**Errors:**
- `503`: Ollama not running (user needs to start Ollama server)
- `500`: Generation failed

**When to use:**
- User wants privacy (no data sent to cloud)
- User wants free generation (no API costs)
- User has Ollama installed locally

**Prerequisites:**
- Ollama must be running on `localhost:11434`
- User must have downloaded a model (e.g., `llama3.2`)

**UI Recommendation:**
```
✓ Ollama (Local & Free) [Selected]
  ⚠ Requires Ollama running locally
  [Check Status] button
```

---

### 9. Groq Only (Fast Cloud)
**POST** `/generate-mcqs-groq`

Uses **Groq API** with Llama 3.3 70B model. Very fast inference!

**Request:**
```json
{
  "text": "Your text here...",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [...],
  "status": "success"
}
```

**Errors:**
- `500`: API key missing or generation failed

**When to use:**
- Fast generation needed
- Small to medium size documents
- User doesn't have Ollama

**Prerequisites:**
- `GROQ_API_KEY` configured in backend `.env`

**UI Recommendation:**
```
⚡ Groq (Fast Cloud)
  Very fast inference
  Best for quick results
```

---

### 10. Gemini Only (Advanced AI)
**POST** `/generate-mcqs-gemini`

Uses **Google Gemini Pro** model. Best for complex documents.

**Request:**
```json
{
  "text": "Your text here...",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [...],
  "status": "success"
}
```

**Errors:**
- `500`: API key missing or generation failed

**When to use:**
- Complex or technical documents
- Large documents (better understanding)
- When Groq fails or unavailable

**Prerequisites:**
- `GEMINI_API_KEY` configured in backend `.env`

**UI Recommendation:**
```
🧠 Gemini (Advanced AI)
  Best for complex documents
  Better understanding
```

---

## Frontend Integration Examples

### Example 1: Check Available Models on Page Load

```javascript
async function checkAvailableModels() {
  const response = await fetch('http://localhost:8000/ai-status');
  const status = await response.json();
  
  // Update UI based on availability
  if (status.ollama.available) {
    enableOllamaButton();
  }
  if (status.groq.available) {
    enableGroqButton();
  }
  if (status.gemini.available) {
    enableGeminiButton();
  }
  
  // Show recommended model
  highlightModel(status.recommended);
}
```

### Example 2: Generate MCQs with Specific Model

```javascript
async function generateMCQs(text, numQuestions, model = 'auto') {
  // Determine endpoint based on model selection
  const endpoints = {
    'auto': '/generate-mcqs',
    'ollama': '/generate-mcqs-ollama',
    'groq': '/generate-mcqs-groq',
    'gemini': '/generate-mcqs-gemini'
  };
  
  const endpoint = endpoints[model];
  
  const response = await fetch(`http://localhost:8000${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: text,
      num_questions: numQuestions
    })
  });
  
  if (!response.ok) {
    if (response.status === 503) {
      alert('Ollama is not running. Please start Ollama server.');
      return null;
    }
    throw new Error('Generation failed');
  }
  
  const data = await response.json();
  return data.questions;
}
```

### Example 3: Upload PDF and Generate

```javascript
async function uploadAndGenerate(pdfFile, model = 'auto') {
  // Step 1: Upload PDF
  const formData = new FormData();
  formData.append('file', pdfFile);
  
  const uploadResponse = await fetch('http://localhost:8000/upload-pdf', {
    method: 'POST',
    body: formData
  });
  
  const uploadData = await uploadResponse.json();
  
  // Step 2: Generate MCQs with selected model
  const questions = await generateMCQs(uploadData.text, 10, model);
  
  return questions;
}
```

---

## Recommended UI Design

### Model Selection Dropdown/Radio Buttons:

```
Select AI Model:

○ Auto (Recommended) - Smart fallback system
○ Ollama (Local & Free) - Private, no API costs
   └─ Status: ✓ Available / ⚠ Not running
○ Groq (Fast Cloud) - Quick results
○ Gemini (Advanced) - Best for complex docs

[Generate MCQs] button
```

### Or Simple Three-Button Layout:

```
Choose Generation Method:

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  🏠 Local       │  │  ⚡ Fast        │  │  🧠 Advanced   │
│  Ollama         │  │  Groq           │  │  Gemini         │
│  Free & Private │  │  Cloud API      │  │  Cloud API      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Error Handling

### Common Errors:

1. **503 - Service Unavailable**
   - **Cause:** Ollama endpoint called but Ollama not running
   - **Solution:** Show user message to start Ollama or use different model

2. **500 - Internal Server Error**
   - **Cause:** API key missing, generation failed, or invalid input
   - **Solution:** Check error detail in response, show user-friendly message

3. **400 - Bad Request**
   - **Cause:** Invalid file type (not PDF) or invalid parameters
   - **Solution:** Validate file before upload

### Example Error Handling:

```javascript
try {
  const questions = await generateMCQs(text, 10, 'ollama');
} catch (error) {
  if (error.status === 503) {
    showError('Ollama is not running. Please start Ollama or use a different model.');
  } else if (error.status === 500) {
    showError('Generation failed. Please try again or use a different model.');
  } else {
    showError('Something went wrong. Please try again.');
  }
}
```

---

## Environment Variables (Backend)

Frontend developers don't need to worry about these, but they should know:

```env
# Local Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Cloud APIs
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

If any API key is missing, that model will be unavailable (shown in `/ai-status` response).

---

## Notes for Frontend Developers

1. **Always check `/ai-status` first** to know which models are available
2. **Disable buttons** for unavailable models in UI
3. **Show loading states** - Generation can take 5-30 seconds depending on model
4. **Handle 503 errors** gracefully for Ollama (show setup instructions)
5. **Default to "Auto" mode** for best user experience
6. **Add model badges** in UI to show which model was used
7. **Consider adding retry logic** if generation fails

---

## Quick Start for Frontend

```javascript
// 1. Check available models
const status = await fetch('/ai-status').then(r => r.json());

// 2. Upload PDF
const formData = new FormData();
formData.append('file', pdfFile);
const upload = await fetch('/upload-pdf', {
  method: 'POST',
  body: formData
}).then(r => r.json());

// 3. Generate MCQs (auto fallback)
const result = await fetch('/generate-mcqs', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: upload.text,
    num_questions: 10
  })
}).then(r => r.json());

console.log(result.questions);
```

---

Need help? Check the API docs at `http://localhost:8000/docs` (FastAPI auto-generated docs)
