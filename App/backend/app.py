import os
import pickle
import faiss
import numpy as np
import time

from fastapi import FastAPI, UploadFile, File, logger
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

from backend.rag import load_files
from backend.vector_store import CHUNKS_PATH, INDEX_PATH
from backend.graph.graph import app_graph

from backend.app_logs.logger import logger
from backend.monitoring.system_health import get_system_health
from backend.monitoring.stats import system_stats
# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)

print("APP STARTING...")
print(f"Upload directory '{UPLOAD_DIR}' is ready.")


# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to MediAssist AI"
    }


# ==========================================================
# Upload Files
# ==========================================================

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):

    try:

        file_paths = []

        for file in files:

            file_path = os.path.join(UPLOAD_DIR, file.filename)

            if os.path.exists(file_path):
                return {
                    "error": f"{file.filename} already exists."
                }

            with open(file_path, "wb") as f:
                f.write(await file.read())

            file_paths.append(file_path)

        chunks_created = load_files(file_paths)

        return {
            "message": "Files uploaded successfully.",
            "chunks_created": chunks_created
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================================================
# List Uploaded Files
# ==========================================================

@app.get("/files")
def list_files():

    return {
        "files": os.listdir(UPLOAD_DIR)
    }


# ==========================================================
# Ask Question (LangGraph)
# ==========================================================

@app.post("/ask")
async def ask(data: dict):
    
    try:

        question = data.get("question")
        logger.info("========== API /ask Called ==========")
        logger.info(f"Question: {question}")
        # if not question:
        #     return {
        #         "error": "Question is required."
        #     }

        file_path = data.get("file_path")
        file_type = data.get("file_type")

        initial_state = {

            "question": question,

            "file_path": file_path,
            "file_type": file_type,

            "is_valid": True,
            "error_type": None,

            "route": None,

            "retrieved_context": None,
            "image_analysis": None,
            "mcp_result": None,

            "answer": None,
            "sources": [],
            "evaluation": {}

        }

        start_time = time.time()
        
        final_state = app_graph.invoke(initial_state)
        
        end_time = time.time()
        system_stats["response_time"] = round(end_time - start_time, 2)
        system_stats["questions_asked"] += 1    
       
        logger.info("Graph execution completed.")
        #logger.info(f"is_valid: {final_state['is_valid']}")
        #logger.info(f"error_type: {final_state['error_type']}")
        logger.info(f"answer: {final_state['answer']}")

        return {

            "answer": final_state["answer"],
            "sources": final_state["sources"]

        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        return {
            "error": str(e)
        }
    logger.info("========== Graph Finished ==========")

# ==========================================================
# Delete File
# ==========================================================

@app.delete("/delete/{filename}")
def delete_file(filename: str):

    try:

        file_path = os.path.join(UPLOAD_DIR, filename)

        file_deleted = False
        chunks_removed = 0

        if os.path.exists(file_path):
            os.remove(file_path)
            file_deleted = True

        if os.path.exists(CHUNKS_PATH):

            with open(CHUNKS_PATH, "rb") as f:
                chunks = pickle.load(f)

            updated_chunks = [
                c for c in chunks
                if c.get("file_name") != filename
            ]

            chunks_removed = len(chunks) - len(updated_chunks)

            with open(CHUNKS_PATH, "wb") as f:
                pickle.dump(updated_chunks, f)

            dim = embedding_model.get_embedding_dimension()

            new_index = faiss.IndexFlatL2(dim)

            if updated_chunks:

                texts = [c["text"] for c in updated_chunks]

                embeddings = embedding_model.encode(texts)
                embeddings = np.array(embeddings).astype("float32")

                new_index.add(embeddings)

            faiss.write_index(new_index, INDEX_PATH)

        if file_deleted:

            return {
                "message": f"{filename} deleted successfully.",
                "chunks_removed": chunks_removed
            }

        return {
            "error": "File not found."
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        return {
            "error": str(e)
        }
@app.get("/system-health")
def system_health():

    return get_system_health()











