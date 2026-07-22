"""
---------------------------------------------------------
MediAssist AI - MCP Agent
---------------------------------------------------------

Purpose
-------
1. Handle database/tool related queries.
2. Call appropriate MCP tools.
3. Store answer and sources in graph state.
---------------------------------------------------------
"""

from backend.app_logs.logger import logger

from backend.MCP.tools import (
    Search_patients,
    Get_patient_history,
    Get_lab_results,
    Get_payment_summary
)

from backend.MCP.db_utils import (
    extract_patient_id,
    format_records
)


def mcp_agent(state):
    """
    Executes MCP database tools.
    """

    logger.info("========== MCP Agent Started ==========")

    try:

        question = state["question"]
        logger.info(f"Question : {question}")

        q = question.lower()

        # -------------------------------
        # Search Patient
        # -------------------------------
        if "search patient" in q or "find patient" in q:

            logger.info("Calling Search_patients()")

            name = (
                q.replace("search patient", "")
                 .replace("find patient", "")
                 .strip()
            )

            records = Search_patients(name)

            state["answer"] = format_records(records)
            state["sources"] = ["Patient Database"]

        # -------------------------------
        # Patient History
        # -------------------------------
        elif "patient history" in q or "medical history" in q:

            logger.info("Calling Get_patient_history()")

            patient_id = extract_patient_id(question)

            if patient_id is None:

                state["answer"] = (
                    "Please provide patient ID.\n"
                    "Example: Get patient history 15"
                )
                state["sources"] = ["Patient History Database"]

                return state

            records = Get_patient_history(patient_id)

            state["answer"] = format_records(records)
            state["sources"] = ["Patient History Database"]

        # -------------------------------
        # Lab Results
        # -------------------------------
        elif (
            "lab result" in q
            or "lab results" in q
            or "test result" in q
            or "lab report" in q
            or "lab reports" in q
        ):

            logger.info("Calling Get_lab_results()")

            patient_id = extract_patient_id(question)

            if patient_id is None:

                state["answer"] = (
                    "Please provide patient ID.\n"
                    "Example: Get lab results 15"
                )
                state["sources"] = ["Laboratory Database"]

                return state

            records = Get_lab_results(patient_id)

            state["answer"] = format_records(records)
            state["sources"] = ["Laboratory Database"]

        # -------------------------------
        # Payment Summary
        # -------------------------------
        elif (
            "payment summary" in q
            or "billing summary" in q
            or "bill summary" in q
        ):

            logger.info("Calling Get_payment_summary()")

            patient_id = extract_patient_id(question)

            if patient_id is None:

                state["answer"] = (
                    "Please provide patient ID.\n"
                    "Example: Get payment summary 15"
                )
                state["sources"] = ["Billing Database"]

                return state

            records = Get_payment_summary(patient_id)

            state["answer"] = format_records(records)
            state["sources"] = ["Billing Database"]

        # -------------------------------
        # Unknown query
        # -------------------------------
        else:

            logger.warning("No matching MCP tool found.")

            state["answer"] = (
                "Unable to identify the requested database operation."
            )

            state["sources"] = []

        logger.info(f"Sources : {state['sources']}")
        logger.info("========== MCP Agent Completed ==========")

        return state

    except Exception as e:

        logger.error(f"MCP Agent Error : {e}")

        state["answer"] = "Unable to retrieve lab results."

        state["retrieved_context"] = ""

        state["sources"] = []

        return state