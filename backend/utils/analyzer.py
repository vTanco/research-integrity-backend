import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

def analyze_text(text: str, metadata: dict) -> dict:
    """
    Analyzes a scientific paper and its metadata for potential conflicts of interest
    using the OpenAI API. Returns structured JSON output or an error message.
    """

    # Recuperar clave de API desde entorno (Render o local)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY is missing from environment variables."}

    # Inicializar cliente dinámicamente
    client = OpenAI(api_key=api_key)

    # Crear prompt
    prompt = f"""
You are an expert in research ethics.
Analyze this scientific paper and its metadata for potential conflicts of interest.

Metadata:
{metadata}

Text sample:
{text[:6000]}

Return a STRICTLY VALID JSON with:
- overall_risk: one of [low, medium, high]
- score: integer 0–100
- categories: list of objects {{ "name": string, "score": int, "level": string }}
- summary: concise paragraph (max 3 sentences)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()
        return {"raw": content}

    except Exception as e:
        return {"error": f"OpenAI API call failed: {str(e)}"}
