import os
import json
import re
import logging
from groq import Groq

log = logging.getLogger(__name__)


def generate_mcqs(txt, num=5):
    if not txt or not txt.strip():
        raise ValueError("Text empty")
    if num < 1 or num > 20:
        raise ValueError("Questions: 1-20")
    
    return generate_with_groq(txt, num)


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
    
    return f"""From this text, make {num} multiple choice questions:

TEXT:
{txt}

Return JSON only:
{{
    "questions": [
        {{
            "question": "Question?",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        }}
    ]
}}

Rules: Exactly {num} questions, 4 options each, JSON only."""


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
