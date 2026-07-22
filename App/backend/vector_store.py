                         
import os
import pickle
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("vector_store.py loaded")

# Embedding Dimension
dimension = 384

# Initialize FAISS index
index = faiss.IndexFlatL2(dimension)

# Store chunks in memory
document_chunks = []

# Paths for saving FAISS index and chunks
STORE_DIR = "store"
INDEX_PATH = os.path.join(STORE_DIR, "faiss_index")
CHUNKS_PATH = os.path.join(STORE_DIR, "chunks.pkl")
os.makedirs(STORE_DIR, exist_ok=True)

def create_embeddings(text_chunks):
    embeddings = embedding_model.encode(text_chunks, show_progress_bar=True)
    return np.array(embeddings).astype("float32")

def store_embeddings(file_name,text_chunks, embeddings,file_type):
    
    global index, document_chunks 
    #It ensures all functions use and modify the SAME FAISS index 
    # and chunk memory instead of creating local copies.

    index.add(embeddings)
    for i,chunk in enumerate(text_chunks):
        document_chunks.append({
    "text": chunk,
    "file_name": file_name,   # pass the file name when loading
    "chunk_id": i,
    "file_type": file_type
   
})
    print(f"Added {len(text_chunks)} chunks from {file_name}")
    save_index_and_chunks()



def save_index_and_chunks():
    """Persist FAISS index and chunks to disk."""
    print("Saving index...")
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(document_chunks, f)
    print(f"Index and {len(document_chunks)} chunks saved to '{STORE_DIR}'")

def load_index_and_chunks():
    """Reload FAISS index and chunks from disk."""
    loaded_index = faiss.read_index(INDEX_PATH)
    
    with open(CHUNKS_PATH, "rb") as f:
        loaded_chunks = pickle.load(f)
    
    print(f"Loaded {len(loaded_chunks)} chunks from '{STORE_DIR}'")
    
    print("First chunk type:", type(loaded_chunks[0]))
    print("First chunk:", loaded_chunks[0])

    return loaded_index, loaded_chunks

# Load existing index if available
if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    index, document_chunks = load_index_and_chunks()

#check file name in question before searching so nother chunks,s file name will 
# appear in sources
def extract_filename(question):
    match = re.search(r'[\w\-.]+\.(png|jpg|jpeg|pdf|docx|csv|txt)', question, re.I)
    return match.group(0) if match else None


def search_similar_chunks(question, k=10, file_name=None):

    if len(document_chunks) == 0:
        return [{"text": "No document uploaded yet", "file_name": None}]

    question_embedding = embedding_model.encode([question])

    distances, indices = index.search(
        np.array(question_embedding).astype("float32"),
        k=k
    )

    retrieved = []

    for i in indices[0]:
        if i == -1:
            continue

        chunk = document_chunks[i]

        if file_name:
            if chunk["file_name"].lower() != file_name.lower():
                continue

        retrieved.append(chunk)

    return retrieved



