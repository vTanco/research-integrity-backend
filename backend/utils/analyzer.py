import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

def analyze_text(text: str, metadata: dict) -> dict:
    """
    Analyzes a scientific paper and its metadata for potential conflicts of interest
    using the OpenAI API, following the "Algoritmo de evaluación de conflictos de interés".
    Returns structured JSON output.
    """

    # Recuperar clave de API desde entorno (Render o local)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY is missing from environment variables."}

    # Inicializar cliente dinámicamente
    client = OpenAI(api_key=api_key)

    # Crear prompt detallado basado en el algoritmo
    prompt = f"""
You are an expert in research ethics and scientific integrity.
Analyze this scientific paper text and its metadata to evaluate the risk of Conflict of Interest (COI).
Follow the "Algoritmo de evaluación de conflictos de interés" strictly.

Dimensions to Analyze:
1. Textual Bias & Reporting Quality:
   - Analyze the language used (sober vs. promotional).
   - Check if limitations are discussed honestly.
   - Check if the methodology is transparently presented.
   - High Risk: Promotional language, hidden limitations.
   - Low Risk: Objective language, acknowledged limitations.

2. Funding-Outcome Alignment:
   - Analyze the relationship between funding sources and study results.
   - Check for promotional language in results.
   - High Risk: Private funding + positive results for sponsor.
   - Low Risk: Public funding or balanced discussion.

3. Author-Institution-Sponsor Network:
   - Analyze connections between authors, institutions, and sponsors.
   - Check for commercial ties or undisclosed conflicts.
   - High Risk: Direct employment or financial ties to sponsor.
   - Low Risk: Academic affiliations, no commercial ties.

4. Journal / Editorial Integrity:
   - Assess the quality and reputation of the publication venue.
   - Check for clear peer review processes.
   - High Risk: Predatory journal, lack of transparency.
   - Low Risk: Reputable journal, clear guidelines.

5. Recommendations for Readers:
   - Provide 3 specific, actionable recommendations for readers based on the analysis.

Scoring Rules:
- Assign a score (0-100) for EACH dimension (except Recommendations) based on the evidence found.
- Determine the Risk Level for each dimension:
  - 0-33: "low"
  - 34-66: "medium"
  - 67-100: "high"
- Calculate 'overall_score' as the average of the 4 dimension scores.
- Determine 'overall_risk' based on the overall_score using the same thresholds.

Input Data:
Metadata: {metadata}
Text Sample: {text[:15000]} (truncated if too long)

Output Format:
Return a STRICTLY VALID JSON object with the following structure. Do not include markdown formatting (like ```json).

{{
  "overall_risk": "low" | "medium" | "high",
  "score": integer (0-100),
  "summary": "Concise paragraph (max 3 sentences) summarizing the main COI risks found.",
  "categories": [
    {{
      "name": "Textual Bias & Reporting Quality",
      "score": integer,
      "level": "low" | "medium" | "high",
      "description": "Brief description of the risk.",
      "evidence": ["List of 3 specific points found..."]
    }},
    {{
      "name": "Funding-Outcome Alignment",
      "score": integer,
      "level": "low" | "medium" | "high",
      "description": "Brief description of the risk.",
      "evidence": ["List of 3 specific points found..."]
    }},
    {{
      "name": "Author-Institution-Sponsor Network",
      "score": integer,
      "level": "low" | "medium" | "high",
      "description": "Brief description of the risk.",
      "evidence": ["List of 3 specific points found..."]
    }},
    {{
      "name": "Journal / Editorial Integrity",
      "score": integer,
      "level": "low" | "medium" | "high",
      "description": "Brief description of the risk.",
      "evidence": ["List of 3 specific points found..."]
    }}
  ],
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2",
    "Recommendation 3"
  ]
}}
"""


    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, # Low temperature for consistent, rule-based output
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content.strip()
        # Ensure it's valid JSON
        return json.loads(content)

    except Exception as e:
        print(f"Error in analyze_text: {e}")
        # Return a fallback error structure that the frontend can handle/display
        return {
            "overall_risk": "medium",
            "score": 50,
            "summary": f"Analysis failed due to an error: {str(e)}. Please try again.",
            "categories": []
        }
