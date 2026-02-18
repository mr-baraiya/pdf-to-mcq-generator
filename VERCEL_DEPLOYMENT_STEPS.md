# Vercel Deployment Steps

## 🔥 Recent Fixes Applied

### Fixed: "This Serverless Function has crashed" Error
**Problem**: FUNCTION_INVOCATION_FAILED on Vercel deployment

**Root Cause**:
1. Startup event handlers don't work well with serverless cold starts
2. Missing `api/__init__.py` package file
3. Incorrect Mangum lifespan configuration
4. Vercel routing configuration issues

**Solutions Applied**:
1. ✅ Made startup handlers conditional (skip on Vercel)
2. ✅ Created `api/__init__.py` package file
3. ✅ Changed Mangum to `lifespan="auto"`
4. ✅ Updated `vercel.json` routing from `/api/index.py` to `/api/index`
5. ✅ Added comprehensive error logging to track issues
6. ✅ Python 3.9 runtime specification

---

## Changes Made for Vercel Deployment

### 1. File Size Limit Increased to 5MB
- Updated `MAX_FILE_SIZE` to 5MB in backend and frontend
- Updated error messages to reflect 5MB limit

### 2. Fixed 404 Error
Added Mangum adapter for Vercel serverless deployment:
- Added `mangum>=0.17.0` to `requirements.txt`
- Updated `api/index.py` to export `handler` for Vercel
- Updated `runtime.txt` to use `python-3.9` (Vercel supported version)
- Updated `vercel.json` with proper configuration

## Deploy to Vercel

### Option 1: Using Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Option 2: Using Vercel Dashboard

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your Git repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Add environment variables:
   - `GROQ_API_KEY`
   - `VERCEL_BLOB_READ_WRITE_TOKEN`
   - `VERCEL_BLOB_STORE_ID`
   - `FRONTEND_URL` (will be your Vercel domain)
6. Click "Deploy"

### Option 3: Git Push (Recommended)

1. Connect your repository to Vercel
2. Push to your main/master branch
3. Vercel will automatically deploy

## Environment Variables

Make sure to set these in Vercel Dashboard → Project Settings → Environment Variables:

```env
GROQ_API_KEY=your_groq_api_key
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
VERCEL_BLOB_STORE_ID=your_vercel_blob_store_id
FRONTEND_URL=https://your-domain.vercel.app
```

## Verify Deployment

After deployment, test these endpoints:

1. **Health Check**: `https://your-domain.vercel.app/api/`
   - Should return: `{"message": "PDF to MCQ Generator API", "version": "1.0.0"}`

2. **Upload PDF**: POST to `https://your-domain.vercel.app/api/upload-pdf`
   - Test with a small PDF (< 5MB)

3. **Frontend**: `https://your-domain.vercel.app`
   - Should load the React app

## Troubleshooting

### Still getting 404?
1. Check Vercel deployment logs
2. Verify `api/index.py` has the `handler` export
3. Ensure `mangum` is installed
4. Check that Python version is 3.9 (not 3.13)

### Getting 413 (Payload Too Large)?
- Vercel has a 4.5MB limit on Hobby plan
- Upgrade to Pro for 100MB limit
- Or implement client-side compression

### Module Import Errors?
- Ensure all dependencies are in `requirements.txt`
- Check deployment logs for missing packages

## Local Testing

To test locally with the Vercel environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
vercel dev
```

This will start both the API and frontend locally, mimicking Vercel's environment.
