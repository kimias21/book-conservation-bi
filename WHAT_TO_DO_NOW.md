# What to do now — simple checklist

You are **almost finished**. Do these in order.

---

## ✅ Already done

- [x] Project code and data
- [x] GitHub repo: https://github.com/kimias21/book-conservation-bi
- [x] Google Colab notebook (you said done)

---

## 1. Push latest files to GitHub (5 min)

Open **Terminal** and run:

```bash
cd "/Users/kimiaasadzadeh/Documents/GitHub/book-conservation-bi"
git add .
git commit -m "Personalise README, report, and dashboard"
git push
```

If `git push` asks for password → use a **GitHub Personal Access Token**, not your normal password.

---

## 2. Deploy Streamlit dashboard (10 min)

1. Go to https://share.streamlit.io/
2. Sign in with **kimias21**
3. **Create app**
   - Repository: `book-conservation-bi`
   - Branch: `main`
   - Main file: `app/streamlit_app.py`
4. Wait until it says **Running**
5. Copy the URL (example: `https://book-conservation-bi-xxxxx.streamlit.app`)

---

## 3. Update links (5 min)

Paste your URLs in:

- `README.md` → table “Links (submission)”
- `report/final_report.md` → top (Colab + Streamlit)

Then push again:

```bash
git add README.md report/final_report.md
git commit -m "Add Colab and Streamlit submission links"
git push
```

---

## 4. PDF report (20 min)

1. Open `report/final_report.md`
2. Check name **Kimia** — change if your official name is different
3. Fill in Colab + Streamlit links
4. Export to PDF (max 10 pages):
   - Open in Word / Google Docs → Download PDF, **or**
   - Print → Save as PDF

---

## 5. What to send the professor

| Item | What to send |
|------|----------------|
| Code | https://github.com/kimias21/book-conservation-bi |
| Colab | Your shared notebook link |
| Dashboard | Your Streamlit URL |
| Report | Your PDF |

---

## 6. Oral exam (practice 10 min)

Show on Streamlit:

1. KPIs at top  
2. Filter by century or material  
3. Map tab  
4. Drill-down → pick a volume  
5. What-if → move humidity slider  

Say out loud:

- “I joined data on site_id because environment is measured per library.”
- “CRI combines climate, materials, age, and events like floods.”
- “Part of the catalogue is simulated; I would add Europeana API next.”

---

## If you are stuck

| Problem | Fix |
|---------|-----|
| `git push` fails | Use GitHub token; or use GitHub Desktop |
| Streamlit error | Check `requirements.txt` is in repo root |
| Colab `ModuleNotFoundError: src` | Run the `git clone` cell first |

You do **not** need to touch the Queen Hokm game folder for this exam.
