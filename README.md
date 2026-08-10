# 🏏 IPL Analytics Dashboard

An interactive analytics dashboard exploring 17 seasons of Indian Premier League cricket — 1,090 matches and 179,000+ ball-by-ball deliveries (2008–2024) — built with Streamlit and Plotly.

🔗 **Live App:** [kripa-garg-ipl-analytics-dashboard-app-ieibcd.streamlit.app](https://kripa-garg-ipl-analytics-dashboard-app-ieibcd.streamlit.app/)

---

## 🎯 Overview

The dashboard turns raw match and delivery-level data into an explorable analytics tool — filterable by season, with dedicated views for team performance, batting, bowling, and venue trends. A statistical validation section backs up the headline finding with a chi-square test rather than just eyeballing a chart.

---

## 🔑 Key Finding

Teams batting second win the majority of IPL matches — a consistent edge across venues and seasons. The dashboard tests whether this is driven by winning the toss (it isn't, largely) using a chi-square test of independence between toss decision and match outcome, with the result (χ², degrees of freedom, and p-value) shown directly in the app.

---

## ✨ Dashboard Features

| Tab | What it shows |
|---|---|
| 📊 **Overview** | IPL titles by team, toss-win vs match-win breakdown, total runs per season trend, toss decision trends over time |
| 🏏 **Team Analysis** | Select any team — matches played, win %, titles, season-by-season win trend, top venues, full head-to-head win % against every opponent |
| ⚡ **Batting** | Top 15 run scorers, strike rate leaders (min. 500 balls faced), batting-second win % trend by season |
| 🎳 **Bowling** | Top 15 wicket takers, best economy rates (min. 300 balls bowled), dot-ball % leaders |
| 🏟️ **Venues** | Batting-second win % by ground (adjustable minimum match threshold), matches hosted per venue, average first-innings score by venue |

Every chart is interactive (hover for details, click legend items to toggle series), and a sidebar season filter re-slices every tab's data live.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas | Data cleaning, merging, and aggregation across 250K+ rows |
| Plotly Express / Graph Objects | Interactive charts |
| Streamlit | Web dashboard framework and deployment |
| SciPy | Chi-square statistical test for the toss/chase analysis |
| PyArrow (Parquet) | Fast columnar data loading |

---

## 🧹 Data Cleaning Highlights

- Standardized team names across 17 seasons of franchise rebranding (e.g. *Delhi Daredevils* → *Delhi Capitals*)
- Handled abandoned matches with no recorded winner
- Merged ball-by-ball delivery data with match-level metadata (season, venue, toss, result)
- Engineered derived columns: `toss_match_win`, `chasing_team_won`, `win_type`
- Auto-detects schema differences between dataset versions (e.g. `batter` vs `batsman` column naming)

---

## 🚀 Run Locally

```bash
git clone https://github.com/Kripa-Garg/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

- `app.py` — Streamlit dashboard (data loading, all 5 tabs, statistical validation)
- `IPL_dashboard.ipynb` — exploratory analysis and data cleaning notebook
- `matches_clean.parquet` — cleaned match-level dataset
- `deliveries_full.parquet` — cleaned ball-by-ball delivery dataset
- `requirements.txt` — Python dependencies
- `README.md` — this file

---

## 👤 Author

**Kripa Garg** — B.Tech AI/ML
[GitHub](https://github.com/Kripa-Garg)
