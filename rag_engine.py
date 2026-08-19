import os
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq


# Load .env
load_dotenv()


# ============================================================
# CONFIG
# ============================================================

CHROMA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "chroma_db"
)
COLLECTION = "nice_cg192_mental_health"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5
SIMILARITY_THRESHOLD = 0.70


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

model = SentenceTransformer(EMBED_MODEL)


# ============================================================
# LOAD CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

col = chroma_client.get_collection(
    name=COLLECTION
)


# ============================================================
# GROQ
# ============================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# RETRIEVAL
# ============================================================

def query(question: str):

    q_vec = model.encode(question).tolist()

    results = col.query(
        query_embeddings=[q_vec],
        n_results=TOP_K,
        include=[
            "documents",
            "metadatas",
            "distances"
        ],
    )

    best_similarity = 0.0
    ranked = []

    for rank, (doc, meta, dist) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ),
        start=1
    ):

        similarity = round(1 - dist, 4)

        best_similarity = max(
            best_similarity,
            similarity
        )

        if similarity < SIMILARITY_THRESHOLD:
            continue

        ranked.append({
            "rank": rank,
            "chunk_id": results["ids"][0][rank - 1],
            "page": meta["page_number"],
            "section_number": meta["section_number"],
            "section_title": meta["section_title"],

            # Updated document name
            "source": "NICE Pregnant Women Mental Health Guideline",

            "similarity": similarity,
            "char_count": meta["char_count"],
            "text": doc,
        })

    return ranked, best_similarity


# ============================================================
# GROQ ANSWER
# ============================================================

def generate_answer(question: str, ranked: list):

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
- If the context does not contain enough information,
  clearly state that the available evidence is insufficient.
- Cite relevant chunk IDs using [chunk_id].
- Keep the answer concise and directly answer the question.
- Do not mention information that is not supported by the retrieved evidence.

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

    ranked, best_similarity = query(question)

    # ========================================================
    # REFUSAL
    # ========================================================

    if not ranked:

        if best_similarity > 0:

            reason = (
                "The available evidence in this guideline does not "
                "contain information relevant enough to answer your "
                f"question reliably "
                f"(best similarity score: {best_similarity:.2f}, "
                f"threshold: {SIMILARITY_THRESHOLD:.2f})."
            )

        else:

            reason = (
                "The retrieval system returned no relevant chunks "
                "for your question."
            )

        return {
            "refused": True,

            "refusal": {
                "reason": reason,

                "next_steps": [
                    "Try rephrasing your question using clinical terminology from the guideline.",
                    "Consult the full guideline document directly for manual lookup.",
                    "Ask a qualified clinician who can draw on sources beyond this document.",
                ]
            }
        }


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    answer, chunk_ids = generate_answer(
        question,
        ranked
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return {
        "refused": False,
        "answer": answer,
        "chunk_ids": chunk_ids,
        "results": ranked
    }