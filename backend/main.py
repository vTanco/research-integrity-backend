from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_extractor import extract_text_from_pdf
from utils.metadata_extractor import extract_metadata_from_text
from utils.analyzer import analyze_text
import tempfile, os

app = FastAPI(title="Research Integrity Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze_pdf")
async def analyze_pdf(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path)
    metadata = extract_metadata_from_text(text)
    analysis = analyze_text(text, metadata)

    os.remove(tmp_path)
    return {"metadata": metadata, "analysis": analysis}

@app.post("/analyze_url")
async def analyze_url(url: str = Form(...)):
    from bs4 import BeautifulSoup
    import requests

    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    text = " ".join([p.get_text() for p in soup.find_all("p")])
    metadata = extract_metadata_from_text(text)
    analysis = analyze_text(text, metadata)
    return {"metadata": metadata, "analysis": analysis}
