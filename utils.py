import os
import base64
import requests
from PyPDF2 import PdfReader

def extract_text_from_resume(filename, file_bytes):
    if filename.endswith(".pdf"):
        from io import BytesIO
        reader = PdfReader(BytesIO(file_bytes))
        return " ".join([page.extract_text() or "" for page in reader.pages])
    else:
        return file_bytes.decode("utf-8")

def build_prompt(resume_text, question):
    return f"""You are a professional resume advisor.
Resume Content:
{resume_text}

User Question: {question}
Give personalized feedback based on the resume above."""

def ask_groq(prompt):
    API_KEY = os.getenv("GROQ_API_KEY")
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    res = requests.post(endpoint, headers=headers, json=data)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    return f"Error: {res.status_code} - {res.text}"
