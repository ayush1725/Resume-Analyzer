import requests

def summarize_with_mistral(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": f"Summarize this resume:\n\n{text}",
                "stream": False
            },
            timeout=20
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error contacting Mistral API: {e}")
        return "Summary could not be generated due to an internal error."
