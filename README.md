# Analysis of the Conservation State of Ancient Books

**Information Systems and Business Intelligence** — A.Y. 2025/2026

End-to-end Business Intelligence project: integrated cultural-heritage data, reproducible analysis (Colab), and an interactive Streamlit dashboard for conservators and curators.

## Project structure

```
book-conservation-bi/
├── app/streamlit_app.py          # Phase 3 — interactive dashboard
├── data/
│   ├── raw/                      # Source fragments + provenance
│   └── processed/                # Integrated analytic table
├── notebooks/
│   └── conservation_analysis.ipynb
├── report/
│   └── final_report.md           # Phase 4 — export to PDF
├── src/
│   ├── data_integration.py       # Phase 1 — build dataset
│   └── conservation_index.py     # CRI definition
├── requirements.txt
└── README.md
```

## Quick start (local)

```bash
cd book-conservation-bi
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.data_integration
streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`.

## Google Colab

1. Push this folder to GitHub (or zip and upload to Drive).
2. Open `notebooks/conservation_analysis.ipynb` in [Google Colab](https://colab.research.google.com/).
3. Clone the repo in the first cell:

```python
!git clone https://github.com/YOUR_USER/book-conservation-bi.git
%cd book-conservation-bi
!pip install -q -r requirements.txt
!python -m src.data_integration
```

4. Share the notebook link (File → Share) for submission.

## Deploy dashboard (Streamlit Community Cloud)

1. Create a public GitHub repository with this folder.
2. Go to [share.streamlit.io](https://share.streamlit.io/) → **New app**.
3. Main file path: `app/streamlit_app.py`
4. Working directory: repository root (where `requirements.txt` lives).
5. Deploy and copy the public URL for your report and oral exam.

**Alternative:** [Hugging Face Spaces](https://huggingface.co/spaces) with SDK **Streamlit**.

## Phase 1 — Data

| File | Description |
|------|-------------|
| `data/raw/sites.csv` | Libraries, archives, coordinates |
| `data/raw/environmental_monitoring.csv` | Monthly T/RH/light campaign |
| `data/raw/volumes_metadata.csv` | Volume-level catalogue |
| `data/processed/integrated_heritage_books.csv` | Joined analytic table + CRI |
| `data/raw/DATA_PROVENANCE.md` | Licences, limits, extensions |

Regenerate:

```bash
python -m src.data_integration --volumes 480
```

## Conservation Risk Index (CRI)

Synthetic indicator (0–100, higher = worse) combining environmental stress (UNI 10829-inspired bands), material vulnerability, age, and exceptional events. Implemented in `src/conservation_index.py`.

## Submission checklist

- [ ] Public GitHub repository
- [ ] `requirements.txt` + this README
- [ ] Shared Colab notebook link
- [ ] Deployed Streamlit (or HF Spaces) URL
- [ ] `report/final_report.md` exported to PDF (max 10 pages)

## Oral exam tips

Demonstrate: filters → map → drill-down → what-if → priority ranking. Explain why data were integrated, how CRI weights were chosen, and main limitations (synthetic catalogue, site-level environment).

## Licence

Code: MIT. Simulated metadata: structure aligned with open heritage catalogues; see `DATA_PROVENANCE.md`.
