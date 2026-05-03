import os
import pandas as pd
import streamlit as st
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CACEIS Value Creation OS",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    hr_kpi = pd.read_csv(os.path.join(base_dir, "outputs", "hr_kpi_table.csv"))
    absence_kpi = pd.read_csv(os.path.join(base_dir, "outputs", "absence_kpi_table.csv"))
    training_kpi = pd.read_csv(os.path.join(base_dir, "outputs", "training_kpi_table.csv"))

    return hr_kpi, absence_kpi, training_kpi


hr_kpi, absence_kpi, training_kpi = load_data()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("CACEIS Value Creation Operating System")
st.caption(
    "Prototype showing how HR indicators can become part of a broader value-creation system."
)

st.markdown(
    """
    **Core idea:** KPIs are not the goal.  
    They are observable by-products of deeper behaviors, decisions, learning loops, and organizational conditions.
    """
)


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Value Creation System",
    "Behavioral Layer",
    "Indicators / KPIs",
    "AI Layer"
])


# --------------------------------------------------
# TAB 1 — VALUE CREATION SYSTEM
# --------------------------------------------------

with tab1:
    st.header("From KPI Tracking to Value Creation")

    st.markdown(
        """
        Traditional HR dashboards mainly answer:

        > What happened?

        This prototype adds a second question:

        > What behaviors and decisions may explain what happened?

        The long-term objective is not to monitor employees, but to help CACEIS understand how human capital creates value.
        """
    )

    st.subheader("Three-Layer Architecture")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 1. Behavioral Layer  
            Captures value drivers:
            - decisions taken
            - hypotheses
            - actions
            - learning loops
            - collaboration signals
            """
        )

    with col2:
        st.markdown(
            """
            ### 2. Indicator Layer  
            Uses available KPIs:
            - performance
            - absenteeism
            - learning intensity
            - progression proxy
            """
        )

    with col3:
        st.markdown(
            """
            ### 3. Value Estimation Layer  
            Future AI layer:
            - clustering
            - regression
            - classification
            - network analysis
            """
        )

    st.subheader("Value Creation Logic")

    st.graphviz_chart(
        """
        digraph {
            rankdir=LR;
            Decision -> Action;
            Action -> Outcome;
            Outcome -> Learning;
            Learning -> Decision;
            Outcome -> KPI;
            KPI -> "Value Estimation";
        }
        """
    )

    st.info(
        "Current prototype: structured HR data and KPIs. "
        "Future version: behavioral data linked to KPIs and value estimation."
    )


# --------------------------------------------------
# TAB 2 — BEHAVIORAL LAYER
# --------------------------------------------------

with tab2:
    st.header("Behavioral Layer — Decision & Experiment Tracking")

    st.markdown(
        """
        This is the core innovation of the system.

        Instead of evaluating employees only through outcomes, this layer captures:
        - what decision was made
        - what was expected
        - what action was taken
        - what actually happened
        - what was learned

        This supports a shift from **outcome-based evaluation** to **decision-quality learning**.
        """
    )

    st.subheader("Prototype Decision Log")

    with st.form("decision_form"):
        col1, col2 = st.columns(2)

        with col1:
            decision = st.text_input("Decision taken")
            hypothesis = st.text_area("Expected outcome / hypothesis")
            action = st.text_area("Action implemented")

        with col2:
            expected_impact = st.slider("Expected impact", 1, 5, 3)
            actual_impact = st.slider("Actual impact", 1, 5, 3)
            learning = st.text_area("Key learning")

        submitted = st.form_submit_button("Log decision")

        if submitted:
            impact_gap = actual_impact - expected_impact

            st.success("Decision recorded in prototype format.")

            st.write(
                {
                    "decision": decision,
                    "hypothesis": hypothesis,
                    "action": action,
                    "expected_impact": expected_impact,
                    "actual_impact": actual_impact,
                    "impact_gap": impact_gap,
                    "learning": learning,
                }
            )

            if impact_gap > 0:
                st.success("Actual impact exceeded expectation.")
            elif impact_gap < 0:
                st.warning("Actual impact was below expectation. This becomes a learning opportunity.")
            else:
                st.info("Actual impact matched expectation.")

    st.subheader("Why this matters")

    st.markdown(
        """
        Outcomes can be influenced by randomness.  
        A good decision can lead to a bad outcome, and a bad decision can sometimes lead to a good outcome.

        Therefore, CACEIS should not only ask:

        > Did the employee hit the KPI?

        It should also ask:

        > Was the decision logical, informed, and value-oriented?
        """
    )


# --------------------------------------------------
# TAB 3 — INDICATORS / KPIS
# --------------------------------------------------

with tab3:
    st.header("Indicators / KPIs")

    st.warning(
        "KPIs are used here as learning indicators, not as control mechanisms. "
        "They are proxies of value drivers, not direct measures of value."
    )

    kpi_section = st.radio(
        "Choose KPI view",
        ["HR & Performance", "Absenteeism", "Learning"],
        horizontal=True
    )

    # -------------------------
    # HR & PERFORMANCE
    # -------------------------
    if kpi_section == "HR & Performance":
        st.subheader("HR & Performance KPIs")

        dept_col = "libelle_organisation_niveau_07"

        if dept_col in hr_kpi.columns:
            departments = sorted(hr_kpi[dept_col].dropna().unique())

            selected_departments = st.multiselect(
                "Filter by department",
                departments,
                default=departments[:5] if len(departments) >= 5 else departments
            )

            filtered_hr = hr_kpi[hr_kpi[dept_col].isin(selected_departments)]
        else:
            filtered_hr = hr_kpi.copy()

        col1, col2, col3 = st.columns(3)

        col1.metric("Employees", len(filtered_hr))

        avg_perf = (
            round(filtered_hr["avg_performance"].mean(), 2)
            if "avg_performance" in filtered_hr.columns and filtered_hr["avg_performance"].notna().any()
            else "N/A"
        )

        col2.metric("Average Performance", avg_perf)

        talent_score = (
            round(filtered_hr["talent_progression_proxy"].mean(), 2)
            if "talent_progression_proxy" in filtered_hr.columns and filtered_hr["talent_progression_proxy"].notna().any()
            else "N/A"
        )

        col3.metric("Talent Progression Proxy", talent_score)

        if "avg_performance" in filtered_hr.columns:
            fig = px.histogram(
                filtered_hr,
                x="avg_performance",
                nbins=10,
                title="Distribution of Average Performance"
            )
            st.plotly_chart(fig, use_container_width=True)

        if dept_col in filtered_hr.columns and "avg_performance" in filtered_hr.columns:
            dept_perf = (
                filtered_hr
                .groupby(dept_col, as_index=False)
                .agg(avg_performance=("avg_performance", "mean"))
                .sort_values("avg_performance", ascending=False)
            )

            fig = px.bar(
                dept_perf,
                x=dept_col,
                y="avg_performance",
                title="Average Performance by Department"
            )
            st.plotly_chart(fig, use_container_width=True)

        if "low_data_flag" in filtered_hr.columns:
            st.subheader("Data Quality: Limited Evaluation Data")

            fig = px.histogram(
                filtered_hr,
                x="low_data_flag",
                title="Employees With Limited Evaluation Data"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(filtered_hr)

    # -------------------------
    # ABSENTEEISM
    # -------------------------
    elif kpi_section == "Absenteeism":
        st.subheader("Absenteeism Risk Score")

        col1, col2, col3 = st.columns(3)

        col1.metric("Employees in Absence Table", len(absence_kpi))
        col2.metric(
            "Average Absence Days",
            round(absence_kpi["absence_days"].mean(), 2)
            if "absence_days" in absence_kpi.columns else "N/A"
        )
        col3.metric(
            "Average Risk Score",
            round(absence_kpi["absenteeism_risk_score"].mean(), 2)
            if "absenteeism_risk_score" in absence_kpi.columns else "N/A"
        )

        if "absenteeism_risk_score" in absence_kpi.columns:
            fig = px.histogram(
                absence_kpi,
                x="absenteeism_risk_score",
                nbins=30,
                title="Distribution of Absenteeism Risk Score"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(absence_kpi)

    # -------------------------
    # LEARNING
    # -------------------------
    elif kpi_section == "Learning":
        st.subheader("Learning Intensity Score")

        col1, col2, col3 = st.columns(3)

        col1.metric("Employees in Training Table", len(training_kpi))
        col2.metric(
            "Average Training Hours",
            round(training_kpi["training_hours"].mean(), 2)
            if "training_hours" in training_kpi.columns else "N/A"
        )
        col3.metric(
            "Average Learning Score",
            round(training_kpi["learning_intensity_score"].mean(), 2)
            if "learning_intensity_score" in training_kpi.columns else "N/A"
        )

        if "learning_intensity_score" in training_kpi.columns:
            fig = px.histogram(
                training_kpi,
                x="learning_intensity_score",
                nbins=30,
                title="Distribution of Learning Intensity Score"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(training_kpi)

    st.info(
        "Data limitation: HR/performance data uses IUG, while absence and training data use Employee Code. "
        "The prototype avoids unsafe merges unless a reliable mapping table is available."
    )


# --------------------------------------------------
# TAB 4 — AI LAYER
# --------------------------------------------------

with tab4:
    st.header("AI Layer — Future Prototype")

    st.markdown(
        """
        The current version prepares the foundation for AI.  
        The future version would connect behavioral data and KPI data to detect patterns that are difficult to see manually.
        """
    )

    st.subheader("Planned Techniques")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ### Clustering  
            Identify employee or team archetypes:
            - stable high performers
            - high learning / low performance
            - high absence risk
            - emerging talent
            """
        )

        st.markdown(
            """
            ### Regression  
            Estimate which factors are associated with:
            - performance
            - learning intensity
            - absence risk
            - progression proxy
            """
        )

    with col2:
        st.markdown(
            """
            ### Classification  
            Predict risk categories:
            - disengagement risk
            - absenteeism risk
            - low performance consistency
            """
        )

        st.markdown(
            """
            ### Network Analysis  
            Future method if collaboration data becomes available:
            - identify bottlenecks
            - detect knowledge hubs
            - map collaboration flows
            """
        )

    st.subheader("AI Principle")

    st.success(
        "AI should identify patterns and learning opportunities. "
        "It should not replace managerial judgment or be used as an automated control tool."
    )

    st.subheader("Current vs Future Data")

    st.markdown(
        """
        **Current data used**
        - HR master data
        - performance evaluations
        - absenteeism records
        - training records

        **Future data needed**
        - decision logs
        - collaboration signals
        - workload data
        - operational productivity
        - error / risk events
        """
    )