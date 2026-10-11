from backend.vector_store import index
from backend.llm_client import client
from backend.MCP.connector import get_db_connection

from backend.monitoring.stats import system_stats


def get_system_health():
    print("Health API id:", id(system_stats))
    print(system_stats)
    

    # ---------------- LLM ----------------

    system_stats["llm"] = client is not None

    # ---------------- Vector DB ----------------

    try:
        system_stats["vectordb"] = True
        system_stats["chunks"] = index.ntotal

    except Exception:

        system_stats["vectordb"] = False
        system_stats["chunks"] = 0

    # ---------------- PostgreSQL ----------------

    try:

        conn = get_db_connection()

        if conn:
            system_stats["postgres"] = True
            conn.close()
        else:
            system_stats["postgres"] = False

    except Exception:

        system_stats["postgres"] = False

    return system_stats




