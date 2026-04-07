# PDF to MCQ Generator

An intelligent web application that automatically generates Multiple Choice Questions (MCQs) from PDF, PowerPoint, and text documents using a Retrieval-Augmented Generation (RAG) pipeline.

### Live Demo
**Frontend:** [https://pdf2mcq-henna.vercel.app/](https://pdf2mcq-henna.vercel.app/)  
**Backend API Docs:** [https://pdf-to-mcq-generator-fastapi.onrender.com/docs](https://pdf-to-mcq-generator-fastapi.onrender.com/docs)

---

## Features

*   **Multi-Format Support**: Upload PDF, PPTX, and TXT files with a simple drag-and-drop interface.
*   **Advanced Text Extraction**: Includes OCR capabilities to extract text from scanned, image-based PDFs.
*   **AI-Powered Generation**: Leverages the Groq Llama 3.3 70B model for high-quality question generation.
*   **Customizable Output**: Generate between 3 and 50 MCQs at a time.
*   **Interactive Results**: View paginated results, with correct answers highlighted for easy review.
*   **Export to PDF**: Save your generated question sets as a PDF document.
*   **Modern UI**: A fully responsive and animated user interface built with React and Framer Motion.

---

## How It Works: The RAG Pipeline

This project uses a **Retrieval-Augmented Generation (RAG)** architecture to ensure that the generated MCQs are accurate and grounded in the provided document's content. The backend pipeline is orchestrated using **LangChain**.

1.  **Text Extraction**: The system first extracts raw text from the uploaded document. It handles standard PDFs and PPTX files, and uses `pytesseract` for OCR on image-based PDFs.
2.  **Chunking**: The extracted text is split into smaller, overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`. This helps in creating manageable pieces of content for embedding.
3.  **Embedding**: Each text chunk is converted into a numerical vector (embedding) using a `sentence-transformers` model (`all-MiniLM-L6-v2`) via LangChain's `HuggingFaceEmbeddings`.
4.  **Indexing & Retrieval**: The embeddings are stored in an in-memory **FAISS** vector store. When a request for MCQs is made, the system searches this store to find the most semantically relevant chunks of text based on a query.
5.  **Generation**: Instead of sending the entire document to the language model, only the most relevant, retrieved chunks are passed as context to the **Groq Llama 3.3 70B** model. This focused context allows the model to generate accurate, relevant questions while minimizing hallucinations.
6.  **Parsing**: The structured JSON output from the model is parsed and sent to the frontend for display.

---

## Tech Stack

| Category      | Technology                                                                                             |
| :------------ | :----------------------------------------------------------------------------------------------------- |
| **Backend**   | [FastAPI](https://fastapi.tiangolo.com/), [Python](https://www.python.org/)                             |
| **Frontend**  | [React](https://reactjs.org/), [Vite](https://vitejs.dev/), [TailwindCSS](https://tailwindcss.com/)      |
| **AI/ML**     | [LangChain](https://www.langchain.com/), [Groq](https://groq.com/) (Llama 3.3 70B), [FAISS](https://faiss.ai/), [Hugging Face](https://huggingface.co/) |
| **Deployment**| [Vercel](https://vercel.com/) (Frontend), [Render](https://render.com/) (Backend)                        |
| **Storage**   | [Vercel Blob](https://vercel.com/storage/blob)                                                         |

---

## Getting Started

### Prerequisites

*   Python 3.9+
*   Node.js 18+
*   Tesseract OCR Engine (must be in your system's PATH)
*   Poppler (for `pdf2image`)

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/pdf-to-mcq-generator.git
    cd pdf-to-mcq-generator/backend
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the `backend` directory and add your API keys:
    ```env
    GROQ_API_KEY="your_groq_api_key"
    HF_TOKEN="your_huggingface_token"
    BLOB_READ_WRITE_TOKEN="your_vercel_blob_token"
    ```

5.  **Run the server:**
    ```bash
    uvicorn index:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.

---

## Project Structure

```
pdf-to-mcq-generator/
│
├── backend/
│   ├── index.py          # FastAPI app entrypoint & middleware
│   ├── routes.py         # API routes (/upload, /generate)
│   ├── mcq_generator.py  # Core RAG pipeline and Groq logic
│   ├── extractor.py      # Text extraction from documents
│   ├── blob_storage.py   # Vercel Blob storage handler
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variable template
│
└── frontend/
    ├── src/
    │   ├── App.jsx       # Main component with routing
    │   ├── pages/        # Page components
    │   └── components/   # Reusable UI components
    └── package.json      # Node.js dependencies
```

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
