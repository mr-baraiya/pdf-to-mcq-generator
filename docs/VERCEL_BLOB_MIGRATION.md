# Vercel Blob Integration Summary

##  What's Been Updated

### New Files Created
-  `backend/src/utils/blob_storage.py` - Vercel Blob utility functions
-  `docs/VERCEL_BLOB_SETUP.md` - Complete setup and usage guide

### Files Modified
-  `backend/requirements.txt` - Added Vercel Blob, aiohttp dependencies
-  `backend/.env.example` - Added Vercel Blob token configuration
-  `backend/app.py` - Updated to use Vercel Blob for PDF storage
-  `backend/src/pdf/extractor.py` - Support for BytesIO objects (cloud files)
-  `backend/src/utils/__init__.py` - Created utils module
-  `README.md` - Updated feature list and documentation links
-  `QUICKSTART.md` - Added optional Vercel Blob section
-  `docs/BACKEND_GUIDE.md` - Added blob storage module documentation

---

##  Key Changes

### File Storage Flow

**Before (Local Disk):**
1. Receive PDF upload
2. Save to temporary file
3. Extract text from file
4. Delete temporary file
5. Return extracted text

**After (Vercel Blob):**
1. Receive PDF upload
2. Upload to Vercel Blob
3. Extract text (from memory/bytes)
4. Return extracted text + blob URL
5. Optional: Delete blob after processing

### API Endpoint Changes

#### `/upload-pdf` Response

**Before:**
```json
{
  "filename": "document.pdf",
  "text": "Extracted text...",
  "status": "success"
}
```

**After:**
```json
{
  "filename": "document.pdf",
  "text": "Extracted text...",
  "blob_url": "https://store_id.blob.vercelusercontent.com/pathname.pdf",
  "blob_pathname": "pathname.pdf",
  "status": "success"
}
```

---

##  New Capabilities

### Cloud Storage Functions

```python
# Upload PDF to Vercel Blob
await upload_pdf_to_blob(file_content, filename)

# Download PDF from Vercel Blob
await download_pdf_from_blob(blob_url)

# Delete PDF from Vercel Blob
await delete_pdf_from_blob(blob_url)

# Get blob metadata
await get_blob_info(blob_url)
```

### PDF Extraction Updates

```python
# Works with file paths (local)
text = extract_text_from_pdf("/path/to/file.pdf")

# Also works with BytesIO (cloud files)
pdf_bytes = io.BytesIO(file_content)
text = extract_text_from_pdf(pdf_bytes)
```

---

##  New Dependencies

```
vercel-blob==0.0.5
aiohttp==3.9.1
requests==2.31.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

##  Configuration

### Environment Variables (.env)

```env
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxx
VERCEL_BLOB_STORE_ID=your_store_id_here
```

Get these from:
1. Vercel Dashboard  Storage  Blob
2. Copy "Read/Write Token" and "Store ID"
3. Add to `.env` file

---

##  Benefits

| Feature | Before | After |
|---------|--------|-------|
| **Storage** | Local disk | Cloud (Vercel Blob) |
| **Disk Usage** | High (stores all PDFs) | Low (no local storage) |
| **Scalability** | Limited | Unlimited |
| **File Retrieval** | File path | URL + pathname |
| **Backup** | Manual | Automatic |
| **Cost** | Free | Pay per GB ($0.50/GB) |
| **Cleanup** | Manual deletion | Programmatic deletion |

---

##  Security

-  HTTPS encrypted uploads/downloads
-  Token-based authentication
-  Unique blob URLs (hard to guess)
-  Token never exposed to frontend
-  All operations logged and tracked

---

##  Architecture Comparison

### Local Storage
```
PDF Upload  FastAPI  Local Disk  Extract Text
```

### Vercel Blob (New)
```
PDF Upload  FastAPI  Vercel Blob  Extract Text
                
         (Store URL for later)
```

---

##  Migration Guide

If you have existing code:

### Update Imports
```python
# Add
from src.utils.blob_storage import upload_pdf_to_blob, download_pdf_from_blob

# Or use directly in endpoints
```

### Update File Handling
```python
# Old: Save to disk
temp_path = f"temp_{file.filename}"
with open(temp_path, "wb") as f:
    f.write(await file.read())
text = extract_text_from_pdf(temp_path)
os.remove(temp_path)

# New: Use Vercel Blob
file_content = await file.read()
blob_info = await upload_pdf_to_blob(file_content, file.filename)
pdf_file = io.BytesIO(file_content)
text = extract_text_from_pdf(pdf_file)
```

---

##  Recommended Next Steps

### Basic Setup (Keep it simple)
1. Configure Vercel Blob token
2. Run backend normally
3. Frontend works unchanged
4. PDFs stored in cloud

### Intermediate (Add features)
1. Store blob URL in database
2. Add ability to reprocess PDFs
3. Implement cleanup mechanism
4. Track storage usage

### Advanced (Full integration)
1. Add user authentication
2. Implement file sharing
3. Build file management UI
4. Add analytics dashboard

---

##  Example Usage

### Upload and Store
```python
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    # Upload to blob
    blob_info = await upload_pdf_to_blob(
        await file.read(),
        file.filename
    )
    # Extract text in memory
    text = extract_text_from_pdf(io.BytesIO(file_content))
    # Return both
    return {
        "text": text,
        "blob_url": blob_info["url"]
    }
```

### Retrieve Later
```python
@app.get("/retrieve-pdf/{pathname}")
async def retrieve_pdf(pathname: str):
    # Reconstruct URL
    blob_url = f"https://{STORE_ID}.blob.vercelusercontent.com/{pathname}"
    # Download and process
    content = await download_pdf_from_blob(blob_url)
    text = extract_text_from_pdf(io.BytesIO(content))
    return {"text": text}
```

### Cleanup Storage
```python
@app.delete("/delete-pdf")
async def delete_pdf(blob_url: str):
    success = await delete_pdf_from_blob(blob_url)
    return {"deleted": success}
```

---

##  Documentation

For detailed setup and usage:
- **[VERCEL_BLOB_SETUP.md](VERCEL_BLOB_SETUP.md)** - Complete guide
- **[README.md](../README.md)** - Project overview
- **[BACKEND_GUIDE.md](BACKEND_GUIDE.md)** - Backend development
- **[API.md](API.md)** - API reference

---

##  Troubleshooting

### Token not working
```bash
# Check .env file
cat backend/.env | grep VERCEL_BLOB

# Verify token is valid in Vercel dashboard
# Regenerate if needed
```

### Upload failing
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check error messages in backend terminal
```

### Performance issues
```python
# Large files may be slow - this is normal
# 100MB PDF might take 5-10 seconds to upload

# Optimize by:
# - Using smaller PDFs for testing
# - Compressing PDFs before upload
# - Using faster internet connection
```

---

##  Verification

Test Vercel Blob integration:

1. **Start backend with Vercel Blob configured**
   ```bash
   cd backend
   python app.py
   ```

2. **Upload a PDF via API**
   ```bash
   curl -X POST http://localhost:8000/upload-pdf \
     -F "file=@sample.pdf"
   ```

3. **Check response includes blob_url**
   ```json
   {
     "blob_url": "https://xxx.blob.vercelusercontent.com/...",
     "status": "success"
   }
   ```

4. **Verify in Vercel dashboard**
   - Go to Vercel project
   - Check Storage  Blob
   - Should see uploaded file

---

**You're all set!  Your PDFs are now stored securely in Vercel Blob.**
