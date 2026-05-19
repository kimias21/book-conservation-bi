# Conservation state of ancient books — BI project

**Kimia · Information Systems and Business Intelligence · A.Y. 2025/2026**

Repository: [github.com/kimias21/book-conservation-bi](https://github.com/kimias21/book-conservation-bi)

---

## What this project does

I built a small decision-support system for libraries and archives: it links **where** books are stored, **environmental** readings (temperature, humidity, light), and **what they are made of** (parchment, paper, inks, binding) to a single **Conservation Risk Index (CRI)**. Curators can filter collections, see sites on a map, drill down to single volumes, and test “what-if” humidity changes before planning restoration.

I chose this topic because open cultural-heritage data are split across catalogues and monitoring studies — no one file had everything. I integrated sources on `site_id` and documented limits in `data/raw/DATA_PROVENANCE.md`.

---

## Links (submission)

| Deliverable | Link |
|-------------|------|
| GitHub | https://github.com/kimias21/book-conservation-bi |
| Google Colab | *paste your shared notebook URL here* |
| Streamlit dashboard | *paste your Streamlit Cloud URL after deploy* |
| Report (PDF) | export from `report/final_report.md` |

---

## Run locally

```bash
git clone https://github.com/kimias21/book-conservation-bi.git
cd book-conservation-bi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.data_integration
streamlit run app/streamlit_app.py
```

Browser: `http://localhost:8501`

---

## Google Colab

Open the notebook directly:

https://colab.research.google.com/github/kimias21/book-conservation-bi/blob/main/notebooks/conservation_analysis.ipynb

Or run setup in a new notebook:

```python
!git clone https://github.com/kimias21/book-conservation-bi.git
%cd book-conservation-bi
!pip install -q -r requirements.txt
!python -m src.data_integration
```

Then open `notebooks/conservation_analysis.ipynb` from the file panel → **Runtime → Run all** → **Share** the notebook.

---

## Deploy Streamlit (one time)

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub account **kimias21**
2. **New app** → repo `kimias21/book-conservation-bi`, branch `main`
3. Main file: `app/streamlit_app.py`
4. Copy the public URL into the table above and into your PDF report

---

## Main files

| Path | Role |
|------|------|
| `src/data_integration.py` | Builds integrated dataset |
| `src/conservation_index.py` | CRI formula |
| `data/processed/integrated_heritage_books.csv` | Main table for analysis |
| `notebooks/conservation_analysis.ipynb` | EDA + models |
| `app/streamlit_app.py` | Dashboard |
| `report/final_report.md` | Written report (→ PDF) |

---

## CRI in one sentence

Score 0–100 (higher = worse): combines environment (UNI 10829-style RH/T bands), material sensitivity, age, and events such as floods. Details in the report and in `src/conservation_index.py`.

---

## Licence

Code MIT · simulated catalogue metadata documented in `DATA_PROVENANCE.md`
