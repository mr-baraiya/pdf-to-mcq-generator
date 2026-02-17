# PDF to MCQ Generator using Ollama (LLM)

An AI-powered application that automatically generates Multiple Choice Questions (MCQs) from PDF documents using Ollama and local Large Language Models (LLMs) like Mistral or Llama3.

This project extracts text from uploaded PDFs and uses deep learning models to generate meaningful questions, options, and correct answers.

---

## Features

- Upload any PDF file
- Extract text automatically
- Generate MCQs using Ollama LLM
- Fully offline (runs locally)
- Fast and accurate question generation
- Simple and clean Streamlit interface
- Modular and scalable project structure

---

## Technologies Used

- Python
- Streamlit
- Ollama (LLM)
- Mistral / Llama3 model
- PyPDF2
- NLP / Deep Learning

---

## Project Structure

```

pdf-to-mcq-generator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── pdf/
│   │   └── extractor.py
│   │
│   ├── llm/
│   │   └── mcq_generator.py
│   │
│   └── utils/
│
├── data/
├── assets/
└── docs/

```

---

## Installation

### 1. Clone repository

```

git clone [https://github.com/yourusername/pdf-to-mcq-generator.git](https://github.com/yourusername/pdf-to-mcq-generator.git)
cd pdf-to-mcq-generator

```

### 2. Install dependencies

```

pip install -r requirements.txt

```

### 3. Install Ollama

Download from:
https://ollama.com/download

Pull model:

```

ollama pull mistral

```

---

## How it works

1. Upload PDF
2. Extract text from PDF
3. Send text to Ollama model
4. Generate MCQs
5. Display questions and answers

---

## Example Output

```

Question: What is Deep Learning?

A. Subset of Machine Learning
B. Programming Language
C. Database System
D. Operating System

Answer: A

```

---

## Future Improvements

- Export MCQs to PDF
- Save MCQs in database
- Difficulty levels
- Web deployment
- Support multiple models

---

## Author

Vishal Baraiya  
B.Tech CSE Student  

---

## Benefits

- Great for students and teachers
- Useful for exam preparation
- Strong NLP and Deep Learning project
- Resume-worthy AI project
