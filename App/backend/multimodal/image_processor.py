# """
# ---------------------------------------------------------
# MediAssist AI - Image Processor
# ---------------------------------------------------------

# Purpose
# -------
# 1. Process uploaded medical images.
# 2. Extract text using EasyOCR.
# 3. Send image + OCR text to Report Analyzer.
# 4. Return final medical report for RAG ingestion.


# ---------------------------------------------------------
# """
import os
from backend.multimodal.ocr import extract_text_from_image
from backend.multimodal.report_analyzer import analyze_medical_report


def process_medical_image(image_path):

    print("=" * 60)
    print(f"Processing: {os.path.basename(image_path)}")
    print("=" * 60)

    # Step 1: OCR
    ocr_result = extract_text_from_image(image_path)
    ocr_text = ocr_result.get("ocr_text", "") # get the value of "ocr_text"  if value not present  u get "" to avoid error.

    print("OCR Completed")

    # Step 2: Vision + LLM analysis
    final_report = analyze_medical_report(
        image_path=image_path,
        ocr_text=ocr_text
    )

    print("Analysis Completed")

    return {
        "file_name": os.path.basename(image_path),
        "ocr_text": ocr_text,
        "final_report": final_report
    }