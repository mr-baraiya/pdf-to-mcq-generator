# Frontend API URL Configuration for Vercel

This guide explains how to configure the frontend to work with the Vercel serverless backend.

---

##  API URL Configuration

The frontend needs to know where the API is. In local development, it's on a different port. In production (Vercel), both frontend and API are on the same domain.

---

##  Solution: Use Environment Variables

### Step 1: Update `frontend/.env`

Create `frontend/.env.local` for local development:

```env
# Local development
VITE_API_URL=http://localhost:8000
```

Create `frontend/.env.production` for production:

```env
# Production (Vercel)
VITE_API_URL=/api
```

### Step 2: Update `frontend/src/App.jsx`

```javascript
import { useState } from 'react';
import axios from 'axios';

function App() {
  // Get API URL from environment variable
  // Falls back to relative path for production
  const API_URL = import.meta.env.VITE_API_URL || '/api';

  const [mcqs, setMcqs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [extractedText, setExtractedText] = useState('');

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Use configured API URL
      const response = await axios.post(`${API_URL}/upload-pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setExtractedText(response.data.text);
      setError('');
    } catch (err) {
      setError('Error uploading file: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const handleGenerateMCQs = async (numQuestions) => {
    if (!extractedText) {
      setError('Please upload a PDF first');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${API_URL}/generate-mcqs`, {
        text: extractedText,
        num_questions: numQuestions
      });
      
      setMcqs(response.data.questions);
      setLoading(false);
    } catch (err) {
      setError('Error generating MCQs: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  // ... rest of component
}

export default App;
```

---

##  Alternative: Detect Environment

Instead of environment files, detect automatically:

```javascript
// Auto-detect API URL based on environment
const getAPIUrl = () => {
  if (import.meta.env.PROD) {
    // Production (Vercel)
    return '/api';
  } else {
    // Development (local)
    return 'http://localhost:8000';
  }
};

const API_URL = getAPIUrl();
```

---

##  Vite Configuration Update

Make sure `frontend/vite.config.js` has proxy for local development:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy API calls to backend during development
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

**Why this works:**
- Local development: Vite proxy redirects `/api`  `http://localhost:8000`
- Vercel production: Requests go to `https://yourdomain.com/api` (routed to serverless function)

---

##  Example: Complete Updated App.jsx

```javascript
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import MCQDisplay from './components/MCQDisplay';
import Loading from './components/Loading';

function App() {
  // API URL configuration - works both locally and on Vercel
  const API_URL = import.meta.env.VITE_API_URL || '/api';
  
  console.log('Using API URL:', API_URL);

  const [mcqs, setMcqs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [extractedText, setExtractedText] = useState('');

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Uploading to:', `${API_URL}/upload-pdf`);
      
      const response = await axios.post(`${API_URL}/upload-pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setExtractedText(response.data.text);
      setError('');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      console.error('Upload error:', errorMsg);
      setError('Error uploading file: ' + errorMsg);
      setLoading(false);
    }
  };

  const handleGenerateMCQs = async (numQuestions) => {
    if (!extractedText) {
      setError('Please upload a PDF first');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      console.log('Generating MCQs with:', `${API_URL}/generate-mcqs`);
      
      const response = await axios.post(`${API_URL}/generate-mcqs`, {
        text: extractedText,
        num_questions: numQuestions
      });
      
      setMcqs(response.data.questions);
      setLoading(false);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      console.error('MCQ generation error:', errorMsg);
      setError('Error generating MCQs: ' + errorMsg);
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1> PDF to MCQ Generator</h1>
        <p>Convert your PDF documents into multiple choice questions automatically</p>
      </header>

      <main className="app-container">
        {error && <div className="error-message">{error}</div>}
        
        {!extractedText ? (
          <FileUpload onFileSelect={handleFileUpload} loading={loading} />
        ) : (
          <>
            <div className="text-preview">
              <h3>Extracted Text Preview</h3>
              <p>{extractedText.substring(0, 300)}...</p>
              <button className="btn-secondary" onClick={() => setExtractedText('')}>
                Upload Another PDF
              </button>
            </div>
            
            {loading ? (
              <Loading />
            ) : mcqs.length === 0 ? (
              <div className="generate-section">
                <h2>Generate MCQs</h2>
                <div className="question-count-selector">
                  {[3, 5, 10].map(num => (
                    <button
                      key={num}
                      className="btn-primary"
                      onClick={() => handleGenerateMCQs(num)}
                    >
                      Generate {num} Questions
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <MCQDisplay mcqs={mcqs} onReset={() => setMcqs([])} />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
```

---

##  Testing Local & Production

### Local Development

```bash
cd frontend
npm run dev
```

- API URL will be: `http://localhost:8000`
- Frontend at: `http://localhost:3000`
- Vite proxy handles `/api`  backend

### Production (Vercel)

```bash
cd frontend
npm run build
```

- API URL will be: `/api` (relative to domain)
- Both at: `https://yourdomain.com`
- Vercel routing handles `/api`  serverless function

---

##  Browser DevTools Verification

### Check Network Requests

1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Upload a PDF
4. Look for POST request to:
   - Local: `http://localhost:3000/api/upload-pdf`
   - Vercel: `https://yourdomain.com/api/upload-pdf`

### Check Console

```javascript
// In browser console
console.log(import.meta.env.VITE_API_URL) // Shows configured URL
```

---

##  Troubleshooting

### "Cannot reach API" locally

**Problem**: Frontend can't connect to backend

**Solution**:
1. Ensure backend is running: `python app.py`
2. Check vite.config.js proxy is configured
3. Check VITE_API_URL in .env

```bash
# Verify backend is running
curl http://localhost:8000/

# Check Vite proxy in vite.config.js
grep -A 5 "proxy:" frontend/vite.config.js
```

### API 404 on Vercel

**Problem**: Vercel says `/api` endpoint not found

**Solution**:
1. Check `vercel.json` routes exist
2. Check `api/index.py` has all endpoints
3. Redeploy

### CORS error

**Problem**: Browser blocks API call

**Solution**:
- Backend has `CORSMiddleware` enabled
- Allows all origins: `allow_origins=["*"]`
- This is fine for development
- For production, restrict to your domain:

```python
# In api/index.py
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

---

##  Summary

| Aspect | Local | Vercel |
|--------|-------|--------|
| Frontend Port | 3000 | 443 (HTTPS) |
| Backend Port | 8000 | Serverless |
| API URL | `http://localhost:8000` | `/api` |
| Configuration | `.env.local` | Env variables in Vercel |
| Routing | Vite proxy | Vercel routing |

---

##  You're Ready!

Your frontend is now configured to work both locally and on Vercel production.

**Next steps:**
1. Update `frontend/src/App.jsx` with API_URL configuration
2. Create `frontend/.env.local` and `.env.production` files
3. Test locally: `npm run dev`
4. Test production: Deploy to Vercel and verify API calls work

---
