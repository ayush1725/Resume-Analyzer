import requests
import json

def summarize_with_mistral(text):
    prompt = f"""
You are an AI Resume Evaluator. Analyze the following resume and provide a structured JSON with three fields:

1. skills_matched: List of key skills found in the resume.
2. skills_missing: List of important skills missing based on modern job requirements (like DevOps, cloud, etc.).
3. experience_fit: One-sentence feedback on how well the candidate’s experience fits a software development role.

Resume:
{text}

Respond strictly in this JSON format:
{{
  "skills_matched": ["Skill1", "Skill2", "..."],
  "skills_missing": ["SkillA", "SkillB", "..."],
  "experience_fit": "Your one-line evaluation here"
}}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error contacting Mistral API: {e}")
        return json.dumps({
            "skills_matched": [],
            "skills_missing": [],
            "experience_fit": "Summary could not be generated due to an internal error."
        })
