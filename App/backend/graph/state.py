"""
---------------------------------------------------------
Shared State for MediAssist LangGraph
---------------------------------------------------------
"""

from typing import TypedDict, Optional


class MediAssistState(TypedDict):

    # -------------------------------------------------
    # User Input
    # -------------------------------------------------

    question: str
    file_path: Optional[str]
    file_type: Optional[str]
    uploaded_files: dict

    # -------------------------------------------------
    # Input Guardrails
    # -------------------------------------------------

    is_valid: bool
    error_type: Optional[str]

    # -------------------------------------------------
    # Planner Output
    # -------------------------------------------------

    route: Optional[str]

    # -------------------------------------------------
    # Agent Outputs
    # -------------------------------------------------

    retrieved_context: Optional[str]
    context: Optional[str]          # <-- Added

    image_analysis: Optional[str]
    mcp_result: Optional[str]

    # -------------------------------------------------
    # Final Response
    # -------------------------------------------------

    answer: Optional[str]
    sources: list

    # -------------------------------------------------
    # Evaluation
    # -------------------------------------------------

    evaluation: Optional[dict]      # <-- Added




# """
# Shared State for MediAssist LangGraph
# """

# from typing import TypedDict, Optional


# class MediAssistState(TypedDict):

#     # User Input
#     question: str
#     file_path: Optional[str]
#     file_type: Optional[str]
#     uploaded_files: dict

#     # Input Guardrails
#     is_valid: bool
#     error_type: Optional[str]

#     # Planner Output
#     route: Optional[str]
    

#     # Agent Outputs
#     retrieved_context: Optional[str]
#     image_analysis: Optional[str]
#     mcp_result: Optional[str]

#     # Final Response
#     answer: Optional[str]
#     sources: list

    