"""
---------------------------------------------------------
MediAssist AI - Retriever Agent
---------------------------------------------------------

Purpose
-------
1. Retrieve relevant document chunks.
2. Generate answer using RAG.
3. Store answer, retrieved context and sources in graph state.
---------------------------------------------------------
"""

from backend.app_logs.logger import logger

print("RETRIEVER LOGGER:", logger)
print("RETRIEVER HANDLERS:", logger.handlers)

from backend.rag import answer_from_rag


def retriever_agent(state):
    """
    Answer questions using uploaded documents.
    """

    print("====== Retriever Agent Started ======")

    logger.info("========== Retriever Agent Started ==========")

    try:

        question = state["question"]

        logger.info(f"Question : {question}")
        logger.info("Calling RAG...")

        # ----------------------------------------
        # Call RAG Pipeline
        # ----------------------------------------

        result = answer_from_rag(question)

        # ----------------------------------------
        # Store Answer
        # ----------------------------------------

        state["answer"] = result.get("answer", "")

        # ----------------------------------------
        # Store Retrieved Context
        # (Required for Evaluation Agent)
        # ----------------------------------------

        state["retrieved_context"] = result.get("context", "")
        state["context"] = result.get("context", "")

        # ----------------------------------------
        # Store Sources
        # ----------------------------------------

        state["sources"] = result.get("sources", [])

        logger.info(f"Retrieved Context Length : {len(state['retrieved_context'])}")
        logger.info(f"Sources : {state['sources']}")
        logger.info("========== Retriever Agent Completed ==========")

        return state

    except Exception as e:

        logger.error(f"Retriever Agent Error : {e}")

        state["answer"] = "Unable to retrieve information from uploaded documents."
        state["retrieved_context"] = ""
        state["context"] = ""
        state["sources"] = []

        return state







