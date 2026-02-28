# Extract text from PDF files

import logging
import os
from io import BytesIO
from PyPDF2 import PdfReader

# Try importing OCR libraries
try:
    from pdf2image import convert_from_bytes, convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

log = logging.getLogger(__name__)


def extract_text_from_pdf(pdf):
    """Extract text from PDF (with OCR fallback)"""
    try:
        # 1. Try PyPDF2 first (fastest)
        if isinstance(pdf, BytesIO):
            reader = PdfReader(pdf)
            pdf.seek(0)
        else:
            with open(pdf, 'rb') as f:
                reader = PdfReader(f)
        
        txt = ""
        for p in reader.pages:
            pt = p.extract_text()
            if pt:
                txt += pt + "\n"
        
        txt = txt.strip()
        
        # 2. If text is sufficient, return it
        if len(txt) > 50:
            log.info(f"Extracted {len(txt)} chars via PyPDF2")
            return txt
            
        # 3. If text is empty/low, try OCR
        if not OCR_AVAILABLE:
            log.warning("OCR not available (missing libraries), returning empty text")
            return txt
            
        log.info("Text empty/low, attempting OCR extraction...")
        
        try:
            images = []
            if isinstance(pdf, BytesIO):
                pdf.seek(0)  # Reset pointer before reading bytes
                images = convert_from_bytes(pdf.read())
            else:
                images = convert_from_path(pdf)
            
            ocr_text = ""
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                ocr_text += page_text + "\n"
                log.info(f"OCR Page {i+1}: {len(page_text)} chars")
            
            ocr_text = ocr_text.strip()
            log.info(f"Extracted {len(ocr_text)} chars via OCR")
            return ocr_text
            
        except Exception as ocr_err:
            log.error(f"OCR failed: {str(ocr_err)}")
            return txt  # Return whatever we got from PyPDF2
        
    except Exception as e:
        log.error(f"Extract error: {str(e)}")
        raise ValueError(f"Failed to extract: {str(e)}")
