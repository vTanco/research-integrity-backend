import re

def extract_metadata_from_text(text: str) -> dict:
    lines = text.split("\n")[:50]
    joined = " ".join(lines)
    title = lines[0][:200] if lines else ""
    authors = re.findall(r"[A-Z][a-z]+\s[A-Z][a-z]+", joined)
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", joined)
    institutions = re.findall(r"University|Institute|Hospital|Center|College", joined, re.IGNORECASE)

    return {
        "title": title.strip(),
        "authors": list(set(authors))[:10],
        "emails": list(set(emails))[:5],
        "institutions": list(set(institutions))[:5]
    }
