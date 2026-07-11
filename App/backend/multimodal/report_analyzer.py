import os
import base64
import mimetypes
from dotenv import load_dotenv
from groq import Groq
from backend.monitoring.stats import system_stats

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_medical_report(image_path, ocr_text):

    try:

        image_base64 = encode_image(image_path)

        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/jpeg"

        prompt = f"""
You are a medical document information extraction system.

Your task is to extract ONLY factual information from the given OCR text and image.

RULES:
- Do NOT diagnose
- Do NOT give medical advice
- Do NOT invent missing information
- Use ONLY visible/explicit data
- If not found, write "Not clearly mentioned"

OCR TEXT:
{ocr_text}

OUTPUT FORMAT:

Document Type:
Patient Name:
Medicines:
- Name:
- Dosage:
- Frequency:

Findings:
-

Doctor Recommendations:
-
"""

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=800
        )

        usage = response.usage

        system_stats["llm"] = True

        system_stats["prompt_tokens"] += usage.prompt_tokens
        system_stats["completion_tokens"] += usage.completion_tokens
        system_stats["total_tokens"] += usage.total_tokens

        cost = (
            usage.prompt_tokens / 1_000_000
        ) * 0.59 + (
            usage.completion_tokens / 1_000_000
        ) * 0.79

        system_stats["cost"] += cost

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"