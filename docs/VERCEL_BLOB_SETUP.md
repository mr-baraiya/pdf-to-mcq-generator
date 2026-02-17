# Vercel Blob Storage Integration Guide

This guide explains how to set up and use Vercel Blob storage with the PDF to MCQ Generator.

---

##  What is Vercel Blob?

Vercel Blob is a serverless blob storage service that allows you to store files (like PDFs) in the cloud without managing infrastructure. It's ideal for:

- Storing uploaded PDF files
- Managing files at scale
- Reducing local server disk usage
- Easy file retrieval and deletion
- Cost-effective storage solution

---

##  Setup Instructions

### Step 1: Create Vercel Project

If you don't have one already:

1. Visit [vercel.com](https://vercel.com)
2. Sign up or log in
3. Create a new project
4. Deploy your backend to Vercel (or keep it local for now)

### Step 2: Create Vercel Blob Store

1. Go to your Vercel project dashboard
2. Navigate to **Storage**  **Create Database**  **Blob**
3. Name your blob store (e.g., "pdf-store")
4. Select a region closest to you

### Step 3: Get Access Token

1. After creating the blob store, go to **Settings**
2. Copy the **Read/Write Token** (starts with `vercelblob_...`)
3. Also note your **Store ID** (visible in the Blob URL)

### Step 4: Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add:

```env
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxx
VERCEL_BLOB_STORE_ID=your_store_id_here
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the new Vercel Blob package and async libraries.

### Step 6: Start the Backend

```bash
python app.py
```

---

##  API Changes

### Updated Upload Endpoint

The `/upload-pdf` endpoint now returns additional blob information:

**Request:**
```http
POST /upload-pdf
Content-Type: multipart/form-data

file: <PDF binary>
```

**Response (200):**
```json
{
  "filename": "document.pdf",
  "text": "Extracted text...",
  "blob_url": "https://STORE_ID.blob.vercelusercontent.com/PATHNAME",
  "blob_pathname": "PATHNAME",
  "status": "success"
}
```

**Key Changes:**
-  PDFs are stored in Vercel Blob (not locally)
-  `blob_url` - Full URL to access the PDF
-  `blob_pathname` - Unique pathname for reference
-  No temporary files on disk

---

##  Architecture

### Before (Local Storage):
```

   Browser   

        Upload PDF
       

  FastAPI Backend         
  1. Save to disk         
  2. Extract text         
  3. Delete temp file     

```

### After (Vercel Blob):
```

   Browser   

        Upload PDF
       
      
  FastAPI Backend                 Vercel Blob       
  1. Upload to Blob         Serverless Storage
  2. Extract text                                   
  3. Return URL                   pdf-pathname      
      
       
       

  MCQ Generation          
  Using Ollama            

```

---

##  Available Functions

### Upload PDF to Blob
```python
await upload_pdf_to_blob(file_content: bytes, filename: str)
```
- Uploads PDF to Vercel Blob
- Returns blob info (url, pathname)
- Automatically handles authentication

### Download PDF from Blob
```python
await download_pdf_from_blob(blob_url: str)
```
- Downloads PDF from Vercel Blob URL
- Returns binary content
- Useful for processing stored PDFs

### Delete PDF from Blob
```python
await delete_pdf_from_blob(blob_url: str)
```
- Deletes PDF from Vercel Blob
- Use after processing to save storage
- Returns True/False for success

### Get Blob Info
```python
await get_blob_info(blob_url: str)
```
- Gets metadata about a blob
- Returns file information

---

##  Usage Examples

### Example 1: Upload and Extract

```python
# Frontend sends PDF
# Backend receives it and:

from src.utils.blob_storage import upload_pdf_to_blob

file_content = await file.read()
blob_info = await upload_pdf_to_blob(file_content, "my-document.pdf")

# blob_info = {
#   "url": "https://abc123.blob.vercelusercontent.com/my-document-xyz.pdf",
#   "pathname": "my-document-xyz.pdf"
# }
```

### Example 2: Store Blob URL for Later Retrieval

```python
# Save blob_url in database (if you add database)
document = {
    "filename": "my-document.pdf",
    "blob_url": blob_info["url"],
    "extracted_text": text,
    "timestamp": datetime.now()
}
db.add(document)
```

### Example 3: Retrieve and Process Stored PDF

```python
from src.utils.blob_storage import download_pdf_from_blob
from src.pdf.extractor import extract_text_from_pdf
import io

# Later, when user wants to reprocess:
pdf_content = await download_pdf_from_blob(stored_blob_url)
pdf_file = io.BytesIO(pdf_content)
text = extract_text_from_pdf(pdf_file)
```

---

##  Frontend Updates (Optional)

The frontend doesn't need changes to use Vercel Blob, but you can optionally:

### Store Blob URL for Reference

```javascript
// In frontend/src/App.jsx
const handleFileUpload = async (file) => {
  const response = await axios.post('http://localhost:8000/upload-pdf', formData);
  
  // Store blob URL if needed
  const { blob_url } = response.data;
  console.log('PDF stored at:', blob_url);
  
  setExtractedText(response.data.text);
};
```

### Display Storage Info

```javascript
{extractedText && (
  <div>
    <p>Extracted Text: {extractedText.substring(0, 100)}...</p>
    <p>Stored at: {response.data.blob_url}</p>
  </div>
)}
```

---

##  Pricing & Limits

### Vercel Blob Pricing:
- **Free Tier**: First 1GB/month, then $0.50/GB
- **No request charges**: Upload and download are free
- **Automatic cleanup**: Old files can be deleted automatically

### File Limits:
- **Max file size**: 500MB per file (suitable for PDFs)
- **Storage**: Unlimited (pay per usage)
- **Bandwidth**: Unlimited

---

##  Security Best Practices

### Token Management:
1. **Never commit tokens to git** - Use `.env` file
2. **Rotate tokens periodically** - Vercel dashboard
3. **Use read-only tokens** - If you only need downloads
4. **.gitignore** - Already configured to exclude `.env`

### File Access:
```python
# All requests are authenticated with token
# Blob URLs are unique and hard to guess
# Optional: Add access control in your API
```

---

##  Troubleshooting

### Error: "VERCEL_BLOB_READ_WRITE_TOKEN not configured"

**Solution:**
```bash
# Make sure .env file exists and contains:
VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_xxxxxxxxxxxxx
```

### Error: "Failed to upload to Vercel Blob"

**Common causes:**
1. Invalid token - Check token is correct
2. Network issue - Verify internet connection
3. File too large - PDFs should be < 500MB
4. Token expired - Regenerate in Vercel dashboard

**Solution:**
```bash
# Check token
echo $VERCEL_BLOB_READ_WRITE_TOKEN

# Verify network
curl https://blob.vercelusercontent.com/

# Test upload in logs
# Check backend terminal for detailed error
```

### Uploads are slow

**Possible reasons:**
1. Large PDF files
2. Slow internet connection
3. Ollama model loading (not Blob related)

**Solution:**
- Use smaller PDFs for testing
- Upload speed depends on file size and connection

### Error: "Connection refused"

**Solution:**
```bash
# Ensure backend is running
python app.py

# Check Ollama is running
curl http://localhost:11434/api/tags
```

---

##  Monitoring & Management

### View Uploaded Blobs

1. Go to Vercel project  Storage  Blob
2. See all uploaded files
3. Check file size and upload date
4. Delete files manually if needed

### Programmatic Deletion

To save storage, delete old PDFs after processing:

```python
@app.post("/cleanup-pdf")
async def cleanup_pdf(blob_url: str):
    """Delete a PDF after processing"""
    success = await delete_pdf_from_blob(blob_url)
    return {"deleted": success}
```

---

##  Integration with Database (Advanced)

Add a database to store metadata:

```python
# models.py
from sqlalchemy import Column, String, DateTime
from datetime import datetime

class PDFRecord(Base):
    __tablename__ = "pdfs"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    blob_url = Column(String)  # Store Vercel Blob URL
    blob_pathname = Column(String)
    extracted_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile, db: Session):
    blob_info = await upload_pdf_to_blob(...)
    
    # Save metadata to database
    record = PDFRecord(
        filename=file.filename,
        blob_url=blob_info["url"],
        extracted_text=text
    )
    db.add(record)
    db.commit()
```

---

##  Additional Resources

- [Vercel Blob Docs](https://vercel.com/docs/storage/vercel-blob)
- [Vercel Blob API Reference](https://vercel.com/docs/storage/vercel-blob/api-reference)
- [Python aiohttp Docs](https://docs.aiohttp.org/)
- [FastAPI File Upload](https://fastapi.tiangolo.com/tutorial/request-files/)

---

##  Verification

To verify Vercel Blob is working:

1. **Check environment variables**
   ```bash
   cat backend/.env | grep VERCEL_BLOB
   ```

2. **Start backend**
   ```bash
   python app.py
   ```

3. **Test upload via API docs**
   ```
   Visit http://localhost:8000/docs
   Click "POST /upload-pdf"
   Upload a PDF
   Check response includes blob_url
   ```

4. **Verify in Vercel dashboard**
   ```
   Go to Vercel project  Storage  Blob
   Should see your uploaded PDF file
   ```

---

##  You're All Set!

Your backend now uses Vercel Blob for secure, scalable PDF storage. The frontend works exactly the same - no changes needed!

**Next steps:**
1. Start backend: `python app.py`
2. Start frontend: `npm run dev`
3. Upload a PDF and verify it's stored in Vercel Blob
4. Generate MCQs as usual

Happy learning! 
