# Ollama Configuration Guide

## What is Ollama?

Ollama is an **open-source AI model runner** that lets you run LLMs (Large Language Models) locally on your computer.

---

## Current .env Configuration

```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
```

### What Each Variable Means:

**1. OLLAMA_HOST**
   - URL where Ollama API runs locally
   - `localhost:11434` = your computer at port 11434
   - Default value: `http://localhost:11434`
   - Change if Ollama runs on different port

**2. OLLAMA_MODEL**
   - Which AI model to use
   - `mistral` = Mistral LLM (lightweight, fast)
   - Other options: `llama2`, `neural-chat`, `dolphin-mixtral`

---

## How to Get Ollama Working

### Step 1: **Check if Ollama is Installed**

Open terminal and run:
```bash
ollama --version
```

If you see version output  Ollama is installed 
If you see "command not found"  Install from: https://ollama.com

### Step 2: **Start Ollama Server**

```bash
ollama serve
```

Output:
```
2024/02/17 13:00:00 "Listening on 127.0.0.1:11434"
```

Leave this running in background. Now Ollama API is at `http://localhost:11434`

### Step 3: **Pull a Model**

Open NEW terminal and run:
```bash
ollama pull mistral
```

This downloads Mistral model (~4GB). Takes 5-10 minutes.

Output:
```
pulling af83e3f3f667
 100%
Success!
```

### Step 4: **List Available Models**

```bash
ollama list
```

Output:
```
NAME              ID              SIZE      MODIFIED
mistral:latest    8eb4a5957a99    4.1 GB    2 minutes ago
```

---

## How to Use in Our App

### When the API starts, it:

1. Connects to Ollama at: `http://localhost:11434`
2. Uses model: `mistral`
3. Sends text prompts to generate MCQs
4. Gets response back and returns to frontend

### Test if it's working:

```bash
curl http://localhost:11434/api/generate \
  -X POST \
  -d '{
    "model": "mistral",
    "prompt": "What is Python?",
    "stream": false
  }'
```

You'll get AI response in JSON format 

---

## Alternative Models

Instead of `mistral`, you can use:

### Lightweight (Fast, Low RAM)
- `mistral` - 4GB (RECOMMENDED)
- `neural-chat` - 3.8GB
- `orca-mini:3b` - 1.8GB

### Powerful but Heavy
- `llama2` - 4GB
- `dolphin-mixtral` - 8GB
- `neural-chat:7b` - 4.1GB

### Change Model in .env

```
OLLAMA_MODEL=llama2
```

Then pull it:
```bash
ollama pull llama2
```

---

## Troubleshooting

### Problem: "Cannot connect to Ollama at http://localhost:11434"

**Solution:**
1. Is Ollama running? Run `ollama serve` in terminal
2. Check localhost is active: `curl http://localhost:11434`
3. Change port in .env if needed

### Problem: "Model not found"

**Solution:**
1. Pull the model: `ollama pull mistral`
2. List models: `ollama list`
3. Use existing model in .env

### Problem: API slow or hanging

**Solution:**
1. Model might be downloading/loading
2. Not enough RAM available
3. Try smaller model like `orca-mini:3b`

---

## Current .env Status

 OLLAMA_HOST=`http://localhost:11434` (CORRECT)
 OLLAMA_MODEL=`mistral` (CORRECT)

### What You Need to Do:

1. **Install Ollama**  https://ollama.com/download
2. **Run:** `ollama serve` (in terminal 1)
3. **Run in NEW terminal:** `ollama pull mistral`
4. **Start backend:** `python api/index.py`
5. **Start frontend:** `cd frontend && npm run dev`

---

## Quick Check

Test Ollama is working:

```bash
# Terminal 1
ollama serve

# Terminal 2
ollama list

# Terminal 3
curl http://localhost:11434/api/tags
```

You should get list of installed models back 

Enjoy your MCQ generator! 
