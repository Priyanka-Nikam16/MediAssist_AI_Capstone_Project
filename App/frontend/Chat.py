import streamlit as st
import requests
import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://host.docker.internal:8000"
)
#BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")  # use full width

st.markdown(
    """
    <div style="
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        ">
        <div style="
            width: 100%;
            border: 2px solid grey;
            padding: 5px 10px;
            background-color: rgba(255, 255, 255, 0.0);
            border-radius: 8px;
            text-align: center;
            ">
            <h2 style="text-align: center; color: white;">MediAssist AI</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()
# --- Initialize state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []




# --- Layout: 3 columns ---
#left_col, middle_col, right_col = st.columns([3, 3, 2])  # adjust ratios
left_col, spacer1, middle_col, spacer2, right_col = st.columns([3, 0.3, 3, 0.3, 3])
# Custom CSS for expander header
st.markdown(
    """
    <style>
    .streamlit-expanderHeader {
        background-color: #2d2d30;   /* Dark background */
        color: #f5f5f5;              /* Light text */
        font-weight: bold;           /* Bold title */
        border: 1px solid grey;      /* Border around header */
        border-radius: 5px;          /* Rounded corners */
        padding: 8px;                /* Spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
)

#css for left col box
# ================= LEFT SECTION =================

# Give uploader a key to evrytime clear the uploader after uploading
uploader_key = "file_uploader"

with left_col:
    # if st.button("🩺 System Health", use_container_width=True):
    #     st.switch_page("pages/System_Health_Dashboard.py")
    
    with st.expander("📂 Upload & Documents", expanded=False):
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload PDF, TXT, DOCX, CSV, or Images",
            type=["pdf", "txt", "docx", "csv", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key=st.session_state.get("uploader_key", "file_uploader")
        )

        if uploaded_files:
            files = [("files", (f.name, f.getvalue(), "application/octet-stream")) for f in uploaded_files]
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.success(data["message"])

            st.session_state.uploaded_files.extend(uploaded_files)
            # 🔑 Reset uploader by changing its key
            st.session_state["uploader_key"] = f"file_uploader_{len(st.session_state.uploaded_files)}"
            #st.rerun()
        st.divider()

        # Uploaded file list
        st.markdown("📂 Uploaded Files")
        res = requests.get(f"{BACKEND_URL}/files")
        data = res.json()

        if "error" in data:
            st.error(data["error"])
        elif data.get("files"):
            st.caption(f"Total Files: {len(data['files'])}")

            for file_name in data["files"]:
                row = st.container(border=True)
                with row:
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.write(f"📄 {file_name}")
                    with col2:
                        if st.button("✖", key=f"delete_{file_name}"):
                            st.session_state["pending_delete"] = file_name
        else:
            st.info("No documents uploaded yet.")
  
        # Confirmation popup inside expander
        if "pending_delete" in st.session_state:
            file_to_delete = st.session_state["pending_delete"]
            st.warning(f"Are you sure you want to delete: {file_to_delete}?")

            colA, colB = st.columns(2)
            with colA:
                if st.button("✅ Yes, delete", key="confirm_delete"):
                    delete_res = requests.delete(f"{BACKEND_URL}/delete/{file_to_delete}")
                    delete_data = delete_res.json()
                    if "error" in delete_data:
                        st.error(delete_data["error"])
                    else:
                        st.success(delete_data["message"])
                    del st.session_state["pending_delete"]
                    st.rerun()
            with colB:
                if st.button("❌ Cancel", key="cancel_delete"):
                    del st.session_state["pending_delete"]
       

   
# ================= MIDDLE SECTION =================
with middle_col:
    st.markdown("### ❓ Ask a Question")
    question = st.text_input("Enter your question:")

    if st.button("Ask"):
        print("=" * 50)
        print("Sending question to backend")
        print("Question:", question)
        print("Backend URL:", f"{BACKEND_URL}/ask")
        print("=" * 50)
        response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
        data = response.json()
        #st.write("debug ans:",data)
        #Extract answer and sources
        answer = data.get("answer", "")
        sources = data.get("sources", [])
        
        st.markdown("### 📝 Answer")
        st.write(answer)
        if sources:
            st.markdown("**Sources:** " + ", ".join(sources))

        # Store history
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })
        st.session_state.chat_history.append({"role": "assistant","content": answer,"sources": sources})
        #st.write("debug:", st.session_state.chat_history)
# ================= RIGHT SECTION =================
with right_col:
    st.subheader(" 💬 Conversation History")
 
# Build one transparent box with border
    conversation_html = """
    <div style='background-color:transparent; color:#f5f5f5;
                padding:15px; border-radius:10px; border:2px solid #444;
                max-height:400px; overflow-y:auto;'>
    """

    # Take last 20 messages
    recent_history = st.session_state.chat_history[-20:]

    # Group into Q&A pairs
    pairs = []
    for i in range(0, len(recent_history), 2):
        if i+1 < len(recent_history):
            q = recent_history[i]["content"]
            a = recent_history[i+1]["content"]
            sources=recent_history[i+1].get("sources",[])
            pairs.append((q, a,sources))

    # Reverse so latest pair comes first
    pairs = list(reversed(pairs))

    # Number newest as 1, then increase
    for idx, entry in enumerate(pairs, start=1):
        q, a, sources = entry
        conversation_html += f"<p><b>{idx}. Que:</b> {q}<br><b>Ans:</b> {a}"
        if sources:
            conversation_html += f"<br><b>Sources:</b> {', '.join(sources)}"
        conversation_html += "</p>"
    conversation_html += "</div>"

    st.markdown(conversation_html, unsafe_allow_html=True)

