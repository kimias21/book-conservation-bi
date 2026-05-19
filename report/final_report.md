# Analysis of the Conservation State of Ancient Books

**Information Systems and Business Intelligence — A.Y. 2025/2026**  
**Author:** Kimia  
**GitHub:** [kimias21/book-conservation-bi](https://github.com/kimias21/book-conservation-bi)  
**Colab:** https://colab.research.google.com/github/kimias21/book-conservation-bi/blob/main/notebooks/conservation_analysis.ipynb  
**Dashboard:** *[paste Streamlit URL after deployment]*  
**Date:** May 2026

---

## Abstract

This project delivers an integrated information system for analysing the conservation state of ancient books across a network of European libraries and archives. Heterogeneous data on environmental monitoring, storage sites, material composition, and production century are combined into a single analytic dataset. A **Conservation Risk Index (CRI)** supports prioritisation of restoration and preventive policies. Results are exposed through a reproducible Colab notebook and a Streamlit dashboard designed for non-technical decision-makers.

---

## 1. Problem definition and decision context

### 1.1 Operational objective

Curators and conservators must allocate limited resources to volumes at highest deterioration risk while maintaining preventive environmental control. The high-level question is:

> *Which books, in which sites, face elevated conservation risk given environment, materials, and age—and what interventions yield the largest risk reduction?*

### 1.2 Conservator decision cycle

The system supports the cycle **monitor → assess → prioritise → intervene → re-monitor**:

1. **Monitor** — Temperature, RH, light, air quality (and exceptional events).
2. **Assess** — Compute CRI and risk levels per volume.
3. **Prioritise** — Rank volumes/sites; simulate environmental improvements.
4. **Intervene** — Restoration or climate remediation.
5. **Re-monitor** — Update campaign data and refresh indicators.

### 1.3 Design decisions

| Choice | Rationale |
|--------|----------------|
| Join on `site_id` | In open data, environmental loggers sit in the building, not on each volume. |
| CRI scale 0–100 | Easy to explain to a curator and to colour on the dashboard. |
| Streamlit | Same language as the course labs; I can deploy free on Streamlit Cloud. |
| 480 volumes | Sufficient for stable analysis and dashboard performance. |

Environmental ranges for site S01 (Coimbra) follow Ferreira et al. (2019). Italian sites were included to improve geographic coverage in the dashboard map.

---

## 2. Information system architecture

```
[Europeana-style metadata] ──┐
[Site registry] ─────────────┼──► data_integration.py ──► integrated_heritage_books.csv
[Environmental campaign] ────┘           │
                                         ▼
                              conservation_index.py (CRI)
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
            Colab notebook        Streamlit app          PDF report
            (analysis)            (BI dashboard)         (documentation)
```

**Layers:** data integration (Phase 1), analytics engine (Phase 2), presentation layer (Phase 3), documentation (Phase 4).

---

## 3. Phase 1 — Dataset retrieval and construction

### 3.1 Sources

- **Institutional sites** — Eight European libraries/archives with coordinates and climate zones (public institutional data).
- **Environmental monitoring** — Methodology and value ranges from Ferreira et al., *Data in Brief* (2019), University of Coimbra historic library (CC BY).
- **Volume metadata** — Field schema aligned with **Europeana** and **Heidelberg UB** open catalogues (CC BY-SA where applicable).

No single dataset contained all dimensions; integration on `site_id` is documented in `data/raw/DATA_PROVENANCE.md`.

### 3.2 Integration

1. `sites.csv` — location, type, climate.  
2. `environmental_monitoring.csv` — six-month monthly aggregates per site.  
3. `volumes_metadata.csv` — century, support, ink, binding, condition proxy.  
4. Inner join → `integrated_heritage_books.csv`.

### 3.3 Data quality

| Issue | Handling |
|-------|----------|
| Missing monitoring | Full coverage in synthetic campaign; real extension via Coimbra CSV download |
| Material heterogeneity | Standard taxonomy: parchment, laid paper, industrial paper, mixed |
| Condition ground truth | `observed_condition_score` (1–5) as survey proxy; CRI primary for decisions |
| Licences | Documented per layer; Europeana API key optional for real records |

### 3.4 Limitations (Phase 1)

Volume records are **procedurally generated** with realistic marginals—not individual catalogue IDs. This is explicitly acknowledged; the pipeline is designed for replacement with API-backed records.

---

## 4. Phase 2 — Analytical methodology

### 4.1 Pre-processing

Type casting, boolean event flags, material label mapping, outlier flags for implausible RH/T, winsorized light for visualisation.

### 4.2 Exploratory analysis

Univariate CRI distribution; bivariate CRI vs RH and support material; correlation heatmap; geographic scatter of site mean CRI; temporal RH series from monitoring campaign.

### 4.3 Conservation Risk Index

Inspired by **UNI 10829** (thermo-hygrometric and lighting thresholds) and preventive conservation literature:

| Component | Weight | Description |
|-----------|--------|-------------|
| Environmental stress | 35% | Distance from RH 45–55%, T 18–22 °C, light ≤50 lux |
| Material stress | 30% | Ordinal vulnerability (parchment > laid paper > industrial paper; iron-gall ink) |
| Age stress | 25% | Function of production century |
| Events | 10% | Flood, HVAC failure, recent restoration |

Risk labels: Low (&lt;35), Moderate (35–55), High (55–75), Critical (≥75).

### 4.4 Inferential and predictive analysis

- **ANOVA** — CRI across support materials.  
- **Chi-square** — High risk vs flood exposure.  
- **Logistic regression** — Classify `high_risk` from environment + materials + site type.  
- **Random forest** — Feature importance for deterioration drivers.  
- **K-means (k=4)** — Risk profiles in stress space.

### 4.5 Results for decision-makers

On the integrated sample (480 volumes):

- Mean **CRI ≈ 39**; most volumes are **Moderate** risk, a small group **High/Critical**.
- **Bologna (Archiginnasio)** shows higher average CRI, linked to **RH around 58–59%** in the simulated campaign — above the 45–55% band I used from UNI 10829-style guidance.
- **Parchment and iron-gall ink** push material stress up; 19th-century industrial paper lowers material stress but not always total CRI if the room climate is poor.
- In the random-forest run, **century, humidity, and site type** mattered more than ink type alone for the high-risk label.

**For a curator:** stabilise humidity before scheduling expensive restoration on “old but stable” volumes in a bad microclimate.

**Assumptions:** Stationary six-month campaign; site-average environment applied to all stacks.

**Operational implications:** Stabilise RH before mass restoration; use dashboard what-if to estimate CRI delta per 5% RH change.

---

## 5. Phase 3 — Business Intelligence dashboard

### 5.1 Framework choice

**Streamlit** — rapid Python deployment, shared codebase with Colab, free Community Cloud hosting. Alternatives (Dash, Power BI) offer richer enterprise integration but add stack complexity; acceptable trade-off for academic demo.

### 5.2 Functionality

| Requirement | Implementation |
|-------------|----------------|
| KPI dashboard | Volume count, mean CRI, high/critical counts, sites above threshold |
| Filters | Century, material, country, site type, RH/T ranges |
| Geographic viz | Plotly mapbox — site mean CRI |
| Temporal viz | Monthly RH/T per site; CRI by century |
| Drill-down | Site → volume list → JSON detail |
| Decision tool | What-if sliders; top-N priority table |

### 5.3 Deployment

Deployed on Streamlit Community Cloud (`app/streamlit_app.py`). Public URL: *[paste here — e.g. https://book-conservation-bi-xxxx.streamlit.app]*.

---

## 6. Critical self-assessment

### 6.1 Strengths

- End-to-end reproducible pipeline.  
- Clear data lineage and honest limits (simulated catalogue).  
- Dashboard usable in the oral demo (filters, map, what-if).

### 6.2 Weaknesses and future work

1. Replace synthetic volumes with **Europeana API** harvest.  
2. Ingest **raw Coimbra CSV** for site S01.  
3. Volume-level microclimate model inside buildings.  
4. Validate CRI against conservator panel scores.  
5. Add **air quality** sensors where available (ICCU / national archives).

### 6.3 Errors recognised

Site-level environment may **underestimate** risk for volumes near exterior walls; CRI weights are not calibrated on a labelled deterioration dataset.

---

## 7. Conclusion

The project translates a cultural-heritage BI problem into an integrated dataset, a motivated conservation index, statistical and machine-learning analyses, and an interactive dashboard aligned with the conservator’s decision cycle. Limitations are explicit; the architecture supports incremental replacement of synthetic data with open institutional sources without redesigning the information system.

---

## References

1. UNI 10829:1999 — Environmental measurement for conservation of cultural heritage.  
2. Ferreira et al. (2019). Temperature and RH in a historic library, Coimbra. *Data in Brief*.  
3. Europeana API — https://api.europeana.eu/  
4. ICCROM preventive conservation guidelines.  
5. Course materials — Streamlit, scikit-learn, exploratory data analysis.

---

*Export to PDF: Pandoc `pandoc final_report.md -o final_report.pdf` or print from VS Code / Word (max 10 pages).*
