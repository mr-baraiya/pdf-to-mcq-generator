# Extract text from PDF files

import logging
from io import BytesIO
from PyPDF2 import PdfReader

log = logging.getLogger(__name__)


def extract_text_from_pdf(pdf):
    """Extract text from PDF"""
    try:
        # Open PDF
        if isinstance(pdf, BytesIO):
            reader = PdfReader(pdf)
        else:
            # From file path
            with open(pdf, 'rb') as f:
                reader = PdfReader(f)
        
        # Get text from all pages
        txt = ""
        for p in reader.pages:
            pt = p.extract_text()
            if pt:
                txt += pt + "\n"
        
        log.info(f"Extracted {len(txt)} chars")
        return txt.strip()
        
    except Exception as e:
        log.error(f"Extract error: {str(e)}")
        raise ValueError(f"Failed to extract: {str(e)}")
