# 🏏 IPL Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive, multi-tab data analytics dashboard analysing **1,090 IPL matches** and **260,000+ ball-by-ball deliveries** from 2007/08 to 2024. Built entirely in Python using Streamlit and Plotly.

## 🔗 Live Demo

**[👉 Open Live Dashboard](https://kripa-garg-ipl-analytics-dashboard-app-ieibcd.streamlit.app/)**

> No installation needed — open the link and start exploring instantly.

---

## 🔑 Key Finding

> Teams batting second win **52.6%** of IPL matches — consistent across venues and seasons. This dashboard explores why, with statistical validation using a chi-square test.

---

## 📸 Dashboard Preview

### Overview Tab
- IPL titles by team, toss impact analysis, total runs per season trend, toss decision trends across all seasons

### Team Analysis Tab
- Select any IPL team — see matches played, wins, win %, titles, season-by-season performance, win/loss split, top venues, and head-to-head win % against every opponent

### Batting Tab
- Top 15 run scorers of all time, strike rate leaders (min 500 balls faced), batting second win % by season

### Bowling Tab
- Top 15 wicket takers, best economy rates (min 300 balls), dot ball % leaders

### Venues Tab
- Batting second win % by ground, matches hosted per venue, average first innings score by venue

---

## 📊 What This Dashboard Analyses

| Metric | Value |
|--------|-------|
| Total Matches | 1,090 |
| Seasons Covered | 17 (2007/08 – 2024) |
| Total Deliveries | 260,430+ |
| Teams | 14 |
| Batting 2nd Win % | 52.6% |
| Interactive Charts | 13 |

---

## 🛠️ How It Was Built

### 1. Data Collection
- Downloaded two datasets from Kaggle:
  - **matches.csv** — one row per match (season, teams, toss, winner, venue)
  - **deliveries.csv** — one row per ball bowled (batsman, bowler, runs, wickets)

### 2. Data Cleaning (Pandas)
- Standardised team names across 17 seasons — e.g. `"Delhi Daredevils"` → `"Delhi Capitals"`, `"Rising Pune Supergiant"` → `"Rising Pune Supergiants"`
- Dropped abandoned matches (null winners)
- Handled column name differences across dataset versions (`batter` vs `batsman`)
- Engineered 3 new columns:
  - `toss_match_win` — did the toss winner also win the match?
  - `chasing_team_won` — did the team batting second win?
  - `win_type` — won by runs (batting first) or wickets (batting second)

### 3. Data Merging
- Merged ball-by-ball deliveries with match metadata on `match_id` to enable filtering by season and venue at delivery level

### 4. Performance Optimisation
- Converted cleaned CSVs to **Parquet format** — 3-4x faster loading than CSV
- Used `@st.cache_data` decorator in Streamlit — data loads once and is cached, preventing reload on every user interaction

### 5. Analysis & Insights
- Calculated win rates, strike rates, economy rates, and dot ball percentages
- Ran a **chi-square statistical test** to validate the batting second advantage (p-value reported in dashboard)
- Identified venue-wise and season-wise patterns in chasing success

### 6. Visualisation (Plotly)
- All 13 charts are fully interactive — hover for exact values, click legend items to toggle
- Used horizontal bar charts for rankings (easier to read player names)
- Used line charts with spline smoothing for time-series trends
- Used RdYlGn colour scale for venue chase charts (green = batting second wins more, red = wins less)

### 7. Deployment
- Built the web interface using **Streamlit** with a 5-tab layout, sidebar season filter, and metric cards
- Deployed for free on **Streamlit Cloud** — auto-updates whenever the GitHub repo is updated

---

## 🗂️ Repository Structure

```
ipl-analytics-dashboard/
│
├── app.py                    # Main Streamlit app — all 5 tabs and 13 charts
├── ipl_dashboard.ipynb       # Colab notebook — data cleaning, EDA, chart exploration
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes venv and pycache
├── matches_clean.parquet     # Cleaned match-level data
├── deliveries_full.parquet   # Cleaned ball-by-ball data merged with match metadata
└── README.md                 # This file
```

---

## ⚙️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| Pandas | 2.x | Data loading, cleaning, merging, aggregation |
| Plotly Express | 5.x | Interactive charts and visualisations |
| Streamlit | 1.x | Web dashboard and deployment |
| SciPy | 1.x | Chi-square statistical test |
| PyArrow | Latest | Parquet file format for fast loading |
| Google Colab | — | Cloud notebook for data exploration |

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Kripa-Garg/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## 📈 Key Insights Found

- **Mumbai Indians** have won the most IPL titles (5) followed by Chennai Super Kings
- **Teams batting second win 52.6%** of matches — validated statistically (chi-square test)
- **Toss winners win the match only ~50% of the time** — barely better than a coin flip despite the strategic choice
- Teams increasingly **choose to field first** after winning the toss — chasing is now the preferred strategy
- **Total runs per season have grown significantly since 2022** as batting evolved and more matches were added
- Certain venues heavily favour chasing teams while others favour teams batting first

---

## 💡 Skills Demonstrated

- Real-world data cleaning — handling inconsistencies across 17 seasons of data
- Multi-dataset merging — joining 260K+ row delivery data with match metadata
- Statistical analysis — chi-square test for validating insights
- Interactive data visualisation — 13 Plotly charts across 5 tabs
- Performance optimisation — Parquet format + Streamlit caching
- Web app deployment — Streamlit Cloud with public URL

---

## 📂 Data Source

- **Dataset:** [IPL Complete Dataset — Kaggle](https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set)
- **Coverage:** Indian Premier League seasons 2007/08 through 2024
- **Files used:** matches.csv and deliveries.csv

---

## 👤 Author

**Kripa Garg**
B.Tech Artificial Intelligence & Machine Learning

[![GitHub](https://img.shields.io/badge/GitHub-Kripa--Garg-181717?logo=github)](https://github.com/Kripa-Garg)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/kripa-garg-4b26a3320/)

---

*Built as part of an internship preparation portfolio — Python · Data Analysis · Streamlit*
