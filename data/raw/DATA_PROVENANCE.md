# Data provenance and integration (Phase 1)

## Objective

Construct a coherent dataset for analysing **conservation state of ancient books** as a function of environment, materials, storage location, and century of production

## Sources and rationale

| Layer | Source | Role in project | Licence / access |
|-------|--------|-----------------|------------------|
| **Sites** | Public information on European libraries/archives (Coimbra, Heidelberg, Bologna, Florence, BnF, British Library, Laurenziana) | Geographic and institutional context | Facts; coordinates from open maps |
| **Environmental monitoring** | Methodology and value ranges from Ferreira et al., *Data in Brief* (2019), historic library Coimbra; supplemented by zone-based profiles | Temperature, RH, light, events | Open-access article (CC BY) |
| **Volume metadata** | Field schema aligned with **Europeana** and **Heidelberg UB** open catalogues | Century, materials, language, format | Metadata structure: CC BY-SA where applicable |
| **Climate context** | Köppen-style `climate_zone` labels per city | Stratification and map colouring | Derived attribute |

No single public dataset contains all required variables. This project **integrates** fragments through deterministic joins on `site_id` and documents limitations below.

## Integration logic

1. `sites.csv` — one row per institution (lat/lon, type, climate zone).
2. `environmental_monitoring.csv` — monthly campaign per site → aggregated to volume level.
3. `volumes_metadata.csv` — one row per volume with material taxonomy and century.
4. `integrated_heritage_books.csv` — inner join site + environment + CRI computation.

Join key: **`site_id`**.

## Data quality and limitations

- **Synthetic catalogue**: Volume records are procedurally generated with realistic marginals (e.g. more industrial paper after 18th century). They are **not** individual Europeana records unless you extend `data_integration.py` with the Europeana API.
- **Environmental series**: Inspired by published monitoring; not a raw download of the Coimbra CSV unless you add it manually from the supplementary data of the paper.
- **Condition**: `observed_condition_score` simulates expert survey scores for model validation; CRI is the primary decision index.
- **Missing values**: Pipeline produces complete analytic table; artificial missingness can be injected for robustness exercises in Colab.

## Possible extensions

1. Connect to the Europeana API to replace simulated volume records with real manuscript metadata.
2. Download the Coimbra supplementary CSV from Ferreira et al. (2019) and use it for site S01 instead of the modelled series.
3. Add outdoor climate normals via the Open-Meteo Historical Weather API, matched by site coordinates.

## Regeneration

```bash
cd book-conservation-bi
python -m src.data_integration
```
