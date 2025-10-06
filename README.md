# 🧠 Benchmarking Token Contamination in AI Agents
**Datathon EA UPY 2025 — July Edition**  
**Polytechnic University of Yucatán**

---

## 📘 Overview
This project benchmarks **token contamination** across multiple AI agents (GPT-4o, Claude 3 Sonnet, Gemini, and DeepSeek).  
It provides a reproducible framework to **generate, evaluate, and analyze AI outputs** under standardized prompt conditions, using **LangChain**, **MongoDB**, and **OpenRouter / vendor APIs**.

> *Token contamination* refers to residual biases, repetition, or pattern artifacts that appear when AI outputs are reused in training data — potentially degrading future model performance or ethical neutrality.

---

## ⚙️ Architecture Overview
Automated evaluations run through a modular **pipeline**:

1. **Prompt ingestion** from structured datasets (`EA_Benchmark_Prompts_200.csv`).  
2. **Agent orchestration** via LangChain wrappers and native SDKs (OpenRouter ↔︎ GPT-4o/Claude, Google Generative AI ↔︎ Gemini, DeepSeek SDK).  
3. **Response storage** in **MongoDB**, separated by model collections.  
4. **Metric computation** (redundancy, entropy, semantic similarity).  
5. **Benchmark reports** and visual analyses in a Jupyter Notebook.

---

## 🧩 Core Components (by file)

### `src/invoke.py` — Model bootstrap
- Initializes clients for **GPT-4o** and **Claude 3 Sonnet** via **OpenRouter**, **Gemini 1.5 Flash** via **Google Generative AI**, and **DeepSeek** via its REST API.
- Reads API keys from environment (`OPENROUTER_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`).
- Exposes a `get_all_models()` factory returning a dictionary of ready-to-use model handles.

### `src/prompts.py` — Prompt sources & Mongo
- Loads prompts from CSV using `CSV_PROMPTS_PATH` (defaults to `/app/data/EA_Benchmark_Prompts_200.csv`).
- Connects to MongoDB database **`etl_processed`** using an Airflow Variable `mongo_uri`
  (default: `mongodb://root:example@mongo:27017/admin`).
- Supports loading prompts directly from Mongo collections when needed.

### `src/load.py` — Execution & persistence
- Iterates **all prompts × all models**, handles per-model invocation nuances (e.g., DeepSeek’s chat API).
- Persists documents into Mongo with fields:
  `prompt`, `response`, `model`, `timestamp (UTC ISO8601)`.
- Uses per-model collections, e.g.:
  `gpt4o_responses`, `claude_responses`, `gemini_responses`, `deepseek_responses`.

### `src/notebook.ipynb` — Analysis & reports
- Notebook for computing metrics, aggregating CSV results, and plotting comparisons.

---

## 🧪 Metrics & Analysis
The benchmark focuses on contamination patterns in token sequences:

| Metric | What it measures | Why it matters |
|---|---|---|
| **Repetition Rate (RR)** | Lexical redundancy / n-gram loops | Flags degenerate loops and low-diversity outputs |
| **Entropy (H)** | Token distribution diversity | Low entropy ↔︎ repetitive or templated outputs |
| **Semantic Overlap (SO)** | Embedding similarity to prompts or reference corpora | Detects overfitting, prompt echoing, or leakage |
| **Contamination Index (CI)** | Composite of RR, H, SO (weighted) | Single score to rank agents by “cleanliness” |

> The notebook computes these from consolidated CSVs and visualizes per-model distributions, confidence intervals, and pairwise deltas.

---

## 📂 Data & Artifacts
**Input & intermediate data (in `data/`):**
- `EA_Benchmark_Prompts_200.csv` — Canonical prompt set (200 items).
- `evaluaciones_con_claude.csv` — Raw evaluation outputs from Claude.
- `evaluaciones_con_claude_fixed.csv` — Cleaned/normalized Claude evaluations (stored in `src/` for convenience in this iteration).
- `model_outputs_clean.csv` — Consolidated and cleaned outputs for metric computation.
- (Batches) `model_outputs_batch_{0,25,50,75}.csv` — Optional staged outputs by chunking prompts.

> Tip: keep large raw generations in Git LFS or external storage to avoid bloating the repo.

---

## 📦 Repository Structure
```bash
bigdatas/
├── data/
│   ├── EA_Benchmark_Prompts_200.csv
│   ├── evaluaciones_con_claude.csv
│   └── model_outputs_clean.csv
├── src/
│   ├── invoke.py
│   ├── load.py
│   ├── prompts.py
│   ├── notebook.ipynb
│   ├── evaluaciones_con_claude_fixed.csv
│   ├── model_outputs.csv
│   ├── model_outputs_batch_0.csv
│   ├── model_outputs_batch_25.csv
│   ├── model_outputs_batch_50.csv
│   └── model_outputs_batch_75.csv
├── requirements.txt
├── LICENSE
└── README.md
