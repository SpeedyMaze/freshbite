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
# DATA LOADING
# ==========================================
def load_data():
    # Balance Sheet Data (in Crores)
    bs_data = pd.DataFrame({
        'Particulars': [
            'Share Capital', 
            'Total Reserves', 
            'Borrowings', 
            'Other N/C Liabilities', 
            'Current Liabilities'
        ],
        'FY2024 (Mar 24)': [868, 21907, 0, 159, 1394],
        'FY2025 (Mar 25)': [907, 33208, 0, 204, 1532]
    })
    
    # P&L Data for BEP (in Crores)
    pl_data = {
        'FY': ['FY 2024', 'FY 2025'],
        'Net_Sales': [6622, 8617],
        'Total_Expenditure': [6089, 7607],
        'Operating_Profit': [533, 1010]
    }
    return bs_data, pd.DataFrame(pl_data)

# ==========================================
# DASHBOARD COMPONENTS
# ==========================================
st.title("📊 Eternal Limited (FY24 & FY25) Financial Dashboard")
st.markdown("Interactive analysis of Balance Sheets, Break-Even Points, and AI Optimization Strategies.")
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
        total_24 = bs_data['FY2024 (Mar 24)'].sum()
        total_25 = bs_data['FY2025 (Mar 25)'].sum()
        
        st.markdown(f"**Total Equity & Liabilities FY24:** ₹{total_24:,} Cr")
        st.markdown(f"**Total Equity & Liabilities FY25:** ₹{total_25:,} Cr")
        st.success(f"Year-over-Year Balance Sheet Growth: {((total_25 - total_24)/total_24)*100:.1f}%")
        
    with col2:
        # Reshape data for visualization
        bs_melt = pd.melt(bs_data, id_vars=['Particulars'], var_name='Financial Year', value_name='Amount (Cr)')
        fig = px.bar(
            bs_melt, 
            x='Particulars', 
            y='Amount (Cr)', 
            color='Financial Year', 
            barmode='group',
            title="Capital Structure Comparison (FY24 vs FY25)"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: BREAK-EVEN ANALYSIS ---
with tab2:
    st.header("Break-Even Point (BEP) Analysis")
    st.markdown("""
    *Note: Exact fixed vs. variable cost splits are not publicly disclosed. For this analysis, we assume 60% of total expenditure is variable (e.g., delivery costs, packaging) and 40% is fixed (e.g., corporate salaries, tech infrastructure, depreciation).*
    """)
    
    # Estimates
    net_sales_25 = 8617
    total_exp_25 = 7607
    fixed_costs = total_exp_25 * 0.40
    variable_costs = total_exp_25 * 0.60
    
    cm_ratio = (net_sales_25 - variable_costs) / net_sales_25
    bep_sales = fixed_costs / cm_ratio
    margin_of_safety = net_sales_25 - bep_sales
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("FY25 Net Sales", f"₹{net_sales_25:,} Cr")
    col_b.metric("Estimated Break-Even Sales", f"₹{int(bep_sales):,} Cr")
    col_c.metric("Margin of Safety", f"₹{int(margin_of_safety):,} Cr", f"{(margin_of_safety/net_sales_25)*100:.1f}%")
    
    # BEP Chart
    sales_range = np.linspace(0, 10000, 100)
    revenue_line = sales_range
    total_cost_line = fixed_costs + (sales_range * (variable_costs / net_sales_25))
    
    fig_bep = go.Figure()
    fig_bep.add_trace(go.Scatter(x=sales_range, y=revenue_line, name="Revenue", line=dict(color="green")))
    fig_bep.add_trace(go.Scatter(x=sales_range, y=total_cost_line, name="Total Cost", line=dict(color="red")))
    fig_bep.add_vline(x=bep_sales, line_dash="dash", line_color="blue", annotation_text=f"BEP: ₹{int(bep_sales)} Cr")
    fig_bep.update_layout(title="Volume-Cost-Profit (VCP) Analysis - FY25", xaxis_title="Sales Volume (₹ Cr)", yaxis_title="Amount (₹ Cr)")
    
    st.plotly_chart(fig_bep, use_container_width=True)

# --- TAB 3: AI INSIGHTS ---
with tab3:
    st.header("Streamlining Operations with AI")
    
    st.markdown("""
    <div class="ai-insight">
        <h4>🤖 The AI Advantage for Eternal Limited</h4>
        <p>With massive growth in reserves (from ₹21,907 Cr to ₹33,208 Cr) and a scaling delivery/quick-commerce network, scaling manual operations is no longer viable. Here is how AI can streamline Eternal Limited's workflow:</p>
        <ul>
            <li><b>Predictive Resource Allocation (Reducing Fixed Costs):</b> AI models can forecast hyper-local demand surges. By dynamically scaling server capacity and logistics deployment ahead of time, Eternal can reduce infrastructure waste, directly lowering the estimated ₹3,042 Cr fixed cost base and lowering the Break-Even Point.</li>
            <li><b>Algorithmic Variable Cost Optimization:</b> Variable costs are currently eating up ~53% of revenue. AI-driven route mapping and batching algorithms can optimize delivery partner routes in real-time, significantly driving down the cost-per-delivery and increasing the Contribution Margin.</li>
            <li><b>Automated Financial Reconciliation:</b> With billions in transactions, deploying AI Agents to handle micro-reconciliations between the payment gateways, restaurants, and the main ledger can eliminate bookkeeping bottlenecks, reducing administrative overhead.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
