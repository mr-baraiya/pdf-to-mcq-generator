# Deployment Guide

This guide covers multiple deployment options for the PDF to MCQ Generator application.

## Table of Contents
- [Docker Compose (Local Development)](#docker-compose-local-development)
- [Docker (Standalone Container)](#docker-standalone-container)
- [Platform Deployment (Heroku/Render/Railway)](#platform-deployment)
- [Vercel Deployment](#vercel-deployment)
- [Environment Variables](#environment-variables)

---

## Docker Compose (Local Development)

The easiest way to run the full stack locally with Docker.

### Prerequisites
- Docker and Docker Compose installed
- `.env` files configured in both `backend/` and `frontend/` directories

### Steps

1. **Build and start all services:**
```bash
docker-compose up --build
```

2. **Access the application:**
   - Backend API: http://localhost:8000
   - Frontend UI: http://localhost:5173
   - API Documentation: http://localhost:8000/docs

3. **Stop the services:**
```bash
docker-compose down
```

4. **View logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Features
- ✅ Auto-reload on code changes (volume mounted)
- ✅ Separate containers for backend and frontend
- ✅ Health checks for backend
- ✅ Network isolation

---

## Docker (Standalone Container)

Deploy just the backend API as a standalone Docker container.

### Build the image:
```bash
docker build -t pdf-mcq-backend .
```

### Run the container:
```bash
docker run -d \
  -p 8000:8000 \
  -e GROQ_API_KEY=your_groq_key \
  -e GEMINI_API_KEY=your_gemini_key \
  -e BLOB_READ_WRITE_TOKEN=your_blob_token \
  --name pdf-mcq-api \
  pdf-mcq-backend
```

### Using env file:
```bash
docker run -d \
  -p 8000:8000 \
  --env-file backend/.env \
  --name pdf-mcq-api \
  pdf-mcq-backend
```

### Container management:
```bash
# View logs
docker logs -f pdf-mcq-api

# Stop container
docker stop pdf-mcq-api

# Remove container
docker rm pdf-mcq-api

# Access container shell
docker exec -it pdf-mcq-api /bin/bash
```

### Push to Docker Hub:
```bash
# Tag the image
docker tag pdf-mcq-backend yourusername/pdf-mcq-backend:latest

# Push to Docker Hub
docker push yourusername/pdf-mcq-backend:latest
```

---

## Platform Deployment

Deploy to cloud platforms like Heroku, Render, or Railway using the `Procfile`.

### Prerequisites
- Git repository with code pushed to GitHub
- Account on chosen platform (Heroku/Render/Railway)
- Environment variables configured

### Option 1: Heroku

1. **Install Heroku CLI:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and create app:**
```bash
heroku login
heroku create pdf-mcq-generator
```

3. **Set environment variables:**
```bash
heroku config:set GROQ_API_KEY=your_groq_key
heroku config:set GEMINI_API_KEY=your_gemini_key
heroku config:set BLOB_READ_WRITE_TOKEN=your_blob_token
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Open the app:**
```bash
heroku open
```

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** pdf-mcq-generator
   - **Environment:** Python 3
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn index:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the dashboard
6. Click "Create Web Service"

### Option 3: Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the `Procfile`
5. Add environment variables in Settings → Variables
6. Deploy automatically starts

---

## Vercel Deployment

Deploy the backend API to Vercel serverless functions.

### Prerequisites
- Vercel account and CLI installed
- `vercel.json` configuration file (already provided)

### Steps

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Deploy from backend directory:**
```bash
cd backend
vercel --prod
```

4. **Set environment variables:**
```bash
vercel env add GROQ_API_KEY
vercel env add GEMINI_API_KEY
vercel env add BLOB_READ_WRITE_TOKEN
```

5. **Redeploy with environment variables:**
```bash
vercel --prod
```

### Frontend Deployment (Vercel)

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Deploy:**
```bash
vercel --prod
```

3. **Update API URL:**
   - Set `VITE_API_URL` in Vercel dashboard to your backend URL

---

## Environment Variables

### Backend Variables

Create `backend/.env` file:

```env
# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Vercel Blob Storage
BLOB_READ_WRITE_TOKEN=your_vercel_blob_token_here

# Optional: Ollama Configuration
OLLAMA_HOST=http://localhost:11434
```

### Frontend Variables

Create `frontend/.env` file:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000

# Optional: Analytics, etc.
```

### Platform-Specific Setup

**Heroku:**
```bash
heroku config:set GROQ_API_KEY=xxx
heroku config:set GEMINI_API_KEY=xxx
heroku config:set BLOB_READ_WRITE_TOKEN=xxx
```

**Render/Railway:**
- Set in dashboard under Environment Variables section

**Docker:**
- Use `--env-file` flag or `-e` for individual variables

**Vercel:**
```bash
vercel env add GROQ_API_KEY
vercel env add GEMINI_API_KEY
vercel env add BLOB_READ_WRITE_TOKEN
```

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys obtained (Groq, Gemini, Vercel Blob)
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] Database/storage configured (Vercel Blob)
- [ ] CORS settings updated for production domain
- [ ] Health check endpoint working (`/`)
- [ ] SSL/HTTPS enabled (automatic on most platforms)
- [ ] Monitoring and logging configured

---

## Troubleshooting

### Port Issues
- **Problem:** Backend not accessible
- **Solution:** Ensure backend binds to `0.0.0.0` and uses `$PORT` environment variable

### CORS Errors
- **Problem:** Frontend can't access backend
- **Solution:** Update CORS origins in `backend/config.py`

### API Key Errors
- **Problem:** AI generation failing
- **Solution:** Verify environment variables are set correctly

### Ollama Not Working
- **Problem:** Ollama endpoints return 503
- **Solution:** Ollama should only be used for local development, not in cloud deployments

### Build Failures
- **Problem:** Deployment fails during build
- **Solution:** Check requirements.txt versions and Python compatibility (3.12+)

---

## Monitoring

### Health Checks

**Backend Health:**
```bash
curl https://your-domain.com/
```

**AI Services Status:**
```bash
curl https://your-domain.com/ai-status
```

### Logs

**Docker:**
```bash
docker logs -f pdf-mcq-api
```

**Heroku:**
```bash
heroku logs --tail
```

**Render/Railway:**
- View in dashboard under "Logs" section

---

## Scaling

### Docker Compose
```bash
docker-compose up --scale backend=3
```

### Heroku
```bash
heroku ps:scale web=2
```

### Render/Railway
- Upgrade to higher tier plans for auto-scaling

---

## Security Best Practices

1. **Never commit `.env` files** → Use `.env.example` templates
2. **Rotate API keys regularly** → Especially if exposed
3. **Use HTTPS only** → Enforce in production
4. **Implement rate limiting** → Prevent API abuse
5. **Validate file uploads** → Check size and type
6. **Keep dependencies updated** → Run `pip list --outdated`

---

## Cost Optimization

### Free Tier Options
- **Heroku:** Free tier available with limitations
- **Render:** 750 free hours/month
- **Railway:** $5 free credit monthly
- **Vercel:** Unlimited free deployments for personal projects
- **Docker:** Free on your own server

### Tips
- Use Vercel Blob free tier (100K writes, 1GB storage)
- Choose Groq (free tier available) over paid APIs
- Implement caching for repeated PDF processing
- Set request limits to avoid quota exhaustion

---

## Next Steps

1. Choose your deployment method
2. Configure environment variables
3. Test in staging environment
4. Deploy to production
5. Monitor and optimize

For detailed API documentation, see [API_ENDPOINTS.md](backend/API_ENDPOINTS.md).
For backend architecture, see [BACKEND_GUIDE.md](docs/BACKEND_GUIDE.md).
For frontend features, see [FEATURES.md](frontend/FEATURES.md).
