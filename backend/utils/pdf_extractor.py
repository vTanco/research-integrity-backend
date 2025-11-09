import fitz

def extract_text_from_pdf(path: str) -> str:
    try:
        with fitz.open(path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip()
    except Exception as e:
        # Devuelve texto vacío para evitar error 500 y facilita depuración
        return f"[PDF extraction failed: {str(e)}]"
