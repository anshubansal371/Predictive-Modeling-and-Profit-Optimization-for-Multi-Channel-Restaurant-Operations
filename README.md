# Predictive-Modeling-and-Profit-Optimization-for-Multi-Channel-Restaurant-Operations
A machine learning and analytics project that predicts restaurant profit across delivery channels (Uber Eats, DoorDash, Self-Delivery, and In-Store), performs sensitivity and scenario analysis, and provides an interactive Streamlit dashboard for strategic decision-making and profit optimization.

## Overview
This project develops a **data-driven decision support system** for restaurant operators to understand how delivery platforms, commissions, and channel mix influence profitability.

Using historical restaurant data, the system builds predictive models to estimate monthly net profit and enables managers to simulate strategic scenarios such as commission changes, channel mix adjustments, and delivery expansion.

The project also includes a **Streamlit dashboard** that allows interactive what-if analysis for business decision-making.

---

## Problem Statement
Restaurant operators increasingly rely on delivery platforms such as Uber Eats and DoorDash. While these platforms increase order volume, they also introduce high commission costs that reduce profit margins.

Most restaurants lack tools to answer questions like:

- What happens if Uber Eats orders increase?
- At what commission rate does delivery become unprofitable?
- When does self-delivery become a better strategy?

This project solves that problem by combining **predictive modeling, scenario simulation, and optimization techniques**.

---

## Key Features

### Predictive Modeling
Machine learning models are used to estimate monthly net profit based on operational and financial variables.

Models explored:
- Linear Regression (baseline)
- Random Forest Regressor
- Gradient Boosting Regressor
- Deep Learning model (experimental)

The **Gradient Boosting model** was selected as the final model due to its performance and stability.

---

### Feature Engineering
Key features created to improve model performance include:

- Profit per order
- Channel revenue ratios
- Cost-to-revenue ratios
- Interaction terms  
  - CommissionRate × UberEats share
  - DeliveryCost × Self-delivery share
- Growth-adjusted demand

---

### Sensitivity Analysis
The model evaluates how profit changes when key variables shift.

Example simulations:
- Commission increase (+1%, +5%, +10%)
- Uber Eats share increase
- Self-delivery expansion
- Delivery radius expansion

This analysis produces a **Profit Sensitivity Index**, showing how vulnerable profits are to operational changes.

---

### Scenario Simulation Engine
The system can answer "what-if" questions by simulating different business strategies and predicting their financial outcomes.

Example scenarios:
- Uber Eats share +10%
- Commission rate increase (25% → 30%)
- Delivery radius expansion

Each scenario generates predicted profit and change relative to the baseline strategy.

---

### Optimization Engine
An optimization layer identifies strategies that maximize profitability.

Key outputs:
- Profit-maximizing channel mix
- Break-even commission rate
- Self-delivery profitability threshold
- Strategy uplift percentage

---

### Business KPIs
Model outputs are translated into business-friendly metrics:

- Predicted Net Profit
- Channel Mix Efficiency Score
- Break-even Commission Rate
- Optimization Uplift %
- Profit Stability Index
- Commission Risk Status
- Self-Delivery Readiness Score

These KPIs help managers understand operational risks and opportunities.

---

### Interactive Streamlit Dashboard
The final system includes an interactive dashboard that allows users to:

- Adjust channel mix with sliders
- Modify commission rates
- Simulate demand growth
- Run scenario simulations
- View profit predictions and risk indicators
- Receive strategy recommendations

The dashboard turns machine learning insights into a **decision support tool for restaurant managers**.

---

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Matplotlib / Seaborn

---

## Project Workflow

1. Data Cleaning and Validation
2. Exploratory Data Analysis
3. Feature Engineering
4. Baseline Modeling
5. Advanced Machine Learning Models
6. Sensitivity Analysis
7. Model Finalization
8. Scenario Simulation Engine
9. Strategy Optimization
10. Business KPI Generation
11. Streamlit Dashboard Development
12. Dashboard Polishing and Visualization

---
