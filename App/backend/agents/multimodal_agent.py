"""
---------------------------------------------------------
MediAssist AI - Multimodal Agent
---------------------------------------------------------

Purpose
-------
1. Answer questions about previously uploaded medical images.
2. Retrieve OCR + AI analysis from FAISS.
3. Store answer and sources in graph state.
---------------------------------------------------------
"""

from backend.app_logs.logger import logger
from backend.rag import answer_from_rag


def multimodal_agent(state):
    """
    Handles questions about uploaded medical images.
    Images are assumed to have already been processed
    and indexed into FAISS during upload.
    """

    logger.info("========== Multimodal Agent Started ==========")

    try:

        question = state["question"]

        logger.info(f"Question : {question}")
        logger.info("Retrieving image information from FAISS...")

        # Retrieve from FAISS (uses filename if present in the question)
        result = answer_from_rag(question)
        logger.info(f"Result Keys : {result.keys()}")
        logger.info(f"Context Length from RAG : {len(result.get('context', ''))}")

        state["retrieved_context"] = result.get("context", "")

        logger.info(
            f"State Context Length : {len(state.get('retrieved_context', ''))}"
        )

        
        # Store results in graph state
        state["answer"] = result["answer"]
        state["sources"] = result["sources"]
        # Required for Evaluation Agent
        state["retrieved_context"] = result.get("context", "")

        logger.info(f"Sources : {state['sources']}")
        logger.info("========== Multimodal Agent Completed ==========")

        return state

    except Exception as e:

        logger.error(f"Multimodal Agent Error : {e}")

        state["answer"] = "Unable to retrieve information for the uploaded medical image."
        state["sources"] = []

        return state






