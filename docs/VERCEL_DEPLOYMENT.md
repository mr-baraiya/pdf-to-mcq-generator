# Vercel Deployment Structure Guide

This guide explains the recommended project structure for deploying to Vercel with serverless backend and React frontend.

---

##  Project Structure for Vercel

```
pdf-to-mcq-generator/

 frontend/                       # React frontend (Vite)
    src/
       App.jsx
       components/
       App.css
       ...
    package.json
    vite.config.js
    index.html

 api/                            # Backend serverless functions
    index.py                    # Main FastAPI app (entry point)

 backend/                        # Backend modules (shared code)
    src/
       pdf/
          __init__.py
          extractor.py
       llm/
          __init__.py
          mcq_generator.py
       utils/
           __init__.py
           blob_storage.py
    __init__.py

 vercel.json                     # Vercel configuration
 requirements.txt                # Python dependencies
 .env.example                    # Environment template
 .gitignore
 README.md
```

**Key Points:**
-  `api/index.py` - Main entry point for serverless backend
-  `backend/` - Shared backend modules
-  `frontend/` - React frontend
-  `vercel.json` - Deployment configuration
-  `requirements.txt` - Python dependencies at root

---

##  How Vercel Deployment Works

### Architecture

```
User Browser (https://yourdomain.com)
       
        Static Files  frontend/dist/ (React Build)
       
        API Calls  /api/*  api/index.py (FastAPI Serverless)
                                              
                                               /upload-pdf
                                               /generate-mcqs
                                               /docs (API docs)
```

### Build Process

1. **Frontend Build**:
   - `cd frontend && npm install && npm run build`
   - Creates optimized build in `frontend/dist/`
   - Served as static files

2. **Backend Build**:
   - `pip install -r requirements.txt`
   - Packages Python dependencies
   - Deploys `api/index.py` as serverless function

3. **Routing**:
   - `/api/*` requests  `api/index.py` (FastAPI)
   - All other requests  `frontend/dist/` (React)

---

##  Configuration Files

### vercel.json

```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "pip install -r requirements.txt",
  "env": {
    "PYTHONUNBUFFERED": "1"
  },
  "functions": {
    "api/index.py": {
      "runtime": "python3.11"
    }
  },
  "routes": [
    {
      "src": "/api(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/$1"
    }
  ]
}
```

**Explanation:**
- `buildCommand`: Build frontend first
- `outputDirectory`: Frontend build output
- `installCommand`: Install Python dependencies
- `functions`: Python runtime
- `routes`: Route mappings

### requirements.txt (Root Level)

```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
PyPDF2==3.0.1
ollama==0.1.5
pydantic==2.5.0
python-dotenv==1.0.0
cors==1.0.1
vercel-blob==0.0.5
requests==2.31.0
aiohttp==3.9.1
```

---

##  Setup Steps

### Step 1: Prepare Local Structure

Ensure your project has this structure:
```bash
ls -la
# Should show:
# api/
# backend/
# frontend/
# vercel.json
# requirements.txt
```

### Step 2: Commit to Git

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts
```

#### Option B: GitHub Integration

1. Push code to GitHub
2. Go to vercel.com
3. Click "New Project"
4. Select your GitHub repository
5. Vercel auto-detects the configuration
6. Click "Deploy"

### Step 4: Add Environment Variables

On Vercel Dashboard:

1. Go to **Project Settings**  **Environment Variables**
2. Add your secrets:
   ```
   VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_your_token
   VERCEL_BLOB_STORE_ID=your_store_id
   OLLAMA_HOST=http://localhost:11434  (or your Ollama server)
   ```

3. Click "Save and Redeploy"

---

##  API Integration in Frontend

### Update API URL

In `frontend/src/App.jsx`, update the API calls:

#### Before (Local Development):
```javascript
const API_URL = "http://localhost:8000";
```

#### After (Vercel Deployment):
```javascript
const API_URL = process.env.NODE_ENV === "production" 
  ? window.location.origin 
  : "http://localhost:8000";
```

Or use a Vite environment variable:

Create `frontend/.env`:
```env
VITE_API_URL=/api
```

Update `frontend/src/App.jsx`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

### Update Axios Calls

```javascript
// Old
axios.post('http://localhost:8000/upload-pdf', formData)

// New
axios.post(`${API_URL}/upload-pdf`, formData)
```

---

##  Environment Variables on Vercel

### Set on Vercel Dashboard

**Project Settings**  **Environment Variables**

```
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxx
VERCEL_BLOB_STORE_ID=your_store_id
OLLAMA_HOST=https://your-ollama-server.com (if remote)
OLLAMA_MODEL=mistral
```

### Test Variables

```bash
# Locally, create .env
cat >> .env << EOF
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxx
VERCEL_BLOB_STORE_ID=your_store_id
EOF

# Run locally
python api/index.py
```

---

##  Deployment Checklist

- [ ] Project structure matches above
- [ ] `api/index.py` exists and imports from `backend/`
- [ ] `vercel.json` is configured
- [ ] `requirements.txt` is at root level
- [ ] Frontend API URL is updated for production
- [ ] Code is committed to git
- [ ] Environment variables added to Vercel
- [ ] Vercel deployment successful

---

##  Test Deployment

After deploying to Vercel:

### 1. Test Frontend
```
https://your-project.vercel.app
```
Should load the React app

### 2. Test API
```
https://your-project.vercel.app/api/
```
Should return:
```json
{"message": "PDF to MCQ Generator API", "version": "1.0.0"}
```

### 3. Test API Docs
```
https://your-project.vercel.app/api/docs
```
Should show Swagger UI

### 4. Test Upload Endpoint
```bash
curl -X POST https://your-project.vercel.app/api/upload-pdf \
  -F "file=@sample.pdf"
```

---

##  Update Deployment

### Auto-deployment on Git Push

Once GitHub integrated:
- Push to `main` branch
- Vercel auto-deploys
- Takes ~3-5 minutes

### Manual Redeploy

```bash
vercel --prod
```

---

##  Monitoring

### Check Logs

```bash
vercel logs
```

### Check Deployment Status

Vercel Dashboard:
- **Deployments** tab shows all deployments
- **Activity** shows recent builds
- **Errors** shows any issues

---

##  Troubleshooting

### Frontend not showing
- Check `frontend/dist/` exists
- Check `vercel.json` routes
- Check build logs

### API returning 404
- Check `api/index.py` exists
- Check `vercel.json` routes
- Verify imports in `api/index.py`

### Blob storage not working
- Check environment variables on Vercel
- Check token validity
- Check logs for errors

### CORS errors
- CORSMiddleware already enables all origins
- Check frontend is calling correct API URL

### Python module not found
- Check `requirements.txt` has all dependencies
- Check imports in `api/index.py`

---

##  Local Development

Run both locally before deploying:

### Terminal 1: Backend
```bash
python api/index.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`

---

##  Next Steps

1. **Restructure** project to match directory layout
2. **Review** `api/index.py` for your endpoints
3. **Update** frontend API URLs
4. **Test** locally
5. **Add** environment variables to Vercel
6. **Deploy** using Vercel CLI or GitHub integration
7. **Test** live deployment

---

##  Documentation

- [Vercel FastAPI Docs](https://vercel.com/docs/functions/quickstart/python)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Vercel Blob Documentation](https://vercel.com/docs/storage/vercel-blob)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

##  Benefits of This Structure

| Benefit | Details |
|---------|---------|
| **Serverless** | No server to manage |
| **Auto-scaling** | Handles traffic spikes |
| **Cost-effective** | Pay only for usage |
| **Fast deployment** | Minutes, not hours |
| **Global CDN** | Fast worldwide delivery |
| **Easy rollback** | One-click version revert |
| **Built-in monitoring** | Logs and analytics included |

---

**Your project is ready for production deployment! **
