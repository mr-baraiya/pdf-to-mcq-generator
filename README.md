# PDF to MCQ Generator

An AI-powered web application that automatically generates Multiple Choice Questions (MCQs) from PDF documents using advanced AI models (Ollama).

**Live Features:**
- Quiz Attempt Mode - Try quiz before seeing answers
- PDF Export - Download questions and results as PDF
- Smart AI Selection - Automatically chooses best AI model
- Cloud Storage - Secure PDF storage with Vercel Blob
- Interactive Quiz - Real-time feedback and scoring

---

## Features

### Core Functionality
- **PDF Upload & Processing** - Drag-and-drop interface with cloud storage
- **AI-Powered Generation** - Uses Groq (Llama 3.3) and Gemini AI models
- **Smart Load Balancing** - Automatically selects optimal AI based on content size
- **Quiz Attempt Mode** - Interactive quiz interface with instant feedback
- **Answer Key View** - Detailed solutions with correct answers highlighted
- **PDF Export** - Download questions and results in PDF format
- **Score Tracking** - Real-time score calculation with percentage display
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
- **PyPDF2** - PDF text extraction
- **Groq API** - Fast LLM inference (Llama 3.3 70B)
- **Google Gemini** - Advanced AI for complex documents
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

### AI Models
- **Groq (Llama 3.3 70B)** - Primary model for fast generation
- **Google Gemini Pro** - Advanced understanding for complex texts
- **Smart Selection** - Auto-switches based on document size

---

## Project Structure

```
pdf-to-mcq-generator/
├── api/                            # Backend API
│   ├── index.py                    # Main Vercel serverless entry
│   ├── routes.py                   # API endpoints
│   ├── handlers.py                 # Request handlers
│   ├── models.py                   # Data models
│   ├── config.py                   # Configuration
│   ├── llm/
│   │   ├── __init__.py
│   │   └── mcq_generator.py        # AI MCQ generation logic
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── extractor.py            # PDF text extraction
│   └── utils/
│       ├── __init__.py
│       └── blob_storage.py         # Vercel Blob integration
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
│   │       ├── FileUpload.jsx      # PDF upload
│   │       ├── MCQDisplay.jsx      # Quiz attempt mode
│   │       ├── MCQResults.jsx      # Answer key view
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
- **Gemini API Key** (get from https://makersuite.google.com/app/apikey)
- **Vercel Account** (for Blob storage - optional for local dev)

### 1. Clone Repository

```bash
git clone https://github.com/mr-baraiya/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```bash
# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Vercel Blob Storage (optional for local)
BLOB_READ_WRITE_TOKEN=your_vercel_blob_token_here
```

Get API keys:
- **Groq**: https://console.groq.com/keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **Vercel Blob**: https://vercel.com/docs/storage/vercel-blob

### 3. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 4. Run Development Servers

**Option A: Using npm scripts (Recommended)**
```bash
npm run build          # Build frontend
python -m http.server 3000 -d frontend/dist  # Serve frontend
vercel dev            # Run backend API
```

**Option B: Separate Terminals**

Terminal 1 - Backend (port 8000):
```bash
python api/index.py
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

1. **Upload PDF**
   - Click on upload area or drag PDF file
   - File is automatically uploaded to cloud storage
   - Text extraction begins immediately

2. **MCQ Generation**
   - After upload, 10 questions are generated automatically
   - AI automatically selects best model based on document size
   - Questions appear in quiz attempt mode

3. **Attempt Quiz**
   - Read each question carefully
   - Select answer (A, B, C, or D) for each question
   - Click "Check Answers" when done

4. **View Results**
   - See your score percentage
   - Correct answers shown in green
   - Incorrect answers shown in red
   - Click "Show Answers" for detailed answer key

5. **Additional Options**
   - **Generate More**: Create 5 additional questions
   - **Download PDF**: Export questions and results
   - **Re-attempt Quiz**: Try again
   - **New PDF**: Start with a new document

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
└──────────────┘         └─────────────┘                │
                                │                       │
                                ↓                       ↓
                         ┌─────────────┐         ┌──────────────┐
                         │ Vercel Blob │         │  Gemini API  │
                         │   Storage   │         │ (Fallback)   │
                         └─────────────┘         └──────────────┘

Flow:
1. User uploads PDF → React Frontend
2. Frontend → FastAPI (upload-pdf endpoint)
3. FastAPI → Vercel Blob (store PDF)
4. FastAPI extracts text from PDF
5. Frontend → FastAPI (generate-mcqs endpoint)
6. FastAPI → AI Model (Groq/Gemini based on size)
7. AI generates MCQs
8. FastAPI → Frontend (return questions)
9. User attempts quiz
10. Frontend shows results & downloads PDF
```

---

## Smart AI Selection

The system automatically selects the best AI model based on document size:

- **Small PDFs (< 50KB)**: Groq (Llama 3.3) - Faster response
- **Large PDFs (> 5MB)**: Gemini Pro - Better comprehension
- **Medium PDFs (50KB - 5MB)**: Round-robin between both
- **Fallback**: If Groq fails, automatically switches to Gemini

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
   GEMINI_API_KEY=your_key
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
- **MCQDisplay.jsx** - Quiz attempt interface
- **MCQResults.jsx** - Answer key view
- **FileUpload.jsx** - PDF upload component

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
- Ensure GROQ_API_KEY and GEMINI_API_KEY are set in `.env`
- Verify keys are valid on respective platforms

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

### Quiz Attempt Flow
1. PDF uploaded → Questions generated automatically
2. User taken directly to quiz attempt page
3. Select answers (A, B, C, D) for each question
4. Click "Check Answers" to submit
5. View score with color-coded results
6. Click "Show Answers" to see detailed answer key

### PDF Export
- Download questions as formatted PDF
- Includes score if quiz attempted
- Correct answers highlighted in green
- Professional formatting with page numbers

### Smart AI Integration
- Groq (Llama 3.3 70B): Fast, efficient for most documents
- Google Gemini Pro: Advanced understanding for complex content
- Automatic selection based on document characteristics
- Seamless fallback if primary model unavailable

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
- **[Google Gemini](https://ai.google.dev/)** - Advanced AI model
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
