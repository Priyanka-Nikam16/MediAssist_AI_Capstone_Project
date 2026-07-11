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

# import os

# from backend.multimodal.ocr import extract_text_from_image
# from backend.multimodal.report_analyzer import analyze_medical_report


# def process_medical_image(image_path):
#     """
#     Process an uploaded medical image.

#     Parameters
#     ----------
#     image_path : str
#         Path of uploaded image.

#     Returns
#     -------
#     str
#         Final medical report generated from OCR + Vision analysis.
#     """

#     print("=" * 60)
#     print(f"Processing Image: {os.path.basename(image_path)}")
#     print("=" * 60)

#     # ---------------------------------------------------
#     # Step 1 : Extract text using EasyOCR
#     # ---------------------------------------------------

#     print("Running OCR...")

#     ocr_text = extract_text_from_image(image_path)

#     if not ocr_text:
#         print("No text detected using OCR.")
#     else:
#         print("OCR Completed.")

#     # ---------------------------------------------------
#     # Step 2 : Generate Medical Report
#     # ---------------------------------------------------

#     print("Running Vision Analysis...")

#     final_report = analyze_medical_report(
#         image_path=image_path,
#         ocr_text=ocr_text
#     )

#     # ---------------------------------------------------
#     # Step 3 : Fallback
#     # ---------------------------------------------------

#     if not final_report:
#         final_report = (
#             "No medical information could be extracted "
#             "from the uploaded image."
#         )

#     print("Image Processing Completed.")
#     print("=" * 60)

#     return final_report

import os
from backend.multimodal.ocr import extract_text_from_image
from backend.multimodal.report_analyzer import analyze_medical_report


def process_medical_image(image_path):

    print("=" * 60)
    print(f"Processing: {os.path.basename(image_path)}")
    print("=" * 60)

    # Step 1: OCR
    ocr_result = extract_text_from_image(image_path)
    ocr_text = ocr_result.get("ocr_text", "")

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