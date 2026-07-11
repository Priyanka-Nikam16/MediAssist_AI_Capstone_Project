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
