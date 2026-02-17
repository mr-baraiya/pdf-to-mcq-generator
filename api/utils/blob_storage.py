# Upload/download PDFs to Vercel cloud storage

import os
import logging
import aiohttp

log = logging.getLogger(__name__)


def get_creds():
    """Get Vercel Blob token and store ID from .env"""
    tok = os.getenv("VERCEL_BLOB_READ_WRITE_TOKEN")
    sid = os.getenv("VERCEL_BLOB_STORE_ID")
    return tok, sid


def validate_blob_credentials():
    """Check if credentials are set"""
    tok, sid = get_creds()
    
    if tok and sid:
        log.info("✓ Vercel Blob ready")
        return True
    else:
        log.warning("⚠ Vercel Blob not configured")
        return False


async def upload_pdf_to_blob(content, fname):
    """Upload PDF to cloud storage"""
    
    tok, sid = get_creds()
    
    if not validate_blob_credentials():
        log.error("Credentials missing")
        return None
    
    try:
        url = "https://blob.vercel-storage.com"
        hdrs = {
            "authorization": f"Bearer {tok}",
            "x-blob-store-id": sid,
            "x-blob-filename": fname
        }
        
        log.info(f"Uploading: {fname}")
        
        async with aiohttp.ClientSession() as s:
            async with s.put(url, data=content, headers=hdrs) as r:
                if r.status == 200:
                    d = await r.json()
                    log.info(f"Uploaded: {d.get('url')}")
                    return d
                else:
                    log.error(f"Upload failed: {r.status}")
                    return None
                    
    except Exception as e:
        log.error(f"Upload error: {str(e)}")
        return None


async def download_pdf_from_blob(url):
    """Download PDF from cloud storage"""
    
    try:
        log.info(f"Downloading: {url}")
        
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                if r.status == 200:
                    c = await r.read()
                    log.info(f"Downloaded: {len(c)} bytes")
                    return c
                else:
                    log.error(f"Download failed: {r.status}")
                    return None
                    
    except Exception as e:
        log.error(f"Download error: {str(e)}")
        return None


async def delete_pdf_from_blob(url):
    """Delete PDF from cloud storage"""
    
    tok, sid = get_creds()
    
    if not validate_blob_credentials():
        log.error("Credentials missing")
        return False
    
    try:
        log.info(f"Deleting: {url}")
        
        hdrs = {
            "authorization": f"Bearer {tok}",
            "x-blob-store-id": sid
        }
        
        async with aiohttp.ClientSession() as s:
            async with s.delete(url, headers=hdrs) as r:
                if r.status in [200, 204]:
                    log.info("Deleted")
                    return True
                else:
                    log.error(f"Delete failed: {r.status}")
                    return False
                    
    except Exception as e:
        log.error(f"Delete error: {str(e)}")
        return False
