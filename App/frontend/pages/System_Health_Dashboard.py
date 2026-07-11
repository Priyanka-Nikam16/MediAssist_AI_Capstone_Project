import streamlit as st
import requests
import os
#BACKEND_URL = "http://127.0.0.1:8000"


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://host.docker.internal:8000"
)

st.set_page_config(
    page_title="System Health Dashboard",
    layout="wide"
)

st.title("🩺 MediAssist AI - System Health Dashboard")

st.divider()

# -----------------------------
# Get Health Data
# -----------------------------

try:
    response = requests.get(f"{BACKEND_URL}/system-health")
    
    #print(response.text)
    stats = response.json()
    #st.write(stats)

    #print(response.json())
    #st.write(response.json())
    
    data = response.json()

except Exception:
    data = {}

left, right = st.columns(2)

# ==================================================
# LEFT BOX
# ==================================================

with left:

    st.subheader("System Health")

    if data.get("llm"):
        st.success("🟢 LLM Connected")
    else:
        st.error("🔴 LLM Disconnected")

    if data.get("vectordb"):
        st.success("🟢 Vector DB Connected")
    else:
        st.error("🔴 Vector DB Disconnected")

    if data.get("postgres"):
        st.success("🟢 PostgreSQL Connected")
    else:
        st.error("🔴 PostgreSQL Disconnected")

    st.info(f"Indexed Chunks : {data.get('chunks',0)}")

# ==================================================
# RIGHT BOX
# ==================================================

with right:

    st.subheader("Token Usage")

    st.metric(
        "Prompt Tokens",
        data.get("prompt_tokens",0)
    )

    st.metric(
        "Completion Tokens",
        data.get("completion_tokens",0)
    )

    st.metric(
        "Total Tokens",
        data.get("total_tokens",0)
    )

    st.metric(
        "Cost ($)",
        f"{data.get('cost',0):.6f}"
    )

st.divider()

# ==================================================
# Evaluation
# ==================================================

st.subheader("Latest Evaluation")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Faithfulness",
    data.get("faithfulness",0)
)

col2.metric(
    "Grounding",
    data.get("grounding",0)
)

col3.metric(
    "Relevance",
    data.get("relevance",0)
)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Completeness",
    data.get("completeness",0)
)

col2.metric(
    "Hallucination",
    data.get("hallucination",0)
)

col3.metric(
    "Overall Score",
    data.get("overall_score",0)
)





# import streamlit as st

# st.set_page_config(page_title="System Health", layout="wide")

# st.title("🩺 MediAssist AI - System Health")

# # if st.button("⬅ Back to Chat"):
# #     st.switch_page("chat.py")

# st.divider()

# left, right = st.columns(2)

# # -------------------------
# # System Health Box
# # -------------------------
# with left:

#     st.subheader("System Health")

#     st.success("🟢 LLM Connected")
#     st.success("🟢 Vector DB Connected")
#     st.success("🟢 PostgreSQL Connected")

# # -------------------------
# # Tokens Box
# # -------------------------
# with right:

#     st.subheader("Token Usage")

#     st.metric("Prompt Tokens", "0")
#     st.metric("Completion Tokens", "0")
#     st.metric("Total Tokens", "0")
#     st.metric("Cost", "$0.0000")