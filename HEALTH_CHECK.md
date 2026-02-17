# System Health Check

Run this checklist to ensure everything is properly set up.

---

## ✅ Prerequisites Check

- [ ] **Python** installed
  ```bash
  python --version  # Should be 3.8+
  ```

- [ ] **Node.js** installed
  ```bash
  node --version    # Should be 14+
  npm --version
  ```

- [ ] **Ollama** downloaded and installed
  ```bash
  # Should open Ollama unless it's a headless system
  ```

- [ ] **Ollama** running
  ```bash
  curl http://localhost:11434/api/tags
  # Should return JSON with available models
  ```

- [ ] **Mistral model** installed
  ```bash
  ollama list
  # Should show "mistral" in the list
  ```

---

## ✅ Backend Setup Check

```bash
cd backend
```

- [ ] **Virtual environment** created and activated
  ```bash
  python -m venv venv
  source venv/bin/activate  # or: venv\Scripts\activate (Windows)
  which python  # Should show path in venv folder
  ```

- [ ] **Dependencies** installed
  ```bash
  pip install -r requirements.txt
  pip list | grep fastapi
  # Should show: fastapi, uvicorn, PyPDF2, ollama, etc.
  ```

- [ ] **.env** file created
  ```bash
  cp .env.example .env
  cat .env  # Should show environment variables
  ```

- [ ] **Server** starts successfully
  ```bash
  python app.py
  # Should show: "Uvicorn running on http://0.0.0.0:8000"
  ```

- [ ] **API** responds
  ```bash
  # In another terminal:
  curl http://localhost:8000/
  # Should return: {"message": "PDF to MCQ Generator API", "version": "1.0.0"}
  ```

- [ ] **Swagger docs** accessible
  ```
  Open: http://localhost:8000/docs
  Should show interactive API documentation
  ```

---

## ✅ Frontend Setup Check

```bash
cd frontend
```

- [ ] **Dependencies** installed
  ```bash
  npm install
  npm list react react-dom
  # Should show installed versions
  ```

- [ ] **Dev server** starts
  ```bash
  npm run dev
  # Should show: "Local: http://localhost:3000"
  ```

- [ ] **Frontend** loads in browser
  ```
  Open: http://localhost:3000
  Should see purple gradient background with title "📄 PDF to MCQ Generator"
  ```

- [ ] **Console has no errors**
  ```bash
  Open http://localhost:3000
  Press F12 to open DevTools
  Check Console tab for any errors (should be clean)
  ```

---

## ✅ Integration Check

With both servers running:

- [ ] **Upload component** displays
  ```
  http://localhost:3000 should show upload area
  ```

- [ ] **API communication** works
  ```bash
  # In browser DevTools, Network tab:
  # Upload a PDF and watch for POST /upload-pdf request
  # Should return with status 200 and extracted text
  ```

- [ ] **PDF extraction** works
  ```
  Upload any PDF file
  Should show preview of extracted text
  ```

- [ ] **MCQ generation** works
  ```
  Click "Generate 5 Questions"
  Should show loading spinner
  After 5-30 seconds, should display questions
  ```

- [ ] **Quiz interaction** works
  ```
  Select answers for questions
  Click "Check Answers"
  Should show score and correct answers
  ```

---

## 🔍 Detailed Diagnostics

### If Backend won't start:

1. **Check Python version**
   ```bash
   python --version
   ```
   Should be 3.8 or higher

2. **Check if port 8000 is free**
   ```bash
   lsof -i :8000
   # If something is using it:
   kill -9 <PID>
   ```

3. **Check dependencies**
   ```bash
   pip list
   # Should include: fastapi, uvicorn, PyPDF2, ollama
   ```

4. **Check Ollama connection**
   ```bash
   curl http://localhost:11434/api/tags
   # Should respond with JSON
   ```

### If Frontend won't start:

1. **Check Node.js version**
   ```bash
   node --version  # 14+
   npm --version   # 6+
   ```

2. **Check if port 3000 is free**
   ```bash
   lsof -i :3000
   # If something is using it:
   kill -9 <PID>
   ```

3. **Check node_modules**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Clear next/cache** (if using Next.js)
   ```bash
   rm -rf .next
   npm run dev
   ```

### If API calls fail:

1. **Check backend is running**
   ```bash
   curl http://localhost:8000/
   ```

2. **Check CORS is enabled**
   - Browser console should not show CORS error
   - If it does, CORS is not properly configured in `backend/app.py`

3. **Check file size limits**
   ```bash
   # Default limit is fine for most PDFs
   # If uploading large files, may need to increase
   ```

4. **Check network tab**
   - Open DevTools → Network tab
   - Upload PDF and watch the request
   - Check response status and body

### If MCQ generation is slow:

1. **First request is normal**
   - First request loads the model (~2-5 minutes)
   - Subsequent requests are much faster

2. **Check Ollama logs**
   - Ollama should show model loading messages
   - Check available RAM

3. **Check model size**
   - Mistral (7B) is default - small and fast
   - If too slow, use neural-chat
   - If too slow for your hardware, use smaller model

---

## 📊 Performance Check

### Backend Performance:
- [ ] Health check (GET /) should respond in <100ms
- [ ] PDF upload should complete in <5 seconds
- [ ] MCQ generation should complete in 5-30 seconds (first request slower)

### Frontend Performance:
- [ ] Page load should be <1 second
- [ ] File upload drag-drop should be instant
- [ ] Button clicks should respond immediately

### Network:
- [ ] All requests should complete without errors
- [ ] File uploads should show progress
- [ ] No CORS warnings in console

---

## 🧪 Test With Sample Data

### Sample PDF Content:

Create a text file with this content and convert to PDF:

```
Machine Learning Basics

Machine learning is a subset of artificial intelligence (AI) that provides systems 
the ability to automatically learn and improve from experience without being 
explicitly programmed.

Types of Machine Learning:
1. Supervised Learning - uses labeled training data
2. Unsupervised Learning - finds patterns in unlabeled data
3. Reinforcement Learning - learns through interaction with environment

Deep Learning is a subset of machine learning that uses artificial neural networks 
with multiple layers (deep networks) to process data and make predictions.

Common ML Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Spam detection
```

### Expected MCQ Output:

The system should generate questions like:
- "What is machine learning?"
- "How many types of machine learning are there?"
- "What is deep learning?"
- "Name an application of machine learning"

---

## 🆘 Still Having Issues?

1. **Check logs**:
   - Backend: Look at terminal running `python app.py`
   - Frontend: Press F12 → Console tab in browser
   - Ollama: Check Ollama application window

2. **Restart services**:
   ```bash
   # Kill backend
   Ctrl+C in backend terminal
   python app.py
   
   # Kill frontend
   Ctrl+C in frontend terminal
   npm run dev
   ```

3. **Clear cache**:
   ```bash
   # For frontend
   rm -rf node_modules
   npm cache clean --force
   npm install
   
   # For backend
   pip cache purge
   pip install -r requirements.txt --force-reinstall
   ```

4. **Reset Ollama**:
   ```bash
   ollama list  # See models
   ollama rm mistral
   ollama pull mistral
   ```

---

## ✨ Success Indicators

You'll know everything is working when:

1. ✅ Backend running: `http://localhost:8000` displays API info
2. ✅ Frontend running: `http://localhost:3000` displays app UI
3. ✅ You can upload a PDF and see extracted text
4. ✅ You can generate MCQs and see questions appear
5. ✅ You can answer questions and get score
6. ✅ No errors in browser console
7. ✅ No errors in backend terminal

---

**If all checks pass, your system is ready! 🎉**

For specific issues, check the documentation:
- [SETUP.md](SETUP.md) - Setup guide
- [API.md](API.md) - API reference
- [BACKEND_GUIDE.md](BACKEND_GUIDE.md) - Backend development
- [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) - Frontend development
