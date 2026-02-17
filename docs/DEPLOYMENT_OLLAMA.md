# Ollama Deployment Guide

## Problem: Ollama on Vercel (Serverless)

Ollama is a **local AI model runner** that needs:
-  Persistent file system (Vercel is stateless)
-  Continuous process running (Serverless functions are short-lived)
-  4GB+ disk space (Vercel limits)

**Vercel Functions CAN'T run Ollama directly!**

---

## Solutions for Production Deployment

### Option 1: **Use Ollama on Your Own Server** (BEST)
**Cost:** Low (your own machine)  
**Setup:** Medium  
**Latency:** Low (if local)

Deploy like this:
```
Your Machine (Ollama Server)
         
   ollama serve
         
  http://your-ip:11434
         
Vercel Backend (connects to it)
```

**Steps:**
1. Keep Ollama running on your local machine
2. In `.env`, set Ollama host to your public IP:
   ```
   OLLAMA_HOST=http://YOUR_PUBLIC_IP:11434
   ```
3. Deploy backend to Vercel
4. Vercel connects to your Ollama server

**Pros:**
-  Free (uses your computer)
-  Simple setup
-  Full control

**Cons:**
-  Your computer must stay on 24/7
-  Needs public IP or Ngrok tunnel

---

### Option 2: **Use Cloud AI API** (RECOMMENDED)
**Cost:** $5-20/month  
**Setup:** Simple  
**Latency:** Good

Instead of local Ollama, use:
- **OpenAI** - ChatGPT API
- **Groq** - Free fast LLM API
- **Hugging Face** - ML models API
- **Together AI** - Multiple models

**Change code:**
```python
# OLD: Uses local Ollama
generate_mcqs(text, num)

# NEW: Uses OpenAI
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(...)
```

**Pros:**
-  Works on Vercel (no local server)
-  Scalable
-  Better quality models

**Cons:**
-  Pay per API call
-  Need internet

---

### Option 3: **Docker Container on VPS** (ADVANCED)
**Cost:** $5-15/month (DigitalOcean, Linode)  
**Setup:** Hard  
**Latency:** Medium

Deploy Ollama in Docker container on your own server.

**Pros:**
-  Full control
-  Cheap
-  Works 24/7

**Cons:**
-  Need server management knowledge
-  More expensive than local

---

## QUICK START: Option 1 (for now)

### Step 1: Install Ollama on Your Computer

Download from: https://ollama.com

### Step 2: Start Ollama Server

```bash
ollama serve
```

Keep this terminal open!

### Step 3: Pull Mistral Model

Open NEW terminal:
```bash
ollama pull mistral
```

### Step 4: Find Your Public IP

```bash
# On Mac/Linux:
curl ifconfig.me

# On Windows:
ipconfig
# Look for "IPv4 Address"
```

Example: `192.168.1.100` (local) or `203.0.113.45` (public)

### Step 5: Update .env

If you're on same network (local development):
```
OLLAMA_HOST=http://localhost:11434
```

If deploying (Vercel needs to reach it):
```
OLLAMA_HOST=http://YOUR_PUBLIC_IP:11434
```

Example:
```
OLLAMA_HOST=http://203.0.113.45:11434
```

### Step 6: FOR VERCEL - Use Ngrok Tunnel

If your computer has dynamic IP:

```bash
# Install ngrok from: https://ngrok.com

# Create tunnel to Ollama:
ngrok http 11434

# You'll get:
Forwarding URL: https://abc123.ngrok.io
```

Update .env:
```
OLLAMA_HOST=https://abc123.ngrok.io
```

---

## Best for YOUR Project

**Recommendation: Option 2 (Cloud API)**

Why?
1. Vercel deployment is easier
2. No need to keep computer running
3. Better for production

### Simple Migration to OpenAI:

1. Get API key: https://platform.openai.com
2. Add to .env:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Change `api/llm/mcq_generator.py` to use OpenAI instead

---

## For Now (Testing)

### Local Setup:

1. Install Ollama: https://ollama.com
2. Run: `ollama serve`
3. Run: `ollama pull mistral`
4. Start your API: `python api/index.py`
5. Verify: `curl http://localhost:11434/api/tags`

### When Ready to Deploy:

Choose Option 1 (Ngrok) or Option 2 (Cloud API)

---

## Testing Options

### Test Local (free):
- Install Ollama
- Run locally
- Test with frontend

### Test with Cloud (cheapest):
- Use Groq API (free tier)
- No installation needed
- Works on Vercel

```python
# Example: Use Groq instead of Ollama
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[{"role": "user", "content": prompt}]
)
```

---

## Summary

| Method | Cost | Setup | Vercel Ready |
|--------|------|-------|--------------|
| Local Ollama | Free | Easy | No |
| Ollama + Ngrok | Free | Medium | Yes |
| OpenAI API | $5/mo | Easy | Yes  |
| Groq API | Free | Easy | Yes  |
| Self-hosted Docker | $5/mo | Hard | Yes |

**PICK ONE:**
- **Development:** Local Ollama (easiest)
- **Deployment:** Groq API (free) or OpenAI (reliable)

