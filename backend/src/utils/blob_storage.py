import os
import aiohttp
import json
from typing import Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Read credentials from environment variables
VERCEL_BLOB_API_URL = "https://blob.vercelusercontent.com"
READ_WRITE_TOKEN = os.getenv("VERCEL_BLOB_READ_WRITE_TOKEN")
STORE_ID = os.getenv("VERCEL_BLOB_STORE_ID")


def validate_blob_credentials() -> bool:
    """
    Validate that Vercel Blob credentials are configured
    
    Returns:
        True if credentials are valid, False otherwise
    """
    if not READ_WRITE_TOKEN:
        logger.warning("VERCEL_BLOB_READ_WRITE_TOKEN not set in environment variables")
        return False
    
    if not STORE_ID:
        logger.warning("VERCEL_BLOB_STORE_ID not set in environment variables")
        return False
    
    if not READ_WRITE_TOKEN.startswith("vercelblob_"):
        logger.warning("VERCEL_BLOB_READ_WRITE_TOKEN invalid format")
        return False
    
    logger.info("Vercel Blob credentials validated successfully")
    return True


def get_blob_credentials() -> dict:
    """
    Get Vercel Blob credentials from environment
    
    Returns:
        Dictionary with token and store_id
        
    Raises:
        ValueError if credentials are not configured
    """
    if not READ_WRITE_TOKEN:
        raise ValueError(
            "VERCEL_BLOB_READ_WRITE_TOKEN not configured. "
            "Add it to your .env file: VERCEL_BLOB_READ_WRITE_TOKEN=vercelblob_..."
        )
    
    if not STORE_ID:
        logger.warning(
            "VERCEL_BLOB_STORE_ID not configured. "
            "This is optional but recommended. Add it to your .env file."
        )
    
    return {
        "token": READ_WRITE_TOKEN,
        "store_id": STORE_ID
    }


async def upload_pdf_to_blob(file_content: bytes, filename: str) -> Optional[dict]:
    """
    Upload PDF to Vercel Blob storage
    
    Args:
        file_content: Binary content of the PDF file
        filename: Name of the file
        
    Returns:
        Dictionary with blob info (url, pathname, contentType, contentDisposition)
        
    Raises:
        ValueError: If credentials are not configured
        Exception: If upload fails
    """
    try:
        credentials = get_blob_credentials()
        token = credentials["token"]
    except ValueError as e:
        logger.error(str(e))
        raise
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
                "x-add-random-suffix": "true",
            }
            
            # Prepare form data
            data = aiohttp.FormData()
            data.add_field("file", file_content, filename=filename)
            
            async with session.post(
                f"{VERCEL_BLOB_API_URL}/upload",
                headers=headers,
                data=data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Vercel Blob upload failed: {error_text}")
                    raise Exception(f"Failed to upload to Vercel Blob: {error_text}")
                
                result = await response.json()
                logger.info(f"Successfully uploaded {filename} to Vercel Blob")
                return result
    except Exception as e:
        logger.error(f"Error uploading to Vercel Blob: {str(e)}")
        raise


async def download_pdf_from_blob(blob_url: str) -> Optional[bytes]:
    """
    Download PDF from Vercel Blob storage URL
    
    Args:
        blob_url: Full URL of the blob
        
    Returns:
        Binary content of the PDF
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(blob_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download from blob: {response.status}")
                    raise Exception(f"Failed to download PDF: {response.status}")
                
                content = await response.read()
                logger.info(f"Successfully downloaded PDF from blob")
                return content
    except Exception as e:
        logger.error(f"Error downloading from Vercel Blob: {str(e)}")
        raise


async def delete_pdf_from_blob(blob_url: str) -> bool:
    """
    Delete PDF from Vercel Blob storage
    
    Args:
        blob_url: Full URL of the blob
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If credentials are not configured
    """
    try:
        credentials = get_blob_credentials()
        token = credentials["token"]
    except ValueError as e:
        logger.error(str(e))
        raise
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            
            async with session.delete(
                blob_url,
                headers=headers,
            ) as response:
                if response.status not in [200, 204]:
                    error_text = await response.text()
                    logger.error(f"Failed to delete from blob: {error_text}")
                    return False
                
                logger.info(f"Successfully deleted PDF from Vercel Blob")
                return True
    except Exception as e:
        logger.error(f"Error deleting from Vercel Blob: {str(e)}")
        return False


async def get_blob_info(blob_url: str) -> Optional[dict]:
    """
    Get metadata about a blob
    
    Args:
        blob_url: Full URL of the blob
        
    Returns:
        Dictionary with blob metadata
        
    Raises:
        ValueError: If credentials are not configured
    """
    try:
        credentials = get_blob_credentials()
        token = credentials["token"]
    except ValueError as e:
        logger.error(str(e))
        raise
    
    try:
        # Extract pathname from URL
        # URL format: https://STORE_ID.blob.vercelusercontent.com/PATHNAME
        pathname = blob_url.split('.blob.vercelusercontent.com/')[-1]
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            
            # Vercel Blob API to list files
            async with session.get(
                f"{VERCEL_BLOB_API_URL}/?pathname={pathname}",
                headers=headers,
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to get blob info: {response.status}")
                    return None
                
                result = await response.json()
                return result
    except Exception as e:
        logger.error(f"Error getting blob info: {str(e)}")
        return None
