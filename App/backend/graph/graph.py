"""
---------------------------------------------------------
MediAssist AI - LangGraph Workflow
---------------------------------------------------------
"""

from langgraph.graph import StateGraph, END

from backend.graph.state import MediAssistState
from backend.graph.router import router

from backend.agents.input_guardrails import validate_input
from backend.agents.planner_agent import planner_agent
from backend.agents.retriever_agent import retriever_agent
from backend.agents.multimodal_agent import multimodal_agent
from backend.agents.mcp_agent import mcp_agent
from backend.agents.reasoning_agent import reasoning_agent
from backend.evaluation.evaluation_agent import evaluation_agent      # <-- NEW
from backend.agents.output_guardrail import output_guardrail


# =====================================================
# Create Workflow
# =====================================================

workflow = StateGraph(MediAssistState)


# =====================================================
# Add Nodes
# =====================================================

workflow.add_node("input_guardrail", validate_input)

workflow.add_node("planner", planner_agent)

workflow.add_node("retriever", retriever_agent)

workflow.add_node("multimodal", multimodal_agent)

workflow.add_node("mcp", mcp_agent)

workflow.add_node("reasoning", reasoning_agent)

workflow.add_node("evaluation", evaluation_agent)                 # <-- NEW

workflow.add_node("output_guardrail", output_guardrail)


# =====================================================
# Entry Point
# =====================================================

workflow.set_entry_point("input_guardrail")


# =====================================================
# Fixed Edges
# =====================================================

#workflow.add_edge("input_guardrail", "planner")


# =====================================================
# Conditional Routing
# =====================================================
def guardrail_router(state):
    if state["is_valid"]:
        return "planner"
    return "end"

workflow.add_conditional_edges(
    "input_guardrail",
    guardrail_router,
    {
        "planner": "planner",
        "end": END,
    }
)
workflow.add_conditional_edges(
    "planner",
    router,
    {
        "rag": "retriever",
        "multimodal": "multimodal",
        "mcp": "mcp",
    },
)


# =====================================================
# Agent → Reasoning
# =====================================================

workflow.add_edge("retriever", "reasoning")

workflow.add_edge("multimodal", "reasoning")

workflow.add_edge("mcp", "reasoning")


# =====================================================
# Reasoning → Evaluation
# =====================================================

workflow.add_edge("reasoning", "evaluation")


# =====================================================
# Evaluation → Output Guardrail
# =====================================================

workflow.add_edge("evaluation", "output_guardrail")


# =====================================================
# End
# =====================================================

workflow.add_edge("output_guardrail", END)


# =====================================================
# Compile Graph
# =====================================================

app_graph = workflow.compile()








# """
# ---------------------------------------------------------
# MediAssist AI - LangGraph Workflow
# ---------------------------------------------------------
# """

# from langgraph.graph import StateGraph, END

# from backend.graph.state import MediAssistState
# from backend.graph.router import router

# from backend.agents.input_guardrails import validate_input
# from backend.agents.planner_agent import planner_agent
# from backend.agents.retriever_agent import retriever_agent
# from backend.agents.multimodal_agent import multimodal_agent
# from backend.agents.mcp_agent import mcp_agent
# from backend.agents.reasoning_agent import reasoning_agent
# from backend.agents.output_guardrail import output_guardrail


# # =====================================================
# # Create Workflow
# # =====================================================

# workflow = StateGraph(MediAssistState)


# # =====================================================
# # Add Nodes
# # =====================================================

# workflow.add_node("input_guardrail", validate_input)

# workflow.add_node("planner", planner_agent)

# workflow.add_node("retriever", retriever_agent)

# workflow.add_node("multimodal", multimodal_agent)

# workflow.add_node("mcp", mcp_agent)

# workflow.add_node("reasoning", reasoning_agent)

# workflow.add_node("output_guardrail", output_guardrail)


# # =====================================================
# # Entry Point
# # =====================================================

# workflow.set_entry_point("input_guardrail")


# # =====================================================
# # Fixed Edges
# # =====================================================

# workflow.add_edge("input_guardrail", "planner")


# # =====================================================
# # Conditional Routing
# # =====================================================

# workflow.add_conditional_edges(
#     "planner",
#     router,
#     {
#         "rag": "retriever",
#         "multimodal": "multimodal",
#         "mcp": "mcp",
#     },
# )


# # =====================================================
# # All Agents → Reasoning
# # =====================================================

# workflow.add_edge("retriever", "reasoning")

# workflow.add_edge("multimodal", "reasoning")

# workflow.add_edge("mcp", "reasoning")


# # =====================================================
# # Reasoning → Output Guardrail
# # =====================================================

# workflow.add_edge("reasoning", "output_guardrail")


# # =====================================================
# # End
# # =====================================================

# workflow.add_edge("output_guardrail", END)


# # =====================================================
# # Compile Graph
# # =====================================================

# app_graph = workflow.compile()