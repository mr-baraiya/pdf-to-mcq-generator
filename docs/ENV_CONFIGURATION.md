# Environment Variables & Credentials Configuration

This guide explains how to properly configure credentials and environment variables for the PDF to MCQ Generator.

---

## 📋 Overview

The application uses a `.env` file to store sensitive credentials and configuration. This keeps secrets out of your code and makes the app secure.

---

## 🚀 Quick Setup

### Step 1: Create `.env` File

```bash
cd backend
cp .env.example .env
```

### Step 2: Add Your Credentials

Edit `backend/.env` and add your values:

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# Vercel Blob Configuration (REQUIRED for PDF upload)
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxxxxxxxxxxxxx
VERCEL_BLOB_STORE_ID=your_store_id_here
```

### Step 3: Start Backend

```bash
python app.py
```

On startup, the app will validate your credentials and show:
- ✓ Success message if configured correctly
- ⚠ Warning if credentials are missing

---

## 📝 Detailed Configuration

### Ollama Configuration

```env
OLLAMA_HOST=http://localhost:11434
```
- **Default**: `http://localhost:11434`
- **Purpose**: URL where Ollama service is running
- **Change if**: Running Ollama on different host/port

```env
OLLAMA_MODEL=mistral
```
- **Default**: `mistral`
- **Options**: `mistral`, `llama2`, `neural-chat`, `dolphin-mixtral`
- **Purpose**: Which model to use for MCQ generation

### FastAPI Configuration

```env
API_HOST=0.0.0.0
```
- **Default**: `0.0.0.0` (listen on all interfaces)
- **Production**: Use specific IP address for security

```env
API_PORT=8000
```
- **Default**: `8000`
- **Change if**: Port 8000 is already in use

### Frontend Configuration

```env
FRONTEND_URL=http://localhost:3000
```
- **Default**: `http://localhost:3000` (localhost development)
- **Production**: Set to your frontend domain
- **Purpose**: Used for CORS configuration

### Vercel Blob Configuration (REQUIRED)

```env
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxxxxxxxxxxxxx
```

**How to get this:**
1. Visit [vercel.com/storage/blob](https://vercel.com/storage/blob)
2. Create a new Blob store
3. Go to Settings → Tokens
4. Copy the "Read/Write Token"
5. Paste into `.env` file

**Format**: Should start with `vercelblob_`

```env
VERCEL_BLOB_STORE_ID=your_store_id_here
```

**How to get this:**
1. In Vercel Blob Settings
2. Copy the "Store ID" (visible in URL)
3. Paste into `.env` file

**Format**: Usually lowercase alphanumeric

---

## ✅ Validation & Verification

### On Startup

The backend automatically validates credentials:

```bash
$ python app.py

INFO:     Starting PDF to MCQ Generator API...
INFO:     ✓ Vercel Blob credentials configured
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### If Credentials Missing

```bash
$ python app.py

WARNING: ⚠ Vercel Blob credentials not configured. 
         PDF uploads will fail. Configure .env with:
  VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_...
  VERCEL_BLOB_STORE_ID=your_store_id
```

### Manual Validation

Check what's loaded:

```python
# In Python shell
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("VERCEL_BLOB_READ_WRITE_TOKEN"))  # Should print token
print(os.getenv("VERCEL_BLOB_STORE_ID"))  # Should print store ID
```

---

## 🔒 Security Best Practices

### Do's ✅
- ✅ Keep `.env` file in `.gitignore` (already configured)
- ✅ Use strong, unique tokens
- ✅ Rotate tokens periodically in Vercel dashboard
- ✅ Never share `.env` file with others
- ✅ Use `.env.example` as template only

### Don'ts ❌
- ❌ Commit `.env` to git repository
- ❌ Share credentials via email or chat
- ❌ Use same token everywhere
- ❌ Hardcode credentials in code
- ❌ Push `.env` to GitHub

### .gitignore Configuration

The `.env` file is already ignored:

```bash
# backend/.gitignore
.env
.env.local
.env.*.local
```

Verify it's working:

```bash
git status
# Should NOT show ".env" file
```

---

## 🔧 Troubleshooting

### Error: "VERCEL_BLOB_READ_WRITE_TOKEN not configured"

**Problem**: Token not found in environment

**Solution**:
```bash
# 1. Check .env file exists
ls -la backend/.env

# 2. Check it contains the token
grep VERCEL_BLOB_READ_WRITE_TOKEN backend/.env

# 3. Verify token format (starts with vercelblob_)
# If not, get new token from Vercel dashboard
```

### Error: "Invalid token format"

**Problem**: Token doesn't start with `vercelblob_`

**Solution**:
1. Go to Vercel Blob settings
2. Verify you copied the correct token type
3. Get a new "Read/Write Token" (not a "Read-only Token")
4. Update `.env` file

### Loading Other Environments

To use different `.env` files:

```bash
# Load specific .env file
cp .env.production /app/.env

# Or set environment
ENVIRONMENT=production python app.py
```

---

## 🌍 Environment-Specific Configuration

### Development (.env.development)

```env
# Development - localhost
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_URL=http://localhost:3000
OLLAMA_HOST=http://localhost:11434
```

### Production (.env.production)

```env
# Production - cloud deployment
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=https://yourdomain.com
OLLAMA_HOST=http://ollama-service:11434
```

### Testing (.env.test)

```env
# Testing - mock services
API_HOST=127.0.0.1
API_PORT=8001
FRONTEND_URL=http://localhost:3001
```

### Load Environment-Specific Files

```python
# In app.py
import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "development")
env_file = f".env.{environment}"

load_dotenv(env_file)
```

---

## 📦 Managing Multiple Instances

If running multiple instances:

**Instance 1**: Use default `.env`
```env
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

**Instance 2**: Use `.env.multi`
```env
API_PORT=8001
FRONTEND_URL=http://localhost:3001
```

**Start differently**:
```bash
# Instance 1
ENVIRONMENT=default python app.py

# Instance 2
ENVIRONMENT=multi python app.py
```

---

## 🔄 Updating Credentials

### Rotate Vercel Blob Token

1. Go to Vercel Blob → Settings → Tokens
2. Create new "Read/Write Token"
3. Update `backend/.env`:
   ```bash
   VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_newtoken
   ```
4. Delete old token from Vercel
5. Restart backend

### Keep Backup

Before rotating, backup your current token:
```bash
# Save current config
cp backend/.env backend/.env.backup

# Make changes
# If something breaks, restore
cp backend/.env.backup backend/.env
```

---

## 📊 Configuration Validation Script

Create `backend/validate_config.py`:

```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "VERCEL_BLOB_READ_WRITE_TOKEN",
    "VERCEL_BLOB_STORE_ID",
]

optional_vars = [
    "OLLAMA_HOST",
    "OLLAMA_MODEL",
    "API_PORT",
]

print("🔍 Checking Configuration...")
print()

errors = []
warnings = []

for var in required_vars:
    value = os.getenv(var)
    if not value:
        errors.append(f"✗ {var} is MISSING")
    else:
        print(f"✓ {var} is set")

for var in optional_vars:
    value = os.getenv(var)
    if not value:
        warnings.append(f"⚠ {var} not set (using default)")
    else:
        print(f"✓ {var} is set")

print()
if errors:
    print("❌ ERRORS:")
    for error in errors:
        print(f"  {error}")
    exit(1)

if warnings:
    print("⚠️ WARNINGS:")
    for warning in warnings:
        print(f"  {warning}")

print("✅ Configuration is valid!")
```

Run validation:
```bash
python validate_config.py
```

---

## 🚀 Docker Configuration

For Docker deployments:

```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app
COPY . .

# Load .env at runtime
ENV $(cat .env | xargs)

RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

Or use Docker secrets:

```bash
docker run --secret vercel_blob_token \
  -e VERCEL_BLOB_READ_WRITE_TOKEN=$(cat /run/secrets/vercel_blob_token) \
  my-app
```

---

## 📚 Related Documentation

- [Vercel Blob Setup](../docs/VERCEL_BLOB_SETUP.md)
- [Environment Variables in Python](https://12factor.net/config)
- [FastAPI Environment Settings](https://fastapi.tiangolo.com/advanced/settings/)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

---

## ✨ Summary

**Key Points:**
1. ✅ Create `backend/.env` from `.env.example`
2. ✅ Add your Vercel Blob credentials
3. ✅ Run `python app.py` - credentials auto-loaded
4. ✅ Check startup logs for validation
5. ✅ Never commit `.env` to git
6. ✅ Keep tokens safe and rotate periodically

**Quick Checklist:**
- [ ] `.env` file created
- [ ] Vercel credentials added
- [ ] `.env.example` is up to date
- [ ] `.env` is in `.gitignore`
- [ ] Startup logs show "✓ Vercel Blob credentials configured"
- [ ] API responds at `http://localhost:8000/docs`

---

**You're all set! Your credentials are now securely loaded from `.env`.** 🎉
