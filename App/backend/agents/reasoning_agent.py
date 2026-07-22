
"""
---------------------------------------------------------
MediAssist AI - Reasoning Agent
---------------------------------------------------------

Purpose
-------
1. Receive answer from previous agent.
2. Improve readability and formatting.
3. Generate the final user response.
---------------------------------------------------------
"""

from backend.app_logs.logger import logger
from backend.llm_client import client, MODEL_NAME
from backend.agents.prompts import REASONING_PROMPT


def reasoning_agent(state):
    """
    Final response generation agent.
    """

    logger.info("========== Reasoning Agent Started ==========")

    try:

        question = state.get("question", "")
        answer = state.get("answer", "")
        sources = state.get("sources", [])

        logger.info(f"Question : {question}")

        # -------------------------------------------------
        # No answer received from previous agent
        # -------------------------------------------------

        if not answer:

            logger.warning("No answer received from previous agent.")

            state["answer"] = "Sorry, I couldn't find any relevant information."

            logger.info("========== Reasoning Agent Completed ==========")

            return state

        # -------------------------------------------------
        # Create Prompt
        # -------------------------------------------------

        prompt = (
            REASONING_PROMPT
            .replace("<<QUESTION>>", question)
            .replace("<<ANSWER>>", answer)
            .replace("<<SOURCES>>", ", ".join(sources))
        )

        logger.info("Calling LLM for final response...")

        # -------------------------------------------------
        # LLM Call
        # -------------------------------------------------

        try:

            response = client.chat.completions.create(

                model=MODEL_NAME,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0

            )

            final_answer = response.choices[0].message.content.strip()

            state["answer"] = final_answer

            logger.info("Final response generated successfully.")

        except Exception as e:

            logger.error(f"Reasoning LLM Error : {e}")

            logger.info("Using previous agent response.")

            # Keep original answer
            state["answer"] = answer

        logger.info(f"Sources : {sources}")

        logger.info("========== Reasoning Agent Completed ==========")

        logger.info(
        f"Reasoning Context Length : {len(state.get('retrieved_context', ''))}"
        )
        return state

    except Exception as e:

        logger.error(f"Reasoning Agent Error : {e}")

        if not state.get("answer"):
            state["answer"] = "Unable to generate final response."

        return state