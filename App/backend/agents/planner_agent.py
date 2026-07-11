
# """
# ---------------------------------------------------------
# MediAssist AI - Planner Agent
# ---------------------------------------------------------

# Purpose
# -------
# 1. Read the user's question.
# 2. Decide which agent(s) should handle it.
# 3. Store the selected route in the state.
# ---------------------------------------------------------
# """

import json
import re

from regex import match

from backend.agents.prompts import PLANNER_PROMPT
from backend.app_logs.logger import logger
from backend.llm_client import client, MODEL_NAME
from backend.monitoring.stats import system_stats

def planner_agent(state):
    """
    Decide which agent(s) should handle the user question.
    """

    logger.info("========== Planner Agent Started ==========")

    # Stop if guardrails failed
    if not state["is_valid"]:
        logger.warning("Input validation failed.")
        return state

    try:
        # User question
        question = state["question"]

        logger.info(f"Question : {question}")

        # Create planner prompt
        prompt = PLANNER_PROMPT.replace("<<QUESTION>>", question)
        logger.info("Calling Groq Planner...")

        # Call LLM
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are the Planner Agent of MediAssist AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
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

        # Get response
        result = response.choices[0].message.content.strip()

        logger.info(f"Planner Response : {result}")
        
        match = re.search(r"\{.*\}", result, re.DOTALL)

        if not match:
            raise ValueError("Planner did not return valid JSON.")

        route = json.loads(match.group())



        # Save route
        state["route"] = route["route"].strip().lower()

        logger.info(f"Selected Route : {state['route']}")

        logger.info("========== Planner Agent Completed ==========")
        
        return state
    
    except Exception as e:

        logger.error(f"Planner Agent Error : {e}")

        print(f"\nPlanner Error: {e}\n")   

        state["route"] = None
        state["answer"] = "Unable to decide the execution route."

        return state
    

# def planner_agent(state):

#     logger.info("========== Planner Agent Started ==========")

#     if not state["is_valid"]:
#         logger.warning("Input validation failed.")
#         return state

#     try:
#         question = state["question"]
#         q = question.lower()

#         logger.info(f"Question: {question}")

#         # -------------------------------------------------
#         # 1. HARD ROUTING LAYER (THIS IS WHAT YOU ARE MISSING)
#         # -------------------------------------------------

#         # MCP ROUTE (highest priority)
#         mcp_keywords = ["patient", "lab", "bill", "billing", "report summary"]
#         if any(k in q for k in mcp_keywords):
#             state["route"] = "mcp"
#             logger.info("Route selected: MCP (rule-based)")
#             return state

#         # MULTIMODAL ROUTE
#         if state.get("has_image", False) or any(x in q for x in ["image", "xray", "mri", "scan"]):
#             state["route"] = "multimodal"
#             logger.info("Route selected: MULTIMODAL (rule-based)")
#             return state

#         # RAG ROUTE (ONLY if PDF exists)
#         if state.get("has_pdf", False):
#             state["route"] = "rag"
#             logger.info("Route selected: RAG (rule-based)")
#             return state

#         # -------------------------------------------------
#         # 2. LLM FALLBACK (ONLY FOR AMBIGUOUS CASES)
#         # -------------------------------------------------

#         prompt = PLANNER_PROMPT.replace("<<QUESTION>>", question)

#         logger.info("Calling LLM Planner...")

#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "Return only JSON: {route: mcp|rag|multimodal|llm}"},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0
#         )

#         result = response.choices[0].message.content.strip()
#         route = json.loads(result)["route"]

#         state["route"] = route

#         logger.info(f"LLM Route selected: {route}")

#         logger.info("========== Planner Agent Completed ==========")

#         return state

#     except Exception as e:
#         logger.error(f"Planner Agent Error: {e}")
#         state["route"] = "llm"
#         state["answer"] = "Unable to decide execution route."
#         return state