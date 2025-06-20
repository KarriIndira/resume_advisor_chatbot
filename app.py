from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from utils import extract_text_from_resume, build_prompt, ask_groq

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile, question: str = Form(...)):
    text = await file.read()
    resume_text = extract_text_from_resume(file.filename, text)
    prompt = build_prompt(resume_text, question)
    response = ask_groq(prompt)
    return JSONResponse(content={"answer": response})
