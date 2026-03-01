import os
import json
import re
import logging
import requests
from groq import Groq

log = logging.getLogger(__name__)
_ollama_available = None


def check_ollama_available():
    global _ollama_available
    if _ollama_available is not None:
        return _ollama_available
    
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=2)
        _ollama_available = response.status_code == 200
        return _ollama_available
    except:
        _ollama_available = False
        return False


def generate_mcqs(txt, num=5):
    if not txt or not txt.strip():
        raise ValueError("Text empty")
    if num < 1 or num > 20:
        raise ValueError("Questions: 1-20")
    
    if check_ollama_available():
        try:
            return generate_with_ollama(txt, num)
        except Exception as e:
            log.warning(f"Ollama failed, using Groq: {str(e)}")
    
    return generate_with_groq(txt, num)


def generate_with_ollama(txt, num):
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    response = requests.post(
        f"{ollama_url}/api/generate",
        json={
            "model": ollama_model,
            "prompt": make_prompt(txt, num),
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.7, "num_predict": 4000}
        },
        timeout=180
    )
    
    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.status_code}")
    
    qs = parse_response(response.json().get("response", ""))
    if not qs:
        raise Exception("No questions generated")
    return qs


def generate_with_groq(txt, num):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found")
    
    client = Groq(api_key=api_key)
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates multiple choice questions."},
            {"role": "user", "content": make_prompt(txt, num)}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return parse_response(res.choices[0].message.content)


def make_prompt(txt, num):
    if len(txt) > 10000:
        txt = txt[:10000] + "...(truncated)"
    
    return f"""From this text, create {num} multiple choice questions with 4 options each.

TEXT:
{txt}

Return ONLY valid JSON in this exact format:
{{
    "questions": [
        {{
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "answer": "C"
        }},
        {{
            "question": "Which planet is closest to the Sun?",
            "options": ["Venus", "Mercury", "Mars", "Earth"],
            "answer": "B"
        }}
    ]
}}

IMPORTANT:
- Create exactly {num} questions based on the text above
- Each question must have exactly 4 options
- The "answer" field must be the letter (A, B, C, or D) of the correct option
- Vary the correct answers - don't make them all the same letter
- Make questions clear and options distinct
- Return ONLY the JSON, no extra text"""


def parse_response(resp):
    try:
        resp = resp.strip()
        resp = re.sub(r'^```json\s*', '', resp)
        resp = re.sub(r'^```\s*', '', resp)
        resp = re.sub(r'\s*```$', '', resp)
        
        try:
            d = json.loads(resp)
            qs = d.get("questions", [])
            if qs:
                return qs
        except json.JSONDecodeError:
            pass
        
        m = re.search(r'\{[\s\S]*\}', resp)
        if m:
            d = json.loads(m.group(0))
            return d.get("questions", [])
        
        return []
    except Exception as e:
        log.error(f"Parse error: {str(e)}")
        return []
