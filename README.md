# PDF to MCQ Generator using FastAPI & React

An AI-powered full-stack application that automatically generates Multiple Choice Questions (MCQs) from PDF documents using Ollama and local Large Language Models (LLMs) like Mistral or Llama3.

**Backend:** FastAPI REST API  
**Frontend:** React with Vite  
**LLM:** Ollama (Mistral, Llama3, etc.)  
**Database:** None (stateless processing)  

---

## 🌟 Features

- 📄 **PDF Upload** - Upload any PDF file with drag-and-drop or file selection
- ☁️ **Vercel Blob Storage** - PDFs stored securely in serverless cloud storage
- 🤖 **AI-Powered MCQ Generation** - Uses Ollama with Mistral/Llama3 models
- 🔌 **REST API** - Well-documented FastAPI endpoints
- 💻 **React Frontend** - Modern, responsive UI built with Vite
- 🚀 **Fully Offline** - Runs completely locally, no cloud services required (optional Blob storage)
- ⚡ **Real-time Processing** - Instant PDF text extraction and MCQ generation
- 🎨 **Beautiful UI** - Clean interface with loading states and result visualization
- ✅ **Answer Verification** - Built-in quiz mode with score calculation
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices

---

## 🛠️ Technologies Used

### Backend
- **Python** 3.8+
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **PyPDF2** - PDF text extraction
- **Ollama** - Local LLM inference
- **Pydantic** - Data validation

### Frontend
- **React** 18
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS 3** - Styling
- **React Icons** - Icon library

### LLM
- **Ollama** - Local inference engine
- **Mistral** - Default model (~/7B)
- **Llama3** - Alternative model option

---

## 📋 Project Structure

```
pdf-to-mcq-generator/
│
├── 📁 backend/
│   ├── app.py                          # FastAPI application
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment template
│   ├── .gitignore
│   │
│   └── 📁 src/
│       ├── 📁 pdf/
│       │   ├── __init__.py
│       │   └── extractor.py            # PDF text extraction
│       │
│       ├── 📁 llm/
│       │   ├── __init__.py
│       │   └── mcq_generator.py        # MCQ generation logic
│       │
│       └── 📁 utils/                   # Utility functions
│
├── 📁 frontend/
│   ├── index.html                      # HTML entry point
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── .gitignore
│   │
│   └── 📁 src/
│       ├── main.jsx                    # React entry point
│       ├── App.jsx                     # Main App component
│       ├── App.css                     # App styles
│       ├── index.css                   # Global styles
│       │
│       └── 📁 components/
│           ├── FileUpload.jsx              # PDF upload component
│           ├── FileUpload.css
│           ├── MCQDisplay.jsx             # Question display
│           ├── MCQDisplay.css
│           ├── Loading.jsx                # Loading indicator
│           └── Loading.css
│
├── 📁 docs/
│   ├── API.md                          # API documentation
│   ├── SETUP.md                        # Setup & deployment guide
│   ├── BACKEND_GUIDE.md                # Backend development guide
│   └── FRONTEND_GUIDE.md               # Frontend development guide
│
└── README.md                           # This file
```

---

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- Ollama (download from https://ollama.com/download)

### 1. Clone repository

```bash
git clone https://github.com/yourusername/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

### 2. Install Ollama and download model

Download Ollama from: https://ollama.com/download

Then pull the Mistral model:

```bash
ollama pull mistral
```

Make sure Ollama is running before starting the API.

### 3. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Start the FastAPI server:

```bash
python app.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Running Both Simultaneously

Open two terminals:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:3000` in your browser.

---

## How it works

### Frontend to Backend Flow

1. **Upload PDF** - User uploads a PDF file via React frontend
2. **API Call** - Frontend sends POST request to `/upload-pdf` endpoint
3. **PDF Processing** - Backend extracts text using PyPDF2
4. **MCQ Generation** - Frontend requests MCQ generation via `/generate-mcqs` endpoint
5. **LLM Processing** - Ollama generates questions using Mistral model
6. **Display Results** - React frontend displays questions and options
7. **User Interaction** - User selects answers and views results

### API Endpoints

- `GET /` - Health check
- `POST /upload-pdf` - Upload and extract text from PDF
- `POST /generate-mcqs` - Generate MCQs from text

### Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   React     │◄────────►│  FastAPI     │◄────────►│   Ollama   │
│  Frontend   │  (Port   │   Backend    │  (LLM   │  (Port     │
│ (Port 3000) │   3000)  │  (Port 8000) │ Model)  │  11434)    │
└─────────────┘         └──────────────┘         └────────────┘
       │                       │                        │
       └───────► PDF Upload    │                        │
       ◄────────────────────────────────────────────────┘
       │
       ├─► Extract Text from PDF
       │
       ├─► Generate MCQs
       │
       └─► Display Results
```

---

---

## 🚀 Quick Start

### Prerequisites
- **Python** 3.8 or higher
- **Node.js** 14 or higher
- **Ollama** (download from https://ollama.com/download)
- **RAM:** 4GB minimum (8GB+ recommended)
- **Disk:** 5GB+ (for models)

### 1️⃣ Install Ollama

Download and install Ollama from: https://ollama.com/download

Pull the Mistral model:
```bash
ollama pull mistral
```

Verify Ollama is running at: http://localhost:11434

### 2️⃣ Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Start the API
python app.py
```

✅ API running at: `http://localhost:8000`  
📚 API Docs at: `http://localhost:8000/docs`

### 3️⃣ Frontend Setup (React)

In a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: `http://localhost:3000`

### 4️⃣ Open in Browser

Visit: **http://localhost:3000**

---

## 📖 Usage

1. **Upload PDF** - Drag and drop or click to select a PDF file
2. **Extract Text** - Text is automatically extracted from the PDF
3. **Generate Questions** - Click "Generate N Questions" button
4. **Answer Questions** - Select your answers for each question
5. **Check Results** - Click "Check Answers" to see your score
6. **Generate More** - Create new questions or upload another PDF

---

## 🔌 API Endpoints

### Health Check
```http
GET /
```

### Upload PDF
```http
POST /upload-pdf
Content-Type: multipart/form-data

file: <PDF file>
```

### Generate MCQs
```http
POST /generate-mcqs
Content-Type: application/json

{
  "text": "Your text here",
  "num_questions": 5
}
```

**📚 Full API Documentation**: See [docs/API.md](docs/API.md)

---

## 🎯 Example Output

```json
{
  "questions": [
    {
      "question": "What is Deep Learning?",
      "options": {
        "A": "Subset of Machine Learning",
        "B": "Programming Language",
        "C": "Database System",
        "D": "Operating System"
      },
      "answer": "A"
    }
  ],
  "status": "success"
}
```

---

## 📚 Documentation

- **[Quick Start](QUICKSTART.md)** - Get up and running in 3 steps
- **[API Documentation](docs/API.md)** - Complete API reference and examples
- **[Environment Configuration](docs/ENV_CONFIGURATION.md)** - Setup credentials and environment variables
- **[Vercel Deployment](docs/VERCEL_DEPLOYMENT.md)** - Deploy to Vercel with serverless backend
- **[Frontend API Configuration](docs/FRONTEND_API_CONFIG.md)** - Configure frontend for local and production APIs
- **[Setup & Deployment](docs/SETUP.md)** - Installation, configuration, and deployment guides
- **[Vercel Blob Setup](docs/VERCEL_BLOB_SETUP.md)** - Cloud storage integration guide
- **[Backend Guide](docs/BACKEND_GUIDE.md)** - Backend architecture and development
- **[Frontend Guide](docs/FRONTEND_GUIDE.md)** - Frontend structure and components
- **[Configuration](docs/CONFIGURATION.md)** - Customization and configuration options

---

## 🔧 Development

### Backend Development

See [docs/BACKEND_GUIDE.md](docs/BACKEND_GUIDE.md) for:
- Architecture overview
- Adding new endpoints
- Error handling & logging
- Testing and debugging
- Performance optimization

### Frontend Development

See [docs/FRONTEND_GUIDE.md](docs/FRONTEND_GUIDE.md) for:
- Component structure
- API integration
- Styling guidelines
- Common tasks
- Troubleshooting

### Testing

```bash
# Test API
curl -X POST http://localhost:8000/generate-mcqs \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text", "num_questions": 3}'

# Visit interactive docs
# http://localhost:8000/docs
```

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
docker-compose up
```

This runs:
- FastAPI backend on port 8000
- React frontend on port 3000
- Ollama service on port 11434

---

## 🚀 Production Deployment

### Option 1: Traditional Server
- Deploy backend with Gunicorn
- Deploy frontend build to static hosting
- Use environment variables for configuration

### Option 2: Cloud Platforms
- **Heroku** - Backend deployment
- **Vercel** - Frontend deployment
- **AWS/GCP/Azure** - Full stack deployment

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Push and create a Pull Request

---

## 📝 License

MIT License - Feel free to use this project for personal or commercial purposes.

---

## 🐛 Troubleshooting

### "Ollama connection refused"
- Ensure Ollama is running
- Check: `http://localhost:11434`

### "Model not found"
```bash
ollama pull mistral
```

### "Frontend can't connect to backend"
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app.py`

### "Slow MCQ generation"
- First request loads the model (normal)
- Subsequent requests are faster
- Use GPU acceleration for better performance

See [docs/SETUP.md](docs/SETUP.md) for more troubleshooting.

---

## 🎓 Learning Resources

This project demonstrates:
- ✅ FastAPI and REST API design
- ✅ React and modern frontend development
- ✅ Integration with LLMs (Large Language Models)
- ✅ File upload handling
- ✅ PDF processing
- ✅ Full-stack web development
- ✅ CORS and API security basics
- ✅ Responsive design

**Perfect for:**
- Students learning full-stack development
- Portfolio projects
- AI/ML integration examples
- Educational applications

---

## 👨‍💻 Author

**Vishal Baraiya**  
B.Tech CSE Student

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - JavaScript UI library
- [Ollama](https://ollama.com/) - Local LLM inference
- [Mistral AI](https://mistral.ai/) - LLM model
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF processing

---

## 💡 Future Enhancements

- [ ] Export MCQs to PDF/Word
- [ ] Database for storing MCQs
- [ ] Difficulty levels (Easy/Medium/Hard)
- [ ] Multi-language support
- [ ] Batch PDF processing
- [ ] Custom model selection UI
- [ ] User authentication
- [ ] Mobile app version
- [ ] MCQ sharing & collaboration
- [ ] Analytics dashboard

---

## 📞 Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

**Happy Learning! 🎉**
