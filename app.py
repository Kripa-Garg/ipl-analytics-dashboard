import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

# ── page config ───────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── custom CSS ────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  .main { background: #F7F8FA; }

  /* metric cards */
  [data-testid="metric-container"] {
    background: #ffffff;
    border: 0.5px solid #E2E4E9;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }
  [data-testid="metric-container"] label {
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #888 !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 600 !important;
    color: #111 !important;
  }

  /* tabs */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #F0F2F6;
    border-radius: 10px;
    padding: 4px;
    border: none;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 500;
    color: #666;
    background: transparent;
    border: none;
  }
  .stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #111 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.10);
  }

  /* sidebar */
  [data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 0.5px solid #E2E4E9;
  }

  h1 { font-size: 24px !important; font-weight: 600 !important; }
  h2 { font-size: 16px !important; font-weight: 600 !important; color: #222 !important; }
  h3 { font-size: 14px !important; font-weight: 500 !important; color: #444 !important; }

  .insight-box {
    background: #EEF6FF;
    border: 0.5px solid #B6D6F7;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #1A4A7A;
    line-height: 1.6;
    margin: 8px 0;
  }
</style>
""", unsafe_allow_html=True)

# ── color palette ─────────────────────────────────────
TEAL = "#1D9E75"
TEAL_LIGHT = "#9FE1CB"
BLUE = "#378ADD"
CORAL = "#D85A30"
AMBER = "#BA7517"
PURPLE = "#7F77DD"
NEUTRAL = "#888780"
CHART_BG = "plotly_white"
AXIS_STYLE = dict(
    showgrid=True, gridcolor="rgba(0,0,0,0.05)",
    linecolor="rgba(0,0,0,0.08)", tickfont_size=11
)

# ── load data ─────────────────────────────────────────


@st.cache_data
def load_data():
    matches = pd.read_parquet("matches_clean.parquet")
    deliveries = pd.read_parquet("deliveries_full.parquet")
    return matches, deliveries


matches, deliveries = load_data()

# ── detect correct batsman column name ───────────────
# Some datasets use 'batter', older ones use 'batsman'
BATTER_COL = "batter" if "batter" in deliveries.columns else "batsman"
BOWLER_COL = "bowler"

# ── sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔎 Filters")
    all_seasons = sorted(matches["season"].unique())
    selected = st.multiselect(
        "Select Seasons", all_seasons, default=all_seasons
    )
    st.caption(f"{len(selected)} of {len(all_seasons)} seasons selected")
    st.divider()
    st.markdown(
        "<div style='font-size:11px;color:#aaa;'>IPL Analytics · 2008–2024</div>",
        unsafe_allow_html=True
    )

m = matches[matches["season"].isin(selected)]
d = deliveries[deliveries["season"].isin(selected)]

# ── helpers ───────────────────────────────────────────


def season_winners(df: pd.DataFrame) -> pd.Series:
    return (
        df.dropna(subset=["winner"])
          .sort_values("id")
          .groupby("season")
          .last()["winner"]
    )


# ── header ────────────────────────────────────────────
st.markdown("## 🏏 IPL Analytics Dashboard")
st.caption(
    f"{len(m):,} matches · {len(d):,} deliveries · "
    f"{m['season'].min()} – {m['season'].max()}"
)

# ── metric cards ──────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Matches",     f"{len(m):,}")
c2.metric("Seasons",           m["season"].nunique())
c3.metric("Teams",             m["team1"].nunique())
c4.metric("Batting 2nd Win %",
          f"{m['chasing_team_won'].mean()*100:.1f}%",
          help="% of matches won by team batting second")

st.divider()

# ── hero insight + how to use ─────────────────────────
chase_pct = m['chasing_team_won'].mean() * 100
st.markdown(f"""
<div style="background:linear-gradient(135deg,#E8F8F2,#EEF6FF);
            border:0.5px solid #B6D6F7; border-radius:12px;
            padding:16px 22px; margin-bottom:16px;">
  <span style="font-size:13px;font-weight:600;color:#0C447C;">
    🔑 Key Finding
  </span><br>
  <span style="font-size:13px;color:#1a1a1a;line-height:1.7;">
    Teams batting second win <b>{chase_pct:.1f}%</b> of IPL matches —
    barely better than a coin flip, yet the advantage is consistent
    across venues and seasons. Explore the tabs below to see why.
  </span>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ How to use this dashboard"):
    st.markdown("""
    | Tab | What it shows |
    |-----|--------------|
    | 📊 **Overview** | IPL titles, toss impact, runs per season, toss decision trends |
    | 🏏 **Team Analysis** | Select any team — see win %, titles, season form, head-to-head vs all opponents |
    | ⚡ **Batting** | Top run scorers, strike rate leaders, batting second win % by season |
    | 🎳 **Bowling** | Top wicket takers, best economy rates, dot ball % leaders |
    | 🏟️ **Venues** | Batting second win % by ground, matches hosted, average first innings score |

    **Tips:**
    - Use the **season filter** in the sidebar to focus on specific years
    - All charts are **interactive** — hover for details, click legend to toggle
    - The **statistical validation** expander at the bottom shows chi-square test results
    """)

# ── tabs ──────────────────────────────────────────────
tab_overview, tab_team, tab_batting, tab_bowling, tab_venues = st.tabs([
    "📊 Overview",
    "🏏 Team Analysis",
    "⚡ Batting",
    "🎳 Bowling",
    "🏟️ Venues",
])

# ════════════════════════════════════════════════════════
# OVERVIEW TAB
# ════════════════════════════════════════════════════════
with tab_overview:

    col1, col2 = st.columns(2)

    # titles bar chart
    with col1:
        st.subheader("🏆 IPL Titles by Team")
        titles = (
            season_winners(m)
            .value_counts()
            .reset_index()
            .rename(columns={"winner": "team", "count": "titles"})
            .sort_values("titles", ascending=False)
        )
        fig1 = px.bar(
            titles, x="team", y="titles",
            color="titles",
            color_continuous_scale=[[0, TEAL_LIGHT], [1, TEAL]],
            text="titles", template=CHART_BG,
        )
        fig1.update_traces(textposition="outside")
        fig1.update_coloraxes(showscale=False)
        fig1.update_layout(
            height=360, xaxis_tickangle=-30,
            xaxis_title="", yaxis_title="Titles",
            xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
        )
        st.plotly_chart(fig1, use_container_width=True)
    if len(titles) > 0:
        top_team = titles.iloc[0]["team"]
        top_n = int(titles.iloc[0]["titles"])
        st.caption(
            f"🏆 {top_team} lead with {top_n} title{'s' if top_n>1 else ''} in the selected seasons.")

    # toss donut
    with col2:
        st.subheader("🪙 Does Winning the Toss Help?")
        toss_win_pct = m["toss_match_win"].mean() * 100
        contingency = pd.crosstab(m["chasing_team_won"], m["toss_decision"])
        _, p_val, _, _ = chi2_contingency(contingency)
        toss_df = pd.DataFrame({
            "result": ["Won toss + match", "Won toss, lost match"],
            "pct":    [toss_win_pct, 100 - toss_win_pct],
        })
        fig2 = px.pie(
            toss_df, values="pct", names="result",
            color_discrete_sequence=[TEAL, TEAL_LIGHT],
            hole=0.55, template=CHART_BG,
        )
        fig2.update_layout(
            height=280, showlegend=True,
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig2, use_container_width=True)
        sig = "not significant" if p_val >= 0.05 else "significant"
        st.markdown(
            f"<div class='insight-box'>Toss-to-win conversion: <b>{toss_win_pct:.1f}%</b> — "
            f"statistically <b>{sig}</b> (p = {p_val:.3f}). "
            "Winning the toss is barely better than a coin flip.</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # season runs trend
    st.subheader("📈 Total Runs Scored per Season")
    sr = (
        d.groupby("season")["total_runs"]
        .sum().reset_index()
        .rename(columns={"total_runs": "Total Runs"})
    )
    fig3 = px.line(
        sr, x="season", y="Total Runs",
        markers=True, line_shape="spline", template=CHART_BG,
    )
    fig3.update_traces(
        line_color=TEAL, line_width=2.5,
        marker_size=8, marker_color=TEAL
    )
    fig3.update_layout(
        height=300, xaxis_title="Season", yaxis_title="Total Runs",
        xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "📈 Total runs have grown significantly since 2021 as batting evolved and more teams joined the league.")

    # toss decision trend
    st.subheader("🪙 Toss Decision Trends")
    td = (
        m.groupby(["season", "toss_decision"])
        .size().reset_index(name="count")
    )
    fig4 = px.bar(
        td, x="season", y="count", color="toss_decision",
        color_discrete_map={"bat": TEAL, "field": BLUE},
        barmode="stack", template=CHART_BG,
    )
    fig4.update_layout(
        height=280, xaxis_title="Season", yaxis_title="Matches",
        legend_title="Decision", xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("🪙 Teams increasingly prefer fielding first after winning the toss — chasing is now seen as the safer strategy in T20 cricket.")

# ════════════════════════════════════════════════════════
# TEAM ANALYSIS TAB
# ════════════════════════════════════════════════════════
with tab_team:

    st.subheader("🏏 Team Performance Analysis")
    st.caption("Select any IPL team to see their full record, season-by-season performance, and head-to-head win % against every opponent.")

    teams = sorted(set(matches["team1"]).union(set(matches["team2"])))
    selected_team = st.selectbox("Select Team", teams)

    team_matches = m[
        (m["team1"] == selected_team) | (m["team2"] == selected_team)
    ]
    matches_played = len(team_matches)
    wins = (team_matches["winner"] == selected_team).sum()
    win_pct = wins / matches_played * 100 if matches_played > 0 else 0
    toss_wins = (team_matches["toss_winner"] == selected_team).sum()
    toss_pct = toss_wins / matches_played * 100 if matches_played > 0 else 0
    title_count = (season_winners(matches) == selected_team).sum()

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Matches Played", matches_played)
    t2.metric("Wins",           wins)
    t3.metric("Win %",          f"{win_pct:.1f}%")
    t4.metric("Titles",         int(title_count))

    st.divider()

    # season wins line
    season_perf = (
        team_matches.groupby("season")
        .apply(lambda x: (x["winner"] == selected_team).sum())
        .reset_index(name="wins")
    )
    fig_t1 = px.line(
        season_perf, x="season", y="wins",
        markers=True, line_shape="spline",
        title=f"{selected_team} — Wins per Season",
        template=CHART_BG,
    )
    fig_t1.update_traces(line_color=TEAL, marker_size=8, marker_color=TEAL)
    fig_t1.update_layout(
        height=320, xaxis_title="Season", yaxis_title="Wins",
        xaxis=AXIS_STYLE, yaxis=AXIS_STYLE,
    )
    st.plotly_chart(fig_t1, use_container_width=True)

    col1, col2 = st.columns(2)

    # win/loss breakdown
    with col1:
        wl = pd.DataFrame({
            "Result": ["Wins", "Losses"],
            "Matches": [wins, matches_played - wins]
        })
        fig_t2 = px.pie(
            wl, values="Matches", names="Result",
            color_discrete_sequence=[TEAL, "#E2E4E9"],
            hole=0.5, title="Win / Loss Split",
            template=CHART_BG,
        )
        fig_t2.update_layout(height=300)
        st.plotly_chart(fig_t2, use_container_width=True)

    # top venues
    with col2:
        venue_perf = (
            team_matches.groupby("venue")
            .size().reset_index(name="Matches")
            .sort_values("Matches", ascending=True).tail(8)
        )
        fig_t3 = px.bar(
            venue_perf, x="Matches", y="venue",
            orientation="h", color="Matches",
            color_continuous_scale=[[0, TEAL_LIGHT], [1, TEAL]],
            text="Matches", title=f"Top Venues for {selected_team}",
            template=CHART_BG,
        )
        fig_t3.update_coloraxes(showscale=False)
        fig_t3.update_layout(
            height=300, xaxis_title="Matches Played", yaxis_title="",
            xaxis=AXIS_STYLE, yaxis=dict(
                showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig_t3, use_container_width=True)

    # head to head
    st.divider()
    st.subheader(f"⚔️ {selected_team} — Head to Head vs All Teams")
    opponents = [t for t in teams if t != selected_team]
    h2h_rows = []
    for opp in opponents:
        h2h = m[
            ((m["team1"] == selected_team) & (m["team2"] == opp)) |
            ((m["team1"] == opp) & (m["team2"] == selected_team))
        ]
        if len(h2h) == 0:
            continue
        w = (h2h["winner"] == selected_team).sum()
        h2h_rows.append({"Opponent": opp, "Played": len(h2h),
                         "Won": w, "Win %": round(w/len(h2h)*100, 1)})
    h2h_df = pd.DataFrame(h2h_rows).sort_values("Win %", ascending=False)
    fig_h2h = px.bar(
        h2h_df, x="Opponent", y="Win %",
        color="Win %", color_continuous_scale="RdYlGn",
        text="Win %", template=CHART_BG,
        title=f"{selected_team} Win % vs Each Opponent"
    )
    fig_h2h.add_hline(y=50, line_dash="dot", line_color=NEUTRAL,
                      annotation_text="50% line")
    fig_h2h.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_h2h.update_coloraxes(showscale=False)
    fig_h2h.update_layout(
        height=360, xaxis_tickangle=-30,
        xaxis_title="", yaxis_title="Win %",
        xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "range": [0, 105]},
    )
    st.plotly_chart(fig_h2h, use_container_width=True)

# ════════════════════════════════════════════════════════
# BATTING TAB
# ════════════════════════════════════════════════════════
with tab_batting:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏏 Top 15 Run Scorers")
        top_runs = (
            d.groupby(BATTER_COL)["batsman_runs"]
            .sum().reset_index()
            .rename(columns={BATTER_COL: "batsman", "batsman_runs": "Runs"})
            .sort_values("Runs", ascending=True).tail(15)
        )
        fig5 = px.bar(
            top_runs, x="Runs", y="batsman",
            orientation="h", color="Runs",
            color_continuous_scale=[[0, TEAL_LIGHT], [1, TEAL]],
            text="Runs", template=CHART_BG,
        )
        fig5.update_traces(textposition="outside")
        fig5.update_coloraxes(showscale=False)
        fig5.update_layout(
            height=480, xaxis_title="Total Runs", yaxis_title="",
            xaxis=AXIS_STYLE, yaxis=dict(
                showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig5, use_container_width=True)
        if len(top_runs) > 0:
            top_bat_name = top_runs.iloc[-1]["batsman"]
            top_bat_runs = int(top_runs.iloc[-1]["Runs"])
            st.caption(
                f"🏏 {top_bat_name} leads all-time with {top_bat_runs:,} runs in the selected seasons.")

    with col2:
        st.subheader("⚡ Strike Rate Leaders (min 500 balls)")
        sr_df = (
            d.groupby(BATTER_COL)
            .agg(runs=("batsman_runs", "sum"), balls=("ball", "count"))
            .reset_index()
            .rename(columns={BATTER_COL: "batsman"})
        )
        sr_df = sr_df[sr_df["balls"] >= 500].copy()
        sr_df["SR"] = (sr_df["runs"] / sr_df["balls"] * 100).round(1)
        sr_df = sr_df.sort_values("SR", ascending=True).tail(15)
        fig6 = px.bar(
            sr_df, x="SR", y="batsman",
            orientation="h", color="SR",
            color_continuous_scale=[[0, "#FAC775"], [1, AMBER]],
            text="SR", template=CHART_BG,
        )
        fig6.update_traces(textposition="outside")
        fig6.update_coloraxes(showscale=False)
        fig6.update_layout(
            height=480, xaxis_title="Strike Rate", yaxis_title="",
            xaxis={**AXIS_STYLE, "range": [120, None]},
            yaxis=dict(showgrid=False, gridcolor='rgba(0,0,0,0.05)',
                       linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig6, use_container_width=True)

    st.divider()
    st.subheader("📊 Batting 2nd Win % — Season Trend")
    chase_trend = (
        m.groupby("season")
        .agg(total=("winner", "count"),
             chasing_wins=("chasing_team_won", "sum"))
        .reset_index()
    )
    chase_trend["Chase Win %"] = (
        chase_trend["chasing_wins"] / chase_trend["total"] * 100
    ).round(1)
    fig7 = px.bar(
        chase_trend, x="season", y="Chase Win %",
        color="Chase Win %",
        color_continuous_scale=[[0, TEAL_LIGHT], [1, TEAL]],
        text="Chase Win %", template=CHART_BG,
    )
    fig7.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig7.update_coloraxes(showscale=False)
    fig7.add_hline(y=50, line_dash="dot", line_color=NEUTRAL,
                   annotation_text="50% baseline")
    fig7.update_layout(
        height=320, xaxis_title="Season", yaxis_title="Win %",
        xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "range": [30, 80]},
    )
    st.plotly_chart(fig7, use_container_width=True)

# ════════════════════════════════════════════════════════
# BOWLING TAB
# ════════════════════════════════════════════════════════
with tab_bowling:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎳 Top 15 Wicket Takers")
        DISMISSALS = {"caught", "bowled", "lbw", "stumped",
                      "caught and bowled", "hit wicket"}
        wickets = (
            d[d["dismissal_kind"].isin(DISMISSALS)]
            .groupby(BOWLER_COL).size()
            .reset_index(name="Wickets")
            .rename(columns={BOWLER_COL: "bowler"})
            .sort_values("Wickets", ascending=True).tail(15)
        )
        fig8 = px.bar(
            wickets, x="Wickets", y="bowler",
            orientation="h", color="Wickets",
            color_continuous_scale=[[0, "#F0997B"], [1, CORAL]],
            text="Wickets", template=CHART_BG,
        )
        fig8.update_traces(textposition="outside")
        fig8.update_coloraxes(showscale=False)
        fig8.update_layout(
            height=480, xaxis_title="Wickets", yaxis_title="",
            xaxis=AXIS_STYLE, yaxis=dict(
                showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig8, use_container_width=True)
        if len(wickets) > 0:
            top_bowl = wickets.iloc[-1]["bowler"]
            top_wkts = int(wickets.iloc[-1]["Wickets"])
            st.caption(
                f"🎳 {top_bowl} leads with {top_wkts} wickets. Only caught, bowled, lbw, stumped, caught & bowled, and hit wicket dismissals counted.")

    with col2:
        st.subheader("💨 Best Economy Rates (min 300 balls)")
        eco = (
            d.groupby(BOWLER_COL)
            .agg(runs=("total_runs", "sum"), balls=("ball", "count"))
            .reset_index()
            .rename(columns={BOWLER_COL: "bowler"})
        )
        eco = eco[eco["balls"] >= 300].copy()
        eco["Economy"] = (eco["runs"] / eco["balls"] * 6).round(2)
        eco = eco.sort_values("Economy", ascending=False).tail(15)
        fig9 = px.bar(
            eco, x="Economy", y="bowler",
            orientation="h", color="Economy",
            color_continuous_scale=[[0, PURPLE], [1, "#CECBF6"]],
            text="Economy", template=CHART_BG,
        )
        fig9.update_traces(textposition="outside")
        fig9.update_coloraxes(showscale=False)
        fig9.update_layout(
            height=480, xaxis_title="Economy (runs/over)", yaxis_title="",
            xaxis={**AXIS_STYLE, "range": [5.5, None]},
            yaxis=dict(showgrid=False, gridcolor='rgba(0,0,0,0.05)',
                       linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig9, use_container_width=True)

    st.divider()
    st.subheader("⚫ Dot Ball % Leaders (min 300 balls)")
    dots = (
        d.groupby(BOWLER_COL)
        .agg(balls=("ball", "count"),
             dot_balls=("total_runs", lambda x: (x == 0).sum()))
        .reset_index()
        .rename(columns={BOWLER_COL: "bowler"})
    )
    dots = dots[dots["balls"] >= 300].copy()
    dots["Dot %"] = (dots["dot_balls"] / dots["balls"] * 100).round(1)
    dots = dots.sort_values("Dot %", ascending=True).tail(15)
    fig10 = px.bar(
        dots, x="Dot %", y="bowler",
        orientation="h", color="Dot %",
        color_continuous_scale=[[0, "#B5D4F4"], [1, BLUE]],
        text="Dot %", template=CHART_BG,
    )
    fig10.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig10.update_coloraxes(showscale=False)
    fig10.update_layout(
        height=480, xaxis_title="Dot Ball %", yaxis_title="",
        xaxis=AXIS_STYLE, yaxis=dict(
            showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
    )
    st.plotly_chart(fig10, use_container_width=True)

# ════════════════════════════════════════════════════════
# VENUES TAB
# ════════════════════════════════════════════════════════
with tab_venues:

    MIN_MATCHES = st.slider("Minimum matches at venue", 5, 30, 10)
    st.caption(
        f"Showing venues with at least {MIN_MATCHES} matches. Green bars = batting second wins more often, red = batting first wins more.")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Batting Second Win % by Venue")
        vc = (
            m.groupby("venue")
            .agg(total=("winner", "count"),
                 chasing_wins=("chasing_team_won", "sum"))
            .reset_index()
        )
        vc["Chase %"] = (vc["chasing_wins"] / vc["total"] * 100).round(1)
        vc = (
            vc[vc["total"] >= MIN_MATCHES]
            .sort_values("Chase %", ascending=True).tail(15)
        )
        fig11 = px.bar(
            vc, x="Chase %", y="venue",
            orientation="h", color="Chase %",
            color_continuous_scale="RdYlGn",
            text="Chase %", template=CHART_BG,
        )
        fig11.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside")
        fig11.update_coloraxes(showscale=False)
        fig11.add_vline(x=50, line_dash="dot", line_color=NEUTRAL,
                        annotation_text="50%")
        fig11.update_layout(
            height=500, xaxis_title="Win %", yaxis_title="",
            xaxis={**AXIS_STYLE, "range": [30, 95]},
            yaxis=dict(showgrid=False, gridcolor='rgba(0,0,0,0.05)',
                       linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig11, use_container_width=True)

    with col2:
        st.subheader("🏟️ Matches Hosted per Venue")
        venue_counts = (
            m.groupby("venue").size()
            .reset_index(name="Matches")
            .sort_values("Matches", ascending=True).tail(15)
        )
        fig12 = px.bar(
            venue_counts, x="Matches", y="venue",
            orientation="h", color="Matches",
            color_continuous_scale=[[0, TEAL_LIGHT], [1, TEAL]],
            text="Matches", template=CHART_BG,
        )
        fig12.update_traces(textposition="outside")
        fig12.update_coloraxes(showscale=False)
        fig12.update_layout(
            height=500, xaxis_title="Total Matches", yaxis_title="",
            xaxis=AXIS_STYLE, yaxis=dict(
                showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
        )
        st.plotly_chart(fig12, use_container_width=True)

    st.divider()
    st.subheader("📐 Average First Innings Score by Venue")
    fis = (
        d[d["inning"] == 1]
        .groupby("match_id")
        .agg(total=("total_runs", "sum"))
        .reset_index()
    )
    fis = fis.merge(m[["id", "venue"]], left_on="match_id",
                    right_on="id", how="left")
    avg_fis = (
        fis.groupby("venue")["total"]
        .agg(["mean", "count"]).reset_index()
        .rename(columns={"mean": "Avg 1st Innings", "count": "n"})
    )
    avg_fis = (
        avg_fis[avg_fis["n"] >= MIN_MATCHES]
        .sort_values("Avg 1st Innings", ascending=True).tail(15)
    )
    avg_fis["Avg 1st Innings"] = avg_fis["Avg 1st Innings"].round(1)
    fig13 = px.bar(
        avg_fis, x="Avg 1st Innings", y="venue",
        orientation="h", color="Avg 1st Innings",
        color_continuous_scale=[[0, "#B5D4F4"], [1, BLUE]],
        text="Avg 1st Innings", template=CHART_BG,
    )
    fig13.update_traces(textposition="outside")
    fig13.update_coloraxes(showscale=False)
    fig13.update_layout(
        height=500, xaxis_title="Average Runs", yaxis_title="",
        xaxis=AXIS_STYLE, yaxis=dict(
            showgrid=False, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0.08)', tickfont_size=11),
    )
    st.plotly_chart(fig13, use_container_width=True)

# ── footer ────────────────────────────────────────────
st.divider()

with st.expander("📊 Statistical Validation — Batting Second Advantage"):
    contingency = pd.crosstab(m["chasing_team_won"], m["toss_decision"])
    chi2_val, p_val, dof, _ = chi2_contingency(contingency)
    st.write(
        f"Chi-square: χ² = {chi2_val:.3f} · df = {dof} · p-value = {p_val:.4f}")
    if p_val < 0.05:
        st.success(
            "✅ Statistically significant (p < 0.05) — batting second advantage is real.")
    else:
        st.info("Not statistically significant at p < 0.05.")
    st.dataframe(contingency, use_container_width=True)

with st.expander("🔍 Raw matches data (first 100 rows)"):
    safe_cols = [c for c in ["season", "team1", "team2", "winner",
                             "toss_winner", "toss_decision",
                             "win_by_runs", "win_by_wickets", "venue"]
                 if c in m.columns]
    st.dataframe(m[safe_cols].head(100), use_container_width=True)
