from PyPDF2 import PdfReader
from typing import Union
import io

def extract_text_from_pdf(pdf_source: Union[str, io.BytesIO]) -> str:
    """
    Extract text from a PDF file or BytesIO object
    
    Args:
        pdf_source: Path to PDF file (str) or BytesIO object
        
    Returns:
        Extracted text from the PDF
    """
    try:
        # Handle both file paths and BytesIO objects
        if isinstance(pdf_source, str):
            reader = PdfReader(pdf_source)
        else:
            # Reset position if it's a BytesIO object
            pdf_source.seek(0)
            reader = PdfReader(pdf_source)
        
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
