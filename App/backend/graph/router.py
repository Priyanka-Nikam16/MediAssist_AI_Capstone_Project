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







































# """
# ---------------------------------------------------------
# MediAssist AI - Router
# ---------------------------------------------------------

# Purpose
# -------
# Routes the workflow to the correct agent based on
# the Planner Agent's decision.
# ---------------------------------------------------------
# """

# from backend.app_logs.logger import logger


# def router(state):
#     """
#     Decide the next node based on planner route.
#     """

#     logger.info("========== Router Started ==========")

#     route = state["route"]
#     logger.info(f"Router received route: {repr(state['route'])}")
#     #logger.info(f"Planner Route : {route}")

#     if route == "rag":
#         logger.info("Routing to Retriever Agent")
#         return "retriever"

#     elif route == "multimodal":
#         logger.info("Routing to Multimodal Agent")
#         return "multimodal"

#     elif route == "mcp":
#         logger.info("Routing to MCP Agent")
#         return "mcp"

#     logger.warning("Invalid route. Ending workflow.")

#     return "END"