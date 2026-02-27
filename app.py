import streamlit as st
import pandas as pd
import joblib

from src.kitting.kitting_engine import FormworkKittingEngine
from src.optimization.scenario_simulator import ScenarioSimulator

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Formwork BoQ AI",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------
# LOAD ML MODEL (CACHED)
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/formwork_demand_model.pkl")

model = load_model()

# -----------------------------
# SESSION STATE (AUTH)
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -----------------------------
# LOGIN PAGE (DUMMY)
# -----------------------------
def login_page():
    st.title("🏗️ Formwork BoQ Optimization Platform")
    st.subheader("Secure Access Portal")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if username and password:
                st.session_state.authenticated = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Please enter valid credentials")

# -----------------------------
# MAIN DASHBOARD
# -----------------------------
def main_dashboard():
    st.sidebar.title("📊 Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "BoQ & Kitting Prediction",
            "Inventory Tracker",
            "Scenario Analysis",
            "Project Updates",
            "About System"
        ]
    )

    if page == "BoQ & Kitting Prediction":
        boq_kitting_page()
    elif page == "Inventory Tracker":
        inventory_page()
    elif page == "Scenario Analysis":
        scenario_analysis_page()
    elif page == "Project Updates":
        project_updates_page()
    elif page == "About System":
        about_page()

# -----------------------------
# PAGE 1: BoQ & Kitting (ML)
# -----------------------------
def boq_kitting_page():
    st.header("📐 Automated BoQ & Formwork Kitting")

    col1, col2, col3 = st.columns(3)

    with col1:
        project_type = st.selectbox(
            "Project Type",
            ["Residential", "Commercial", "Infrastructure"]
        )
        floors = st.number_input("Number of Floors", min_value=1, value=10)
        element_type = st.selectbox(
            "Element Type", ["Slab", "Beam", "Column", "Wall"]
        )

    with col2:
        formwork_type = st.selectbox(
            "Formwork Type", ["Aluminium", "Steel", "Timber"]
        )
        area_sqm = st.number_input("Area (sqm)", min_value=1.0, value=100.0)
        quantity = st.number_input("Quantity", min_value=1, value=1)

    with col3:
        cycle_time_days = st.number_input("Cycle Time (days)", min_value=1, value=7)
        total_units = st.number_input("Available Inventory Units", min_value=0, value=100)
        reuse_limit = st.number_input("Reuse Limit", min_value=1, value=20)

    if st.button("🔮 Predict Requirement"):
        input_df = pd.DataFrame([{
            "project_type": project_type,
            "floors": floors,
            "element_type": element_type,
            "formwork_type": formwork_type,
            "area_sqm": area_sqm,
            "quantity": quantity,
            "cycle_time_days": cycle_time_days,
            "total_units": total_units,
            "reuse_limit": reuse_limit
        }])

        prediction = model.predict(input_df)[0]

        colA, colB = st.columns(2)
        colA.metric("🔩 Required New Units", int(round(prediction)))
        colB.metric(
            "♻️ Units via Reuse",
            int(max(total_units * reuse_limit - prediction, 0))
        )

# -----------------------------
# PAGE 2: INVENTORY TRACKER
# -----------------------------
def inventory_page():
    st.header("📦 Inventory Tracking & Kitting")

    if st.button("🔄 Generate Kitting Plan"):
        engine = FormworkKittingEngine(
            inventory_path="data/inventory.csv",
            schedule_path="data/schedule.csv"
        )

        df = engine.build_kitting_plan()

        col1, col2 = st.columns(2)
        col1.metric("Allocated", (df["status"] == "ALLOCATED").sum())
        col2.metric("Shortages", (df["status"] == "SHORTAGE").sum())

        st.dataframe(df, use_container_width=True)

# -----------------------------
# PAGE 3: SCENARIO ANALYSIS (NEW)
# -----------------------------
def scenario_analysis_page():
    st.header("🔬 Scenario & What-If Analysis")

    col1, col2 = st.columns(2)

    with col1:
        project_type = st.selectbox(
            "Project Type",
            ["Residential", "Commercial", "Infrastructure"]
        )
        floors = st.number_input("Floors", min_value=1, value=8)
        area = st.number_input("Area (sqm)", min_value=100.0, value=12000.0)

    with col2:
        duration_days = st.number_input("Duration (days)", min_value=30, value=180)
        reuse_limit = st.slider("Reuse Limit", 5, 40, 20)
        cycle_time_days = st.slider("Cycle Time (days)", 3, 14, 7)

    if st.button("📊 Run Scenario Comparison"):
        base_payload = {
            "project_type": project_type,
            "floors": floors,
            "area": area,
            "duration_days": duration_days
        }

        simulator = ScenarioSimulator(base_payload)

        simulator.run_scenario("Baseline", {})
        simulator.run_scenario("Higher Reuse", {"reuse_limit": reuse_limit})
        simulator.run_scenario("Faster Cycle", {"cycle_time_days": cycle_time_days})

        df = simulator.get_comparison_table()

        st.dataframe(df, use_container_width=True)

        best = df.sort_values("shortages").iloc[0]
        st.success(f"Best scenario: {best['scenario']}")

# -----------------------------
# PAGE 4: PROJECT UPDATES
# -----------------------------
def project_updates_page():
    st.header("🗓️ Project Updates & Impact Analysis")

    st.markdown(
        """
        This module allows planners to **update project conditions**
        (delay, cycle time, reuse policy) and instantly view the
        **impact on formwork demand and inventory risk**.
        """
    )

    # -----------------------------
    # BASELINE (REFERENCE)
    # -----------------------------
    st.subheader("📌 Baseline Project")

    col1, col2, col3 = st.columns(3)
    with col1:
        base_duration = st.number_input(
            "Planned Duration (days)", value=180, disabled=True
        )
    with col2:
        base_inventory = st.number_input(
            "Available Inventory Units", value=100, disabled=True
        )
    with col3:
        base_cycle = st.number_input(
            "Original Cycle Time (days)", value=7, disabled=True
        )

    st.divider()

    # -----------------------------
    # UPDATE INPUTS
    # -----------------------------
    st.subheader("✏️ Update Project Conditions")

    delay_days = st.slider(
        "Project Delay / Extension (days)",
        min_value=0,
        max_value=90,
        value=0
    )

    new_cycle_time = st.selectbox(
        "Revised Cycle Time (days)",
        options=[7, 6, 5, 4]
    )

    new_reuse_limit = st.slider(
        "Revised Reuse Limit",
        min_value=10,
        max_value=40,
        value=20
    )

    if st.button("🔄 Evaluate Impact"):

        # -----------------------------
        # UPDATED PAYLOAD (SAFE)
        # -----------------------------
        payload = {
            "project_type": "Residential",
            "floors": 8,
            "element_type": "Slab",
            "formwork_type": "Aluminium",
            "area_sqm": 12000,
            "quantity": 1,
            "cycle_time_days": new_cycle_time,
            "total_units": base_inventory,
            "reuse_limit": new_reuse_limit
        }

        prediction = model.predict(pd.DataFrame([payload]))[0]

        updated_duration = base_duration + delay_days
        shortage_risk = "HIGH" if prediction > base_inventory else "LOW"

        # -----------------------------
        # RESULTS
        # -----------------------------
        st.success("✅ Impact Analysis Completed")

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric(
                "⏱️ Updated Duration (days)",
                updated_duration,
                delta=delay_days
            )

        with colB:
            st.metric(
                "🔩 Required New Units",
                int(round(prediction))
            )

        with colC:
            st.metric(
                "⚠️ Inventory Risk",
                shortage_risk
            )

        # -----------------------------
        # INSIGHTS
        # -----------------------------
        st.subheader("📊 Planner Insight")

        if shortage_risk == "HIGH":
            st.error(
                "Project delay and faster cycle increase formwork demand "
                "beyond current inventory. Procurement or schedule revision required."
            )
        else:
            st.success(
                "Inventory reuse absorbs the updated schedule. "
                "No additional procurement needed."
            )

# -----------------------------
# PAGE 5: ABOUT
# -----------------------------
def about_page():
    st.header("ℹ️ About System")
    st.markdown(
        """
        **AI-driven Formwork BoQ & Kitting Platform**

        - ML-based procurement prediction  
        - Inventory-aware reuse optimization  
        - Scenario planning & what-if analysis  

        Built for **real construction planning teams**.
        """
    )

# -----------------------------
# APP ENTRY
# -----------------------------
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()