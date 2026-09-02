# Nivra (निव्रा / నివ్రా)

> **A Production-Grade Multilingual RAG Platform for Indian Women Entrepreneurs**
> *Helping women entrepreneurs find, understand, and apply for government schemes in plain English, Telugu, and Hindi.*

---

## 🌟 Overview & Features

Nivra bridges the digital literacy gap for Indian women micro-entrepreneurs by converting complex, jargon-heavy government scheme PDFs (loans, subsidies, scholarships, incubation grants) into accessible plain-language summaries and interactive tools.

- **🎨 Modern React (Vite) SaaS Frontend**: Soft lavender aesthetic, glassmorphism cards, micro-animations, high contrast readability, and responsive mobile layout.
- **⚡ FastAPI Python Backend**: Fast REST API exposing Hybrid RRF search, grounded Q&A, eligibility evaluation, and document checklists.
- **🔍 Hybrid Reciprocal Rank Fusion (RRF)**: Combines dense vector similarity (384-dim Qdrant) with sparse keyword search (BM25Okapi) for maximum precision (+54.5% Context Precision improvement over vector-only search).
- **🌐 Multilingual Plain Language**: Grounded LLM generation with automatic translation into **Telugu (తెలుగు)** and **Hindi (हिन्दी)**.
- **📋 Form-Driven Eligibility Checker**: Match scoring system evaluating user profile inputs (age, business stage, category, state) against scheme criteria.
- **📄 Interactive Document Checklists**: One-click categorized document lists (Identity, Business, Financial, Category Proofs) with progress checkboxes.

---

## 📐 System Architecture

```
                               ┌───────────────────────────┐
                               │ React + Vite Frontend UI  │
                               │  (http://localhost:5180)  │
                               └─────────────┬─────────────┘
                                             │ HTTP REST API (JSON)
                                             ▼
                               ┌───────────────────────────┐
                               │  FastAPI Python Backend   │
                               │  (http://localhost:8080)  │
                               └─────────────┬─────────────┘
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      │                                      │                                      │
      ▼                                      ▼                                      ▼
┌───────────┐                          ┌───────────┐                          ┌───────────┐
│ Ingestion │                          │ Retrieval │                          │Generation │
│  Docling  │                          │ Qdrant +  │                          │ Grounded  │
│ PyPDF Fall│                          │   BM25    │                          │LLM + Trans│
└───────────┘                          └───────────┘                          └───────────┘
```

---

## 📊 RAG Evaluation Benchmark Results

Evaluated using RAGAS across **20 ground-truth test QA pairs**:

| Metric | Semantic-Only (Baseline) | Hybrid RRF (Nivra) | Relative Improvement |
| :--- | :---: | :---: | :---: |
| **Faithfulness (Groundedness)** | 95.0% | **98.0%** | **+3.2%** |
| **Context Precision** | 60.4% | **93.2%** | **+54.5%** 🚀 |
| **Context Recall** | 54.8% | **78.7%** | **+43.6%** 🚀 |
| **Answer Relevance** | 83.3% | **89.9%** | **+8.0%** |

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**

### 2. Environment Setup
Clone the repository and install backend Python dependencies:
```bash
py -3 -m pip install -r requirements.txt
```

Set up your `.env` file (optional for online Groq LLM generation):
```bash
cp .env.example .env
```

### 3. Data Processing & Index Building
Extract text from raw PDFs, create section chunks, and build Qdrant & BM25 search indices:
```bash
# 1. Generate sample scheme PDFs (if starting fresh)
py -3 -m data.generate_sample_pdfs

# 2. Extract structured text with Docling / PyPDF
py -3 -m src.ingestion.extract

# 3. Perform header-aware semantic section chunking
py -3 -m src.ingestion.chunk

# 4. Generate dense Qdrant vector embeddings
py -3 -m src.retrieval.embed_store

# 5. Build sparse BM25 keyword index
py -3 -m src.retrieval.bm25_index
```

### 4. Running the Web Application

#### Option A: Local Dev Execution
```bash
# Start Backend
py -3 -m uvicorn backend.main:app --port 8080

# Start Frontend (in frontend/ directory)
cd frontend
npx vite --port 5180
```
*Frontend available at: **`http://localhost:5180`***

#### Option B: Docker Production Deployment
```bash
docker-compose up -d --build
```
*Production Nginx Frontend available at: **`http://localhost`*** (Port 80)

*For detailed Vercel, Render, and Railway deployment instructions, see [DEPLOYMENT.md](file:///c:/Users/Dell/OneDrive/Desktop/rag%20system/DEPLOYMENT.md).*

---

## 📁 Repository Structure

```
.
├── backend/
│   └── main.py              # FastAPI REST endpoints (/api/search, /api/ask, /api/eligibility, etc.)
├── frontend/
│   ├── index.html           # React app HTML template
│   ├── vite.config.js       # Vite build & API proxy configuration
│   └── src/
│       ├── index.css        # Soft lavender CSS design system
│       ├── App.jsx          # Root React app component
│       └── components/
│           ├── Sidebar.jsx             # Left navigation menu
│           ├── Header.jsx              # Global header with language selector
│           ├── DashboardHome.jsx       # Search bar & recommended scheme cards
│           ├── AskQuestion.jsx         # Multilingual grounded Q&A
│           ├── EligibilityChecker.jsx  # Form profile matcher
│           ├── DocumentChecklistModal.jsx # Required document checklist
│           ├── SavedSchemes.jsx        # Bookmarked schemes
│           └── MetricsView.jsx         # RAG evaluation metrics dashboard
├── data/
│   ├── raw_pdfs/            # Source government scheme PDFs
│   └── processed/          # Cleaned text & chunks JSON
├── src/
│   ├── ingestion/           # Docling PDF extraction & section chunking
│   ├── retrieval/           # Dense Qdrant + Sparse BM25 RRF engine
│   ├── generation/          # Grounded LLM generator & deep-translator
│   ├── eligibility/         # Profile form eligibility matcher
│   └── evaluation/          # RAGAS test dataset & evaluation harness
├── requirements.txt
└── README.md
```

---

## 📜 License
Developed under MIT License for empowering Indian women micro-entrepreneurs.
