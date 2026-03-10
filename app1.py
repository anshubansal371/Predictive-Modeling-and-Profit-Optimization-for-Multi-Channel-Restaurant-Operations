import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Load saved model & features
# -----------------------------
model = joblib.load("final_profit_model.pkl")
features = joblib.load("model_features.pkl")

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Restaurant Profit Simulator", layout="wide")

st.title("🍽️ Restaurant Profit Prediction Dashboard")
st.write("Simple what-if profit simulation using a trained ML model")

# -----------------------------
# Sidebar – Inputs
# -----------------------------
st.sidebar.header("🔧 Scenario Inputs")

commission = st.sidebar.slider("Commission Rate (%)", 20, 40, 30) / 100
ue_share = st.sidebar.slider("Uber Eats Share", 0.0, 0.6, 0.30)
sd_share = st.sidebar.slider("Self-Delivery Share", 0.0, 0.5, 0.20)

dd_share = max(0.0, 1 - (ue_share + sd_share))
instore_share = max(0.0, 1 - (ue_share + sd_share + dd_share))

delivery_cost = st.sidebar.slider("Delivery Cost per Order", 1.0, 6.0, 3.0)
monthly_orders = st.sidebar.number_input("Monthly Orders", 500, 6000, 2000)
growth_factor = st.sidebar.slider("Growth Factor", 0.95, 1.10, 1.02)

# -----------------------------
# Build input row
# -----------------------------
input_data = {
    "InStoreShare": instore_share,
    "UE_TotalShare": ue_share,
    "DD_TotalShare": dd_share,
    "SD_TotalShare": sd_share,
    "CommissionRate": commission,
    "DeliveryCostPerOrder": delivery_cost,
    "TotalCostRate": 0.70,  # fixed average
    "Commission_UE_Interaction": commission * ue_share,
    "DeliveryCost_SD_Interaction": delivery_cost * sd_share,
    "MonthlyOrders": monthly_orders,
    "GrowthAdjustedOrders": monthly_orders * growth_factor
}

input_df = pd.DataFrame([input_data])[features]

# -----------------------------
# Prediction
# -----------------------------
predicted_profit = model.predict(input_df)[0]

st.subheader("📊 Predicted Result")
st.metric("Predicted Monthly Net Profit", f"{predicted_profit:,.2f}")

# -----------------------------
# Scenario Simulations
# -----------------------------
st.subheader("🔄 Scenario Results")

scenarios = []

# Uber Eats +10%
ue_sim = input_df.copy()
ue_sim["UE_TotalShare"] *= 1.10
ue_sim["Commission_UE_Interaction"] = ue_sim["UE_TotalShare"] * ue_sim["CommissionRate"]
scenarios.append(["Uber Eats Share +10%", model.predict(ue_sim)[0]])

# Commission 25 → 30
comm_sim = input_df.copy()
comm_sim["CommissionRate"] = 0.30
comm_sim["Commission_UE_Interaction"] = 0.30 * comm_sim["UE_TotalShare"]
scenarios.append(["Commission 25% → 30%", model.predict(comm_sim)[0]])

# Delivery radius 5 → 10 km (cost proxy)
radius_sim = input_df.copy()
radius_sim["DeliveryCostPerOrder"] *= 2
radius_sim["DeliveryCost_SD_Interaction"] = (
    radius_sim["DeliveryCostPerOrder"] * radius_sim["SD_TotalShare"]
)
scenarios.append(["Delivery Radius 5 → 10 km", model.predict(radius_sim)[0]])

scenario_df = pd.DataFrame(scenarios, columns=["Scenario", "Predicted Profit"])
st.dataframe(scenario_df)

# -----------------------------
# Recommendations
# -----------------------------
st.subheader("🧠 Recommendations")

if commission > 0.30:
    st.warning("⚠️ Commission is above break-even. Profit risk is high.")
else:
    st.success("✅ Commission is within safe range.")

if sd_share > 0.30:
    st.warning("⚠️ High self-delivery share may increase logistics risk.")
else:
    st.info("ℹ️ Self-delivery level is manageable.")

# run command python -m streamlit run app.py    
