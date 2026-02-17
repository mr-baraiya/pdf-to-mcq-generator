# Generate MCQ questions using Local Ollama (priority), Groq AI, or Gemini AI

import os
import json
import re
import logging
import requests
from groq import Groq

log = logging.getLogger(__name__)

# Track last used API for round-robin
_last_api_used = None
_ollama_available = None  # Cache Ollama availability check


def check_ollama_available():
    """Check if local Ollama is available"""
    global _ollama_available
    
    # Use cached result if available
    if _ollama_available is not None:
        return _ollama_available
    
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=2)
        _ollama_available = response.status_code == 200
        if _ollama_available:
            log.info(f"✅ Local Ollama detected at {ollama_url}")
        return _ollama_available
    except Exception as e:
        log.info(f"ℹ️ Local Ollama not available: {str(e)}")
        _ollama_available = False
        return False


def select_api(text_size_bytes):
    """
    Smart API selection based on size and round-robin
    
    Rules:
    1. If text > 5MB → Always use Gemini
    2. If text < 50KB → Always use Groq (faster)
    3. If 50KB < text < 5MB → Round-robin between both
    """
    global _last_api_used
    
    size_mb = text_size_bytes / (1024 * 1024)
    size_kb = text_size_bytes / 1024
    
    # Large files (>5MB) → Gemini only
    if size_mb > 5:
        log.info(f"Large text ({size_mb:.2f}MB) → Using Gemini (better understanding)")
        return "gemini"
    
    # Small files (<50KB) → Groq only (faster)
    if size_kb < 50:
        log.info(f"Small text ({size_kb:.2f}KB) → Using Groq (faster)")
        return "groq"
    
    # Medium files (50KB - 5MB) → Round-robin
    if _last_api_used == "groq":
        api = "gemini"
    else:
        api = "groq"
    
    _last_api_used = api
    log.info(f"Medium text ({size_kb:.2f}KB) → Round-robin: {api.upper()}")
    return api


def generate_mcqs(txt, num=5):
    """Generate MCQ from text - Try Ollama first, then fallback to Groq/Gemini"""
    
    # Validate
    if not txt or not txt.strip():
        raise ValueError("Text empty")
    
    if num < 1 or num > 20:
        raise ValueError("Questions: 1-20")
    
    # Priority 1: Try local Ollama first
    if check_ollama_available():
        try:
            log.info("🏠 Using Local Ollama (Priority)")
            return generate_with_ollama(txt, num)
        except Exception as e:
            log.warning(f"⚠️ Ollama failed: {str(e)}, falling back to cloud APIs")
    
    # Priority 2: Fallback to Groq/Gemini
    text_size = len(txt.encode('utf-8'))
    selected_api = select_api(text_size)
    
    # Use selected API
    if selected_api == "gemini":
        return generate_with_gemini(txt, num)
    else:
        return generate_with_groq(txt, num)


def generate_with_ollama(txt, num):
    """Generate MCQ using local Ollama"""
    
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    log.info(f"🏠 Generating {num} MCQs with Ollama ({ollama_model})")
    
    try:
        prompt = make_prompt(txt, num)
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code}")
        
        result = response.json()
        resp = result.get("response", "")
        
        qs = parse_response(resp)
        
        if not qs:
            raise Exception("No questions generated")
        
        log.info(f"✅ Ollama: Generated {len(qs)} questions")
        return qs
        
    except Exception as e:
        log.error(f"❌ Ollama error: {str(e)}")
        raise


def generate_with_groq(txt, num):
    """Generate MCQ using Groq API"""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    log.info(f"🚀 Generating {num} MCQs with Groq (Llama 3.3)")
    
    try:
        client = Groq(api_key=api_key)
        prompt = make_prompt(txt, num)
    
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
        
        resp = res.choices[0].message.content
        qs = parse_response(resp)
        
        log.info(f"✅ Groq: Generated {len(qs)} questions")
        return qs
        
    except Exception as e:
        log.error(f"❌ Groq error: {str(e)}")
        # Fallback to Gemini if Groq fails
        log.info("Falling back to Gemini...")
        return generate_with_gemini(txt, num)


def generate_with_gemini(txt, num):
    """Generate MCQ using Gemini REST API (lightweight, no SDK)"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    log.info(f"🧠 Generating {num} MCQs with Gemini")
    
    try:
        prompt = make_prompt(txt, num)
        
        # Use Gemini REST API directly (no heavy SDK)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
        
        result = response.json()
        resp = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if not resp:
            raise Exception("Empty response from Gemini")
        
        qs = parse_response(resp)
        
        log.info(f"✅ Gemini: Generated {len(qs)} questions")
        return qs
        
    except Exception as e:
        log.error(f"❌ Gemini error: {str(e)}")
        raise


def make_prompt(txt, num):
    """Create prompt for AI"""
    
    # Truncate text if too large (for API limits)
    max_chars = 10000
    if len(txt) > max_chars:
        txt = txt[:max_chars] + "...(truncated)"
    
    return f"""From this text, make {num} multiple choice questions:

TEXT:
{txt}

Return JSON only (no extra text):
{{
    "questions": [
        {{
            "question": "Question?",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        }}
    ]
}}

Rules:
1. Exactly {num} questions
2. 4 options per question
3. 1 correct answer (field: "answer")
4. Based on text only
5. JSON only, no markdown

Make questions:"""


def parse_response(resp):
    """Extract JSON from response"""
    
    try:
        # Remove markdown code blocks if present
        resp = resp.strip()
        resp = re.sub(r'^```json\s*', '', resp)
        resp = re.sub(r'^```\s*', '', resp)
        resp = re.sub(r'\s*```$', '', resp)
        
        # Try to parse directly first
        try:
            d = json.loads(resp)
            qs = d.get("questions", [])
            if qs:
                log.info(f"Parsed {len(qs)} questions")
                return qs
        except json.JSONDecodeError:
            pass
        
        # Find JSON with regex
        m = re.search(r'\{[\s\S]*\}', resp)
        
        if m:
            j = m.group(0)
            d = json.loads(j)
            qs = d.get("questions", [])
            
            if qs:
                log.info(f"Parsed {len(qs)} questions")
                return qs
        
        log.warning(f"No JSON found in response: {resp[:200]}")
        return []
        
    except json.JSONDecodeError as e:
        log.error(f"JSON error: {str(e)}, Response: {resp[:200]}")
        return []
    except Exception as e:
        log.error(f"Parse error: {str(e)}")
        return []
