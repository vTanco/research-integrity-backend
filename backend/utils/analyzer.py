import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(text: str, metadata: dict) -> dict:
    try:
        prompt = f"""
You are an expert in research ethics.
Analyze this scientific paper and its metadata for potential conflicts of interest.

Metadata:
{metadata}

Text sample:
{text[:6000]}

Return strictly valid JSON with:
- overall_risk: low|medium|high
- score: 0-100
- categories: list of objects {{ name, score, level }}
- summary: short paragraph.
"""

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        return {"raw": content}

    except Exception as e:
        return {"error": f"OpenAI API call failed: {str(e)}"}
