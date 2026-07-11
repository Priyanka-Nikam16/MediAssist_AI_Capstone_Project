"""
Input Guardrails

Checks:
1. Empty question
2. Supported file type
3. Prompt injection
4. Medical advice requests
"""

# Supported files
#from fastapi import logger


from backend.app_logs.logger import logger

SUPPORTED_FILES = [
    "pdf",
    "docx",
    "txt",
    "csv",
    "jpg",
    "jpeg",
    "png"
]
def validate_input(state):

    logger.info("========== Input Guardrail Started ==========")

    try:
        #logger.info("Step 1")

        question = state["question"].lower().strip()

        logger.info(f"Question = {question}")

        file_type = state.get("file_type")

        #logger.info("Step 2")

        if question == "":
            logger.info("Empty question")
            state["is_valid"] = False
            state["answer"] = "Please enter your question."
            return state

        #logger.info("Step 3")

        if (
            "ignore previous instructions" in question
            or "system prompt" in question
            or "developer message" in question
            or "jailbreak" in question
        ):
            logger.info("Prompt Injection")
            state["is_valid"] = False
            state["answer"] = "Invalid request."
            return state

        #logger.info("Step 4")

        if (
            "diagnose" in question
            or ("recommend" in question and "medicine" in question)
            or ("suggest" in question and "medicine" in question)
            or ("prescribe" in question and "medicine" in question)
        ):

            logger.info("Medical advice detected")

            state["is_valid"] = False
            state["error_type"] = "Medical Advice"

            state["answer"] = (
                "MediAssist cannot diagnose diseases, prescribe medicines "
                "or provide treatment advice."
            )

            logger.info("Returning from medical advice")
            return state

        #logger.info("Step 5")

        if file_type:
            logger.info("Checking file type")

            if file_type.lower() not in SUPPORTED_FILES:
                logger.info("Unsupported file")
                state["is_valid"] = False
                state["answer"] = "Unsupported file type."
                return state

        #logger.info("Step 6")

        state["is_valid"] = True
        state["error_type"] = None

        logger.info("========== Input Guardrail Completed ==========")

        return state

    except Exception:
        logger.exception("Guardrail crashed")
        raise

