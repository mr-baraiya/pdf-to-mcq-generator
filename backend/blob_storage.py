# Upload/download PDFs to Vercel cloud storage

import os
import logging
from vercel_blob import put, delete
import asyncio

log = logging.getLogger(__name__)


def get_token():
    """Get Vercel Blob token from .env"""
    return os.getenv("VERCEL_BLOB_READ_WRITE_TOKEN")


def validate_blob_credentials():
    """Check if credentials are set"""
    tok = get_token()
    
    if tok:
        log.info("Vercel Blob ready")
        return True
    else:
        log.warning("Vercel Blob not configured")
        return False


async def upload_pdf_to_blob(content, fname):
    """Upload PDF to cloud storage using official Vercel SDK"""
    
    tok = get_token()
    
    if not tok:
        log.error("Vercel Blob token missing")
        return None
    
    try:
        log.info(f"Uploading: {fname}")
        
        # Run synchronous put in executor to make it async
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: put(
                fname,
                content,
                options={"token": tok, "addRandomSuffix": "true"}
            )
        )
        
        log.info(f"Uploaded: {result.get('url')}")
        return result
                    
    except Exception as e:
        log.error(f"Upload error: {str(e)}")
        return None




async def download_pdf_from_blob(url):
    """Download PDF from cloud storage"""
    import aiohttp
    
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
    """Delete PDF from cloud storage using official Vercel SDK"""
    
    tok = get_token()
    
    if not tok:
        log.error("Vercel Blob token missing")
        return False
    
    try:
        log.info(f"Deleting: {url}")
        
        # Run synchronous delete in executor to make it async
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: delete([url], options={"token": tok})
        )
        
        log.info("Deleted")
        return True
                    
    except Exception as e:
        log.error(f"Delete error: {str(e)}")
        return False

