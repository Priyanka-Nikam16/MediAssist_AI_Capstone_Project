"""
---------------------------------------------------------
MediAssist AI - OCR Module
---------------------------------------------------------

Purpose:
1. Extract raw text from medical images using EasyOCR.
2. Provide clean text output for downstream LLM processing.
3. Keep module lightweight (NO embedding / NO LLM logic).

Flow:
Image → OCR → Raw Text → image_processor.py → FAISS

---------------------------------------------------------
"""


import easyocr

# -------------------------------------------------------
# Load EasyOCR Model (Loads only once)
# -------------------------------------------------------

print("Loading EasyOCR...")

reader = easyocr.Reader(['en'])

print("EasyOCR Loaded Successfully")


# -------------------------------------------------------
# OCR Function
# -------------------------------------------------------
reader = None

def get_reader():
    global reader

    if reader is None:
        print("Loading EasyOCR...")
        reader = easyocr.Reader(["en"])
        print("EasyOCR Loaded Successfully")

    return reader

def extract_text_from_image(image_path):
    try:
        reader = get_reader()
        results = reader.readtext(image_path)

        text = "\n".join([res[1] for res in results])
        print("=*OCR OUTPUT*"*20)
        print(text)
        print("=**"*20)

        return {
            "ocr_text": text.strip()
        }

    except Exception as e:
        return {
            "ocr_text": "",
            "error": str(e)
        }