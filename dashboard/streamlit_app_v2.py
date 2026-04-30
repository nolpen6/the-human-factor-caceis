from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="The Human Factor @ CACEIS",
    page_icon="🌸",
    layout="wide",
)


# --------------------------------------------------
# VISUAL IDENTITY
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff7fb 0%, #ffffff 45%, #f8f5ff 100%);
    }

    h1, h2, h3 {
        color: #5c2448;
    }

    [data-testid="stMetricValue"] {
        color: #7a2f63;
    }

    .human-card {
        background-color: #ffffff;
        border: 1px solid #f0d8e8;
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 4px 14px rgba(92, 36, 72, 0.08);
        margin-bottom: 1rem;
    }

    .soft-note {
        background-color: #fff0f7;
        border-left: 5px solid #c05a9b;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #4b2940;
    }

    .governance-note {
        background-color: #f5f0ff;
        border-left: 5px solid #7c5cc4;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #3d3158;
    }

    .small-muted {
        color: #6f6070;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    """Load the KPI outputs created by the notebooks."""
    project_root = Path(__file__).resolve().parents[1]
    outputs_dir = project_root / "outputs"

    hr_kpi = pd.read_csv(outputs_dir / "hr_kpi_table.csv")
    absence_kpi = pd.read_csv(outputs_dir / "absence_kpi_table.csv")
    training_kpi = pd.read_csv(outputs_dir / "training_kpi_table.csv")
    employee_value = pd.read_csv(outputs_dir / "employee_value_table_v2.csv")

    department_summary_path = outputs_dir / "department_value_summary_v2.csv"
    department_summary = pd.read_csv(department_summary_path) if department_summary_path.exists() else pd.DataFrame()

    segment_summary_path = outputs_dir / "ai_segment_summary_v2.csv"
    segment_summary = pd.read_csv(segment_summary_path) if segment_summary_path.exists() else pd.DataFrame()

    return hr_kpi, absence_kpi, training_kpi, employee_value, department_summary, segment_summary


hr_kpi, absence_kpi, training_kpi, employee_value, department_summary, segment_summary = load_data()


# --------------------------------------------------
# BASIC CLEANUP / COMPATIBILITY
# --------------------------------------------------
SEGMENT_LABELS = {
    0: "Low Visibility Employees",
    1: "High Engagement / High Risk",
    2: "High Performers / Low Development",
}

if "segment_name" not in employee_value.columns:
    if "cluster" in employee_value.columns:
        employee_value["segment_name"] = employee_value["cluster"].map(SEGMENT_LABELS).fillna("Unclassified")
    elif "ai_segment" in employee_value.columns:
        employee_value["segment_name"] = employee_value["ai_segment"].map(SEGMENT_LABELS).fillna("Unclassified")
    else:
        employee_value["segment_name"] = "Unclassified"

# Preserve old segment wording if already exported under earlier names.
employee_value["segment_name"] = employee_value["segment_name"].replace(
    {
        "Low Information": "Low Visibility Employees",
        "Engaged but At Risk": "High Engagement / High Risk",
    }
)

possible_department_cols = [
    "libelle_organisation_niveau_07",
    "department",
    "organisation",
    "entity",
]
department_col = next((col for col in possible_department_cols if col in employee_value.columns), None)

# Create optional human-centered helper columns if possible.
if {
    "learning_intensity_score",
    "absenteeism_risk_score",
}.issubset(employee_value.columns):
    employee_value["sustainability_balance"] = (
        employee_value["learning_intensity_score"] - employee_value["absenteeism_risk_score"]
    )

if {
    "human_capital_value_proxy",
    "kpi_reliability_score",
}.issubset(employee_value.columns):
    employee_value["confidence_gap"] = (
        employee_value["human_capital_value_proxy"] * (1 - employee_value["kpi_reliability_score"])
    )


# --------------------------------------------------
# SMALL HELPERS
# --------------------------------------------------
def safe_mean(df: pd.DataFrame, col: str, decimals: int = 3):
    if col in df.columns and len(df) > 0:
        return round(df[col].mean(), decimals)
    return "N/A"


def soft_card(title: str, body: str):
    st.markdown(
        f"""
        <div class="human-card">
            <h3 style="margin-top:0;">{title}</h3>
            <p style="margin-bottom:0;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🌸 The Human Factor")
    st.markdown(
        """
        <p class="small-muted">
        A student prototype for exploring human capital as a living asset:
        performance, learning, risk, reliability, and context.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### 🧭 Reading guide")
    st.markdown(
        """
        - **Do not rank people mechanically**  
        - **Check data reliability first**  
        - **Use AI segments as questions, not verdicts**  
        - **Interpret value as a proxy, not truth**
        """
    )
    st.divider()
    st.caption("Made for the CACEIS x Albert School Alberthon")


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🌸 The Human Factor @ CACEIS")
st.caption("Rethinking human capital as a living, dynamic asset — not just a cost line.")

st.markdown(
    """
    <div class="soft-note">
    <b>Core idea:</b> value is not only created by what people produce. It also emerges from how they learn,
    adapt, collaborate, and sustain performance over time.
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns(3)
with col_a:
    soft_card("🧍 Human signals", "HR, absenteeism, training, performance, and workforce structure.")
with col_b:
    soft_card("📊 Behavioral KPIs", "Proxies for learning, continuity risk, development, and reliability.")
with col_c:
    soft_card("🤖 AI insight layer", "Segmentation that structures discussion without replacing human judgment.")


# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🌷 Overview",
        "💎 Value Explorer",
        "🤖 AI Segments",
        "📊 KPI Garden",
        "🛡️ Method & Governance",
    ]
)


# --------------------------------------------------
# TAB 1 — OVERVIEW
# --------------------------------------------------
with tab1:
    st.header("🌷 Integrated Human Capital Overview")
    st.markdown(
        "This page gives the jury a quick view of the integrated employee-level table and the main value signals."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees mapped", f"{len(employee_value):,}")
    col2.metric("Average value proxy", safe_mean(employee_value, "human_capital_value_proxy"))
    col3.metric("Average reliability", safe_mean(employee_value, "kpi_reliability_score"))
    col4.metric(
        "Training visibility",
        f"{int(employee_value['has_training_record'].sum()):,}"
        if "has_training_record" in employee_value.columns
        else "N/A",
    )

    st.subheader("💎 Distribution of Human Capital Value Proxy")
    if "human_capital_value_proxy" in employee_value.columns:
        fig = px.histogram(
            employee_value,
            x="human_capital_value_proxy",
            nbins=40,
            title="Human Capital Value Proxy Distribution",
            labels={"human_capital_value_proxy": "Human capital value proxy"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="soft-note">
        <b>How to read this:</b> the distribution is not a ranking. It shows where available data suggests stronger,
        weaker, or less visible human capital signals. Low values may reflect missing data, not low human value.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🧠 AI Segment Size")
    if "segment_name" in employee_value.columns:
        segment_counts = (
            employee_value["segment_name"]
            .value_counts()
            .rename_axis("segment_name")
            .reset_index(name="employees")
        )
        fig = px.bar(
            segment_counts,
            x="segment_name",
            y="employees",
            title="Number of Employees by AI Segment",
            labels={"segment_name": "AI segment", "employees": "Employees"},
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(segment_counts, use_container_width=True)


# --------------------------------------------------
# TAB 2 — VALUE EXPLORER
# --------------------------------------------------
with tab2:
    st.header("💎 Employee Value Explorer")

    st.markdown(
        """
        Explore how performance, learning, absenteeism risk, and data reliability combine into a first value proxy.
        This is designed for diagnosis and discussion — not automatic individual evaluation.
        """
    )

    filtered = employee_value.copy()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_segments = st.multiselect(
            "Filter by AI segment",
            sorted(filtered["segment_name"].dropna().unique()),
            default=sorted(filtered["segment_name"].dropna().unique()),
        )
        filtered = filtered[filtered["segment_name"].isin(selected_segments)]

    with col2:
        if "low_data_flag" in filtered.columns:
            low_data_choice = st.selectbox(
                "Data visibility",
                ["All", "Only low-visibility employees", "Exclude low-visibility employees"],
            )
            if low_data_choice == "Only low-visibility employees":
                filtered = filtered[filtered["low_data_flag"] == True]
            elif low_data_choice == "Exclude low-visibility employees":
                filtered = filtered[filtered["low_data_flag"] == False]

    with col3:
        if department_col:
            departments = sorted(filtered[department_col].dropna().unique())
            selected_departments = st.multiselect(
                "Filter by department/entity",
                departments,
                default=departments,
            )
            filtered = filtered[filtered[department_col].isin(selected_departments)]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Selected employees", f"{len(filtered):,}")
    col2.metric("Avg value proxy", safe_mean(filtered, "human_capital_value_proxy"))
    col3.metric("Avg learning signal", safe_mean(filtered, "learning_intensity_score"))
    col4.metric("Avg continuity risk", safe_mean(filtered, "absenteeism_risk_score"))

    st.subheader("🌱 Value vs Learning")
    if {"learning_intensity_score", "human_capital_value_proxy", "segment_name"}.issubset(filtered.columns):
        fig = px.scatter(
            filtered,
            x="learning_intensity_score",
            y="human_capital_value_proxy",
            color="segment_name",
            hover_data=[
                col
                for col in ["employee_id", "performance_score", "absenteeism_risk_score", "kpi_reliability_score"]
                if col in filtered.columns
            ],
            title="Learning Intensity vs Human Capital Value Proxy",
            labels={
                "learning_intensity_score": "Learning intensity score",
                "human_capital_value_proxy": "Human capital value proxy",
                "segment_name": "AI segment",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    if "sustainability_balance" in filtered.columns:
        st.subheader("💗 Sustainability Balance")
        st.markdown(
            "A simple psychological proxy: learning energy minus continuity risk. Positive values suggest stronger development capacity; negative values suggest pressure or fragility."
        )
        fig = px.histogram(
            filtered,
            x="sustainability_balance",
            nbins=30,
            color="segment_name",
            title="Sustainability Balance Distribution",
            labels={"sustainability_balance": "Learning intensity - absenteeism risk"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Employee-Level Table")
    preferred_cols = [
        "employee_id",
        department_col,
        "segment_name",
        "human_capital_value_proxy",
        "reliability_adjusted_value_proxy",
        "kpi_reliability_score",
        "performance_score",
        "learning_intensity_score",
        "absenteeism_risk_score",
        "sustainability_balance",
        "data_coverage_score",
        "low_data_flag",
        "has_performance_record",
        "has_absence_record",
        "has_training_record",
    ]
    display_cols = [col for col in preferred_cols if col and col in filtered.columns]
    st.dataframe(filtered[display_cols], use_container_width=True)


# --------------------------------------------------
# TAB 3 — AI SEGMENTS
# --------------------------------------------------
with tab3:
    st.header("🤖 AI Segmentation")

    st.markdown(
        """
        The clustering model groups employees into broad behavioral profiles. The purpose is to reveal patterns and
        generate better HR questions — not to automate decisions.
        """
    )

    segment_actions = pd.DataFrame(
        [
            {
                "Segment": "Low Visibility Employees",
                "What it may mean": "Low data coverage or limited observed signals.",
                "Human-centered question": "Are we missing data, or is this employee genuinely disconnected from tracked systems?",
                "Recommended action": "Improve data completeness before drawing conclusions.",
            },
            {
                "Segment": "High Engagement / High Risk",
                "What it may mean": "Strong learning or activity signals combined with higher absenteeism risk.",
                "Human-centered question": "Is this a motivated employee under pressure?",
                "Recommended action": "Monitor workload, recovery, wellbeing, and possible burnout risk.",
            },
            {
                "Segment": "High Performers / Low Development",
                "What it may mean": "Strong performance but lower training participation.",
                "Human-centered question": "Are strong performers being stretched without future development?",
                "Recommended action": "Protect performance while investing in growth opportunities.",
            },
        ]
    )
    st.dataframe(segment_actions, use_container_width=True)

    st.subheader("📊 Average KPIs by Segment")
    segment_metrics = [
        "human_capital_value_proxy",
        "reliability_adjusted_value_proxy",
        "performance_score",
        "learning_intensity_score",
        "absenteeism_risk_score",
        "sustainability_balance",
        "data_coverage_score",
        "kpi_reliability_score",
    ]
    available_metrics = [col for col in segment_metrics if col in employee_value.columns]

    if available_metrics:
        summary = employee_value.groupby("segment_name", as_index=False)[available_metrics].mean()
        counts = employee_value.groupby("segment_name", as_index=False).size().rename(columns={"size": "employees"})
        summary = counts.merge(summary, on="segment_name", how="left")
        st.dataframe(summary, use_container_width=True)

        fig = px.bar(
            summary,
            x="segment_name",
            y="human_capital_value_proxy",
            title="Average Value Proxy by Segment",
            labels={"segment_name": "AI segment", "human_capital_value_proxy": "Average value proxy"},
        )
        st.plotly_chart(fig, use_container_width=True)

        if "sustainability_balance" in summary.columns:
            fig = px.bar(
                summary,
                x="segment_name",
                y="sustainability_balance",
                title="Average Sustainability Balance by Segment",
                labels={"segment_name": "AI segment", "sustainability_balance": "Learning minus risk"},
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="governance-note">
        <b>Ethical guardrail:</b> AI segments are conversation starters, not verdicts. They should guide investigation,
        support managers, and improve systems — never punish individuals automatically.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# TAB 4 — KPI DETAIL
# --------------------------------------------------
with tab4:
    st.header("📊 KPI Garden")

    st.markdown(
        """
        KPIs are treated as flowers in a garden: they show visible signals, but the root system — context,
        workload, motivation, team dynamics, and data quality — still needs interpretation.
        """
    )

    kpi_section = st.radio(
        "Choose KPI view",
        ["HR & Performance", "Absenteeism / Continuity", "Learning"],
        horizontal=True,
    )

    if kpi_section == "HR & Performance":
        st.subheader("🌟 HR & Performance KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Employees", f"{len(hr_kpi):,}")
        col2.metric("Average performance", safe_mean(hr_kpi, "avg_performance", 2))
        col3.metric("Average talent progression", safe_mean(hr_kpi, "talent_progression_proxy", 2))

        if "avg_performance" in hr_kpi.columns:
            fig = px.histogram(hr_kpi, x="avg_performance", nbins=10, title="Average Performance Distribution")
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(hr_kpi, use_container_width=True)

    elif kpi_section == "Absenteeism / Continuity":
        st.subheader("💔 Absenteeism / Continuity KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Employees", f"{len(absence_kpi):,}")
        col2.metric("Average absence days", safe_mean(absence_kpi, "absence_days", 2))
        col3.metric("Average continuity risk", safe_mean(absence_kpi, "absenteeism_risk_score", 2))

        if "absenteeism_risk_score" in absence_kpi.columns:
            fig = px.histogram(
                absence_kpi,
                x="absenteeism_risk_score",
                nbins=30,
                title="Absenteeism Risk Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(absence_kpi, use_container_width=True)

    elif kpi_section == "Learning":
        st.subheader("🌱 Training / Learning KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Employees", f"{len(training_kpi):,}")
        col2.metric("Average training hours", safe_mean(training_kpi, "training_hours", 2))
        col3.metric("Average learning intensity", safe_mean(training_kpi, "learning_intensity_score", 2))

        if "learning_intensity_score" in training_kpi.columns:
            fig = px.histogram(
                training_kpi,
                x="learning_intensity_score",
                nbins=30,
                title="Learning Intensity Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(training_kpi, use_container_width=True)


# --------------------------------------------------
# TAB 5 — METHOD & GOVERNANCE
# --------------------------------------------------
with tab5:
    st.header("🛡️ Method and Governance")

    st.subheader("🔄 Pipeline")
    st.markdown(
        """
        1. Clean separate HR, absence, and training files.  
        2. Calculate KPI tables for each source.  
        3. Validate common anonymized employee identifiers.  
        4. Merge available indicators into an employee-level table.  
        5. Create a first human capital value proxy.  
        6. Use clustering to identify broad employee profiles.  
        7. Export outputs for dashboard exploration and future Snowflake integration.
        """
    )

    st.subheader("💎 Value Proxy Logic")
    st.markdown(
        """
        The proxy is not a financial valuation. It is a structured approximation based on available signals:

        - **Performance** = current contribution signal  
        - **Learning intensity** = future capability signal  
        - **Talent progression** = development signal  
        - **Absenteeism risk** = operational continuity risk  
        - **Reliability score** = confidence in the available data  
        - **Sustainability balance** = learning energy minus continuity pressure  
        """
    )

    st.subheader("🧠 Psychological Interpretation")
    st.markdown(
        """
        The dashboard intentionally includes human-centered language because human capital is not only technical.
        Signals such as learning, absenteeism, and performance may reflect motivation, workload, recognition,
        recovery, manager support, and team context. The tool therefore helps CACEIS ask better questions rather
        than reducing people to a single score.
        """
    )

    st.subheader("🛡️ Governance Principles")
    st.markdown(
        """
        - Use anonymized / pseudonymized identifiers.  
        - Do not use dashboard outputs for automatic individual sanctions.  
        - Display reliability and data coverage before interpreting value scores.  
        - Monitor possible bias in performance reviews and training access.  
        - Treat AI segments as conversation starters, not final decisions.  
        - Keep humans in the loop for all HR decisions.  
        """
    )

    st.subheader("❄️ Future Architecture")
    st.info(
        "In a target architecture, Snowflake could store cleaned KPI tables and the integrated value table. "
        "The current prototype runs locally, but the outputs are structured for future warehouse integration."
    )
