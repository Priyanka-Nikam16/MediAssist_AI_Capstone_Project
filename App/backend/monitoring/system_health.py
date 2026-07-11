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





# from backend.vector_store import index
# from backend.llm_client import client
# from backend.MCP.connector import get_db_connection


# def get_system_health():

#     # ---------------- LLM ----------------

#     llm_status = client is not None

#     # ---------------- Vector DB ----------------

#     try:
#         vectordb_status = index.ntotal >= 0
#         total_chunks = index.ntotal
#     except:
#         vectordb_status = False
#         total_chunks = 0

#     # ---------------- PostgreSQL ----------------

#     try:
#         conn = get_db_connection()

#         if conn:
#             postgres_status = True
#             conn.close()
#         else:
#             postgres_status = False

#     except:
#         postgres_status = False

#     # ---------------- Tokens ----------------
#     # Hardcoded for now

#     prompt_tokens = 0
#     completion_tokens = 0

#     total_tokens = prompt_tokens + completion_tokens

#     cost = 0

#     return {

#         "llm": llm_status,

#         "vectordb": vectordb_status,

#         "postgres": postgres_status,

#         "chunks": total_chunks,

#         "prompt_tokens": prompt_tokens,

#         "completion_tokens": completion_tokens,

#         "total_tokens": total_tokens,

#         "cost": cost

#     }



