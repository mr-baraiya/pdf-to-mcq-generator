# Setup & Deployment Guide

## System Requirements

- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Node.js**: 14 or higher
- **RAM**: Minimum 4GB (8GB+ recommended for smooth LLM operation)
- **Disk Space**: 5GB+ (for Ollama models)

## Development Setup

### Step 1: Clone and Navigate

```bash
git clone https://github.com/yourusername/pdf-to-mcq-generator.git
cd pdf-to-mcq-generator
```

### Step 2: Install Ollama

1. Download from: https://ollama.com/download
2. Install and run the application
3. Pull the Mistral model:
   ```bash
   ollama pull mistral
   ```
4. Verify Ollama is running at `http://localhost:11434`

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the backend
python app.py
```

The backend API will be available at: `http://localhost:8000`

Swagger UI Documentation: `http://localhost:8000/docs`

### Step 4: Frontend Setup

In a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

---

## Environment Variables

### Backend (.env)

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

---

## Project Structure

```
pdf-to-mcq-generator/
├── backend/
│   ├── app.py                    # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   ├── .gitignore
│   └── src/
│       ├── pdf/
│       │   ├── __init__.py
│       │   └── extractor.py      # PDF text extraction
│       ├── llm/
│       │   ├── __init__.py
│       │   └── mcq_generator.py  # MCQ generation logic
│       └── utils/                # Utility functions
│
├── frontend/
│   ├── index.html                # HTML entry point
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── .gitignore
│   └── src/
│       ├── main.jsx              # React entry point
│       ├── App.jsx               # Main App component
│       ├── App.css               # App styles
│       ├── index.css             # Global styles
│       └── components/
│           ├── FileUpload.jsx    # PDF upload component
│           ├── FileUpload.css
│           ├── MCQDisplay.jsx    # Questions display
│           ├── MCQDisplay.css
│           ├── Loading.jsx       # Loading spinner
│           └── Loading.css
│
├── docs/
│   ├── API.md                    # API documentation
│   └── SETUP.md                  # This file
│
└── README.md
```

---

## Testing the Application

### 1. Test API Endpoints

Visit the interactive Swagger UI:
```
http://localhost:8000/docs
```

### 2. Test Frontend

1. Open `http://localhost:3000`
2. Upload a PDF file
3. Click "Generate 5 Questions"
4. Answer the questions
5. Click "Check Answers"

### 3. Test with Sample PDF

Create a simple text file with content and convert it to PDF:

```
Sample content about machine learning:
Machine learning is a subset of artificial intelligence that enables 
systems to learn and improve from experience without being explicitly programmed.
It focuses on developing neural networks and algorithms that can process 
data and make predictions with minimal human intervention.
```

---

## Running Tests

### Backend Tests

```bash
cd backend
pip install pytest
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Building for Production

### Backend

```bash
cd backend

# Regular Python deployment
python app.py

# Or with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Frontend

```bash
cd frontend

# Build production bundle
npm run build

# The output will be in the 'dist' folder
# Serve with any static server:
# python -m http.server 3000 --directory dist
```

---

## Deployment Options

### Option 1: Docker (Recommended)

Create a `docker-compose.yml` in the root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      OLLAMA_HOST: http://ollama:11434
    depends_on:
      - ollama

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

volumes:
  ollama_data:
```

Run with:
```bash
docker-compose up
```

### Option 2: Cloud Deployment

#### Heroku
```bash
# Backend
git push heroku main:main

# Frontend
npm run build
# Deploy the dist folder to any static hosting (Vercel, Netlify)
```

#### AWS/GCP/Azure
- Deploy backend to EC2/Cloud Run/App Service
- Deploy frontend to CloudFront/Cloud Storage/Static Web Apps
- Use managed services for Ollama (RAPIDS on GPU instances)

---

## Troubleshooting

### Issue: "Connection refused" at localhost:8000

**Solution:**
- Ensure backend is running: `python app.py`
- Check if port 8000 is available: `lsof -i :8000`
- Kill process if needed: `kill -9 <PID>`

### Issue: "Ollama model not found"

**Solution:**
```bash
ollama pull mistral
# or use another model
ollama pull llama2
```

### Issue: Frontend can't connect to backend

**Solution:**
- Check CORS settings in `backend/app.py`
- Ensure backend is running on correct port
- Update API URL in frontend if needed

### Issue: Slow MCQ generation

**Solution:**
- First request initializes the model (normal)
- Use a smaller model: `ollama pull neural-chat`
- Increase available memory/RAM
- Use GPU acceleration if available

### Issue: "No space left on device"

**Solution:**
- Models require significant disk space
- Check disk usage: `df -h`
- Clean up old model: `ollama rm <model_name>`

---

## Performance Optimization

### Backend

- Use async processing for large PDFs
- Implement caching for frequently requested MCQs
- Use connection pooling for Ollama

### Frontend

- Implement lazy loading for large question sets
- Cache API responses
- Use React.memo for performance optimization
- Optimize images and assets

### General

- Use GPU acceleration for Ollama models
- Deploy on high-performance servers
- Use CDN for static frontend assets

---

## Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Push to branch: `git push origin feature/your-feature`
4. Create a Pull Request

---

## License

MIT License - See LICENSE file

---

## Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with detailed description
- Include error logs and system information

---

## Version History

### v1.0.0 (Current)
- Initial release with FastAPI backend
- React frontend with Vite
- PDF extraction with PyPDF2
- MCQ generation with Ollama/Mistral
