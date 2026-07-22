import json
import re

from backend.evaluation.prompts import SYSTEM_PROMPT, EVALUATION_PROMPT
from backend.app_logs.logger import logger
from backend.llm_client import client
from backend.monitoring.stats import system_stats

def clean_json(text):

    if not text:
        return None

    text = text.strip()

    text = text.replace("```json", "").replace("```", "")

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    return text.strip()


def evaluate_answer(question, context, generated_answer):
    question = str(question or "")
    context = str(context or "")
    generated_answer = str(generated_answer or "")
    logger.info("Calling Judge LLM...")
    # print(type(question), question)
    # print(type(context), context)
    # print(type(generated_answer), generated_answer)

    prompt = (
        EVALUATION_PROMPT
        .replace("<<QUESTION>>", question)
        .replace("<<CONTEXT>>", context)
        .replace("<<ANSWER>>", generated_answer)
)
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=messages
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

        result = response.choices[0].message.content

        logger.info(f"Raw Judge Output:\n{result}")

        result = clean_json(result)

        evaluation = json.loads(result)

        logger.info("Judge Evaluation Completed.")

        return evaluation

    except Exception as e:

        logger.error(f"Judge Error : {e}")

        return {
            "faithfulness": {"score": 0, "reason": "Evaluation Failed"},
            "grounding": {"score": 0, "reason": "Evaluation Failed"},
            "relevance": {"score": 0, "reason": "Evaluation Failed"},
            "completeness": {"score": 0, "reason": "Evaluation Failed"},
            "hallucination": {"score": 0, "reason": "Evaluation Failed"},
            "overall_score": 0,
            "summary": "Evaluation Failed"
        }






