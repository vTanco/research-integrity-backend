import fitz
import sys

path = "/Users/vicente.tancoedu.uah.es/Documents/APP/DOCUMENTACION PROYECTO/RESOURCES/Algoritmo de evaluación de conflictos de interés.pdf"

try:
    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        print(text)
except Exception as e:
    print(f"Error: {e}")
