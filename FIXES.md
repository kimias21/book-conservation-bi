# Common errors — how to fix them

## Colab: `ModuleNotFoundError: No module named 'src'`

**Cause:** Notebook opened without the project folder.

**Fix:** Run the **first code cell** (it clones the repo and installs packages).  
Or open: https://colab.research.google.com/github/kimias21/book-conservation-bi/blob/main/notebooks/conservation_analysis.ipynb

---

## Colab: `FileNotFoundError` for CSV

**Cause:** Data file missing.

**Fix:** Run in a cell:

```python
!python -m src.data_integration
```

---

## Colab: `ValueError` on `train_test_split(..., stratify=y)`

**Cause:** Too few “high risk” volumes (only 4 in the dataset).

**Fix:** Notebook now uses `elevated_risk` (CRI ≥ 45) and only stratifies when enough samples exist. **Re-download** the notebook from GitHub after `git push`.

---

## Cursor shows errors in `Queen Hokm` (Unity)

**Cause:** Wrong folder open — that is the **card game**, not this exam project.

**Fix:** **File → Open Folder** →  
`/Users/kimiaasadzadeh/Documents/GitHub/book-conservation-bi`

---

## Streamlit: app won’t start

```bash
cd "/Users/kimiaasadzadeh/Documents/GitHub/book-conservation-bi"
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## Push fixes to GitHub

```bash
cd "/Users/kimiaasadzadeh/Documents/GitHub/book-conservation-bi"
git add .
git commit -m "Fix notebook setup and model training errors"
git push
```

Then in Colab: **Runtime → Factory reset runtime → Run all**.
