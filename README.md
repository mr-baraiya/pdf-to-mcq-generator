# File to MCQ Generator

**Live Demo:** [https://pdf2mcq-henna.vercel.app/](https://pdf2mcq-henna.vercel.app/)  
**Backend API:** [https://pdf-to-mcq-generator-production.up.railway.app](https://pdf-to-mcq-generator-production.up.railway.app)  
**API Docs:** [https://pdf-to-mcq-generator-production.up.railway.app/docs](https://pdf-to-mcq-generator-production.up.railway.app/docs)

A smart web application that automatically generates Multiple Choice Questions (MCQs) from PDF, PowerPoint, and Text documents using Groq AI.

**Live Features:**
- AI-Powered Generation - Fast MCQ creation with Groq (Llama 3.3 70B)
- Multiple File Formats - Upload PDF, PPTX, and TXT files
- Answer Key Display - View questions with correct answers
- PDF Export - Download questions and answers as PDF
- Cloud Storage - Secure file storage with Vercel Blob
- Modern UI - Clean, responsive interface

---

## Features

### Core Functionality
- **Multiple File Formats** - Drag-and-drop interface for PDF, PPTX, and TXT files
- **AI-Powered Generation** - Fast MCQ creation using Groq (Llama 3.3 70B)
- **Answer Key Display** - View all questions with correct answers highlighted
- **PDF Export** - Download questions and answers in PDF format
- **Generate More** - Add additional questions to existing set
- **Responsive Design** - Works seamlessly on all devices

### Technical Features
- **REST API** - FastAPI backend with comprehensive documentation
- **Cloud Storage** - Vercel Blob integration for PDF files
- **Serverless Ready** - Vercel deployment support
- **Error Handling** - Robust error management and user feedback
- **Modern UI** - React with Framer Motion animations

---

## Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI server
- **PyPDF2 & python-pptx** - PDF and PowerPoint text extraction
- **Text files** - Native TXT file support
- **Groq API** - Fast LLM inference (Llama 3.3 70B)
- **Vercel Blob** - Cloud file storage
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Axios** - HTTP client
- **jsPDF** - PDF generation
- **Lucide React** - Icon library

### AI Model
- **Groq (Llama 3.3 70B)** - Fast, powerful cloud LLM inference

---

## Project Structure

```
pdf-to-mcq-generator/
├── backend/                        # Backend API
│   ├── api/                        # Main API package
│   │   ├── index.py                # Main FastAPI application
│   │   ├── routes.py               # API endpoints
│   │   ├── handlers.py             # Request handlers
│   │   ├── models.py               # Data models
│   │   ├── config.py               # Configuration
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   └── mcq_generator.py    # AI MCQ generation logic
│   │   ├── pdf/
│   │   │   ├── __init__.py
│   │   │   └── extractor.py        # PDF text extraction
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── blob_storage.py     # Vercel Blob integration
│   ├── requirements.txt            # Python dependencies
│   ├── vercel.json                 # Vercel deployment config
│   ├── .env                        # Backend environment variables
│   ├── .env.example                # Backend env template
│   ├── package.json                # Backend package metadata
│   └── README.md                   # Backend documentation
│
├── frontend/                       # React Frontend
│   ├── src/
│   │   ├── main.jsx                # Entry point
│   │   ├── App.jsx                 # Main component
│   │   ├── App.css
│   │   ├── index.css
│   │   └── components/
│   │       ├── Navbar.jsx
│   │       ├── Hero.jsx
│   │       ├── Features.jsx
│   │       ├── FileUpload.jsx      # File upload interface
│   │       ├── MCQResults.jsx      # Answer key display
│   │       ├── LoadingAnimation.jsx
│   │       └── AnimatedBackground.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── docs/                           # Documentation
│   ├── API.md
│   ├── SETUP.md
│   ├── VERCEL_DEPLOYMENT.md
│   ├── ENV_CONFIGURATION.md
│   └── ...
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── vercel.json                     # Vercel config
└── README.md
```

---

## Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Groq API Key** (get from https://console.groq.com)
- **Vercel Account** (for Blob storage - optional for local dev)

### 1. Clone Repository

```bash
git clone https://github.com/mr-baraiya/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

### 2. Environment Setup

**Backend Environment Variables:**

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```bash
# Groq API Key (required)
GROQ_API_KEY=your_groq_api_key_here

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# Vercel Blob Storage (optional for local)
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token_here
VERCEL_BLOB_STORE_ID=your_store_id_here
```

**Frontend Environment Variables:**

Create a `.env` file in the `frontend/` directory:

```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env`:
```bash
# Backend API URL
VITE_API_URL=http://localhost:8000
```

**Setup Options:**

Get API keys:
- **Groq**: https://console.groq.com/keys (required)
- **Vercel Blob**: https://vercel.com/docs/storage/vercel-blob (optional for local dev)

### 3. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

Or use the root package.json:
```bash
npm run install
```

### 4. Run Development Servers

**Option A: Using npm scripts (Recommended)**
```bash
npm run dev          # Runs both backend and frontend concurrently
```

**Option B: Separate Terminals**

Terminal 1 - Backend (port 8000):
```bash
cd backend
python -m uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend (port 3000):
```bash
cd frontend
npm run dev
```

### 5. Access Application

Open your browser and visit:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## Usage Guide

### Generating MCQs

1. **Upload File**
   - Click on upload area or drag PDF/PPTX/TXT file
   - File is automatically uploaded to cloud storage
   - Text extraction begins immediately

2. **MCQ Generation**
   - After upload, 10 questions are generated automatically
   - AI processes content using Groq (Llama 3.3 70B)
   - Questions appear with correct answers highlighted

3. **View Results**
   - All questions displayed with answer keys
   - Correct answers shown in green
   - Clear, organized format

4. **Additional Options**
   - **Generate More**: Create additional questions from same document
   - **Download PDF**: Export questions and answers
   - **New File**: Start with a new document

---

## API Endpoints

### Health Check
```http
GET /
```
Response:
```json
{
  "message": "PDF to MCQ Generator API",
  "version": "1.0.0"
}
```

### Upload PDF
```http
POST /api/upload-pdf
Content-Type: multipart/form-data

file: <PDF file>
```
Response:
```json
{
  "filename": "document.pdf",
  "text": "Extracted text content...",
  "blob_url": "https://blob.vercel-storage.com/...",
  "status": "success"
}
```

### Generate MCQs
```http
POST /api/generate-mcqs
Content-Type: application/json

{
  "text": "Your document text here",
  "num_questions": 10
}
```
Response:
```json
{
  "questions": [
    {
      "question": "What is machine learning?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "A"
    }
  ],
  "status": "success"
}
```

**Full API Documentation**: Visit `/docs` endpoint for interactive Swagger UI

---

## Architecture

```
┌──────────────┐         ┌─────────────┐         ┌──────────────┐
│    React     │◄───────►│   FastAPI   │◄───────►│  Groq API    │
│   Frontend   │  HTTP   │   Backend   │  HTTP   │ (Llama 3.3)  │
│  (Port 3000) │         │ (Port 8000) │         └──────────────┘
└──────────────┘         └─────────────┘
                                │
                                ↓
                         ┌─────────────┐
                         │ Vercel Blob │
                         │   Storage   │
                         └─────────────┘

Flow:
1. User uploads PDF → React Frontend
2. Frontend → FastAPI (upload-pdf endpoint)
3. FastAPI → Vercel Blob (store PDF)
4. FastAPI extracts text from PDF
5. Frontend → FastAPI (generate-mcqs endpoint)
6. FastAPI → Groq AI (Llama 3.3)
7. AI generates MCQs
8. FastAPI → Frontend (return questions)
9. User views questions with answers
10. Frontend allows PDF download
```

---

## AI System

The application uses Groq API with Llama 3.3 70B for fast, powerful MCQ generation.

---

## Documentation

- **[API Documentation](docs/API.md)** - Complete API reference
- **[Setup Guide](docs/SETUP.md)** - Detailed setup instructions
- **[Environment Configuration](docs/ENV_CONFIGURATION.md)** - Environment variables guide
- **[Vercel Deployment](docs/VERCEL_DEPLOYMENT.md)** - Deploy to Vercel
- **[Vercel Blob Setup](docs/VERCEL_BLOB_SETUP.md)** - Cloud storage setup
- **[Backend Guide](docs/BACKEND_GUIDE.md)** - Backend architecture
- **[Frontend Guide](docs/FRONTEND_GUIDE.md)** - Frontend development
- **[Configuration](docs/CONFIGURATION.md)** - Customization options

---

## Deployment

### Vercel (Recommended)

1. **Fork/Clone Repository**
2. **Connect to Vercel**
   - Import project on Vercel dashboard
   - Select the repository
3. **Configure Environment Variables**
   ```
   GROQ_API_KEY=your_key
   BLOB_READ_WRITE_TOKEN=auto_generated
   ```
4. **Deploy**
   - Vercel automatically builds and deploys
   - Frontend and API deployed together

**Live Demo**: Your app will be live at `your-app.vercel.app`

See [docs/VERCEL_DEPLOYMENT.md](docs/VERCEL_DEPLOYMENT.md) for detailed guide.

### Local Production Build

```bash
# Build frontend
cd frontend
npm run build

# Serve production build
npm run preview

# Or use Python server
python -m http.server 3000 -d dist
```

---

## Development

### Backend Development

The backend uses FastAPI with a serverless architecture:

- **routes.py** - API endpoint definitions
- **handlers.py** - Business logic
- **models.py** - Pydantic data models
- **mcq_generator.py** - AI integration

Add new features by:
1. Define route in `routes.py`
2. Add model in `models.py`
3. Implement logic in appropriate module

### Frontend Development

React frontend with component-based architecture:

- **App.jsx** - Main state management
- **MCQResults.jsx** - Answer key display
- **FileUpload.jsx** - File upload component
- **LoadingAnimation.jsx** - Loading states

Styling: Tailwind CSS classes with custom gradients

### Testing API

```bash
# Test health endpoint
curl http://localhost:8000/

# Test with sample data
curl -X POST http://localhost:8000/api/generate-mcqs \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text", "num_questions": 3}'
```

Interactive testing: http://localhost:8000/docs

---

## Troubleshooting

### "API Key Required" Error
- Ensure GROQ_API_KEY is set in `.env`
- Verify key is valid on Groq platform

### "CORS Error" in Browser
- Check backend is running on port 8000
- Verify CORS settings in backend allow frontend origin

### "Blob Upload Failed"
- Verify BLOB_READ_WRITE_TOKEN is configured
- Check Vercel Blob storage is enabled in project

### "Failed to Generate MCQs"
- Check PDF has extractable text (not scanned images)
- Verify AI API keys are valid
- Check API quota/limits not exceeded

### Slow Generation
- First request may be slower (model initialization)
- Large PDFs take longer to process
- Check internet connection for API calls

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

For more help, see [docs/SETUP.md](docs/SETUP.md)

---

## Key Features Explained

### MCQ Generation Flow
1. File uploaded (PDF/PPTX/TXT) → Text extraction begins
2. AI generates questions automatically using Groq
3. Questions displayed immediately with correct answers highlighted
4. Download as PDF or generate more questions

### PDF Export
- Download questions as formatted PDF
- Includes all questions with correct answers
- Correct answers highlighted in green
- Professional formatting with page numbers

### Smart AI Integration
- Groq (Llama 3.3 70B): Fast, powerful cloud LLM inference
- Optimized prompts for high-quality MCQ generation

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Changes**
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly
4. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open Pull Request**
   - Describe your changes
   - Link any related issues

### Areas for Contribution
- Add more AI model options
- Improve UI/UX
- Add question difficulty levels
- Support more file formats
- Add analytics and tracking
- Improve error handling
- Write tests

---

## License

MIT License

Copyright (c) 2026 Vishal Baraiya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## Acknowledgments

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://react.dev/)** - JavaScript library for building user interfaces
- **[Groq](https://groq.com/)** - High-performance AI inference
- **[Vercel](https://vercel.com/)** - Deployment and blob storage platform
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Framer Motion](https://www.framer.com/motion/)** - Animation library
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF processing library
- **[jsPDF](https://github.com/parallax/jsPDF)** - PDF generation in JavaScript

---

## Author

**Vishal Baraiya**  
B.Tech CSE Student

GitHub: [@mr-baraiya](https://github.com/mr-baraiya)  
Repository: [pdf-to-mcq-generator](https://github.com/mr-baraiya/pdf-to-mcq-generator)

---

## Future Enhancements

- [ ] Multiple choice and True/False question types
- [ ] Question difficulty levels (Easy/Medium/Hard)
- [ ] Export to Word/Excel formats
- [ ] Database integration for saving quizzes
- [ ] User authentication and profiles
- [ ] Quiz history and analytics
- [ ] Support for PowerPoint and Word documents
- [ ] Batch processing multiple PDFs
- [ ] Custom AI model selection in UI
- [ ] Mobile app version (React Native)
- [ ] Collaborative quiz creation
- [ ] Question bank and library
- [ ] Time-limited quiz mode
- [ ] Leaderboard and gamification

---

## Support

Need help? Try these resources:

- **Documentation**: Check the `/docs` folder
- **Issues**: Open an issue on GitHub
- **API Docs**: Visit `/docs` endpoint when running locally
- **Discussions**: GitHub Discussions for questions

---

**Built with care for education and learning**

Star this repository if you find it useful!
