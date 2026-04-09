import os
import json
import re
import logging
import gc
from groq import Groq
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)
_EMBEDDINGS = None
_EMBEDDING_MODEL = None


class _SentenceTransformerEmbeddings:
    def __init__(self, model):
        self._model = model

    def embed_documents(self, texts):
        return self._model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return self._model.encode([text], normalize_embeddings=True)[0].tolist()


def _get_embeddings():
    global _EMBEDDINGS
    global _EMBEDDING_MODEL
    if _EMBEDDINGS is None:
        if _EMBEDDING_MODEL is None:
            _EMBEDDING_MODEL = SentenceTransformer(
                "sentence-transformers/paraphrase-MiniLM-L3-v2"
            )
        _EMBEDDINGS = _SentenceTransformerEmbeddings(_EMBEDDING_MODEL)
    return _EMBEDDINGS


def _build_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    docs = splitter.create_documents([text])
    if not docs:
        return None
    return FAISS.from_documents(docs, _get_embeddings())


def _retrieve_context(text, k=4):
    store = _build_vector_store(text)
    if not store:
        return ""
    query = (
        "Key concepts, definitions, explanations, examples, and applications from the document."
    )
    try:
        docs = store.similarity_search(query, k=k)
        return "\n\n".join(doc.page_content for doc in docs).strip()
    finally:
        del store
        gc.collect()


def generate_mcqs(txt, num=5):
    try:
        if not txt or not txt.strip():
            raise ValueError("Text empty")
        if num < 1 or num > 50:
            raise ValueError("Questions: 1-50")

        context = _retrieve_context(txt)
        if not context:
            return []

        return generate_with_groq(context, num)
    finally:
        gc.collect()


def generate_with_groq(txt, num):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found")
    
    client = Groq(api_key=api_key)
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intelligent educational assistant that generates high-quality multiple-choice questions."
                ),
            },
            {"role": "user", "content": make_prompt(txt, num)},
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    
    return parse_response(res.choices[0].message.content)


def make_prompt(txt, num):
    if len(txt) > 10000:
        txt = txt[:10000] + "...(truncated)"
    
    return f"""You are an intelligent educational assistant designed to generate high-quality multiple-choice questions (MCQs) from academic content.

Your task is to generate MCQs ONLY from the provided context. The context is retrieved from a larger document using a retrieval system, so you must strictly rely on it.

Instructions:
1. Carefully read and understand the given context.
2. Generate multiple-choice questions that test conceptual understanding, not just memorization.
3. Each question must have exactly 4 options (A, B, C, D).
4. Clearly indicate the correct answer.
5. Provide a brief explanation for the correct answer.
6. Avoid duplicate or trivial questions.
7. Ensure questions are clear, concise, and relevant to the context.
8. If the context is insufficient, do NOT hallucinate — instead, return an empty list.
9. Ensure options are plausible and not obviously incorrect.
10. Shuffle correct answers across A, B, C, D positions.
11. Avoid repeating the same answer pattern.
12. Focus on key concepts, definitions, examples, and applications.

Difficulty Levels:
- Easy: Basic definitions or direct facts
- Medium: Conceptual understanding
- Hard: Application-based or tricky questions

Output JSON only in this format:
{{
    "questions": [
        {{
            "question": "Question?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "A",
            "explanation": "Short explanation.",
            "difficulty": "Easy|Medium|Hard"
        }}
    ]
}}

Context:
{txt}

Generate exactly {num} questions.
"""


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
