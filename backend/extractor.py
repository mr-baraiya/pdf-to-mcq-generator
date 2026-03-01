# Extract text from PDF files

import logging
import os
from io import BytesIO
from PyPDF2 import PdfReader

try:
    from pdf2image import convert_from_bytes, convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from pptx import Presentation
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False

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
            log.warning("OCR not available (missing libraries)")
            raise ValueError("PDF contains only images. Install OCR: (1) pip install pdf2image pytesseract (2) Install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/ (3) Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
            
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
            
            if len(ocr_text) < 50:
                raise ValueError("PDF contains only images but no readable text was extracted. Please upload a PDF with text content.")
            
            log.info(f"Extracted {len(ocr_text)} chars via OCR")
            return ocr_text
            
        except Exception as ocr_err:
            log.error(f"OCR failed: {str(ocr_err)}")
            error_msg = str(ocr_err)
            
            # Check for Poppler not installed error
            if "poppler" in error_msg.lower() or "unable to get page count" in error_msg.lower():
                raise ValueError("PDF contains only images. Poppler not installed. Download from: https://github.com/oschwartz10612/poppler-windows/releases/ and add to PATH")
            
            # Check for Tesseract not installed error
            if "tesseract is not installed" in error_msg.lower() or "tesseractnotfound" in error_msg.lower():
                raise ValueError("PDF contains only images. Tesseract OCR engine not installed. Install from: https://github.com/UB-Mannheim/tesseract/wiki")
            
            # Check if no text was extracted
            if len(txt) == 0:
                raise ValueError(f"Failed to extract text from image-based PDF: {error_msg}")
            
            return txt  # Return whatever we got from PyPDF2
        
    except Exception as e:
        log.error(f"Extract error: {str(e)}")
        raise ValueError(f"Failed to extract: {str(e)}")


def extract_text_from_pptx(pptx):
    try:
        if not PPTX_AVAILABLE:
            raise ValueError("python-pptx not installed")
        
        if isinstance(pptx, BytesIO):
            prs = Presentation(pptx)
        else:
            prs = Presentation(pptx)
        
        txt = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    txt += shape.text + "\n"
        
        txt = txt.strip()
        log.info(f"Extracted {len(txt)} chars from PPTX")
        return txt
        
    except Exception as e:
        log.error(f"PPTX extract error: {str(e)}")
        raise ValueError(f"Failed to extract from PPTX: {str(e)}")


def extract_text_from_txt(txt_file):
    try:
        if isinstance(txt_file, BytesIO):
            content = txt_file.read().decode('utf-8', errors='ignore')
        else:
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        content = content.strip()
        log.info(f"Extracted {len(content)} chars from TXT")
        return content
        
    except Exception as e:
        log.error(f"TXT extract error: {str(e)}")
        raise ValueError(f"Failed to extract from TXT: {str(e)}")
