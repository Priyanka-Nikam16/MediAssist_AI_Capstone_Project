"""
---------------------------------------------------------
Evaluation Metrics
---------------------------------------------------------
Calculates the overall evaluation score.
---------------------------------------------------------
"""


def calculate_overall_score(evaluation):
    """
    Calculate the average score of all evaluation metrics.
    """

    scores = [
        evaluation["faithfulness"]["score"],
        evaluation["grounding"]["score"],
        evaluation["relevance"]["score"],
        evaluation["completeness"]["score"],
        evaluation["hallucination"]["score"]
    ]

    overall_score = round(sum(scores) / len(scores), 2)

    return overall_score