import json
import ollama

def generate_mcqs(text: str, num_questions: int = 5) -> list:
    """
    Generate MCQs from given text using Ollama
    
    Args:
        text: The text to generate questions from
        num_questions: Number of questions to generate
        
    Returns:
        List of generated MCQs with options and answers
    """
    try:
        prompt = f"""Generate {num_questions} multiple choice questions (MCQs) from the following text. 
For each question, provide 4 options (A, B, C, D) and the correct answer.

Text:
{text}

Return the response as a JSON array with this structure:
[
    {{
        "question": "Question text here?",
        "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
        "answer": "A"
    }}
]

Only return the JSON array, no other text."""

        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            stream=False,
        )
        
        # Extract JSON from response
        response_text = response['response'].strip()
        
        # Try to parse JSON
        try:
            questions = json.loads(response_text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                questions = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse MCQs from model response")
        
        return questions
    except Exception as e:
        raise Exception(f"Error generating MCQs: {str(e)}")
