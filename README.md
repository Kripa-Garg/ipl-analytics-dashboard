# IPL Analytics Dashboard 🏏

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-purple)

Interactive data analytics dashboard analysing 816 IPL matches
and 179,000+ ball-by-ball deliveries from 2008 to 2020.

🔗 **[Live Demo](YOUR_STREAMLIT_URL)**

---

## Key Insights Found

- 🏆 Mumbai Indians won the most IPL titles (5)
- 🎯 Teams batting second win **X%** of matches overall
- 📍 Batting second advantage is statistically validated
  (chi-square test, p < 0.05)
- 🪙 Toss winners win the match only ~50% of the time —
  barely better than chance

---

## Dashboard Features

- Season filter — analyse any combination of seasons
- 5 interactive Plotly charts with hover details
- Statistical validation with chi-square test
- Metric cards showing live summary stats

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data cleaning and merging (250K+ rows) |
| Plotly Express | Interactive charts |
| Streamlit | Web dashboard and deployment |
| SciPy | Chi-square statistical test |
| PyArrow | Parquet file format for fast loading |

---

## Data Cleaning Highlights

- Standardised team names across 13 seasons
  (e.g. "Delhi Daredevils" → "Delhi Capitals")
- Handled abandoned matches (null winners)
- Merged ball-by-ball data with match metadata
- Engineered: toss_match_win, chasing_team_won, win_type columns

---

## How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/ipl-analytics-dashboard
cd ipl-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## Author
**Kripa Garg** — B.Tech AIML
[GitHub](https://github.com/Kripa-Garg)
