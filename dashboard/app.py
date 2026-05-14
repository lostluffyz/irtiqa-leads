import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from database.db import get_connection

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Irtiqa AI Lead Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1400px;
    padding: 2rem 2.5rem;
}

/* App background */
.stApp {
    background: #020817;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(37,99,235,0.12), transparent),
        radial-gradient(ellipse 60% 40% at 80% 60%, rgba(99,102,241,0.06), transparent);
    color: #e2e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1326 100%);
    border-right: 1px solid rgba(37,99,235,0.15);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Sidebar inputs */
.stTextInput input {
    background: rgba(15,23,42,0.8) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus {
    border-color: rgba(37,99,235,0.6) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* Metric containers (native) */
div[data-testid="metric-container"] {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(37,99,235,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(37,99,235,0.15) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(37,99,235,0.35) !important;
}

/* Alert */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(37,99,235,0.2) !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: white !important;
}

/* Subheader style */
.stSubheader {
    font-family: 'Syne', sans-serif !important;
}

/* Plotly chart background */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}

/* Remove streamlit branding */
#MainMenu, footer { visibility: hidden; }

/* Divider */
hr {
    border-color: rgba(37,99,235,0.12) !important;
    margin: 2rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD LEADS
# =========================

def load_verified_leads():
    conn = get_connection()
    query = "SELECT * FROM verified_leads ORDER BY verified_at DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# =========================
# LOAD DATA
# =========================

df = load_verified_leads()


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem; display:flex; align-items:center; gap:10px;">
        <div style="
            width:36px; height:36px; border-radius:10px;
            background:linear-gradient(135deg,#1d4ed8,#6366f1);
            display:flex; align-items:center; justify-content:center;
            font-size:18px; flex-shrink:0;
        ">⚡</div>
        <div>
            <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:15px; color:white; line-height:1.2;">Irtiqa AI</div>
            <div style="font-size:11px; color:#475569; letter-spacing:0.05em;">Lead Intelligence</div>
        </div>
    </div>
    <div style="font-family:'Syne',sans-serif; font-size:10px; font-weight:700; letter-spacing:0.12em; color:#334155; text-transform:uppercase; margin-bottom:0.75rem;">Filters</div>
    """, unsafe_allow_html=True)

    company_search = st.text_input("🔍  Search Leads", placeholder="Company, URL, tier...")
    industry_search = st.text_input("🏭  Search Industry", placeholder="e.g. Digital Marketing")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    selected_tier = st.selectbox("Lead Tier", ["All", "Hot Lead", "Warm Lead", "Cold Lead"], key="lead_tier_filter")
    selected_intent = st.selectbox("Intent Level", ["All", "High Intent", "Medium Intent", "Low Intent"], key="intent_filter")

    industry_options = ["All"]
    if not df.empty and "industry_type" in df.columns:
        industry_options += sorted(df["industry_type"].dropna().astype(str).unique().tolist())
    selected_industry = st.selectbox("Industry", industry_options, key="industry_filter")

    st.markdown("<div style='margin-top:2rem; padding-top:1.5rem; border-top:1px solid rgba(37,99,235,0.1);'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px; color:#334155; line-height:1.8;">
        <div>🗄️ &nbsp;SQLite Database</div>
        <div>🤖 &nbsp;AI-Powered Scoring</div>
        <div>📊 &nbsp;Real-time Analytics</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# APPLY FILTERS
# =========================

filtered_df = df.copy()

if company_search:
    company_mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
    if "company_name" in filtered_df.columns:
        company_mask = filtered_df["company_name"].astype(str).str.contains(company_search, case=False, na=False)
    elif "title" in filtered_df.columns:
        company_mask = filtered_df["title"].astype(str).str.contains(company_search, case=False, na=False)

    industry_mask = filtered_df["industry_type"].astype(str).str.contains(company_search, case=False, na=False)
    url_mask = filtered_df["url"].astype(str).str.contains(company_search, case=False, na=False)
    tier_mask = filtered_df["lead_tier"].astype(str).str.contains(company_search, case=False, na=False)

    title_mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
    if "website_title" in filtered_df.columns:
        title_mask = filtered_df["website_title"].astype(str).str.contains(company_search, case=False, na=False)

    filtered_df = filtered_df[company_mask | industry_mask | tier_mask | url_mask | title_mask]

if industry_search:
    filtered_df = filtered_df[filtered_df["industry_type"].astype(str).str.contains(industry_search, case=False, na=False)]

if selected_tier != "All":
    filtered_df = filtered_df[filtered_df["lead_tier"] == selected_tier]

if selected_intent != "All" and "intent_level" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["intent_level"] == selected_intent]

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["industry_type"] == selected_industry]


# =========================
# HERO SECTION
# =========================

st.markdown("""
<div style="
    padding: 3rem 0 2.5rem;
    text-align: center;
    position: relative;
">
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, rgba(37,99,235,0.15), rgba(99,102,241,0.1));
        border: 1px solid rgba(37,99,235,0.25);
        border-radius: 100px;
        padding: 6px 18px;
        font-size: 12px;
        font-weight: 600;
        color: #60a5fa;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        font-family: 'DM Sans', sans-serif;
    ">
        ⚡ AI-Powered Lead Intelligence
    </div>
    <h1 style="
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.2rem, 5vw, 3.8rem);
        font-weight: 800;
        color: white;
        margin: 0 0 1rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    ">
        Irtiqa AI<br>
        <span style="
            background: linear-gradient(135deg, #3b82f6, #818cf8, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">Lead Intelligence</span>
    </h1>
    <p style="
        color: #64748b;
        font-size: 1.1rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 400;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.7;
    ">
        Qualify, score, and prioritize leads with AI — turning raw data into actionable sales intelligence.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# METRICS
# =========================

total_leads = len(filtered_df)
hot_leads = len(filtered_df[filtered_df["lead_tier"] == "Hot Lead"])
warm_leads = len(filtered_df[filtered_df["lead_tier"] == "Warm Lead"])
avg_score = round(filtered_df["lead_score"].mean(), 1) if not filtered_df.empty else 0

col1, col2, col3, col4 = st.columns(4, gap="medium")

def metric_card(label, value, icon, border_color, glow_color, bg_color):
    return f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color};
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        min-height: 160px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 30px {glow_color};
        transition: transform 0.2s ease;
    ">
        <div style="
            position: absolute; top: -30px; right: -20px;
            font-size: 90px; opacity: 0.05; line-height: 1;
            pointer-events: none;
        ">{icon}</div>
        <div style="
            font-size: 13px;
            font-weight: 600;
            color: #64748b;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            font-family: 'DM Sans', sans-serif;
            margin-bottom: 1rem;
        ">{icon} &nbsp;{label}</div>
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            color: white;
            line-height: 1;
        ">{value}</div>
    </div>
    """

with col1:
    st.markdown(metric_card(
        "Total Leads", total_leads, "📊",
        "rgba(59,130,246,0.2)", "rgba(59,130,246,0.08)",
        "linear-gradient(145deg, rgba(15,23,42,0.9), rgba(10,15,30,0.95))"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(metric_card(
        "Hot Leads", hot_leads, "🔥",
        "rgba(34,197,94,0.25)", "rgba(34,197,94,0.1)",
        "linear-gradient(145deg, rgba(3,31,17,0.95), rgba(5,40,20,0.9))"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(metric_card(
        "Warm Leads", warm_leads, "⚡",
        "rgba(251,146,60,0.25)", "rgba(251,146,60,0.08)",
        "linear-gradient(145deg, rgba(60,20,0,0.95), rgba(50,25,5,0.9))"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(metric_card(
        "Avg Score", avg_score, "🎯",
        "rgba(99,102,241,0.25)", "rgba(99,102,241,0.1)",
        "linear-gradient(145deg, rgba(30,27,75,0.95), rgba(20,18,60,0.9))"
    ), unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)


# =========================
# CHARTS
# =========================

st.markdown("""
<div style="
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
">
    📈 &nbsp;Lead Analytics
</div>
""", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2, gap="medium")

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8"),
    title_font=dict(family="Syne, sans-serif", color="white", size=16),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor="rgba(15,23,42,0.5)",
        bordercolor="rgba(37,99,235,0.2)",
        borderwidth=1,
        font=dict(color="#94a3b8")
    )
)

if not filtered_df.empty:
    with chart_col1:
        tier_counts = filtered_df["lead_tier"].value_counts()
        tier_colors = {
            "Hot Lead": "#22c55e",
            "Warm Lead": "#f59e0b",
            "Cold Lead": "#ef4444"
        }
        colors = [tier_colors.get(t, "#3b82f6") for t in tier_counts.index]

        fig1 = go.Figure(data=[go.Pie(
            labels=tier_counts.index,
            values=tier_counts.values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#020817", width=3)),
            textfont=dict(family="DM Sans, sans-serif", color="white"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
        )])
        fig1.update_layout(
            title="Lead Tier Distribution",
            **CHART_LAYOUT,
            annotations=[dict(
                text=f"<b>{total_leads}</b><br>Total",
                x=0.5, y=0.5, font_size=18,
                font=dict(family="Syne, sans-serif", color="white"),
                showarrow=False
            )]
        )
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        industry_counts = filtered_df["industry_type"].value_counts().reset_index()
        industry_counts.columns = ["industry", "count"]

        fig2 = go.Figure(data=[go.Bar(
            x=industry_counts["industry"],
            y=industry_counts["count"],
            marker=dict(
                color=industry_counts["count"],
                colorscale=[[0, "#1d4ed8"], [0.5, "#3b82f6"], [1, "#818cf8"]],
                line=dict(color="rgba(0,0,0,0)", width=0),
                cornerradius=8
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
        )])
        fig2.update_layout(
            title="Industry Distribution",
            xaxis=dict(gridcolor="rgba(37,99,235,0.08)", tickfont=dict(color="#64748b")),
            yaxis=dict(gridcolor="rgba(37,99,235,0.08)", tickfont=dict(color="#64748b")),
            **CHART_LAYOUT
        )
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# =========================
# VERIFIED LEADS TABLE
# =========================

st.markdown("""
<div style="
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1.2rem;
">
    🗂️ &nbsp;Verified Leads
</div>
""", unsafe_allow_html=True)

def color_tier(val):
    if val == "Hot Lead":
        return "background-color: #16a34a; color: white; border-radius: 6px; padding: 2px 8px;"
    elif val == "Warm Lead":
        return "background-color: #d97706; color: white; border-radius: 6px; padding: 2px 8px;"
    elif val == "Cold Lead":
        return "background-color: #dc2626; color: white; border-radius: 6px; padding: 2px 8px;"
    return ""

if not filtered_df.empty:
    company_column = "company_name" if "company_name" in filtered_df.columns else "title"
    display_columns = ["id", company_column, "url", "industry_type", "lead_score", "lead_tier", "confidence", "verified_at"]
    existing_columns = [col for col in display_columns if col in filtered_df.columns]
    display_df = filtered_df[existing_columns]
    styled_df = display_df.style.map(color_tier, subset=["lead_tier"])
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("No leads found matching current filters.")

# CSV Export
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="⬇️  Download Leads CSV",
    data=csv,
    file_name="verified_leads.csv",
    mime="text/csv"
)

st.markdown("<hr>", unsafe_allow_html=True)


# =========================
# LEAD DETAIL VIEWER
# =========================

st.markdown("""
<div style="
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1.2rem;
">
    🔍 &nbsp;Lead Detail Viewer
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No leads available for current filters.")
    st.stop()

lead_ids = filtered_df["id"].tolist()
selected_id = st.selectbox("Select Lead ID", lead_ids, key="lead_detail_selector")
selected_rows = filtered_df[filtered_df["id"] == selected_id]

if selected_rows.empty:
    st.warning("Selected lead not found.")
    st.stop()

selected_lead = selected_rows.iloc[0]


# =========================
# AI LEAD INTELLIGENCE PANEL
# =========================

st.markdown("""
<div style="
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: white;
    margin: 2rem 0 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
">
    <span style="
        background: linear-gradient(135deg, #3b82f6, #818cf8);
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 1.1rem;
    ">🧠</span>
    AI Lead Intelligence Panel
</div>
""", unsafe_allow_html=True)

company_name = str(selected_lead.get("company_name", selected_lead.get("title", "Unknown Company")))
website_url = str(selected_lead.get("url", "N/A"))
industry = str(selected_lead.get("industry_type", "Unknown"))
lead_score = selected_lead.get("lead_score", 0)
lead_tier = str(selected_lead.get("lead_tier", "Unknown"))
confidence = selected_lead.get("confidence", 0)
reasoning = str(selected_lead.get("reasoning", "No reasoning available."))
outreach = str(selected_lead.get("linkedin_message", ""))

tier_color_map = {"Hot Lead": "#22c55e", "Warm Lead": "#f59e0b", "Cold Lead": "#ef4444"}
tier_color = tier_color_map.get(lead_tier, "#3b82f6")
tier_bg_map = {"Hot Lead": "rgba(34,197,94,0.12)", "Warm Lead": "rgba(245,158,11,0.12)", "Cold Lead": "rgba(239,68,68,0.12)"}
tier_bg = tier_bg_map.get(lead_tier, "rgba(59,130,246,0.12)")

col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #0a0f1e, #0d1326);
        border: 1px solid rgba(37,99,235,0.15);
        border-radius: 20px;
        padding: 2rem;
        min-height: 240px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(37,99,235,0.06);
    ">
        <div style="
            position: absolute; bottom: -20px; right: -20px;
            width: 120px; height: 120px; border-radius: 50%;
            background: radial-gradient(circle, rgba(37,99,235,0.08), transparent);
            pointer-events: none;
        "></div>
        <div style="
            display: inline-block;
            background: rgba(37,99,235,0.1);
            border: 1px solid rgba(37,99,235,0.2);
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 600;
            color: #60a5fa;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: 'DM Sans', sans-serif;
            margin-bottom: 1rem;
        ">Company Profile</div>
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 1.7rem;
            font-weight: 800;
            color: white;
            line-height: 1.25;
            margin-bottom: 1.2rem;
        ">{company_name}</div>
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            color: #3b82f6;
            font-size: 0.9rem;
            font-family: 'DM Sans', sans-serif;
            word-break: break-all;
        ">
            🌐 <span>{website_url}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #0a0f1e, #0d1326);
        border: 1px solid rgba(37,99,235,0.15);
        border-radius: 20px;
        padding: 2rem;
        min-height: 240px;
        box-shadow: 0 0 40px rgba(37,99,235,0.06);
    ">
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1.4rem;
        ">📊 Lead Insights</div>
        <div style="display:flex; flex-direction:column; gap:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(37,99,235,0.08); padding-bottom:12px;">
                <span style="font-size:13px; color:#64748b; font-family:'DM Sans',sans-serif; font-weight:500;">Industry</span>
                <span style="font-size:14px; color:#e2e8f0; font-family:'DM Sans',sans-serif; font-weight:600;">{industry}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(37,99,235,0.08); padding-bottom:12px;">
                <span style="font-size:13px; color:#64748b; font-family:'DM Sans',sans-serif; font-weight:500;">Lead Score</span>
                <span style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#3b82f6;">{lead_score}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(37,99,235,0.08); padding-bottom:12px;">
                <span style="font-size:13px; color:#64748b; font-family:'DM Sans',sans-serif; font-weight:500;">Tier</span>
                <span style="
                    background:{tier_bg};
                    border:1px solid {tier_color};
                    border-radius:20px;
                    padding:4px 14px;
                    font-size:13px;
                    font-weight:700;
                    color:{tier_color};
                    font-family:'DM Sans',sans-serif;
                ">{lead_tier}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:13px; color:#64748b; font-family:'DM Sans',sans-serif; font-weight:500;">Confidence</span>
                <span style="font-size:14px; color:#e2e8f0; font-family:'DM Sans',sans-serif; font-weight:600;">{confidence}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# AI REASONING
# =========================

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:white; margin-bottom:0.8rem;">
    🧠 AI Reasoning
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(10,15,30,0.9), rgba(13,19,38,0.95));
    border: 1px solid rgba(37,99,235,0.2);
    border-left: 4px solid #3b82f6;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.8rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.8;
">
    {reasoning}
</div>
""", unsafe_allow_html=True)


# =========================
# PAIN POINTS
# =========================

st.markdown("""
<div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:white; margin-bottom:0.8rem;">
    ⚠️ Detected Pain Points
</div>
""", unsafe_allow_html=True)

try:
    pain_points = json.loads(selected_lead["pain_points"])
except Exception:
    pain_points = []

if pain_points:
    for point in pain_points:
        if isinstance(point, dict):
            category = point.get("category", "Unknown")
            signal = point.get("signal", "")
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(10,15,30,0.9), rgba(13,19,38,0.95));
                border: 1px solid rgba(245,158,11,0.2);
                border-left: 4px solid #f59e0b;
                border-radius: 16px;
                padding: 1.4rem 1.8rem;
                margin-bottom: 1rem;
            ">
                <div style="
                    font-family: 'Syne', sans-serif;
                    font-size: 1rem;
                    font-weight: 700;
                    color: #fbbf24;
                    margin-bottom: 0.6rem;
                ">{category}</div>
                <div style="
                    font-family: 'DM Sans', sans-serif;
                    font-size: 0.9rem;
                    color: #94a3b8;
                    line-height: 1.7;
                ">{signal}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================
# OUTREACH MESSAGE
# =========================

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:white; margin-bottom:0.8rem;">
    ✉️ AI Outreach Message
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(10,15,30,0.95), rgba(13,19,38,0.98));
    border: 1px solid rgba(37,99,235,0.2);
    border-radius: 16px;
    padding: 1.8rem;
    font-family: 'DM Mono', 'Courier New', monospace;
    font-size: 0.9rem;
    color: #e2e8f0;
    line-height: 1.9;
    white-space: pre-wrap;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1d4ed8, #6366f1, #a78bfa);
        border-radius: 16px 16px 0 0;
    "></div>
    <div style="padding-top:0.4rem;">{outreach}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)