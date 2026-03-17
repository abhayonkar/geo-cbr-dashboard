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
    /* Main Background */
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    
    /* Custom Metric Card Styling */
    .metric-container {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        text-align: left;
        transition: transform 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        border-color: rgba(52, 211, 153, 0.4);
    }
    .metric-label {
        color: #9ca3af;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #34d399;
        font-size: 40px;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(52, 211, 153, 0.4);
    }
    .metric-unit {
        font-size: 20px;
        margin-left: 4px;
        opacity: 0.8;
    }

    /* Sidebar Table Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
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
                        textfont=dict(color="white", size=13, family="Inter, bold")
                    ))

                fig.update_layout(
                    barmode='stack',
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="#d1d5db",
                    xaxis_title="Thickness (mm)",
                    yaxis=dict(autorange="reversed", tickfont=dict(size=14, color="white")),
                    margin=dict(l=20, r=20, t=40, b=40),
                    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
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
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)

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