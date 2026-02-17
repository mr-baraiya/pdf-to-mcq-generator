# Generate MCQ questions using Groq AI

import os
import json
import re
import logging
from groq import Groq

log = logging.getLogger(__name__)


def generate_mcqs(txt, num=5):
    """Generate MCQ from text using Groq API"""
    
    # Validate
    if not txt or not txt.strip():
        raise ValueError("Text empty")
    
    if num < 1 or num > 20:
        raise ValueError("Questions: 1-20")
    
    # Get Groq API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    log.info(f"Generating {num} MCQs with Groq API")
    
    try:
        # Create Groq client
        client = Groq(api_key=api_key)
        
        # Make prompt
        prompt = make_prompt(txt, num)
    
        # Send to Groq API
        res = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates multiple choice questions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Get response
        resp = res.choices[0].message.content
        
        # Parse JSON
        qs = parse_response(resp)
        
        log.info(f"Generated {len(qs)} questions")
        return qs
        
    except Exception as e:
        log.error(f"Groq error: {str(e)}")
        raise


def make_prompt(txt, num):
    """Create prompt for AI"""
    
    return f"""From this text, make {num} multiple choice questions:

TEXT:
{txt}

Return JSON only (no extra text):
{{
    "questions": [
        {{
            "question": "Question?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }}
    ]
}}

Rules:
1. Exactly {num} questions
2. 4 options per question
3. 1 correct answer
4. Based on text only
5. JSON only, no markdown

Make questions:"""


def parse_response(resp):
    """Extract JSON from response"""
    
    try:
        # Find JSON
        m = re.search(r'\{{[\s\S]*\}}', resp)
        
        if m:
            j = m.group(0)
            d = json.loads(j)
            qs = d.get("questions", [])
            
            if qs:
                log.debug(f"Parsed {len(qs)} questions")
                return qs
        
        log.warning("No JSON found")
        return []
        
    except json.JSONDecodeError as e:
        log.error(f"JSON error: {str(e)}")
        return []
