# PDF to MCQ Generator

**Live Demo:** [https://pdf2mcq-henna.vercel.app/](https://pdf2mcq-henna.vercel.app/)  
**Backend API:** [https://pdf-to-mcq-generator-production.up.railway.app](https://pdf-to-mcq-generator-production.up.railway.app)  
**API Docs:** [https://pdf-to-mcq-generator-production.up.railway.app/docs](https://pdf-to-mcq-generator-production.up.railway.app/docs)

A web application that automatically generates Multiple Choice Questions (MCQs) from PDF, PowerPoint, and Text documents using Groq AI.

---

## Features

- Upload PDF, PPTX, and TXT files with drag-and-drop
- Extracts text from both selectable and image-based (scanned) PDFs via OCR
- Generate 3–50 MCQs using Groq Llama 3.3 70B
- View questions with highlighted correct answers
- Paginated results with customizable items per page
- Export questions as PDF
- Modern responsive UI with smooth animations

## Tech Stack

**Backend:** Python 3.12, FastAPI, Groq API, Vercel Blob Storage, PyPDF2, Tesseract OCR  
**Frontend:** React 18, Vite, Tailwind CSS, Framer Motion

## Quick Start

**Prerequisites:** Python 3.8+, Node.js 16+, Groq API key, `tesseract-ocr` and `poppler-utils` system packages

```bash
# Ubuntu / Debian
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng poppler-utils
```

### 1. Clone

```bash
git clone https://github.com/mr-baraiya/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=http://localhost:3000
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
VERCEL_BLOB_STORE_ID=your_vercel_store_id
```

```bash
uvicorn index:app --reload
# Runs on http://localhost:8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

The Vite dev server proxies `/api/*` → `http://localhost:8000/*` automatically.

## API Endpoints

```
GET  /               → Health check
POST /upload-file    → Upload file, extract text, store in Vercel Blob
POST /generate-mcqs  → Generate MCQs from extracted text
```

Full interactive docs: `http://localhost:8000/docs`

## Project Structure

```
backend/
  index.py          # FastAPI app, CORS config
  routes.py         # API endpoints
  extractor.py      # PDF/PPTX/TXT text extraction + OCR fallback
  mcq_generator.py  # Groq API call + response parsing
  blob_storage.py   # Vercel Blob upload/download
  requirements.txt
  nixpacks.toml     # Railway: installs tesseract + poppler at build time
  railway.toml      # Railway: start command
  build.sh          # Render: installs system packages + pip deps
  Procfile          # Render/Heroku: start command

frontend/
  src/
    App.jsx
    pages/
      HomePage.jsx
      GeneratorPage.jsx
    components/
      FileUpload.jsx
      MCQResults.jsx
      LoadingAnimation.jsx
      Navbar.jsx
      Hero.jsx
      Features.jsx
      AnimatedBackground.jsx
  vite.config.js    # Dev proxy: /api → localhost:8000
```

## Deployment

### Railway

The `backend/` folder contains `railway.toml` and `nixpacks.toml`.  
Set the **Root Directory** to `backend` in Railway settings, then add environment variables:

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key |
| `VERCEL_BLOB_READ_WRITE_TOKEN` | Vercel Blob token |
| `VERCEL_BLOB_STORE_ID` | Vercel Blob store ID |
| `FRONTEND_URL` | Your frontend URL (for CORS) |

### Render

The repo root contains `render.yaml`. Connect the repo on Render and add the same environment variables above in the dashboard (they are marked `sync: false` so they won't be committed).

### Frontend (Vercel)

Set `VITE_API_URL` to your Railway or Render backend URL in Vercel project settings.

## License

MIT — see [LICENSE](LICENSE)

## Author

Vishal Baraiya — B.Tech CSE  
GitHub: [@mr-baraiya](https://github.com/mr-baraiya)
