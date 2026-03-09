# PDF to MCQ Generator

Live Demo:
[https://pdf2mcq-henna.vercel.app/](https://pdf2mcq-henna.vercel.app/)

Backend API (Railway):
[https://pdf-to-mcq-generator-production.up.railway.app/docs](https://pdf-to-mcq-generator-production.up.railway.app/docs)

Backend API (Render):
[https://pdf-to-mcq-generator-fastapi.onrender.com/docs](https://pdf-to-mcq-generator-fastapi.onrender.com/docs)

PDF to MCQ Generator is a web application that automatically generates Multiple Choice Questions from PDF, PowerPoint, and text documents using AI. The system extracts content from uploaded documents, including scanned PDFs through OCR, and uses the Groq Llama 3.3 70B model to generate structured MCQs.

---

# Features

* Upload PDF, PPTX, and TXT files with drag-and-drop support
* Extract text from both selectable PDFs and scanned image-based PDFs using OCR
* Generate between 3 and 50 multiple choice questions
* Highlight correct answers in generated results
* Paginated results with configurable items per page
* Export generated questions as PDF
* Responsive UI with smooth animations
* AI-powered question generation using Groq

---

# Tech Stack

Backend
FastAPI
Python
PyPDF2
Tesseract OCR
pdf2image

Frontend
Vite
React
TailwindCSS
Framer Motion
GSAP
jsPDF
React Router DOM

AI
Groq Llama 3.3 70B

Storage
Vercel Blob Storage

Deployment
Vercel (Frontend)
Railway (Backend)
Render (Docker Backend)

Key Backend Libraries
fastapi 0.115
uvicorn 0.35
python-pptx 1.0
PyPDF2 3.0
pytesseract 0.3
pdf2image 1.17
Pillow 11.1
groq 1.0
vercel-blob 0.4
aiohttp 3.13

---

# Project Structure

```
pdf-to-mcq-generator/
│
├── backend/
│   ├── index.py
│   ├── main.py
│   ├── routes.py
│   ├── extractor.py
│   ├── mcq_generator.py
│   ├── blob_storage.py
│   ├── build.sh
│   ├── Dockerfile
│   ├── render.yaml
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   └── GeneratorPage.jsx
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── MCQResults.jsx
│   │   │   ├── LoadingAnimation.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Features.jsx
│   │   │   └── AnimatedBackground.jsx
│   │
│   └── vite.config.js
│
└── README.md
```

---

# Prerequisites

Python 3.11 or higher
Node.js 18 or higher
Tesseract OCR (for scanned PDFs)
Poppler utilities (for PDF image conversion)

---

# Install System Dependencies

Ubuntu or Debian

```
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

macOS

```
brew install tesseract poppler
```

Windows

Download and install Tesseract from the official UB-Mannheim build:

```
https://github.com/UB-Mannheim/tesseract/wiki
```

Download Poppler for Windows and add it to your PATH:

```
https://github.com/oschwartz10612/poppler-windows/releases
```

After installing, add both bin directories to your system PATH environment variable.

---

# Run Locally

Clone the repository

```
git clone https://github.com/mr-baraiya/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

---

## Setup Backend

```
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create environment file

```
cp .env.example .env
```

Edit `.env` and add your keys.

Start backend server

```
python3 main.py
```

Backend runs at

```
http://localhost:10000
```

API docs

```
http://localhost:10000/docs
```

---

## Setup Frontend

```
cd frontend

npm install
npm run dev
```

Frontend runs at

```
http://localhost:3000
```

---

# Environment Variables

Create `backend/.env`

```
GROQ_API_KEY=your_groq_api_key

FRONTEND_URL=http://localhost:3000

VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token

VERCEL_BLOB_STORE_ID=your_vercel_blob_store_id
```

---

# Run With Docker

```
cd backend

docker build -t pdf-to-mcq-generator .

docker run -p 10000:10000 --env-file .env pdf-to-mcq-generator
```

---

# Deploy to Render

Push your code to GitHub.

Open Render Dashboard.

Create a new Web Service and connect your repository.

Configuration:

Root Directory

```
backend
```

Runtime

```
Docker
```

Dockerfile Path

```
./Dockerfile
```

Add environment variables:

```
GROQ_API_KEY
FRONTEND_URL
VERCEL_BLOB_READ_WRITE_TOKEN
VERCEL_BLOB_STORE_ID
```

Deploy the service.

API Docs after deployment

```
https://pdf-to-mcq-generator-fastapi.onrender.com/docs
```

---

# Deploy Backend to Railway

Set **Root Directory** to

```
backend
```

Add environment variables:

```
GROQ_API_KEY
VERCEL_BLOB_READ_WRITE_TOKEN
VERCEL_BLOB_STORE_ID
FRONTEND_URL
```

Deploy the service.

API docs

```
https://pdf-to-mcq-generator-production.up.railway.app/docs
```

---

# Deploy Frontend to Vercel

Connect the repository to Vercel.

Set environment variable

```
VITE_API_URL=https://pdf-to-mcq-generator-production.up.railway.app
```

or

```
VITE_API_URL=https://pdf-to-mcq-generator-fastapi.onrender.com
```

Deploy the frontend.

---

# API Endpoints

POST `/upload-file`
Upload a document and extract text.

POST `/generate-mcq`
Generate multiple choice questions from extracted text.

GET `/docs`
Interactive API documentation.

---

# Author

Vishal Baraiya
B.Tech Computer Science and Engineering

GitHub
[https://github.com/mr-baraiya](https://github.com/mr-baraiya)

---

# License

MIT License
See the LICENSE file for details.
