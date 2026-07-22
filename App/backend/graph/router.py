"""
---------------------------------------------------------
MediAssist AI - Router
---------------------------------------------------------

Purpose
-------
Routes the workflow to the correct agent based on
the Planner Agent's decision.
---------------------------------------------------------
"""

from backend.app_logs.logger import logger


def router(state):
    """
    Return the planner route.
    LangGraph will map it to the correct node.
    """

    logger.info("========== Router Started ==========")

    route = state.get("route")

    logger.info(f"Router received route : {route}")

    if route in ["rag", "multimodal", "mcp"]:
        logger.info(f"Routing using key : {route}")
        return route

    logger.warning(f"Invalid route : {route}")

    return "__end__"






































