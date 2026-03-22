import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="CBR-SBG Performance Dashboard",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ENHANCED UI STYLING (CSS)
st.markdown("""
    <style>
    /* ── GLOBAL ───────────────────────────────────────────── */
    html, body, [class*="css"], .stApp {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        font-family: 'Inter', sans-serif;
    }

    /* ── HEADINGS ─────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }

    /* ── ALL GENERIC TEXT & LABELS ────────────────────────── */
    p, span, label, li,
    .stMarkdown p,
    .stMarkdown span,
    div[data-testid="stMarkdownContainer"] p {
        color: #334155 !important;
    }

    /* ── DIVIDER ──────────────────────────────────────────── */
    hr {
        border-color: #cbd5e1 !important;
    }

    /* ── SIDEBAR ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    /* Sidebar table */
    section[data-testid="stSidebar"] table {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    section[data-testid="stSidebar"] th {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        font-weight: 700;
        padding: 8px 12px;
    }
    section[data-testid="stSidebar"] td {
        background-color: #ffffff !important;
        color: #334155 !important;
        padding: 6px 12px;
        border-top: 1px solid #f1f5f9;
    }

    /* ── SELECTBOX / DROPDOWN ─────────────────────────────── */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #1e293b !important;
        background-color: transparent !important;
    }
    div[data-baseweb="select"] svg {
        fill: #475569 !important;
    }
    /* Dropdown open list */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[data-baseweb="menu"],
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
    }
    li[role="option"],
    div[data-baseweb="option"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    li[role="option"]:hover,
    div[data-baseweb="option"]:hover {
        background-color: #eff6ff !important;
        color: #7697f4 !important;
    }
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #7697f4 !important;
        font-weight: 600;
    }

    /* ── BUTTON ───────────────────────────────────────────── */
    .stButton > button {
        background-color: #7697f4 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1e40af !important;
    }

    /* ── INFO / WARNING / ERROR BOXES ─────────────────────── */
    div[data-testid="stNotification"],
    .stAlert {
        border-radius: 10px !important;
    }
    div[data-baseweb="notification"] {
        background-color: #eff6ff !important;
        color: #1e40af !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 10px !important;
    }

    /* ── EXPANDER ─────────────────────────────────────────── */
    details {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 4px 8px;
    }
    details summary {
        color: #1e293b !important;
        font-weight: 600;
    }
    details summary:hover {
        color: #7697f4 !important;
    }
    /* Expander toggle arrow icon */
    details summary svg,
    button[data-testid="stExpanderToggleIcon"] svg,
    div[data-testid="stExpander"] summary svg,
    div[data-testid="stExpander"] button svg {
        fill: #7697f4 !important;
        color: #7697f4 !important;
        stroke: #7697f4 !important;
    }
    /* Streamlit uses span.material-icons for the arrow */
    details summary span[data-testid],
    div[data-testid="stExpander"] span {
        color: #7697f4 !important;
    }

    /* ── MAIN CONTENT HTML TABLE (st.table) ───────────────── */
    div[data-testid="stTable"] table,
    .stTable table {
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        font-size: 14px;
    }
    div[data-testid="stTable"] thead th,
    .stTable thead th {
        background-color: #7697f4 !important;
        color: #ffffff !important;
        font-weight: 700;
        padding: 10px 14px;
        text-align: left;
        border: none !important;
        white-space: nowrap;
    }
    div[data-testid="stTable"] tbody td,
    .stTable tbody td {
        background-color: #ffffff !important;
        color: #1e293b !important;
        padding: 9px 14px;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    div[data-testid="stTable"] tbody tr:nth-child(even) td,
    .stTable tbody tr:nth-child(even) td {
        background-color: #f8fafc !important;
    }
    div[data-testid="stTable"] tbody tr:hover td,
    .stTable tbody tr:hover td {
        background-color: #eff6ff !important;
        color: #7697f4 !important;
    }

    /* ── METRIC CARDS ─────────────────────────────────────── */
    .metric-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        text-align: left;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
    }
    .metric-container:hover {
        transform: translateY(-4px);
        border-color: #93c5fd;
        box-shadow: 0 6px 20px rgba(29, 78, 216, 0.12);
    }
    .metric-label {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #7697f4;
        font-size: 42px;
        font-weight: 700;
    }
    .metric-unit {
        font-size: 20px;
        color: #475569;
        margin-left: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA LOADING
FILE_NAME = "cbr.csv"

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return None

df = load_data()

# 4. SIDEBAR - COST REFERENCE
with st.sidebar:
    st.header("💰 Cost Reference")
    st.markdown("Unit rates used for comparison:")
    cost_ref = {
        "Material": ["BC", "DBM", "WMM", "GSB", "GEOGRID"],
        "Cost": ["9,500", "8,750", "1,850", "1,775", "100"],
        "Unit": ["/m³", "/m³", "/m³", "/m³", "/m²"]
    }
    st.table(pd.DataFrame(cost_ref))
    st.info("Note: Geogrid cost is calculated per Square Meter.")
    
    st.divider()
    
    # Reset Button Logic
    if st.button("🔄 Clear All Selections", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 5. MAIN DASHBOARD HEADER
st.title("Impact of Geogrid Reinforcement on Structural and Functional Performance of Flexible Pavement")
st.markdown("Comparative analysis of Reinforced vs Unreinforced pavement sections.")
st.divider()

if df is not None:
    # 6. SELECTION CONTROLS
    col_c, col_m = st.columns(2)
    
    with col_c:
        cbr_opts = [None] + sorted(df['CBR'].unique().tolist())
        selected_cbr = st.selectbox("Select CBR Value (%)", options=cbr_opts, index=0)
        
    with col_m:
        msa_opts = [None] + sorted(df['MSA'].unique().tolist())
        selected_msa = st.selectbox("Select MSA Value", options=msa_opts, index=0)

    # 7. DASHBOARD LOGIC
    if selected_cbr is not None and selected_msa is not None:
        mask = (df['CBR'] == selected_cbr) & (df['MSA'] == selected_msa)
        filtered_df = df[mask]

        if not filtered_df.empty:
            # Data Extraction
            total_row = filtered_df[filtered_df['Layer'] == 'TOTAL'].iloc[0]
            
            def get_t(layer, col):
                val = filtered_df[filtered_df['Layer'] == layer][col]
                return val.iloc[0] if not val.empty else 0

            # Totals for Labels
            t_un = total_row['Unreinforced_Thickness']
            t_re = total_row['Reinforced_Thickness']
            
            # Categories for Y-axis
            cats = [f"IRC (Unreinforced) [{t_un} mm]", f"GG (Reinforced) [{t_re} mm]"]
            
            # Layer Stacks
            gsb = [get_t("GSB", "Unreinforced_Thickness"), get_t("GSB", "Reinforced_Thickness")]
            geogrid = [0, 10] # Visual divider for GG section
            wmm = [get_t("WMM", "Unreinforced_Thickness"), get_t("WMM", "Reinforced_Thickness")]
            dbm = [get_t("DBM", "Unreinforced_Thickness"), get_t("DBM", "Reinforced_Thickness")]
            bc = [get_t("BC", "Unreinforced_Thickness"), get_t("BC", "Reinforced_Thickness")]

            st.markdown("### Pavement Thickness Analysis")
            col_graph, col_stats = st.columns([2, 1])

            # 8. THE PLOTLY GRAPH
            with col_graph:
                fig = go.Figure()
                
                layers = [
                    ("GSB", gsb, "#f59e0b"),      # Orange
                    ("Geogrid", geogrid, "#4ade80"), # Green
                    ("WMM", wmm, "#3b82f6"),      # Blue
                    ("DBM", dbm, "#ef4444"),      # Red
                    ("BC", bc, "#8b5cf6")         # Purple
                ]

                for name, data, color in layers:
                    fig.add_trace(go.Bar(
                        name=name,
                        y=cats,
                        x=data,
                        orientation='h',
                        marker_color=color,
                        text=[f"{v}mm" if v > 0 else "" for v in data],
                        textposition='inside',
                        insidetextanchor='middle',
                        textfont=dict(color="#ffffff", size=13, family="Inter, bold")
                    ))

                fig.update_layout(
                    barmode='stack',
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='#f8fafc',
                    font=dict(color="#1e293b", family="Inter, sans-serif"),
                    xaxis=dict(
                        title=dict(text="Thickness (mm)", font=dict(color="#475569", size=13)),
                        tickfont=dict(color="#475569", size=12),
                        gridcolor="#e2e8f0",
                        linecolor="#cbd5e1",
                        zerolinecolor="#cbd5e1"
                    ),
                    yaxis=dict(
                        autorange="reversed",
                        tickfont=dict(size=13, color="#0f172a"),
                        gridcolor="#e2e8f0",
                        linecolor="#cbd5e1"
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom", y=1.05,
                        xanchor="right", x=1,
                        font=dict(color="#1e293b", size=13),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#e2e8f0",
                        borderwidth=1
                    ),
                    margin=dict(l=20, r=20, t=40, b=40)
                )
                st.plotly_chart(fig, use_container_width=True)

            # 9. THE BEAUTIFIED METRICS
            with col_stats:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">Cost Reduction</div>
                        <div class="metric-value">{total_row['Cost_Reduction_%']}<span class="metric-unit">%</span></div>
                    </div>
                    <div class="metric-container">
                        <div class="metric-label">Design Life Increase</div>
                        <div class="metric-value">{total_row['Design_Life_Increase_%']}<span class="metric-unit">%</span></div>
                    </div>
                    <div class="metric-container">
                        <div class="metric-label">Total Thickness Saved</div>
                        <div class="metric-value">{t_un - t_re}<span class="metric-unit">mm</span></div>
                    </div>
                """, unsafe_allow_html=True)
                
            # Detailed Table
            with st.expander("📊 View Detailed Layer Calculations"):
                st.table(filtered_df.reset_index(drop=True))

        else:
            st.warning("⚠️ No matching data found in cbr.csv for these parameters.")
    else:
        # Initial Landing State
        st.info("💡 Please select both **CBR** and **MSA** values above to visualize the pavement performance.")
        st.markdown("""
            <div style="text-align: center; padding: 50px; opacity: 0.5;">
                <h1 style="font-size: 100px;">🏗️</h1>
                <p>Awaiting selection...</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error(f"❌ Error: `{FILE_NAME}` not found. Please upload the data file to the project directory.")