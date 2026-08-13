import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Eternal Limited - Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #d32f2f;
        color: #333333;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .ai-insight {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 20px;
        border-left: 5px solid #1976d2;
        color: #0d47a1;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING (FY25 & FY26)
# ==========================================
def load_data():
    # Balance Sheet Data (in Crores)
    bs_data = pd.DataFrame({
        'Particulars': [
            'Share Capital', 
            'Total Reserves', 
            'Borrowings', 
            'Other Liabilities', 
            'Accounts Payable / Current Liab'
        ],
        'FY2025 (Mar 25)': [907, 29410, 0, 3770, 1536],
        'FY2026 (Mar 26)': [910, 30070, 0, 6732, 3010]
    })
    
    # P&L Data for BEP (in Crores)
    pl_data = {
        'FY': ['FY 2025', 'FY 2026'],
        'Net_Sales': [20243, 54364],
        'Total_Expenditure': [19657, 53206],
        'Operating_Profit': [586, 1158]
    }
    return bs_data, pd.DataFrame(pl_data)

# ==========================================
# DASHBOARD COMPONENTS
# ==========================================
st.title("📊 Eternal Limited (FY25 & FY26) Financial Dashboard")
st.markdown("Interactive analysis of Balance Sheets, Break-Even Points, and AI Optimization Strategies for India's Quick Commerce Leader.")
st.divider()

bs_data, pl_data = load_data()

tab1, tab2, tab3 = st.tabs([
    "📈 Balance Sheet Analysis", 
    "⚖️ Break-Even Point (BEP)", 
    "🤖 AI Strategic Insights"
])

# --- TAB 1: BALANCE SHEET ---
with tab1:
    st.header("Balance Sheet (₹ in Crores)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.dataframe(bs_data, hide_index=True, use_container_width=True)
        
        # Calculate Totals
        total_25 = bs_data['FY2025 (Mar 25)'].sum()
        total_26 = bs_data['FY2026 (Mar 26)'].sum()
        
        st.markdown(f"**Total Equity & Liabilities FY25:** ₹{total_25:,} Cr")
        st.markdown(f"**Total Equity & Liabilities FY26:** ₹{total_26:,} Cr")
        st.success(f"Year-over-Year Balance Sheet Growth: {((total_26 - total_25)/total_25)*100:.1f}%")
        
    with col2:
        # Reshape data for visualization
        bs_melt = pd.melt(bs_data, id_vars=['Particulars'], var_name='Financial Year', value_name='Amount (Cr)')
        fig = px.bar(
            bs_melt, 
            x='Particulars', 
            y='Amount (Cr)', 
            color='Financial Year', 
            barmode='group',
            title="Capital Structure Comparison (FY25 vs FY26)"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: BREAK-EVEN ANALYSIS ---
with tab2:
    st.header("Break-Even Point (BEP) Analysis (FY26)")
    st.markdown("""
    *Note: Exact fixed vs. variable cost splits are not publicly disclosed. For this analysis, we assume 70% of total expenditure is variable (e.g., delivery costs, inventory purchases for Quick Commerce) and 30% is fixed (e.g., corporate salaries, dark store leases, tech infrastructure).*
    """)
    
    # Estimates for FY26
    net_sales_26 = 54364
    total_exp_26 = 53206
    fixed_costs = total_exp_26 * 0.30
    variable_costs = total_exp_26 * 0.70
    
    cm_ratio = (net_sales_26 - variable_costs) / net_sales_26
    bep_sales = fixed_costs / cm_ratio
    margin_of_safety = net_sales_26 - bep_sales
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("FY26 Net Sales", f"₹{net_sales_26:,} Cr", "+169% YoY")
    col_b.metric("Estimated Break-Even Sales", f"₹{int(bep_sales):,} Cr")
    col_c.metric("Margin of Safety", f"₹{int(margin_of_safety):,} Cr", f"{(margin_of_safety/net_sales_26)*100:.1f}%")
    
    # BEP Chart
    sales_range = np.linspace(0, 70000, 100)
    revenue_line = sales_range
    total_cost_line = fixed_costs + (sales_range * (variable_costs / net_sales_26))
    
    fig_bep = go.Figure()
    fig_bep.add_trace(go.Scatter(x=sales_range, y=revenue_line, name="Revenue", line=dict(color="green")))
    fig_bep.add_trace(go.Scatter(x=sales_range, y=total_cost_line, name="Total Cost", line=dict(color="red")))
    fig_bep.add_vline(x=bep_sales, line_dash="dash", line_color="blue", annotation_text=f"BEP: ₹{int(bep_sales)} Cr")
    fig_bep.add_vline(x=net_sales_26, line_dash="dot", line_color="black", annotation_text=f"Actual FY26 Sales")
    fig_bep.update_layout(title="Volume-Cost-Profit (VCP) Analysis - FY26", xaxis_title="Sales Volume (₹ Cr)", yaxis_title="Amount (₹ Cr)")
    
    st.plotly_chart(fig_bep, use_container_width=True)

# --- TAB 3: AI INSIGHTS ---
with tab3:
    st.header("Streamlining Quick Commerce Operations with AI")
    
    st.markdown("""
    <div class="ai-insight">
        <h4>🤖 The AI Advantage for Eternal Limited (FY26 Context)</h4>
        <p>With revenue surging 169% year-over-year and operations expanding to over 2,243 dark stores, scaling manual management is no longer viable. Here is how AI can streamline Eternal Limited's workflow to protect its estimated ₹1,158 Cr operating profit:</p>
        <ul>
            <li><b>Hyper-Local Predictive Inventory (Reducing Variable Costs):</b> Quick commerce thrives on speed, but suffers from inventory write-offs. AI models can forecast hyper-local demand surges down to the specific dark store level. By predicting what a neighborhood will order before they order it, Eternal can reduce spoilage and optimize the ₹37,244 Cr variable cost base.</li>
            <li><b>Dynamic Fleet Routing Algorithms:</b> AI-driven route mapping and batching algorithms can optimize delivery partner paths in real-time. Factoring in traffic, weather, and order density, AI ensures more deliveries per hour, directly driving down the cost-per-delivery and increasing the Contribution Margin.</li>
            <li><b>Automated Financial Reconciliation & Anomaly Detection:</b> With ₹54,364 Cr in transaction volume, deploying AI Agents to handle micro-reconciliations between payment gateways, restaurants, FMCG brands, and the main ledger eliminates bookkeeping bottlenecks and detects fraudulent transactions instantly.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
