# 🧠 AI Contamination Benchmark

**Datathon EA UPY 2025 — July Edition**
**Universidad Politécnica de Yucatán**

---

## 📘 Overview

This project provides a reproducible framework to benchmark **token contamination** across multiple AI agents: **GPT-4o**, **Claude 3 Sonnet**, **Gemini**, and **DeepSeek**. It is designed to generate, evaluate, and analyze AI outputs under standardized prompt conditions, leveraging a robust technical stack that includes **LangChain**, **MongoDB**, and various vendor APIs like **OpenRouter**.

> **Token contamination** refers to the residual biases, repetition, or pattern artifacts that appear when AI outputs are reused in training data. This phenomenon can potentially degrade future model performance and compromise ethical neutrality.

---

## ⚙️ Architecture Overview

The automated evaluation process follows a modular pipeline:

1.  **Prompt Ingestion**: Structured datasets are ingested from `EA_Benchmark_Prompts_200.csv`.
2.  **Agent Orchestration**: AI agents are orchestrated via LangChain wrappers and native SDKs (OpenRouter for GPT-4o/Claude, Google Generative AI for Gemini, and DeepSeek SDK).
3.  **Response Storage**: The generated responses are stored in a **MongoDB** database, with separate collections for each model.
4.  **Metric Computation**: Key metrics such as redundancy, entropy, and semantic similarity are computed.
5.  **Benchmark Reports**: Finally, benchmark reports and visual analyses are generated in a Jupyter Notebook.

---

## 🧩 Core Components (by file)

### `src/invoke.py` — Model Bootstrap

-   Initializes clients for **GPT-4o** and **Claude 3 Sonnet** via **OpenRouter**, **Gemini 1.5 Flash** via **Google Generative AI**, and **DeepSeek** via its REST API.
-   Reads API keys from environment variables: `OPENROUTER_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`.
-   Exposes a `get_all_models()` factory function that returns a dictionary of ready-to-use model handles.

### `src/prompts.py` — Prompt Sources & MongoDB

-   Loads prompts from a CSV file specified by `CSV_PROMPTS_PATH` (defaults to `/app/data/EA_Benchmark_Prompts_200.csv`).
-   Connects to the **`etl_processed`** MongoDB database using an Airflow Variable `mongo_uri` (default: `mongodb://root:example@mongo:27017/admin`).
-   Supports loading prompts directly from MongoDB collections when needed.

### `src/load.py` — Execution & Persistence

-   Iterates through all prompts and all models, handling per-model invocation nuances (e.g., DeepSeek’s chat API).
-   Persists documents into MongoDB with the following fields: `prompt`, `response`, `model`, and `timestamp (UTC ISO8601)`.
-   Uses per-model collections, such as `gpt4o_responses`, `claude_responses`, `gemini_responses`, and `deepseek_responses`.

### `src/notebook.ipynb` — Analysis & Reports

-   A Jupyter Notebook for computing metrics, aggregating CSV results, and plotting comparisons.

---

## 🧪 Metrics & Analysis

The benchmark focuses on contamination patterns in token sequences, using the following metrics:

| Metric                  | What it measures                                | Why it matters                                      |
| ----------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Repetition Rate (RR)** | Lexical redundancy / n-gram loops               | Flags degenerate loops and low-diversity outputs    |
| **Entropy (H)** | Token distribution diversity                    | Low entropy suggests repetitive or templated outputs|
| **Semantic Overlap (SO)** | Embedding similarity to prompts or reference corpora | Detects overfitting, prompt echoing, or leakage      |
| **Contamination Index (CI)** | Composite of RR, H, SO (weighted)             | A single score to rank agents by "cleanliness"      |

> The notebook computes these metrics from consolidated CSVs and visualizes per-model distributions, confidence intervals, and pairwise deltas.

---

## 📂 Data & Artifacts

**Input & intermediate data (in `data/`):**

-   `EA_Benchmark_Prompts_200.csv`: The canonical prompt set with 200 items.
-   `evaluaciones_con_claude.csv`: Raw evaluation outputs from Claude.
-   `evaluaciones_con_claude_fixed.csv`: Cleaned and normalized Claude evaluations (stored in `src/` for convenience).
-   `model_outputs_clean.csv`: Consolidated and cleaned outputs for metric computation.
-   `model_outputs_batch_{0,25,50,75}.csv`: Optional staged outputs by chunking prompts.

> **Tip**: Keep large raw generations in Git LFS or external storage to avoid bloating the repository.

---

## 📦 Repository Structure

```bash
AI-Contamination-Benchmark/
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
````

-----

## ⚙️ Setup & Installation

#### 1\. Clone the repository

```bash
git clone [https://github.com/Giobbva/AI-Contamination-Benchmark.git](https://github.com/Giobbva/AI-Contamination-Benchmark.git)
cd AI-Contamination-Benchmark
```

#### 2\. Environment variables

Create a `.env` file at the root of the repository:

```env
OPENROUTER_API_KEY=your_openrouter_key
GOOGLE_API_KEY=your_gemini_key
DEEPSEEK_API_KEY=your_deepseek_key

# Optional for prompts.py (defaults shown)
CSV_PROMPTS_PATH=/app/data/EA_Benchmark_Prompts_200.csv

# If running with Airflow Variables disabled, you can export MONGO_URI directly
# MONGO_URI=mongodb://root:example@mongo:27017/admin
```

> If using Airflow, set `mongo_uri` as an Airflow Variable; otherwise, expose `MONGO_URI` in your runtime environment and adapt `prompts.py` accordingly.

#### 3\. Dependencies

Install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 4\. Run the notebook

Launch the Jupyter Notebook for analysis:

```bash
jupyter notebook src/notebook.ipynb
```

-----

## 🚀 Running the Pipeline (headless idea)

A simple orchestration pattern is as follows:

1.  **Load prompts** (from CSV or MongoDB).
2.  **Instantiate models** (`get_all_models()`).
3.  **Invoke and persist** (`procesar_modelos(...)`).
4.  **Export CSVs** for analysis (optional).
5.  **Explore** `src/notebook.ipynb` for metrics and plots.

> **Note**: In this iteration, execution entrypoints are modular (scripts and notebook). You can wire them into a CLI or an Airflow DAG as needed.

-----

## 🧰 Tech Stack

  - **Python**
  - **LangChain**
  - **Pandas**
  - **Matplotlib**
  - **OpenRouter**
  - **Google Generative AI**
  - **DeepSeek**
  - **MongoDB** for structured storage
  - **Jupyter** for exploratory analysis

-----

## `requirements.txt`

```
langchain
langchain-core
openai
google-generativeai
python-dotenv
pandas
jupyter
langchain_community
langchain-openai
matplotlib
```

-----

## 🔒 Data & Safety Notes

  - **Avoid committing secrets**; rely on `.env` or secret managers.
  - Consider **de-identification** if prompts or outputs contain Personally Identifiable Information (PII).
  - Use **rate limits and retries** for vendor APIs.
  - **Log only what you need**; raw generations can be large.

-----

## 📈 Results (example narrative)

  - **Claude 3 Sonnet** showed lower Repetition Rate (RR) and higher entropy on reasoning prompts.
  - **GPT-4o** balanced entropy and overlap, with a stable Contamination Index (CI) across domains.
  - **Gemini 1.5 Flash** varied more with long prompts, showing higher overlap on narrative tasks.
  - **DeepSeek** improved with prompt scaffolds; RR decreased after few-shot exemplars.

> Your exact outcomes will depend on the prompt mix, temperature, and sampling settings. Reproduce the results via the provided CSVs and notebook.

-----

## 🛣️ Roadmap

  - [ ] Add per-domain CI (reasoning, code, safety, instruction-following).
  - [ ] Support batch async invocation with backoff & tracing.
  - [ ] Add embedding backends switch (e.g., OpenAI/Instructor/Local) for Semantic Overlap (SO).
  - [ ] Export HTML reports (per-model scorecards).

-----

## ⚖️ Ethical Considerations

Reusing model outputs in training can amplify biases and artifacts. This benchmark aims to measure and reduce such contamination risks. Interpret the Contamination Index (CI) alongside qualitative review; numbers don’t replace human judgment.

-----

## 🤝 Contributors

  - **Giovanni Rafael Soriano Pacheco** (maintainer) - [Giobbva](https://github.com/Giobbva)
  - Cesar Antonio Pinto May
  - Suny Ricarte Ramirez Perez

> Community collaborators are welcome\! Please open an Issue or Pull Request with your proposed changes.

-----

## 🧾 Citation

If you build on this repository, please cite:

```
Giovanni Rafael Soriano Pacheco. Benchmarking Token Contamination in AI Agents.
Datathon EA UPY 2025 — Universidad Politécnica de Yucatán, 2025.
[https://github.com/Giobbva/AI-Contamination-Benchmark](https://github.com/Giobbva/AI-Contamination-Benchmark)
```

**BibTeX:**

```bibtex
@misc{giobbva2025tokencontamination,
  title  = {Benchmarking Token Contamination in AI Agents},
  author = {Giovanni Rafael Soriano Pacheco},
  year   = {2025},
  note   = {Datathon EA UPY 2025 — Universidad Politécnica de Yucatán},
  howpublished = {\url{[https://github.com/Giobbva/AI-Contamination-Benchmark](https://github.com/Giobbva/AI-Contamination-Benchmark)}}
}
```

-----

## 📄 License

This project is released under the **MIT License**. See the `LICENSE` file for full terms.

-----

## 🪪 Acknowledgements

  - Datathon EA UPY 2025 organizers and mentors
  - Dexter Enrique Gomez Ek (Mentor)
  - Jason Maximiliano Pinelo Hau (Mentor)
  - OpenRouter, Google Generative AI, and DeepSeek teams for API access
  - The open-source community for LangChain and other Python libraries.
