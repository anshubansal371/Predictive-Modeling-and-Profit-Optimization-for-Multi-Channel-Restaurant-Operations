import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Load model & features
# -----------------------------
model = joblib.load("../final_profit_model.pkl")
features = joblib.load("../model_features.pkl")

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Restaurant Profit Decision Dashboard",
    layout="wide"
)

st.title("🍽️ Restaurant Profit Decision Dashboard")
st.markdown(
    """
    This dashboard helps **restaurant managers** understand how  
    **commission rates, channel mix, and delivery strategy**  
    affect **monthly net profit**.
    """
)

# =====================================================
# SIDEBAR – INPUT CONTROLS
# =====================================================
st.sidebar.header("🔧 Strategy Inputs")

commission = st.sidebar.slider(
    "Commission Rate (%)",
    20, 40, 30,
    help="Percentage charged by delivery platforms (Uber Eats / DoorDash)"
) / 100

ue_share = st.sidebar.slider(
    "Uber Eats Share",
    0.0, 0.6, 0.30,
    help="Proportion of total orders from Uber Eats"
)

sd_share = st.sidebar.slider(
    "Self-Delivery Share",
    0.0, 0.5, 0.20,
    help="Orders delivered using restaurant’s own delivery"
)

dd_share = max(0.0, 1 - (ue_share + sd_share))
instore_share = max(0.0, 1 - (ue_share + sd_share + dd_share))

delivery_cost = st.sidebar.slider(
    "Delivery Cost per Order",
    1.0, 6.0, 3.0,
    help="Average cost per self-delivery order"
)

monthly_orders = st.sidebar.number_input(
    "Monthly Orders",
    500, 6000, 2000,
    help="Expected total monthly orders"
)

growth_factor = st.sidebar.slider(
    "Growth Factor",
    0.95, 1.10, 1.02,
    help="Expected demand growth or decline"
)

# =====================================================
# BUILD INPUT ROW SAFELY
# =====================================================
input_data = {
    "InStoreShare": instore_share,
    "UE_TotalShare": ue_share,
    "DD_TotalShare": dd_share,
    "SD_TotalShare": sd_share,
    "CommissionRate": commission,
    "DeliveryCostPerOrder": delivery_cost,
    "TotalCostRate": 0.70,
    "Commission_UE_Interaction": commission * ue_share,
    "DeliveryCost_SD_Interaction": delivery_cost * sd_share,
    "MonthlyOrders": monthly_orders,
    "GrowthAdjustedOrders": monthly_orders * growth_factor
}

input_df = pd.DataFrame(
    [{f: input_data.get(f, 0) for f in features}]
)

# =====================================================
# PROFIT PREDICTION
# =====================================================
predicted_profit = model.predict(input_df)[0]

st.subheader("📊 Predicted Monthly Net Profit")
st.metric(
    "Estimated Net Profit",
    f"{predicted_profit:,.2f}",
    help="Model-predicted profit under current strategy"
)

# =====================================================
# SIMPLE RISK INDICATORS
# =====================================================
st.subheader("⚠️ Risk Indicators")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    if commission > 0.30:
        st.error("High Commission Risk")
        st.caption("Commission is above break-even threshold.")
    else:
        st.success("Commission Risk: Low")

with risk_col2:
    if sd_share > 0.30:
        st.warning("Operational Risk (Self-Delivery)")
        termination_text = "High self-delivery may strain logistics."
    else:
        st.success("Operational Risk: Manageable")

# =====================================================
# SCENARIO ANALYSIS
# =====================================================
st.subheader("🔄 Scenario Comparison")

scenarios = []

# Baseline
scenarios.append(["Current Strategy", predicted_profit])

# UE +10%
ue_sim = input_df.copy()
ue_sim["UE_TotalShare"] *= 1.10
ue_sim["Commission_UE_Interaction"] = ue_sim["UE_TotalShare"] * ue_sim["CommissionRate"]
scenarios.append(["Uber Eats +10%", model.predict(ue_sim)[0]])

# Commission increase
comm_sim = input_df.copy()
comm_sim["CommissionRate"] = 0.30
comm_sim["Commission_UE_Interaction"] = 0.30 * comm_sim["UE_TotalShare"]
scenarios.append(["Commission Increase", model.predict(comm_sim)[0]])

scenario_df = pd.DataFrame(
    scenarios,
    columns=["Scenario", "Predicted Profit"]
)

st.dataframe(scenario_df)

# =====================================================
# PROFIT CHART
# =====================================================
st.subheader("📈 Profit Comparison Chart")

st.bar_chart(
    scenario_df.set_index("Scenario"),
    height=350
)

# =====================================================
# RECOMMENDATIONS PANEL
# =====================================================
st.subheader("🧠 Recommendations")

if commission > 0.30:
    st.warning(
        "Reduce aggregator dependence or renegotiate commissions "
        "to avoid margin erosion."
    )

if sd_share < 0.30:
    st.info(
        "Self-delivery can be expanded gradually to improve margins."
    )

st.success(
    "Use small, incremental changes — profits are sensitive to strategy shifts."
)

# =====================================================
# FOOTER
# =====================================================
st.caption(
    "📌 Predictions are based on historical data and machine learning models. "
    "Use for decision support, not as financial guarantees."
)

