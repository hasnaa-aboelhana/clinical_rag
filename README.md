# 404: Hallucination Not Found 🏥

> **RAG-Based Clinical Decision Support for Mental Health During Pregnancy**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=flat-square&logo=streamlit)](https://hallucination-not-found-rag.streamlit.app)
[![Guideline](https://img.shields.io/badge/Guideline-NICE%20CG192-4A7C6F?style=flat-square)](https://www.nice.org.uk/guidance/cg192)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 🧠 What Is This?

Standard LLMs hallucinate. In clinical settings, that's not just inaccurate — it's dangerous.

**404: Hallucination Not Found** is a Retrieval-Augmented Generation (RAG) system that answers clinical questions about perinatal mental health by retrieving and citing exact passages from the **NICE CG192** guideline. Every answer is grounded. Every claim is cited. If the answer isn't in the guideline, the system says so — and refuses to make something up.

---

## 🔴 The Problem

| Failure Mode | What It Looks Like |
|---|---|
| Frequent Hallucination | LLMs fill knowledge gaps with plausible-sounding myths |
| Fabricated Clinical Advice | Invented citations, trials, and drug guidelines |
| Dangerous False Confidence | Incorrect advice delivered in an authoritative tone |

In perinatal mental health — where decisions affect both mother and unborn child — **zero tolerance for inaccuracy** is not a preference. It's a requirement.

---

## ✅ The Solution

```
Your Clinical Question
        ↓
  Embed with SentenceTransformer
        ↓
  Cosine Similarity Search (ChromaDB)
        ↓
  Similarity Score ≥ 0.70?
       / \
     YES   NO
      ↓     ↓
 Grounded  Graceful
 Answer +  Refusal
 Citation
```

- **Retrieves** exact chunks from NICE CG192
- **Cites** every claim back to its source chunk
- **Refuses** to answer when evidence is absent or below threshold
- **Never** hallucinates, speculates, or invents citations

---

## 🏗️ System Architecture

### Pipeline Overview

```
NICE CG192 PDF
      ↓
  LlamaParse          → parsed_document.json
      ↓
  Regex Cleaner       → cleaned_document.json
      ↓
  LangChain Chunker   → chunks.json
  (300 tokens, 100 overlap)
      ↓
  SentenceTransformer → 384-dim embeddings
  (all-MiniLM-L6-v2)
      ↓
  ChromaDB            → nice_cg192_mental_health collection
      ↓
  [At query time]
  User Query → Embed → Cosine Similarity → Top-5 Chunks → Groq LLM → Grounded Answer
```

### Chunking Parameters

| Parameter | Value |
|---|---|
| Chunk size | 300 tokens |
| Overlap | 100 tokens |
| Top-k retrieval | 5 |
| Similarity threshold | 0.70 |

### ChromaDB Schema

Each stored record contains:
- `id` — unique chunk identifier
- `document` — raw chunk text
- `embedding` — 384-dim float vector
- `metadata` — `{ page, section, source, char_count }`

---

## 📊 Evaluation Results

| Prompt | Chunks | Precision@5 | Citation Acc. | Faithfulness |
|---|---|---|---|---|
| Sertraline at 20 weeks — should I stop? *(out-of-scope)* | 0 | 0 | 0 | 0 |
| How is bipolar diagnosed for pregnant women? | 4 | 0.80 | 1 | 0.833 |
| Managing tokophobia / extreme fear of childbirth | 1 | 0.20 | 1 | 0.500 |
| Treatment options: TCAs, SSRIs, or SNRIs? | 3 | 0.60 | 1 | 0.667 |
| Safety risks & management of lithium during pregnancy | 5 | **1.00** | 1 | 0.750 |

**Key results:**
- Out-of-scope query correctly refused — all metrics at 0 ✓
- Citation accuracy **1.0** across all in-scope queries ✓
- Lithium query (highest-stakes) achieved perfect Precision@5 ✓

### Refusal Quality Rubric — Score: 3/3

| # | Criterion | Status |
|---|---|---|
| 1 | States Insufficiency — clearly detects missing guideline context | ✓ |
| 2 | Stays Honest — refuses to hallucinate or speculate | ✓ |
| 3 | Offers Next Step — redirects to specialist or primary docs | ✓ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Language | Python 3.10+ |
| Embeddings | SentenceTransformers `all-MiniLM-L6-v2` |
| Vector DB | ChromaDB |
| LLM | Groq API |
| PDF Parsing | LlamaParse |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Deployment | Streamlit Community Cloud |
| Secrets | Streamlit Secrets |
| Version Control | Git & GitHub |

---

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.10
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/404-hallucination-not-found.git
cd 404-hallucination-not-found

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
LLAMA_CLOUD_API_KEY = "your_llama_cloud_key_here"
```

> ⚠️ Never commit this file. It's already in `.gitignore`.

### Run Locally

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
404-hallucination-not-found/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .gitignore
│
├── data/
│   ├── parsed_document.json    # LlamaParse output
│   ├── cleaned_document.json   # Regex-cleaned text
│   └── chunks.json             # Chunked passages
│
├── embeddings/
│   └── chroma_db/              # ChromaDB persistent store
│       └── nice_cg192_mental_health/
│
├── pipeline/
│   ├── parse.py                # PDF parsing with LlamaParse
│   ├── clean.py                # Regex noise-stripping
│   ├── chunk.py                # LangChain chunking
│   ├── embed.py                # SentenceTransformer embedding
│   └── retrieve.py             # ChromaDB similarity retrieval
│
└── evaluation/
    └── metrics.py              # Precision@5, Faithfulness, Citation Accuracy
```

---

## ☁️ Deployment

The app is deployed on **Streamlit Community Cloud**.

**Workflow:**

```
Local Dev → Git push → GitHub → Streamlit Cloud auto-deploys → Live App
```

- `requirements.txt` is used to build the environment automatically
- `GROQ_API_KEY` is stored in Streamlit Secrets — never in the repo
- ChromaDB collection is initialised from the guideline data on first run in cloud

**Live App:** [hallucination-not-found-rag.streamlit.app](https://hallucination-not-found-rag.streamlit.app)

---

## ⚕️ Clinical Disclaimer

This system is a **decision support tool only**. It is not a substitute for clinical judgment. All responses should be verified against the original NICE CG192 guideline and reviewed by a qualified healthcare professional before any clinical action is taken.

---

## 👥 Team

| Name | Role |
|---|---|
| Hasnaa Aboelhana | Team Member |
| Arwa Eisa | Team Member |
| Ereny Habib | Team Member |
| Marym Waled | Team Member |
| Warda | Team Member |

**Instructor:** Jumana Mahammed
**Mentor:** Mahmoud Mostafa
**Program:** DEPI Machine Learning Track · 2025

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <em>Halting AI Hallucination, Healing Trust.</em>
</p>
