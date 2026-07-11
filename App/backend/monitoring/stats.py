system_stats = {

    # Connection Status
    "llm": False,
    "vectordb": False,
    "postgres": False,

    # Token Usage
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "cost": 0.0,

    # Evaluation
    "faithfulness": 0,
    "grounding": 0,
    "relevance": 0,
    "completeness": 0,
    "hallucination": 0,
    "overall_score": 0

}

print("stats.py id:", id(system_stats))