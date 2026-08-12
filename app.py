import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="FreshBite Decision Matrix", layout="wide")

# FIX: Added 'color: #333333;' so the text doesn't turn white in Dark Mode!
st.markdown("""
<style>
    .kpi-container { 
        padding: 1.5rem; 
        border-radius: 8px; 
        background: #f8f9fa; 
        border-left: 5px solid #004085; 
        margin-bottom: 1rem; 
        color: #333333; 
    }
    .status-viable { color: #155724; background-color: #d4edda; padding: 5px 10px; border-radius: 4px; font-weight: 600; }
    .status-unviable { color: #721c24; background-color: #f8d7da; padding: 5px 10px; border-radius: 4px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA MODELS
# ==========================================
def load_data():
    hist_data = pd.DataFrame({
        'Month': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
        'Sales_Volume': [2800, 3000, 3200, 2900, 3500, 3800, 4100, 3900, 4300, 4500, 4200, 4600]
    })
    
    fin = {
        'price': 250,
        'vc_base': 130, 
        'fc_base': 300000,
        'capacity_base': 5000,
        'corp_volume': 600,
        'corp_price': 175,
        'reg_demand_fwd': 4700,
        'outsource_vc': 125,
        'new_sys_fc': 120000,
        'new_sys_vc': 115,
        'new_sys_capex': 1200000,
        'new_sys_cap': 8000
    }
    return hist_data, fin

# ==========================================
# DASHBOARD MODULES
# ==========================================
def render_executive_summary():
    st.title("📊 FreshBite Foods: Strategic Management Dashboard")
    st.markdown("### ⏱️ Executive Recommendation & Option Analysis")
    
    # INTERACTIVE BUTTON / TOGGLE
    st.write("**Select a strategic option below to view the analysis:**")
    selected_option = st.radio(
        "Options:",
        ["Option A: Status Quo", "Option B: Outsource (Recommended)", "Option C: ₹12L New System"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # DYNAMIC CONTENT BASED ON SELECTION
    if "Option A" in selected_option:
        content = """
        <h4 style='margin-top:0;'>Option A: Maintain Current System (Status Quo)</h4>
        <p><b>Status:</b> <span style='color:#d9534f; font-weight:bold;'>❌ UNVIABLE</span></p>
        <p><b>Why:</b> FreshBite's factory is capped at 5,000 bowls/month. The expected forward demand is 5,300 bowls (4,700 regular + 600 corporate). Sticking to the current system forces Ananya to reject guaranteed, profitable revenue from the new corporate client because there isn't enough capacity.</p>
        """
    elif "Option B" in selected_option:
        content = """
        <h4 style='margin-top:0;'>Option B: Outsource Additional Production</h4>
        <p><b>Status:</b> <span style='color:#5cb85c; font-weight:bold;'>✅ VIABLE (RECOMMENDED)</span></p>
        <p><b>Why:</b> Outsourcing requires <b>₹0 initial investment</b> and adds <b>zero fixed costs</b>. It allows FreshBite to fulfill the entire 5,300 bowl demand. Better yet, the outsourced cost is ₹125/bowl (cheaper than the in-house ₹130/bowl), securing a guaranteed ₹50 margin on the corporate order without taking on any long-term risk.</p>
        """
    else:
        content = """
        <h4 style='margin-top:0;'>Option C: Invest in New Semi-Automated System</h4>
        <p><b>Status:</b> <span style='color:#d9534f; font-weight:bold;'>❌ HIGH RISK / UNVIABLE</span></p>
        <p><b>Why:</b> This requires a massive <b>₹12,00,000 CapEx</b> and raises monthly fixed costs by ₹1,20,000 (a 40% increase). While variable costs drop to ₹115, the break-even point jumps drastically. If market prices drop by just 10%, this high fixed-cost structure will destroy profitability.</p>
        """
        
    st.markdown(f'<div class="kpi-container">{content}</div>', unsafe_allow_html=True)
    st.divider()

def render_performance_and_breakeven(hist_data, fin):
    st.header("1. Business Performance & Break-Even Analysis")
    
    cm = fin['price'] - fin['vc_base']
    be_units = fin['fc_base'] / cm
    
    hist_data['Revenue'] = hist_data['Sales_Volume'] * fin['price']
    hist_data['Total_Cost'] = fin['fc_base'] + (hist_data['Sales_Volume'] * fin['vc_base'])
    hist_data['Profit'] = hist_data['Revenue'] - hist_data['Total_Cost']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Capacity", f"{fin['capacity_base']:,} units")
    col2.metric("Contribution Margin", f"₹{cm:.2f} / unit")
    col3.metric("Break-Even Point", f"{int(be_units):,} units")
    col4.metric("Avg Monthly Profit (L12M)", f"₹{hist_data['Profit'].mean():,.0f}")
    
    vol_range = np.linspace(0, 6000, 100)
    rev = vol_range * fin['price']
    tc = fin['fc_base'] + (vol_range * fin['vc_base'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vol_range, y=rev, name='Revenue', line=dict(color='#2ca02c')))
    fig.add_trace(go.Scatter(x=vol_range, y=tc, name='Total Cost', line=dict(color='#d62728')))
    fig.add_vline(x=be_units, line_dash="dash", annotation_text="Break-Even Point")
    fig.update_layout(title="Volume-Cost-Profit (VCP) Analysis", xaxis_title="Units Sold", yaxis_title="INR (₹)", height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_decision_matrix(fin):
    st.header("2. Strategic Options & Corporate Order Analysis")
    st.write("Assumed Forward Demand: **5,300 units** (4,700 Regular @ ₹250 + 600 Corporate @ ₹175)")
    
    data = {
        "Strategic Option": ["A. Status Quo", "B. Outsource (Recommended)", "C. Semi-Automated System"],
        "Viability": ["❌ UNVIABLE", "✅ VIABLE", "❌ UNVIABLE"],
        "CapEx Requirement": ["₹0", "₹0", "₹12,00,000"],
        "New Fixed Cost/Mo": ["₹3,00,000", "₹3,00,000", "₹4,20,000"],
        "Break-Even Point (Units)": ["2,500", "2,500", "3,111"],
        "Demand Fulfilled": ["5,000 (Capped)", "5,300 (100%)", "5,300 (100%)"]
    }
    st.table(pd.DataFrame(data))

def render_sensitivity(fin):
    st.header("3. Risk & Sensitivity Analysis (Base: 4,500 units)")
    
    base_profit = (4500 * fin['price']) - (fin['fc_base'] + 4500 * fin['vc_base'])
    scen_a = (4500 * (fin['price'] * 0.90)) - (fin['fc_base'] + 4500 * fin['vc_base'])
    scen_b = ((4500 * 0.80) * fin['price']) - (fin['fc_base'] + (4500 * 0.80) * fin['vc_base'])
    scen_c = (4500 * fin['price']) - (fin['fc_base'] + 4500 * (fin['vc_base'] * 1.15))
    
    sens_data = pd.DataFrame({
        'Scenario': ['Base Case', 'Price -10%', 'Volume -20%', 'Variable Cost +15%'],
        'Net Profit (₹)': [base_profit, scen_a, scen_b, scen_c]
    })
    
    fig = px.bar(sens_data, x='Scenario', y='Net Profit (₹)', title="Stress Testing Margins", text_auto='.2s', color='Net Profit (₹)', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Management Insight:** A 10% price drop destroys nearly half the profitability. This proves that taking on an extra ₹1,20,000 in fixed costs (Option C) is too high a risk profile for FreshBite's current margins.")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    hist_data, fin = load_data()
    render_executive_summary()
    
    tab1, tab2, tab3 = st.tabs(["📈 Perf. & Break-Even", "🔀 Decision Matrix", "⚠️ Sensitivity"])
    with tab1: render_performance_and_breakeven(hist_data, fin)
    with tab2: render_decision_matrix(fin)
    with tab3: render_sensitivity(fin)
