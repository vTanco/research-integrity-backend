from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.pdf_extractor import extract_text_from_pdf
from backend.utils.metadata_extractor import extract_metadata_from_text
from backend.utils.analyzer import analyze_text
import tempfile, os
from bs4 import BeautifulSoup
import requests

app = FastAPI(title="Research Integrity Analyzer API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze_pdf")
async def analyze_pdf(file: UploadFile):
    # Guardar temporalmente el archivo PDF
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Procesar el PDF
    text = extract_text_from_pdf(tmp_path)
    metadata = extract_metadata_from_text(text)
    analysis = analyze_text(text, metadata)

    # Limpiar archivo temporal
    os.remove(tmp_path)

    return {
        "metadata": metadata,
        "analysis": analysis
    }


@app.post("/analyze_url")
async def analyze_url(url: str = Form(...)):
    # Descargar y limpiar el HTML
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join([p.get_text() for p in soup.find_all("p")])

    # Analizar el texto extraído
    metadata = extract_metadata_from_text(text)
    analysis = analyze_text(text, metadata)

    return {
        "metadata": metadata,
        "analysis": analysis
    }
