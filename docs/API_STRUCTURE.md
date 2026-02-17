# API Folder Structure - Explanation Guide

This document explains how the API code is organized in separate files for better maintainability and understanding.

##  File Organization

```
api/
 index.py          # Main entry point (combines all modules)
 config.py         # Configuration & middleware setup
 models.py         # Data models (Pydantic)
 routes.py         # API endpoints/routes
 handlers.py       # Event & exception handlers
```

##  File-by-File ExplanationFile

### 1. **index.py** - Main Application Entry Point
**Purpose:** Combines all components into one working application

```python
# Imports all module functions
from api.config import create_app
from api.handlers import setup_event_handlers, setup_exception_handlers
from api.routes import setup_routes

# Creates the app
app = create_app()

# Adds event handlers (startup logic)
setup_event_handlers(app)

# Adds exception handlers (error handling)
setup_exception_handlers(app)

# Adds all routes/endpoints
setup_routes(app)
```

**Why separate:** Keeps the entry point clean and shows the overall structure clearly.

---

### 2. **config.py** - Configuration & Middleware
**Purpose:** Handles FastAPI app creation, CORS setup, and logging

**Key Functions:**
- `create_app()` - Creates and configures FastAPI app instance
- `get_logger()` - Returns logger for debugging

**What it does:**
- Loads environment variables from `.env` file
- Sets up CORS (allows frontend to communicate with backend)
- Configures logging for debugging

**Example:**
```python
def create_app() -> FastAPI:
    app = FastAPI(title="PDF to MCQ Generator API", version="1.0.0")
    
    # Enable CORS - allows React frontend to call this API
    app.add_middleware(CORSMiddleware, ...)
    
    return app
```

---

### 3. **models.py** - Data Models
**Purpose:** Defines request/response formats using Pydantic

**Models:**
- `MCQRequest` - What client sends when requesting MCQs
  ```python
  {
    "text": "Some paragraph",
    "num_questions": 5
  }
  ```

- `MCQResponse` - What API returns after generating MCQs
  ```python
  {
    "questions": [...],
    "status": "success"
  }
  ```

**Why separate:** Makes data validation centralized and reusable.

---

### 4. **routes.py** - API Endpoints
**Purpose:** Defines all API endpoints/routes that clients can call

**Endpoints:**

####  GET `/`
- **Purpose:** Health check
- **Returns:** API version info

####  POST `/upload-pdf`
- **Purpose:** Upload PDF and extract text
- **Input:** PDF file
- **Process:**
  1. Validate it's a PDF
  2. Upload to Vercel Blob (cloud storage)
  3. Extract text from PDF
  4. Return extracted text + blob URL
- **Output:** Text, blob URL, success status

####  POST `/generate-mcqs`
- **Purpose:** Generate MCQs from text
- **Input:** Text + number of questions
- **Process:**
  1. Send text to Ollama AI model
  2. Get MCQ format response
  3. Return questions
- **Output:** MCQs list, success status

**Why separate:** All endpoint logic in one organized place.

---

### 5. **handlers.py** - Event & Exception Handlers
**Purpose:** Handle app lifecycle events and errors

**Functions:**

#### `setup_event_handlers(app)`
Runs when API starts:
```python
@app.on_event("startup")
async def startup_event():
    # Check if Vercel Blob credentials are configured
    # Log warnings if missing
```

#### `setup_exception_handlers(app)`
Catches all errors:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Returns clean error message instead of crash
    return {"detail": "Internal server error"}
```

---

##  How It All Works Together

```
User Request
    
index.py (entry point)
    
routes.py (handles request)
    
Uses models.py (validates data)
    
Uses backend/src/ modules (processes)
    
Returns response via models.py
    
handlers.py catches any errors
    
User Gets Response
```

##  Data Flow Example

### Uploading a PDF:
```
1. User sends PDF  routes.py:upload_pdf()
2. Validates file type (is it PDF?)
3. Uploads to Vercel Blob (cloud storage)
4. Extracts text using backend/src/pdf/extractor.py
5. Returns: filename, text, blob_url
6. If error occurs  handlers.py catches it
```

### Generating MCQs:
```
1. User sends text + 5 questions  routes.py:generate_mcqs_endpoint()
2. Validates using models.py:MCQRequest
3. Sends text to Ollama AI  backend/src/llm/mcq_generator.py
4. Returns: questions list + status
5. Response validated by models.py:MCQResponse
```

---

##  Key Concepts to Explain to Your Sir

### 1. **Separation of Concerns**
Each file has ONE responsibility:
- `config.py`  Configuration only
- `models.py`  Data validation only
- `routes.py`  API endpoints only  
- `handlers.py`  Error handling only
- `index.py`  Combine everything

### 2. **Maintainability**
If you need to add a new endpoint:
- Only edit `routes.py`
- Add model if needed in `models.py`
- Other files remain untouched

### 3. **Testability**
Each module can be tested independently:
```python
# Test models
test_models.py

# Test routes
test_routes.py

# Test handlers
test_handlers.py
```

### 4. **Scalability**
Easy to expand:
- Add more endpoints  edit `routes.py`
- Add more models  edit `models.py`
- Add more error handlers  edit `handlers.py`

---

##  Summary

| File | Responsibility | Lines of Code |
|------|-----------------|---------------|
| `index.py` | Combines components | ~10 |
| `config.py` | App setup & middleware | ~40 |
| `models.py` | Data structures | ~15 |
| `routes.py` | API endpoints | ~110 |
| `handlers.py` | Event & error handling | ~60 |

**Total:** Clean, organized, easy to understand and explain! 

