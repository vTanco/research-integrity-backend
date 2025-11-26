import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.analyzer import analyze_text

def test_analyzer():
    mock_text = """
    This study was funded by Big Pharma Inc. The authors declare no conflict of interest.
    However, Dr. Smith is a consultant for Big Pharma Inc.
    The data is available upon reasonable request.
    The results show a miraculous improvement in patients treated with our drug.
    """
    
    mock_metadata = {
        "title": "Test Study",
        "authors": ["Dr. Smith", "Dr. Jones"],
        "date": "2023-01-01"
    }

    print("Running analysis...")
    result = analyze_text(mock_text, mock_metadata)
    
    print("\nAnalysis Result:")
    print(json.dumps(result, indent=2))

    # Basic validation
    if "overall_risk" in result and "categories" in result:
        print("\n✅ Structure validation passed.")
    else:
        print("\n❌ Structure validation failed.")

if __name__ == "__main__":
    test_analyzer()
