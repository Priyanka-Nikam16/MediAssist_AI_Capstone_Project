from backend.app_logs.logger import logger
from backend.evaluation.judge import evaluate_answer
from backend.evaluation.metrics import calculate_overall_score

import csv
from pathlib import Path
from datetime import datetime
from backend.monitoring.stats import system_stats

RESULT_PATH = Path(__file__).parent.parent / "evaluation" / "results.csv"


def evaluation_agent(state):

    logger.info("========== Evaluation Agent Started ==========")

    try:
        logger.info(
         f"Evaluation Context Length : {len(state.get('retrieved_context', ''))}"
        )
        evaluation = evaluate_answer(
            question=state.get("question", ""),
            context=state.get("retrieved_context", ""),
            generated_answer=state.get("answer", "")
        )

        overall = calculate_overall_score(evaluation)

        logger.info(f"Overall Score : {overall}")

        state["evaluation"] = evaluation

        # ---------------- Update System Health Dashboard ----------------

        system_stats["faithfulness"] = evaluation["faithfulness"]["score"]
        system_stats["grounding"] = evaluation["grounding"]["score"]
        system_stats["relevance"] = evaluation["relevance"]["score"]
        system_stats["completeness"] = evaluation["completeness"]["score"]
        system_stats["hallucination"] = evaluation["hallucination"]["score"]
        system_stats["overall_score"] = overall

        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": state.get("question", ""),
            "route": state.get("route", ""),
            "sources": ", ".join(state.get("sources", [])),
            "faithfulness": evaluation["faithfulness"]["score"],
            "grounding": evaluation["grounding"]["score"],
            "relevance": evaluation["relevance"]["score"],
            "completeness": evaluation["completeness"]["score"],
            "hallucination": evaluation["hallucination"]["score"],
            "overall_score": overall,
            "answer": state.get("answer", "")
        }

        file_exists = RESULT_PATH.exists()

        with open(RESULT_PATH, "a", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(
                f,
                fieldnames=row.keys()
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)

        logger.info("Evaluation CSV Updated")

    except Exception as e:

        logger.error(f"Evaluation Agent Error : {e}")

        state["evaluation"] = {}

    logger.info("========== Evaluation Agent Completed ==========")

    return state

# import json
# import time
# import csv
# from pathlib import Path

# from backend.graph.graph import app_graph
# from backend.evaluation.judge import evaluate_answer
# from backend.evaluation.metrics import calculate_overall_score
# from backend.app_logs.logger import logger


# # ---------------------------
# # Load Dataset
# # ---------------------------
# BASE_DIR = Path(__file__).parent
# dataset_path = BASE_DIR / "golden_dataset.json"

# with open(dataset_path, "r", encoding="utf-8") as f:
#     golden_dataset = json.load(f)

# logger.info("Golden Dataset Loaded Successfully.")


# results = []

# # ---------------------------
# # Evaluation Loop
# # ---------------------------
# for sample in golden_dataset:

#     question = sample["question"]

#     logger.info("=" * 60)
#     logger.info(f"Question : {question}")

#     start = time.time()

#     # ---------------------------
#     # Run LangGraph
#     # ---------------------------
#     state = app_graph.invoke({
#         "question": question,
#         "file_path": None,
#         "file_type": None,
#         "uploaded_files": {}
#     })

#     response_time = round(time.time() - start, 2)

#     logger.info("LangGraph Execution Completed.")

#     generated_answer = state.get("answer", "")
#     retrieved_context = state.get("retrieved_context", "")
#     actual_route = state.get("route", "")
#     actual_sources = state.get("sources", [])

#     # ---------------------------
#     # LLM Judge
#     # ---------------------------
#     logger.info("Running LLM Judge...")

#     evaluation = evaluate_answer(
#         question=question,
#         context=retrieved_context,
#         generated_answer=generated_answer,
#         golden_answer=sample["golden_answer"]
#     )

#     # ---------------------------
#     # SAFE evaluation handling
#     # ---------------------------
#     def safe_get(metric):
#         return evaluation.get(metric, {}).get("score", 0)

#     overall_score = calculate_overall_score(evaluation)

#     logger.info(f"Overall Score : {overall_score}")

#     results.append({
#         "id": sample["id"],
#         "question": question,
#         "expected_route": sample["expected_route"],
#         "actual_route": actual_route,
#         "expected_source": sample["expected_source"],
#         "actual_sources": ", ".join(actual_sources) if isinstance(actual_sources, list) else str(actual_sources),
#         "response_time": response_time,

#         "faithfulness": safe_get("faithfulness"),
#         "grounding": safe_get("grounding"),
#         "relevance": safe_get("relevance"),
#         "completeness": safe_get("completeness"),
#         "hallucination": safe_get("hallucination"),

#         "overall_score": overall_score,
#         "generated_answer": generated_answer,
#         "golden_answer": sample["golden_answer"]
#     })


# # ---------------------------
# # Save CSV Safely
# # ---------------------------
# RESULT_PATH = Path(__file__).parent / "results.csv"

# if results:   # IMPORTANT safety check
#     with open(RESULT_PATH, "w", encoding="utf-8", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=results[0].keys())
#         writer.writeheader()
#         writer.writerows(results)

#     logger.info("Evaluation Completed Successfully.")
#     logger.info(f"Results saved to {RESULT_PATH}")
# else:
#     logger.warning("No results generated. CSV not created.")