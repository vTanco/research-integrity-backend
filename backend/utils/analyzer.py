import openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_text(text: str, metadata: dict) -> dict:
    prompt = f"""
You are an expert in research ethics.
Analyze this scientific paper and its metadata for potential conflicts of interest.

Metadata:
{metadata}

Text sample:
{text[:6000]}

Return JSON with:
- overall_risk: low|medium|high
- score: 0-100
- categories: list of objects {{ name, score, level }}
- summary: short paragraph.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return {"raw": response.choices[0].message.content}
