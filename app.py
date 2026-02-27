import streamlit as st
import pandas as pd
import joblib
from src.kitting.kitting_engine import FormworkKittingEngine

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
            "Project Updates",
            "About System"
        ]
    )

    if page == "BoQ & Kitting Prediction":
        boq_kitting_page()
    elif page == "Inventory Tracker":
        inventory_page()
    elif page == "Project Updates":
        project_updates_page()
    elif page == "About System":
        about_page()

# -----------------------------
# PAGE 1: BoQ & Kitting (ML)
# -----------------------------
def boq_kitting_page():
    st.header("📐 Automated BoQ & Formwork Kitting")

    st.info(
        "Enter project parameters. "
        "The ML model predicts how many NEW formwork units "
        "must be procured after accounting for reuse."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        project_type = st.selectbox(
            "Project Type",
            ["Residential", "Commercial", "Infrastructure"]
        )
        floors = st.number_input(
            "Number of Floors",
            min_value=1,
            value=10
        )
        element_type = st.selectbox(
            "Element Type",
            ["Slab", "Beam", "Column", "Wall"]
        )

    with col2:
        formwork_type = st.selectbox(
            "Formwork Type",
            ["Aluminium", "Steel", "Timber"]
        )
        area_sqm = st.number_input(
            "Area (sqm)",
            min_value=1.0,
            value=100.0
        )
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

    with col3:
        cycle_time_days = st.number_input(
            "Cycle Time (days)",
            min_value=1,
            value=7
        )
        total_units = st.number_input(
            "Available Inventory Units",
            min_value=0,
            value=100
        )
        reuse_limit = st.number_input(
            "Reuse Limit",
            min_value=1,
            value=20
        )

    if st.button("🔮 Predict Requirement"):

        # Build ML input exactly like training data
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

        st.success("✅ Prediction Completed")

        colA, colB = st.columns(2)

        with colA:
            st.metric(
                "🔩 Required New Formwork Units",
                int(round(prediction))
            )

        with colB:
            reused_units = max(
                total_units * reuse_limit - prediction, 0
            )
            st.metric(
                "♻️ Units Covered via Reuse",
                int(round(reused_units))
            )

        st.info(
            "Prediction is inventory-aware and reuse-constrained, "
            "reducing excess procurement."
        )

# -----------------------------
# PAGE 2: Inventory Tracker
# -----------------------------
def inventory_page():
    st.header("📦 Inventory Tracking & Formwork Kitting")

    st.markdown(
        """
        This module simulates **formwork kitting and reuse cycles**
        based on project schedules and available inventory.
        """
    )

    if st.button("🔄 Generate Kitting Plan"):

        engine = FormworkKittingEngine(
            inventory_path="data/inventory.csv",
            schedule_path="data/schedule.csv"
        )

        kitting_df = engine.build_kitting_plan()

        st.success("Kitting plan generated successfully")

        # -----------------------------
        # SHOW SUMMARY
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            total_allocations = (kitting_df["status"] == "ALLOCATED").sum()
            st.metric("✅ Allocated Tasks", total_allocations)

        with col2:
            shortages = (kitting_df["status"] == "SHORTAGE").sum()
            st.metric("❌ Shortages Detected", shortages)

        # -----------------------------
        # FILTER OPTIONS
        # -----------------------------
        st.subheader("🔍 Filter View")

        view_option = st.selectbox(
            "Select view",
            ["All", "Allocated Only", "Shortages Only"]
        )

        if view_option == "Allocated Only":
            display_df = kitting_df[kitting_df["status"] == "ALLOCATED"]
        elif view_option == "Shortages Only":
            display_df = kitting_df[kitting_df["status"] == "SHORTAGE"]
        else:
            display_df = kitting_df

        st.dataframe(display_df, use_container_width=True)

        # -----------------------------
        # INSIGHT BOX
        # -----------------------------
        if shortages > 0:
            st.error(
                "⚠️ Inventory shortage detected. "
                "Consider procuring additional formwork units "
                "or adjusting project schedule."
            )
        else:
            st.success(
                "♻️ Inventory reuse optimized successfully. "
                "No shortages detected."
            )

# -----------------------------
# PAGE 3: Project Updates
# -----------------------------
def project_updates_page():
    st.header("🗓️ Project Schedule & Updates")

    st.info(
        "Update project delays or extensions. "
        "Predictions will auto-adjust."
    )

    st.warning("Dynamic schedule feedback loop coming next")

# -----------------------------
# PAGE 4: About
# -----------------------------
def about_page():
    st.header("ℹ️ About This System")

    st.markdown(
        """
        **Automation of Formwork BoQ & Kitting Using Machine Learning**

        **Core Capabilities**
        - ML-driven procurement prediction
        - Inventory-aware reuse optimization
        - Schedule-linked decision making
        - Reduced material & carrying costs

        Designed as an **industry-ready decision support system**.
        """
    )

# -----------------------------
# APP ENTRY
# -----------------------------
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()