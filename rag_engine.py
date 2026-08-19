import os
import json
from pathlib import Path

from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PATHS / CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = str(BASE_DIR / "chroma_db")
CHUNKS_FILE = BASE_DIR / "data" / "chunks.json"

COLLECTION = "nice_cg192_mental_health"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5
SIMILARITY_THRESHOLD = 0.70


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(EMBED_MODEL)

print("Embedding model loaded.")


# ============================================================
# LOAD CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)


# ============================================================
# CREATE / LOAD COLLECTION
# ============================================================

try:

    col = chroma_client.get_collection(
        name=COLLECTION
    )

    print(
        f"Existing Chroma collection loaded: "
        f"{col.count()} chunks"
    )

except Exception:

    print("Chroma collection not found.")
    print("Building collection from chunks.json...")


    if not CHUNKS_FILE.exists():

        raise FileNotFoundError(
            f"Could not find chunks file: {CHUNKS_FILE}"
        )


    # --------------------------------------------------------
    # LOAD CHUNKS
    # --------------------------------------------------------

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)


    print(
        f"Loaded {len(chunks)} chunks."
    )


    # --------------------------------------------------------
    # CREATE COLLECTION
    # --------------------------------------------------------

    col = chroma_client.get_or_create_collection(
        name=COLLECTION,
        metadata={
            "hnsw:space": "cosine"
        }
    )


    # --------------------------------------------------------
    # EMBED CHUNKS
    # --------------------------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True
    )


    # --------------------------------------------------------
    # STORE IN CHROMA
    # --------------------------------------------------------

    BATCH_SIZE = 100

    for start in range(
        0,
        len(chunks),
        BATCH_SIZE
    ):

        batch = chunks[
            start:start + BATCH_SIZE
        ]

        col.add(

            ids=[
                chunk["chunk_id"]
                for chunk in batch
            ],

            documents=[
                chunk["text"]
                for chunk in batch
            ],

            embeddings=[
                embeddings[start + i].tolist()
                for i in range(len(batch))
            ],

            metadatas=[

                {
                    "page_number":
                        chunk["page_number"],

                    "section_number":
                        chunk["section_number"],

                    "section_title":
                        chunk["section_title"],

                    "source":
                        "NICE Mental Health Guideline",

                    "char_count":
                        chunk["char_count"]
                }

                for chunk in batch
            ]
        )


    print(
        f"Chroma collection created with "
        f"{col.count()} chunks."
    )


# ============================================================
# GROQ
# ============================================================

# ============================================================
# GROQ
# ============================================================

try:
    import streamlit as st

    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except Exception:

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured."
    )


client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# RETRIEVAL
# ============================================================

def query(question: str):

    q_vec = model.encode(
        question
    ).tolist()


    results = col.query(

        query_embeddings=[
            q_vec
        ],

        n_results=TOP_K,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )


    best_similarity = 0.0

    ranked = []


    for rank, (
        doc,
        meta,
        dist
    ) in enumerate(

        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ),

        start=1
    ):

        similarity = round(
            1 - dist,
            4
        )


        best_similarity = max(
            best_similarity,
            similarity
        )


        if similarity < SIMILARITY_THRESHOLD:
            continue


        ranked.append({

            "rank":
                rank,

            "chunk_id":
                results["ids"][0][rank - 1],

            "page":
                meta["page_number"],

            "section_number":
                meta["section_number"],

            "section_title":
                meta["section_title"],

            "source":
                meta["source"],

            "similarity":
                similarity,

            "char_count":
                meta["char_count"],

            "text":
                doc
        })


    return ranked, best_similarity


# ============================================================
# GROQ ANSWER
# ============================================================

def generate_answer(
    question: str,
    ranked: list
):

    if not ranked:

        return "", []


    context = "\n\n".join(

        f"[{r['chunk_id']}] {r['text']}"

        for r in ranked
    )


    prompt = f"""
You are a clinical guideline assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- Do not add recommendations that are not explicitly supported
  by the retrieved evidence.
- Keep the answer concise and directly answer the question.
- Cite the relevant chunk IDs using [chunk_id].
- If the context does not contain enough information,
  clearly state that the available evidence is insufficient.

User question:
{question}

Retrieved context:
{context}
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0
    )


    answer = response.choices[0].message.content


    chunk_ids = [

        r["chunk_id"]

        for r in ranked

    ]


    return answer, chunk_ids


# ============================================================
# STREAMLIT FUNCTION
# ============================================================

def retrieve(question: str):

    ranked, best_similarity = query(
        question
    )


    # --------------------------------------------------------
    # REFUSAL
    # --------------------------------------------------------

    if not ranked:

        if best_similarity > 0:

            reason = (

                "The available evidence in this guideline "
                "does not contain information relevant enough "
                "to answer your question reliably "

                f"(best similarity score: "
                f"{best_similarity:.2f}, "

                f"threshold: "
                f"{SIMILARITY_THRESHOLD:.2f})."

            )

        else:

            reason = (

                "The retrieval system returned no relevant "
                "chunks for your question."

            )


        return {

            "refused":
                True,

            "refusal": {

                "reason":
                    reason,

                "next_steps": [

                    "Try rephrasing your question using "
                    "clinical terminology from the guideline.",

                    "Consult the full guideline document "
                    "directly for manual lookup.",

                    "Ask a qualified clinician who can draw "
                    "on sources beyond this document."

                ]

            }

        }


    # --------------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------------

    answer, chunk_ids = generate_answer(

        question,
        ranked

    )


    return {

        "refused":
            False,

        "answer":
            answer,

        "chunk_ids":
            chunk_ids,

        "results":
            ranked

    }