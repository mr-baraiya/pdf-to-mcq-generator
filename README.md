# File to MCQ Generator

**Live Demo:** [https://pdf2mcq-henna.vercel.app/](https://pdf2mcq-henna.vercel.app/)  
**Backend API:** [https://pdf-to-mcq-generator-production.up.railway.app](https://pdf-to-mcq-generator-production.up.railway.app)  
**API Docs:** [https://pdf-to-mcq-generator-production.up.railway.app/docs](https://pdf-to-mcq-generator-production.up.railway.app/docs)

A smart web application that automatically generates Multiple Choice Questions (MCQs) from PDF, PowerPoint, and Text documents using Groq AI.

---

## Features

- Upload PDF, PPTX, and TXT files with drag-and-drop
- Generate 3-50 MCQs using AI (Groq Llama 3.3 70B)
- View questions with highlighted correct answers
- Paginated results with customizable items per page
- Export questions and answers as PDF
- Modern responsive interface with smooth animations

## Tech Stack

Backend: Python, FastAPI, Groq API, Vercel Blob Storage
Frontend: React, Vite, Tailwind CSS, Framer Motion

## Quick Start

Prerequisites: Python 3.8+, Node.js 16+, Groq API Key

1. Clone repository
```bash
git clone https://github.com/mr-baraiya/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

2. Setup environment variables

Backend (.env in backend/):
```
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=http://localhost:3000
BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
```

Frontend (.env in frontend/):
```
VITE_API_URL=http://localhost:8000
```

3. Install dependencies
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

4. Run servers
```bash
# Backend (port 8000)
cd backend
python -m uvicorn index:app --reload

# Frontend (port 3000)
cd frontend
npm run dev
```

Access at http://localhost:3000

## API Endpoints

```
GET  /                     → Health check
POST /api/upload-pdf       → Upload file & extract text
POST /api/generate-mcqs    → Generate MCQs
```

Full API docs: http://localhost:8000/docs

## Deployment

Vercel: Import project, set GROQ_API_KEY, deploy

## Project Structure

```
backend/
  index.py              # FastAPI app
  routes.py            # API endpoints
  handlers.py          # Business logic
  models.py            # Data models
  llm/mcq_generator.py # AI generation
  pdf/extractor.py     # Text extraction
  utils/blob_storage.py # Cloud storage

frontend/
  src/
    App.jsx            # Main component
    components/
      FileUpload.jsx   # Upload interface
      MCQResults.jsx   # Results display
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Vishal Baraiya - B.Tech CSE Student
GitHub: [@mr-baraiya](https://github.com/mr-baraiya)
