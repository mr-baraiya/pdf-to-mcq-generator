# Configuration & Customization Guide

This guide explains how to configure and customize the PDF to MCQ Generator for your specific needs.

---

## 🔧 Environment Configuration

### Backend Configuration (.env)

Located at: `backend/.env`

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

### Available Ollama Models

You can use any Ollama model. Popular options:

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| **mistral** | 7B | ⚡ Fast | Very Good | `ollama pull mistral` |
| **llama2** | 7B | ⚡ Fast | Good | `ollama pull llama2` |
| **neural-chat** | 7B | ⚡⚡ Very Fast | Good | `ollama pull neural-chat` |
| **dolphin-mixtral** | 46B | 🐢 Slow | Excellent | `ollama pull dolphin-mixtral` |
| **llama2-uncensored** | 7B | ⚡ Fast | Good | `ollama pull llama2-uncensored` |

Change model in `backend/src/llm/mcq_generator.py`:

```python
def generate_mcqs(text: str, num_questions: int = 5, model: str = "mistral"):
    response = ollama.generate(
        model=model,  # Change here
        # ...
    )
```

---

## 🎨 Frontend Customization

### Color Scheme

Modify `frontend/src/App.css`:

```css
/* Current colors */
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #28a745;
  --danger: #dc3545;
  --warning: #fbbf24;
}
```

Change these values to customize colors:

```css
:root {
  --primary-gradient: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
  --primary: #FF6B6B;
  --secondary: #FF8E53;
  --success: #4CAF50;
  --danger: #F44336;
  --warning: #FFC107;
}
```

### Font Size & Typography

In `frontend/src/App.css`:

```css
.app-header h1 {
  font-size: 2.5rem;  /* Change main title size */
}

.generate-section h2 {
  font-size: 1.5rem;  /* Change section heading size */
}
```

### Button Styling

In `frontend/src/App.css`:

```css
.btn-primary {
  padding: 12px 28px;           /* Change padding */
  font-size: 1rem;              /* Change font size */
  border-radius: 8px;           /* Change border radius */
  background: linear-gradient(...);  /* Change colors */
}
```

### Component Styling

Each component has its own CSS file:
- `FileUpload.css` - Upload area styling
- `MCQDisplay.css` - Question display styling
- `Loading.css` - Loading spinner styling

---

## 📝 MCQ Generation Customization

### Modify the Prompt

Edit `backend/src/llm/mcq_generator.py`:

```python
prompt = f"""Generate {num_questions} multiple choice questions (MCQs) from the following text. 
For each question, provide 4 options (A, B, C, D) and the correct answer.

Text:
{text}

Return the response as a JSON array with this structure:
[
    {{
        "question": "Question text here?",
        "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
        "answer": "A"
    }}
]

Only return the JSON array, no other text."""
```

### Examples of Modifications

**For harder questions:**
```python
prompt = f"""Generate {num_questions} DIFFICULT multiple choice questions (MCQs)..."""
```

**For easier questions:**
```python
prompt = f"""Generate {num_questions} SIMPLE multiple choice questions (MCQs)..."""
```

**For specific subject:**
```python
prompt = f"""Generate {num_questions} multiple choice questions about BIOLOGY from the following text..."""
```

**For different number of options:**
```python
prompt = f"""Generate {num_questions} multiple choice questions with 5 options (A, B, C, D, E)..."""
```

### Change Number of Options

Modify both the prompt and response parsing in `mcq_generator.py`:

```python
# In prompt:
"options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D", "E": "Option E"}}

# Update MCQDisplay.jsx to render 5 options instead of 4
```

---

## 🔌 API Customization

### Add New Endpoint

Edit `backend/app.py`:

```python
@app.post("/your-new-endpoint")
async def your_new_endpoint(request: YourRequest):
    """Description of what this endpoint does"""
    try:
        result = process_data(request)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Modify CORS Settings

For production, change in `backend/app.py`:

```python
# Development (allow all)
allow_origins=["*"]

# Production (specific domain)
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]

# Multiple domains
allow_origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com",
    "https://admin.yourdomain.com"
]
```

---

## 📱 Frontend Features Customization

### Customize Question Count Options

Edit `frontend/src/App.jsx`:

```javascript
// Current options: 3, 5, 10
[3, 5, 10].map(num => (
  <button onClick={() => handleGenerateMCQs(num)}>
    Generate {num} Questions
  </button>
))

// Change to your preference
[5, 10, 15, 20].map(num => (
  <button onClick={() => handleGenerateMCQs(num)}>
    Generate {num} Questions
  </button>
))
```

### Add Features to MCQDisplay

Ideas:
- Timer for quiz
- Hint system
- Difficulty levels
- Save answers
- Export results

Example - Add timer:

```javascript
const [timeLeft, setTimeLeft] = useState(300); // 5 minutes

useEffect(() => {
  const timer = setInterval(() => {
    setTimeLeft(t => t - 1);
  }, 1000);
  return () => clearInterval(timer);
}, []);
```

---

## 🔒 Security Customization

### API Key Authentication

Add to `backend/app.py`:

```python
from fastapi.security import APIKey, APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/generate-mcqs")
async def generate_mcqs_endpoint(
    request: MCQRequest, 
    api_key: str = Depends(get_api_key)
):
    # your code
```

### Rate Limiting

```python
pip install slowapi

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/generate-mcqs")
@limiter.limit("10/minute")
async def generate_mcqs_endpoint(request: Request, ...):
    # your code
```

---

## 🚀 Performance Customization

### Increase Model Context

In `backend/src/llm/mcq_generator.py`:

```python
response = ollama.generate(
    model="mistral",
    prompt=prompt,
    stream=False,
    num_ctx=2048,  # Increase context size
    num_predict=500,  # Increase output length
)
```

### Add Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cache_mcq_generation(text: str, num_q: int):
    return generate_mcqs(text, num_q)
```

### Database Integration

Replace in-memory storage with database:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./mcqs.db"
engine = create_engine(DATABASE_URL)

@app.post("/generate-mcqs")
async def generate_mcqs_endpoint(request: MCQRequest, db: Session = Depends(get_db)):
    # Save to database
    mcq_record = MCQRecord(text=request.text, questions=json.dumps(mcqs))
    db.add(mcq_record)
    db.commit()
    return mcqs
```

---

## 🌐 Frontend Language Customization

### Add i18n (Internationalization)

```bash
npm install i18next react-i18next
```

Create translation files:
- `public/locales/en-US/translation.json`
- `public/locales/es-ES/translation.json`

Use in components:
```javascript
import { useTranslation } from 'react-i18next';

function App() {
  const { t } = useTranslation();
  return <h1>{t('app.title')}</h1>;
}
```

---

## 🎯 Theme Customization

### Light/Dark Mode

Add to `frontend/src/App.css`:

```css
body.light-mode {
  background-color: #ffffff;
  color: #000000;
}

body.dark-mode {
  background-color: #1a1a1a;
  color: #ffffff;
}
```

Toggle in App.jsx:

```javascript
const [darkMode, setDarkMode] = useState(false);

useEffect(() => {
  document.body.className = darkMode ? 'dark-mode' : 'light-mode';
}, [darkMode]);

return (
  <>
    <button onClick={() => setDarkMode(!darkMode)}>
      {darkMode ? '☀️' : '🌙'}
    </button>
  </>
);
```

---

## 📊 Logging and Monitoring

### Add Logging

In `backend/app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/generate-mcqs")
async def generate_mcqs_endpoint(request: MCQRequest):
    logger.info(f"Generating {request.num_questions} MCQs")
    try:
        result = generate_mcqs(request.text, request.num_questions)
        logger.info("MCQs generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise
```

---

## 📦 Dependencies Customization

### Add New Dependencies

Backend:
```bash
cd backend
pip install <package-name>
pip freeze > requirements.txt
```

Frontend:
```bash
cd frontend
npm install <package-name>
npm install --save-dev <dev-package>
```

---

## ✅ Testing Customization

### Add Unit Tests

Backend (pytest):
```python
# test_app.py
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_upload_pdf():
    # Test code
    pass
```

Frontend (Jest):
```javascript
// App.test.jsx
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders upload component', () => {
  render(<App />);
  // assertions
});
```

---

## 🔄 Integration Customization

### Add Chat Interface

```javascript
// In frontend
const [chatMessages, setChatMessages] = useState([]);

const addMessage = (text, sender) => {
  setChatMessages([...chatMessages, { text, sender }]);
};
```

### Add Real-time Updates (WebSocket)

```python
# In backend
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

---

## 📚 Need More Help?

- Check individual guide files in `docs/`
- Review component source code (well-commented)
- Refer to framework documentation:
  - [FastAPI Docs](https://fastapi.tiangolo.com/)
  - [React Docs](https://react.dev/)
  - [Ollama Docs](https://github.com/jmorganca/ollama)

---

**Happy customizing! 🎨**
