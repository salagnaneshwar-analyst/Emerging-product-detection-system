"""
app.py
Emerging Products NLP Dashboard — Streamlit
Run: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import numpy as np
import io

# ── Optional heavy libraries (graceful fallback) ──────────────────────────
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    HAS_WC = True
except ImportError:
    HAS_WC = False

from modules.preprocess import preprocess_dataframe
from modules.sentiment import analyze_sentiment, sentiment_summary, product_sentiment
from modules.trends import compute_growth_score, top_keywords, detect_pain_points, monthly_mentions
from modules.utils import compute_kpis, generate_insights, word_cloud_data, df_to_csv_bytes


# ────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Emerging Products Detector",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .main { background: #0d1117; }

    .kpi-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%);
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 2.4rem; font-weight: 700; color: #60a5fa; margin: 0; }
    .kpi-label { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; letter-spacing: 0.5px; }

    .insight-card {
        background: linear-gradient(135deg, #1e2a1e 0%, #1a2e1a 100%);
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #d1fae5;
        font-size: 0.95rem;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        padding: 8px 0 4px;
        border-bottom: 2px solid #2d3748;
        margin-bottom: 16px;
    }

    .stSelectbox label, .stFileUploader label { color: #94a3b8 !important; }
    div[data-testid="stMetricValue"] { color: #60a5fa; }
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# Sidebar
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=60)
    st.title("🚀 Product Radar")
    st.markdown("**NLP-powered Market Intelligence**")
    st.markdown("---")

    uploaded = st.file_uploader("📂 Upload CSV Dataset", type=["csv"])
    st.markdown("---")

    st.markdown("**Filters**")
    st.markdown("*(apply after data loads)*")

    st.markdown("---")
    st.markdown("**Project Info**")
    st.caption("Woxsen University — MBA Business Analytics")
    st.caption("NLP Project: Detect Emerging Products")
    st.caption("Dr. Shyam Krishan | Deadline: 5 May 2026")


# ────────────────────────────────────────────────────────────────────────────
# Load data
# ────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_and_process(raw_bytes: bytes = None):
    if raw_bytes:
        df = pd.read_csv(io.BytesIO(raw_bytes))
    else:
        df = pd.read_csv("data/market_reviews.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = preprocess_dataframe(df)
    df = analyze_sentiment(df)
    return df


with st.spinner("⚙️  Processing data pipeline..."):
    try:
        if uploaded:
            df = load_and_process(uploaded.read())
        else:
            df = load_and_process()
        DATA_OK = True
    except Exception as e:
        st.error(f"❌ Data error: {e}")
        DATA_OK = False

if not DATA_OK:
    st.stop()


# ── Sidebar filters ──────────────────────────────────────────────────────
with st.sidebar:
    all_cats = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
    selected_cat = st.selectbox("📦 Product Category", all_cats)

    all_sources = ["All"] + sorted(df["source"].dropna().unique().tolist())
    selected_source = st.selectbox("🌐 Source Platform", all_sources)

    date_min = df["date"].min().date()
    date_max = df["date"].max().date()
    date_range = st.date_input("📅 Date Range", [date_min, date_max])

fdf = df.copy()
if selected_cat != "All":
    fdf = fdf[fdf["product_category"] == selected_cat]
if selected_source != "All":
    fdf = fdf[fdf["source"] == selected_source]
if len(date_range) == 2:
    fdf = fdf[(fdf["date"].dt.date >= date_range[0]) & (fdf["date"].dt.date <= date_range[1])]


# ────────────────────────────────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────────────────────────────────
st.markdown("## 🚀 Emerging Product Detection Dashboard")
st.markdown("*Real-time NLP-powered market intelligence for early product discovery*")
st.markdown("---")


# ────────────────────────────────────────────────────────────────────────────
# KPI Cards
# ────────────────────────────────────────────────────────────────────────────
kpis = compute_kpis(fdf)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-value">{kpis['total_reviews']:,}</p>
        <p class="kpi-label">TOTAL REVIEWS ANALYZED</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-value">{kpis['unique_products']}</p>
        <p class="kpi-label">UNIQUE PRODUCTS TRACKED</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-value">{kpis['unique_categories']}</p>
        <p class="kpi-label">PRODUCT CATEGORIES</p>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-value">{kpis['positive_sentiment_pct']}%</p>
        <p class="kpi-label">POSITIVE SENTIMENT</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# Tab layout
# ────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trending Products",
    "💬 Sentiment Analysis",
    "🔍 Keyword Insights",
    "🔮 Forecasting",
    "💡 Business Insights"
])


# ── Tab 1: Trending Products ─────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">📈 Product Growth Leaderboard</p>', unsafe_allow_html=True)

    growth = compute_growth_score(fdf)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        if HAS_PLOTLY:
            colors = ["#22c55e" if g >= 40 else "#60a5fa" if g >= 15 else "#f59e0b" if g >= 0 else "#ef4444"
                      for g in growth["growth_score_pct"]]
            fig = go.Figure(go.Bar(
                x=growth["growth_score_pct"],
                y=growth["product_name"],
                orientation="h",
                marker_color=colors,
                text=[f"{v:+.0f}%" for v in growth["growth_score_pct"]],
                textposition="outside"
            ))
            fig.update_layout(
                title="Growth Score: Recent 3 Months vs Prior 3 Months",
                xaxis_title="Growth %",
                yaxis_title="",
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#e2e8f0",
                height=600,
                margin=dict(l=10, r=60, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(growth)

    with col_b:
        st.markdown("**🏆 Top Emerging Products**")
        for _, row in growth.head(10).iterrows():
            emoji_color = "🟢" if row["growth_score_pct"] >= 40 else "🔵" if row["growth_score_pct"] >= 15 else "🟡" if row["growth_score_pct"] >= 0 else "🔴"
            st.markdown(f"{emoji_color} **{row['product_name']}**  \n"
                        f"&nbsp;&nbsp;&nbsp;&nbsp;{row['trend_label']} &nbsp;|&nbsp; "
                        f"`{row['growth_score_pct']:+.1f}%` &nbsp;|&nbsp; "
                        f"{row['recent_mentions']} mentions")

    st.markdown("---")
    st.markdown('<p class="section-header">📅 Product Mention Timeline</p>', unsafe_allow_html=True)

    monthly = monthly_mentions(fdf)
    top5 = growth.head(5)["product_name"].tolist()
    timeline_data = monthly[monthly["product_name"].isin(top5)]

    if HAS_PLOTLY and not timeline_data.empty:
        fig2 = px.line(
            timeline_data,
            x="month_dt", y="mention_count",
            color="product_name",
            markers=True,
            title="Monthly Mention Trend — Top 5 Emerging Products",
            labels={"month_dt": "Month", "mention_count": "Mentions", "product_name": "Product"}
        )
        fig2.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#e2e8f0", height=400
        )
        st.plotly_chart(fig2, use_container_width=True)


# ── Tab 2: Sentiment ─────────────────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-header">💬 Sentiment Analysis</p>', unsafe_allow_html=True)

    summary = sentiment_summary(fdf)
    prod_sent = product_sentiment(fdf)

    col1, col2 = st.columns(2)

    with col1:
        if HAS_PLOTLY:
            fig3 = go.Figure(go.Pie(
                labels=["Positive", "Negative", "Neutral"],
                values=[summary["positive"], summary["negative"], summary["neutral"]],
                hole=0.55,
                marker_colors=["#22c55e", "#ef4444", "#f59e0b"]
            ))
            fig3.update_layout(
                title="Overall Sentiment Distribution",
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
                font_color="#e2e8f0", height=380,
                annotations=[dict(text=f"{summary['positive_pct']}%<br>Positive",
                                  x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#22c55e")]
            )
            st.plotly_chart(fig3, use_container_width=True)

    with col2:
        if HAS_PLOTLY and not prod_sent.empty:
            top_sent = prod_sent.head(12)
            bar_colors = ["#22c55e" if v >= 0 else "#ef4444" for v in top_sent["avg_polarity"]]
            fig4 = go.Figure(go.Bar(
                x=top_sent["product_name"],
                y=top_sent["avg_polarity"],
                marker_color=bar_colors,
                text=[f"{v:.3f}" for v in top_sent["avg_polarity"]],
                textposition="outside"
            ))
            fig4.update_layout(
                title="Average Polarity by Product",
                xaxis_title="Product", yaxis_title="Polarity Score",
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
                font_color="#e2e8f0", height=380,
                xaxis_tickangle=-35
            )
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Sentiment by Platform**")
    if HAS_PLOTLY:
        plat_sent = fdf.groupby(["source", "predicted_sentiment"]).size().reset_index(name="count")
        fig5 = px.bar(
            plat_sent, x="source", y="count", color="predicted_sentiment",
            barmode="group",
            color_discrete_map={"positive": "#22c55e", "negative": "#ef4444", "neutral": "#f59e0b"},
            title="Sentiment Distribution by Platform"
        )
        fig5.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#e2e8f0", height=360
        )
        st.plotly_chart(fig5, use_container_width=True)


# ── Tab 3: Keywords ──────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-header">🔍 Keyword & Topic Insights</p>', unsafe_allow_html=True)

    kw_df = top_keywords(fdf, text_col="cleaned_text", top_n=30)
    pain = detect_pain_points(fdf, text_col="cleaned_text")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📊 Top 20 Keywords by Frequency**")
        if HAS_PLOTLY and not kw_df.empty:
            fig6 = px.bar(
                kw_df.head(20), x="frequency", y="word",
                orientation="h", color="frequency",
                color_continuous_scale="Blues",
                title="Most Frequent Market Keywords"
            )
            fig6.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
                font_color="#e2e8f0", height=520,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.markdown("**⚠️ Customer Pain Points by Product**")
        if HAS_PLOTLY and not pain.empty:
            fig7 = px.bar(
                pain.head(15), x="product_name", y="pain_count",
                color="pain_count", color_continuous_scale="Reds",
                title="Pain Point Mentions per Product"
            )
            fig7.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
                font_color="#e2e8f0", height=520,
                xaxis_tickangle=-35, coloraxis_showscale=False
            )
            st.plotly_chart(fig7, use_container_width=True)
        elif pain.empty:
            st.info("No pain points detected in current filter.")

    # Word cloud
    if HAS_WC:
        st.markdown("**☁️ Market Word Cloud**")
        wc_data = word_cloud_data(fdf)
        if wc_data:
            wc = WordCloud(
                width=1200, height=400,
                background_color="#0d1117",
                colormap="cool",
                max_words=80,
                prefer_horizontal=0.85
            ).generate_from_frequencies(wc_data)
            fig_wc, ax = plt.subplots(figsize=(12, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            fig_wc.patch.set_facecolor("#0d1117")
            st.pyplot(fig_wc)
    else:
        st.markdown("**Top Keywords**")
        st.dataframe(kw_df, use_container_width=True)


# ── Tab 4: Forecasting ───────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-header">🔮 3-Month Demand Forecasting</p>', unsafe_allow_html=True)
    st.info("Linear trend extrapolation — based on historical monthly mention growth.")

    from modules.trends import full_forecast
    forecasts = full_forecast(fdf, top_n=8)

    growth = compute_growth_score(fdf)
    top8 = growth.head(8)["product_name"].tolist()

    if HAS_PLOTLY:
        for product in top8:
            if product not in forecasts:
                continue
            fcast_df = forecasts[product]
            hist = fcast_df[~fcast_df["is_forecast"]]
            pred = fcast_df[fcast_df["is_forecast"]]

            fig8 = go.Figure()
            fig8.add_trace(go.Scatter(
                x=hist["month_dt"], y=hist["mention_count"],
                mode="lines+markers", name="Historical",
                line=dict(color="#60a5fa", width=2.5),
                marker=dict(size=7)
            ))
            if not pred.empty:
                fig8.add_trace(go.Scatter(
                    x=pd.concat([hist["month_dt"].iloc[[-1]], pred["month_dt"]]),
                    y=pd.concat([hist["mention_count"].iloc[[-1]], pred["mention_count"]]),
                    mode="lines+markers", name="Forecast",
                    line=dict(color="#22c55e", width=2.5, dash="dash"),
                    marker=dict(size=8, symbol="diamond")
                ))
            fig8.update_layout(
                title=f"📦 {product} — Demand Forecast",
                xaxis_title="Month", yaxis_title="Predicted Mentions",
                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
                font_color="#e2e8f0", height=280,
                margin=dict(t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig8, use_container_width=True)


# ── Tab 5: Business Insights ─────────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-header">💡 AI-Generated Business Insights</p>', unsafe_allow_html=True)

    growth = compute_growth_score(fdf)
    prod_sent = product_sentiment(fdf)
    insights = generate_insights(growth, prod_sent)

    for ins in insights:
        st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📋 Full Growth Scores Table**")
        st.dataframe(
            growth.style.background_gradient(subset=["growth_score_pct"], cmap="RdYlGn"),
            use_container_width=True, height=420
        )
    with col2:
        st.markdown("**🎯 Product Sentiment Scores**")
        st.dataframe(
            prod_sent.head(20).style.background_gradient(subset=["avg_polarity"], cmap="RdYlGn"),
            use_container_width=True, height=420
        )

    st.markdown("---")
    st.markdown("**📥 Download Reports**")
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.download_button("⬇️ Growth Scores CSV", df_to_csv_bytes(growth),
                           "growth_scores.csv", "text/csv")
    with dc2:
        st.download_button("⬇️ Sentiment Report CSV", df_to_csv_bytes(prod_sent),
                           "sentiment_report.csv", "text/csv")
    with dc3:
        st.download_button("⬇️ Full Dataset CSV", df_to_csv_bytes(fdf),
                           "full_analysis.csv", "text/csv")

    # Power BI section
    st.markdown("---")
    st.markdown('<p class="section-header">📊 Power BI Dashboard — Recommended Visuals & KPIs</p>', unsafe_allow_html=True)
    st.markdown("""
    | # | Visual | Type | Fields |
    |---|--------|------|--------|
    | 1 | **Emerging Products Leaderboard** | Clustered Bar Chart | Product Name × Growth Score % |
    | 2 | **Sentiment Donut** | Donut Chart | Sentiment Label (count) |
    | 3 | **Monthly Mention Trend** | Line Chart | Date × Mention Count (by Product) |
    | 4 | **Product Category Heatmap** | Matrix | Category × Sentiment |
    | 5 | **Platform Source Breakdown** | Pie Chart | Source × Count |
    | 6 | **Pain Point Ranking** | Horizontal Bar | Product × Pain Count |
    | 7 | **Top KPIs** | Card Visuals | Total Reviews, Unique Products, Avg Polarity |
    | 8 | **Word Cloud** | Word Cloud visual | Top 50 Keywords |
    | 9 | **Forecast Table** | Table | Product, Recent, Prior, Growth %, Trend |
    | 10 | **Geo Slicer** | Slicer | Source Platform (multi-select) |

    **DAX Measures:**
    ```
    Growth % = DIVIDE([Recent Mentions] - [Prior Mentions], [Prior Mentions]) * 100
    Positive % = DIVIDE(COUNTROWS(FILTER(Reviews, Reviews[Sentiment]="positive")), COUNTROWS(Reviews)) * 100
    Avg Polarity = AVERAGE(Reviews[polarity_score])
    ```
    """)
