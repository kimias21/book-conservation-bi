# Analysis of the Conservation State of Ancient Books

**Information Systems and Business Intelligence** — A.Y. 2025/2026  
**Author:** Kimia · [kimias21](https://github.com/kimias21)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kimias21/book-conservation-bi/blob/main/notebooks/conservation_analysis.ipynb)

---

## Overview

Business Intelligence project on cultural heritage: integration of environmental monitoring, storage sites, and bibliographic metadata to assess conservation risk for ancient books. Outputs include a reproducible analysis notebook and a Streamlit dashboard for curators.

---

## Project links

| Resource | URL |
|----------|-----|
| Repository | https://github.com/kimias21/book-conservation-bi |
| Colab notebook | https://colab.research.google.com/github/kimias21/book-conservation-bi/blob/main/notebooks/conservation_analysis.ipynb |
| Written report | `report/final_report.md` (export to PDF) |
| Streamlit dashboard | https://book-conservation-bi-xcdbvyjzkzp7rvyvkqecs2.streamlit.app |

---

## Structure

```
book-conservation-bi/
├── src/                    # Data integration and CRI
├── data/raw/               # Source tables and provenance
├── data/processed/         # Integrated dataset
├── notebooks/              # Phase 2 analysis
├── app/                    # Phase 3 dashboard
└── report/                 # Phase 4 documentation
```

---

## Installation and run

```bash
git clone https://github.com/kimias21/book-conservation-bi.git
cd book-conservation-bi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.data_integration
streamlit run app/streamlit_app.py
```

---

## Colab

Open the notebook with the badge above, or run:

```python
!git clone https://github.com/kimias21/book-conservation-bi.git
%cd book-conservation-bi
!pip install -q -r requirements.txt
```

Then **Runtime → Run all** on `notebooks/conservation_analysis.ipynb`.

---

## Conservation Risk Index (CRI)

Composite score (0–100, higher = worse) based on environmental stress (UNI 10829-inspired thresholds), material vulnerability, document age, and exceptional events. Implementation: `src/conservation_index.py`.

---

## Data

Integrated table: `data/processed/integrated_heritage_books.csv`  
Provenance and limitations: `data/raw/DATA_PROVENANCE.md`

---

## Licence

Code: MIT · Metadata simulation documented in `DATA_PROVENANCE.md`
