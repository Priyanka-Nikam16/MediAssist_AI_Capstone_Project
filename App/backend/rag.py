import os
from urllib import response
from dotenv import load_dotenv
import re
from backend.agents.prompts import RETRIEVER_PROMPT
from backend.app_logs.logger import logger
# print("RAG LOGGER:", logger)
# print("RAG HANDLERS:", logger.handlers)
from collections import Counter
from backend.monitoring.stats import system_stats
# Document loaders
from langchain_community.document_loaders import PyPDFLoader,TextLoader, Docx2txtLoader, CSVLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.llm_client import client, MODEL_NAME

# Vector store functions
from backend.vector_store import (
    create_embeddings,
    store_embeddings,
    search_similar_chunks,
    save_index_and_chunks,
    extract_filename
)

# For image processing 
from backend.multimodal.image_processor import process_medical_image


logger.info("RAG Module Loaded.")
##----------------------------for multimodel---------

def load_files(file_paths):

    logger.info("========== Document Loading Started ==========")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    total_chunks = 0

    for file_path in file_paths:
        logger.info(f"Loading File : {os.path.basename(file_path)}")
        ext = os.path.splitext(file_path)[1].lower()

        # -----------------------------------
        # Decide file type
        # -----------------------------------

        if ext in [".jpg", ".jpeg", ".png"]:
            file_type = "medical_image"
        else:
            file_type = "document"

        # -----------------------------------
        # Load documents
        # -----------------------------------

        if ext == ".pdf":

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_type"] = file_type

        elif ext == ".txt":

            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_type"] = file_type

        elif ext == ".docx":

            loader = Docx2txtLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_type"] = file_type

        elif ext == ".csv":

            loader = CSVLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_type"] = file_type

        elif ext in [".jpg", ".jpeg", ".png"]:

            processed = process_medical_image(file_path)

            logger.info(f"Processing Medical Image : {os.path.basename(file_path)}")
            logger.info(f"Processed Image : {processed}")

            ocr_text = processed.get("ocr_text", "")
            final_report = processed.get("final_report", "")

            if not ocr_text and not final_report:
                logger.info(f"No information extracted from {file_path}")
                continue

            combined_text = f"""
        OCR TEXT
        -----------------
        {ocr_text}

        ==================================================

        AI SUMMARY
        -----------------
        {final_report}
        """

            docs = [
                Document(
                    page_content=combined_text,
                    metadata={
                        "source": processed["file_name"],
                        "file_type": file_type
                    }
                )
            ]

        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # -----------------------------------
        # Chunking
        # -----------------------------------

        chunks = text_splitter.split_documents(docs)

        text_chunks = [
            chunk.page_content
            for chunk in chunks
        ]

        if not text_chunks:
            continue

        # -----------------------------------
        # Embeddings
        # -----------------------------------

        embeddings = create_embeddings(text_chunks)

        # -----------------------------------
        # Store in FAISS
        # -----------------------------------

        store_embeddings(
            file_name=os.path.basename(file_path),
            text_chunks=text_chunks,
            embeddings=embeddings,
            file_type=file_type
        )

        total_chunks += len(text_chunks)

        logger.info(
            f"{os.path.basename(file_path)} stored successfully "
            f"({len(text_chunks)} chunks)"
)

    return total_chunks
#----------


def answer_from_rag(question):
    """
    Retrieve relevant document chunks and generate answer.
    """

    logger.info("=" * 60)
    logger.info("========== RAG Pipeline Started ==========")
    logger.info(f"Question : {question}")

    try:

        # -------------------------------------------------
        # STEP 1 : Extract filename
        # -------------------------------------------------

        logger.info("STEP 1 : Extracting filename...")

        file_name = extract_filename(question)

        if file_name:
            logger.info(f"File Filter : {file_name}")
        else:
            logger.info("No filename detected. Searching all uploaded documents.")

        # -------------------------------------------------
        # STEP 2 : Search FAISS
        # -------------------------------------------------

        logger.info("STEP 2 : Searching FAISS...")

        retrieved_chunks = search_similar_chunks(
            question=question,
            file_name=file_name
        )

        logger.info("STEP 2 Completed")

        if retrieved_chunks is None:

            logger.warning("search_similar_chunks() returned None")

            return {
                "answer": "Unable to retrieve documents.",
                "context": "",
                "sources": []
            }

        logger.info(f"Retrieved {len(retrieved_chunks)} chunk(s).")

        

        # -------------------------------------------------
        # STEP 2.5 : Keep chunks from dominant file
        # -------------------------------------------------

        if not file_name and len(retrieved_chunks) > 1:

            file_counts = Counter(
                chunk["file_name"]
                for chunk in retrieved_chunks
                if chunk.get("file_name")
            )

            dominant_file = file_counts.most_common(1)[0][0]

            logger.info(f"Dominant File : {dominant_file}")

            retrieved_chunks = [
                chunk
                for chunk in retrieved_chunks
                if chunk["file_name"] == dominant_file
            ]

            logger.info(
                f"Chunks after filtering : {len(retrieved_chunks)}"
            )


        
        
        # -------------------------------------------------
        # STEP 3 : No chunks found
        # -------------------------------------------------

        if len(retrieved_chunks) == 0:

            logger.warning("No relevant chunks found.")

            return {
                "answer": "Sorry, I couldn't find the answer in the uploaded documents.",
                "context": "",
                "sources": []
            }

        # -------------------------------------------------
        # STEP 4 : Prepare context
        # -------------------------------------------------

        logger.info("STEP 3 : Preparing context...")

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        logger.info(f"Context Length : {len(context)} characters")

        # -------------------------------------------------
        # STEP 5 : Collect sources
        # -------------------------------------------------

        sources = list({
            chunk["file_name"]
            for chunk in retrieved_chunks
            if chunk.get("file_name")
        })

        logger.info(f"Sources : {sources}")

        # -------------------------------------------------
        # STEP 6 : Create prompt
        # -------------------------------------------------

        logger.info("STEP 4 : Creating prompt...")

        prompt = (
            RETRIEVER_PROMPT
            .replace("<<CONTEXT>>", context)
            .replace("<<QUESTION>>", question)
        )

        logger.info("Prompt created successfully.")

        # -------------------------------------------------
        # STEP 7 : Call LLM
        # -------------------------------------------------

        logger.info("STEP 5 : Calling Groq LLM...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
        print(response)
        print(response.usage)
        usage = response.usage
        system_stats["llm"] = True
        print("RAG id:", id(system_stats))
        print(system_stats)
        system_stats["prompt_tokens"] += usage.prompt_tokens
        system_stats["completion_tokens"] += usage.completion_tokens
        system_stats["total_tokens"] += usage.total_tokens

        INPUT_PRICE = 0.59
        OUTPUT_PRICE = 0.79

        cost = (
            usage.prompt_tokens / 1_000_000
        ) * INPUT_PRICE + (
            usage.completion_tokens / 1_000_000
        ) * OUTPUT_PRICE

        system_stats["cost"] += cost
        
        print("RAG stats id:", id(system_stats))
        print("Updated system_stats:", system_stats)
        
        logger.info("LLM call completed.")

        answer = response.choices[0].message.content.strip()

        logger.info("Answer generated successfully.")

        logger.info("=" * 60)
        logger.info("========== RAG Pipeline Completed ==========")
        logger.info("=" * 60)

        # -------------------------------------------------
        # Return everything needed by graph + evaluation
        # -------------------------------------------------

        return {
            "answer": answer,
            "context": context,
            "sources": sources
        }

    except Exception as e:

        logger.exception(f"RAG Pipeline Error : {e}")

        return {
            "answer": "Unable to retrieve information due to an internal error.",
            "context": "",
            "sources": []
        }



