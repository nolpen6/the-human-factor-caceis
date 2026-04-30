from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Force readable charts even when browser/Streamlit is in dark mode.
px.defaults.template = "plotly_white"


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="The Human Factor @ CACEIS",
    page_icon="🧭",
    layout="wide",
)


# --------------------------------------------------
# VISUAL IDENTITY
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root { color-scheme: light; }

    .stApp,
    section.main,
    div[data-testid="stAppViewContainer"],
    div[data-testid="stHeader"] {
        background-color: #f8fafc !important;
        color: #1f2933 !important;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, span, label, div {
        color: #1f2933 !important;
    }

    [data-testid="stSidebar"] { background-color: #20242e !important; }
    [data-testid="stSidebar"] * { color: #f5f7fa !important; }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1f2933 !important;
        border: 1px solid #94a3b8 !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {
        color: #1f2933 !important;
        -webkit-text-fill-color: #1f2933 !important;
    }
    ul[role="listbox"], div[role="listbox"], div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        color: #1f2933 !important;
    }
    li[role="option"], div[role="option"] {
        background-color: #ffffff !important;
        color: #1f2933 !important;
    }
    li[role="option"] span, div[role="option"] span { color: #1f2933 !important; }
    li[role="option"]:hover, div[role="option"]:hover { background-color: #e0f2f1 !important; }

    button[data-baseweb="tab"] { color: #334155 !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0f766e !important;
        border-bottom-color: #0f766e !important;
    }

    [data-testid="stMetricValue"] { color: #1f2933 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #52616b !important; }

    .human-card {
        background-color: #ffffff !important;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }
    .soft-note {
        background-color: #eaf7f6 !important;
        border-left: 5px solid #0f766e;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #1f2933 !important;
    }
    .governance-note {
        background-color: #f1f5f9 !important;
        border-left: 5px solid #475569;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #1f2933 !important;
    }
    .warning-note {
        background-color: #fff7ed !important;
        border-left: 5px solid #c2410c;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #1f2933 !important;
    }
    .small-muted { color: #cbd5e1 !important; font-size: 0.92rem; }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background-color: #ffffff !important;
        color: #1f2933 !important;
    }


    /* Dark-mode safe form controls and chart containers */
    div[data-testid="stSelectbox"], div[data-testid="stMultiSelect"], div[data-testid="stRadio"] {
        color: #1f2933 !important;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #ffffff !important;
        border-radius: 10px;
        padding: 0.3rem;
    }

    input, textarea {
        background-color: #ffffff !important;
        color: #1f2933 !important;
        -webkit-text-fill-color: #1f2933 !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #1f2933 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    """Load structured KPI outputs and optional document intelligence outputs."""
    project_root = Path(__file__).resolve().parents[1]
    outputs_dir = project_root / "outputs"
    doc_dir = project_root / "data" / "document_intelligence"

    hr_kpi = pd.read_csv(outputs_dir / "hr_kpi_table.csv")
    absence_kpi = pd.read_csv(outputs_dir / "absence_kpi_table.csv")
    training_kpi = pd.read_csv(outputs_dir / "training_kpi_table.csv")
    employee_value = pd.read_csv(outputs_dir / "employee_value_table_v2.csv")

    department_summary_path = outputs_dir / "department_value_summary_v2.csv"
    department_summary = pd.read_csv(department_summary_path) if department_summary_path.exists() else pd.DataFrame()

    segment_summary_path = outputs_dir / "ai_segment_summary_v2.csv"
    segment_summary = pd.read_csv(segment_summary_path) if segment_summary_path.exists() else pd.DataFrame()

    doc_theme_path = doc_dir / "document_theme_summary.csv"
    doc_theme = pd.read_csv(doc_theme_path) if doc_theme_path.exists() else pd.DataFrame()

    doc_inventory_path = doc_dir / "document_inventory.csv"
    doc_inventory = pd.read_csv(doc_inventory_path) if doc_inventory_path.exists() else pd.DataFrame()

    recommendation_path = outputs_dir / "recommendation_table.csv"
    recommendation_df = (
        pd.read_csv(recommendation_path)
        if recommendation_path.exists() and recommendation_path.stat().st_size > 0
        else pd.DataFrame()
    )

    return (
        hr_kpi,
        absence_kpi,
        training_kpi,
        employee_value,
        department_summary,
        segment_summary,
        doc_theme,
        doc_inventory,
        recommendation_df,
    )


(
    hr_kpi,
    absence_kpi,
    training_kpi,
    employee_value,
    department_summary,
    segment_summary,
    doc_theme,
    doc_inventory,
    recommendation_df,
) = load_data()


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

# --------------------------------------------------
# PRIVACY-SAFE EMPLOYEE DISPLAY IDS
# --------------------------------------------------
# The dashboard never needs to expose raw employee identifiers.
# Stable pseudonyms make the demo readable while preserving privacy.
employee_value = employee_value.reset_index(drop=True)
employee_value["display_employee"] = [
    f"Employee P-{i + 1:03d}" for i in range(len(employee_value))
]

if {"learning_intensity_score", "absenteeism_risk_score"}.issubset(employee_value.columns):
    employee_value["sustainability_balance"] = (
        employee_value["learning_intensity_score"] - employee_value["absenteeism_risk_score"]
    )

if {"human_capital_value_proxy", "kpi_reliability_score"}.issubset(employee_value.columns):
    employee_value["confidence_gap"] = (
        employee_value["human_capital_value_proxy"] * (1 - employee_value["kpi_reliability_score"])
    )

# Simple demo risk label. This is not a final production model; it makes the interface actionable.
if "absenteeism_risk_score" in employee_value.columns:
    q75 = employee_value["absenteeism_risk_score"].quantile(0.75)
    q40 = employee_value["absenteeism_risk_score"].quantile(0.40)
    employee_value["risk_prediction_label"] = employee_value["absenteeism_risk_score"].apply(
        lambda x: "High" if x >= q75 else ("Medium" if x >= q40 else "Low")
    )
else:
    employee_value["risk_prediction_label"] = "Not available"


def recommendation_from_row(row: pd.Series) -> str:
    segment = row.get("segment_name", "")
    risk = row.get("risk_prediction_label", "")
    low_data = bool(row.get("low_data_flag", False))
    sustain = row.get("sustainability_balance", None)

    if low_data or segment == "Low Visibility Employees":
        return "Improve data completeness before interpreting this profile."
    if risk == "High" or segment == "High Engagement / High Risk":
        return "Review workload, recovery balance, and possible wellbeing support."
    if segment == "High Performers / Low Development":
        return "Protect current contribution while offering targeted development opportunities."
    if sustain is not None and pd.notna(sustain) and sustain < 0:
        return "Investigate whether effort is sustainable and discuss recovery or support needs."
    return "Maintain monitoring and discuss development goals in regular check-ins."

employee_value["recommended_action"] = employee_value.apply(recommendation_from_row, axis=1)


# --------------------------------------------------
# RECOMMENDATION TABLE COMPATIBILITY
# --------------------------------------------------
def build_recommendation_table_from_employee_value(source_df: pd.DataFrame) -> pd.DataFrame:
    """Fallback recommendation layer used when outputs/recommendation_table.csv is missing or empty."""
    rows = []
    for _, row in source_df.iterrows():
        segment = str(row.get("segment_name", "Unclassified"))
        risk = str(row.get("risk_prediction_label", "Unknown"))
        low_data = bool(row.get("low_data_flag", False))
        absenteeism = row.get("absenteeism_risk_score", None)
        learning = row.get("learning_intensity_score", None)
        reliability = row.get("kpi_reliability_score", None)

        sustainability = None
        if pd.notna(learning) and pd.notna(absenteeism):
            sustainability = learning - absenteeism

        if low_data or segment == "Low Visibility Employees":
            key_signal = "Low data visibility"
            recommendation = "Improve data completeness before interpreting this profile."
            priority_level = "Medium"
            role_target = "HR / Data AI"
            human_question = "Are we missing important data, or is this employee outside tracked systems?"
        elif risk == "High" or segment == "High Engagement / High Risk":
            key_signal = "High continuity risk"
            recommendation = "Review workload, recovery balance, and wellbeing support."
            priority_level = "High"
            role_target = "Manager / HR"
            human_question = "Is this a motivated employee or team under unsustainable pressure?"
        elif segment == "High Performers / Low Development":
            key_signal = "Strong contribution but limited development signal"
            recommendation = "Offer targeted development opportunities and protect long-term capability."
            priority_level = "Medium"
            role_target = "Manager"
            human_question = "Are strong performers being stretched without enough future skill investment?"
        elif sustainability is not None and pd.notna(sustainability) and sustainability < 0:
            key_signal = "Negative sustainability balance"
            recommendation = "Discuss recovery, workload, and whether current effort is sustainable."
            priority_level = "High"
            role_target = "Manager"
            human_question = "Is value being created in a way that may not be sustainable over time?"
        elif pd.notna(reliability) and reliability < 0.5:
            key_signal = "Low KPI reliability"
            recommendation = "Validate data sources before using this profile for decisions."
            priority_level = "Medium"
            role_target = "HR / Data AI"
            human_question = "Can this signal be trusted enough to guide action?"
        elif pd.notna(learning) and learning < 0.3:
            key_signal = "Low learning intensity"
            recommendation = "Explore relevant training, mobility, or upskilling opportunities."
            priority_level = "Low"
            role_target = "Employee / Manager"
            human_question = "What future capability should be developed next?"
        else:
            key_signal = "Stable profile"
            recommendation = "Maintain regular development check-ins and continue monitoring signals."
            priority_level = "Low"
            role_target = "Employee / Manager"
            human_question = "How can current contribution and learning be sustained?"

        rows.append(
            {
                "display_employee": row.get("display_employee", ""),
                "segment_name": segment,
                "risk_prediction_label": risk,
                "absenteeism_risk_score": row.get("absenteeism_risk_score", None),
                "learning_intensity_score": row.get("learning_intensity_score", None),
                "performance_score": row.get("performance_score", None),
                "kpi_reliability_score": row.get("kpi_reliability_score", None),
                "human_capital_value_proxy": row.get("human_capital_value_proxy", None),
                "reliability_adjusted_value_proxy": row.get("reliability_adjusted_value_proxy", None),
                "key_signal": key_signal,
                "recommendation": recommendation,
                "priority_level": priority_level,
                "role_target": role_target,
                "human_question": human_question,
            }
        )
    return pd.DataFrame(rows)


if recommendation_df.empty:
    recommendation_df = build_recommendation_table_from_employee_value(employee_value)
else:
    if "display_employee" not in recommendation_df.columns:
        recommendation_df = recommendation_df.reset_index(drop=True)
        recommendation_df["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(recommendation_df))]

    merge_cols = [
        c
        for c in [
            "display_employee",
            department_col,
            "segment_name",
            "risk_prediction_label",
            "recommended_action",
        ]
        if c and c in employee_value.columns
    ]
    if "display_employee" in merge_cols:
        recommendation_df = recommendation_df.merge(
            employee_value[merge_cols].drop_duplicates("display_employee"),
            on="display_employee",
            how="left",
            suffixes=("", "_from_employee_table"),
        )

    if "recommendation" not in recommendation_df.columns and "recommended_action" in recommendation_df.columns:
        recommendation_df["recommendation"] = recommendation_df["recommended_action"]
    for col, default in {
        "priority_level": "Low",
        "role_target": "Employee / Manager",
        "key_signal": "Generated recommendation",
        "human_question": "What action would make this signal useful for learning or support?",
    }.items():
        if col not in recommendation_df.columns:
            recommendation_df[col] = default


# --------------------------------------------------
# SMALL HELPERS
# --------------------------------------------------
def safe_mean(df: pd.DataFrame, col: str, decimals: int = 3):
    if col in df.columns and len(df) > 0:
        return round(df[col].mean(), decimals)
    return "N/A"


def safe_value(row: pd.Series, col: str, decimals: int = 3):
    if col in row.index and pd.notna(row[col]):
        val = row[col]
        if isinstance(val, (float, int)):
            return round(val, decimals)
        return val
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


def note(body: str, kind: str = "soft"):
    css_class = {
        "soft": "soft-note",
        "governance": "governance-note",
        "warning": "warning-note",
    }.get(kind, "soft-note")
    st.markdown(f'<div class="{css_class}">{body}</div>', unsafe_allow_html=True)


def segment_actions_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Segment": "Low Visibility Employees",
                "What it may mean": "Low data coverage or limited observed signals.",
                "Human-centered question": "Are we missing data, or is this employee/team genuinely disconnected from tracked systems?",
                "Recommended action": "Improve data completeness before drawing conclusions.",
            },
            {
                "Segment": "High Engagement / High Risk",
                "What it may mean": "Strong learning or activity signals combined with higher absenteeism risk.",
                "Human-centered question": "Is this a motivated person/team under pressure?",
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


def clean_chart(fig):
    """Force Plotly charts to remain readable in browser/Streamlit dark mode."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#1f2933"),
        title_font=dict(color="#1f2933"),
        legend=dict(font=dict(color="#1f2933")),
        margin=dict(l=40, r=30, t=60, b=40),
    )
    fig.update_xaxes(color="#1f2933", gridcolor="#e5e7eb", zerolinecolor="#e5e7eb")
    fig.update_yaxes(color="#1f2933", gridcolor="#e5e7eb", zerolinecolor="#e5e7eb")
    return fig


def show_document_intelligence():
    st.header("Document Intelligence")
    st.markdown(
        """
        Unstructured documents are transformed into structured context signals. This connects qualitative material
        such as engagement, governance, social, and inclusion reports with the quantitative KPI system.
        """
    )

    if doc_inventory.empty and doc_theme.empty:
        st.warning("Document intelligence outputs not found. Run `python src/document_theme_extraction.py` first.")
        return

    if not doc_inventory.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Documents processed", f"{len(doc_inventory):,}")
        col2.metric("File types", f"{doc_inventory['file_type'].nunique():,}" if "file_type" in doc_inventory.columns else "N/A")
        col3.metric("Source folders", f"{doc_inventory['folder'].nunique():,}" if "folder" in doc_inventory.columns else "N/A")

    if not doc_theme.empty:
        st.subheader("Top organizational themes")
        top_themes = (
            doc_theme.groupby("theme", as_index=False)["keyword_count"]
            .sum()
            .sort_values("keyword_count", ascending=False)
        )
        st.dataframe(top_themes, use_container_width=True)

        fig = px.bar(
            top_themes,
            x="theme",
            y="keyword_count",
            title="Theme intensity across unstructured documents",
            labels={"theme": "Theme", "keyword_count": "Keyword mentions"},
        )
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Document-level evidence")
        fig = px.bar(
            doc_theme,
            x="theme",
            y="keyword_count",
            color="document",
            title="Detected themes by document",
            labels={"theme": "Theme", "keyword_count": "Keyword mentions"},
        )
        st.plotly_chart(clean_chart(fig), use_container_width=True)
        st.dataframe(doc_theme, use_container_width=True)

        note(
            "<b>How to read this:</b> document themes are contextual evidence, not direct measures. They help interpret why certain structured signals may appear, for example wellbeing language supporting absenteeism-risk interpretation."
        )

    if not doc_inventory.empty:
        with st.expander("Document inventory"):
            st.dataframe(doc_inventory, use_container_width=True)


def show_recommendations(rec_df: pd.DataFrame, title: str = "Recommended Actions"):
    st.header(title)
    st.markdown(
        """
        This layer translates signals into action. It is the bridge between analytics and real-world decisions:
        what should CACEIS investigate, support, or improve next?
        """
    )

    if rec_df.empty:
        st.warning("No recommendations available. Run `python src/recommendation_engine.py` or check outputs/recommendation_table.csv.")
        return

    working = rec_df.copy()

    col1, col2, col3 = st.columns(3)
    col1.metric("Recommendations", f"{len(working):,}")
    col2.metric(
        "High priority",
        f"{int((working['priority_level'] == 'High').sum()):,}" if "priority_level" in working.columns else "N/A",
    )
    col3.metric(
        "Target roles",
        f"{working['role_target'].nunique():,}" if "role_target" in working.columns else "N/A",
    )

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        if "priority_level" in working.columns:
            priorities = sorted(working["priority_level"].dropna().unique())
            selected_priorities = st.multiselect("Priority level", priorities, default=priorities)
            working = working[working["priority_level"].isin(selected_priorities)]
    with filter_col2:
        if "role_target" in working.columns:
            roles = sorted(working["role_target"].dropna().unique())
            selected_roles = st.multiselect("Role target", roles, default=roles)
            working = working[working["role_target"].isin(selected_roles)]

    if "recommendation" in working.columns:
        action_summary = (
            working["recommendation"]
            .value_counts()
            .rename_axis("recommendation")
            .reset_index(name="profiles")
        )
        st.subheader("Recommendation summary")
        fig = px.bar(
            action_summary.head(10),
            x="profiles",
            y="recommendation",
            orientation="h",
            title="Most frequent recommended actions",
            labels={"profiles": "Profiles", "recommendation": "Recommendation"},
        )
        st.plotly_chart(clean_chart(fig), use_container_width=True)
        st.dataframe(action_summary, use_container_width=True)

    st.subheader("Detailed recommendation table")
    preferred_cols = [
        "display_employee",
        department_col,
        "segment_name",
        "risk_prediction_label",
        "key_signal",
        "recommendation",
        "priority_level",
        "role_target",
        "human_question",
        "absenteeism_risk_score",
        "learning_intensity_score",
        "performance_score",
        "kpi_reliability_score",
    ]
    preferred_cols = [c for c in preferred_cols if c and c in working.columns]
    st.dataframe(working[preferred_cols], use_container_width=True)

    note(
        "<b>Governance guardrail:</b> recommendations are decision-support prompts. They should start a human conversation, not trigger automatic sanctions.",
        "governance",
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## The Human Factor")
    st.markdown(
        """
        <p class="small-muted">
        A role-based student prototype for exploring human capital as a living asset:
        performance, learning, risk, reliability, and context.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### Reading guide")
    st.markdown(
        """
        - **Do not rank people mechanically**  
        - **Check data reliability first**  
        - **Use AI outputs as questions, not verdicts**  
        - **Interpret value as a proxy, not truth**
        """
    )
    st.divider()
    st.caption("Made for the CACEIS x Albert School Alberthon")


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("The Human Factor @ CACEIS")
st.caption("A role-based human capital intelligence prototype — built for learning, coaching, governance, and model monitoring.")

note(
    "<b>Core idea:</b> we are not measuring people as scores. We are building a system that helps different users interpret signals of learning, risk, reliability, and value creation.",
    "soft",
)

col_a, col_b, col_c = st.columns(3)
with col_a:
    soft_card("Human signals", "HR, absenteeism, training, performance, finance/FTE, and unstructured documents.")
with col_b:
    soft_card("Behavioral KPIs", "Proxies for learning, continuity risk, development, and data reliability.")
with col_c:
    soft_card("AI insight layer", "Segmentation, risk labelling, and recommendations that support—not replace—human judgment.")


# --------------------------------------------------
# ROLE SELECTOR
# --------------------------------------------------
role = st.selectbox(
    "Select user perspective",
    ["Employee", "Manager", "HR", "Data / AI Admin"],
    index=2,
)

ROLE_DESCRIPTIONS = {
    "Employee": "Self-development and learning. The employee sees only their own signals, interpretation, and suggested development actions.",
    "Manager": "Team coaching and workload support. The manager sees aggregated team indicators and risk signals, not a punitive ranking tool.",
    "HR": "Workforce governance and strategic planning. HR sees cross-team patterns, bias/data-quality checks, document context, and recommendations.",
    "Data / AI Admin": "Model development and monitoring. The admin view checks data coverage, pipeline outputs, AI segments, and document intelligence quality.",
}

note(f"<b>Current view:</b> {ROLE_DESCRIPTIONS[role]}", "governance")


# --------------------------------------------------
# EMPLOYEE VIEW
# --------------------------------------------------
if role == "Employee":
    tab1, tab2 = st.tabs(["My Signals", "My Development"])

    employee_profiles = sorted(employee_value["display_employee"].dropna().unique()) if "display_employee" in employee_value.columns else []
    selected_employee = st.selectbox("Select employee profile for demo", employee_profiles) if employee_profiles else None
    emp = employee_value[employee_value["display_employee"] == selected_employee].iloc[0] if selected_employee else None

    with tab1:
        st.header("My Signals")
        if emp is None:
            st.warning("No employee profiles found in the integrated table.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Learning signal", safe_value(emp, "learning_intensity_score"))
            col2.metric("Performance signal", safe_value(emp, "performance_score"))
            col3.metric("Continuity risk", safe_value(emp, "absenteeism_risk_score"))
            col4.metric("Data reliability", safe_value(emp, "kpi_reliability_score"))

            st.subheader("Profile summary")
            profile_cols = [
                "display_employee",
                department_col,
                "segment_name",
                "human_capital_value_proxy",
                "reliability_adjusted_value_proxy",
                "sustainability_balance",
                "risk_prediction_label",
                "recommended_action",
            ]
            profile_cols = [c for c in profile_cols if c and c in employee_value.columns]
            st.dataframe(employee_value[employee_value["display_employee"] == selected_employee][profile_cols], use_container_width=True)

            note(
                "<b>Important:</b> this view is designed for self-understanding. It should not compare the employee to named colleagues or be used as an automatic evaluation tool.",
                "governance",
            )

    with tab2:
        st.header("My Development")
        if emp is not None:
            st.subheader("What this may mean")
            balance = emp.get("sustainability_balance", None)
            if balance is not None and pd.notna(balance):
                if balance < 0:
                    st.warning("Your learning/continuity balance suggests possible pressure. This is a prompt to discuss workload, recovery, or support—not a judgment.")
                else:
                    st.success("Your learning/continuity balance is positive. This suggests current development activity is more visible than risk pressure.")

            st.subheader("Recommended next step")
            personal_rec = recommendation_df[recommendation_df["display_employee"] == selected_employee]
            if not personal_rec.empty and "recommendation" in personal_rec.columns:
                st.info(personal_rec.iloc[0]["recommendation"])
                if "human_question" in personal_rec.columns:
                    st.markdown(f"**Human question to discuss:** {personal_rec.iloc[0]['human_question']}")
            else:
                st.info(emp.get("recommended_action", "Maintain regular check-ins and update development goals."))

            st.subheader("Questions to bring to a manager")
            st.markdown(
                """
                - What skills should I develop next?
                - Is my current workload sustainable?
                - Are there development opportunities aligned with my role?
                - Is any important work invisible in the current data?
                """
            )


# --------------------------------------------------
# MANAGER VIEW
# --------------------------------------------------
elif role == "Manager":
    tab1, tab2, tab3 = st.tabs(["Team Overview", "Risk & Signals", "Actions"])

    if department_col:
        departments = sorted(employee_value[department_col].dropna().unique())
        selected_department = st.selectbox("Select team / department", departments)
        team = employee_value[employee_value[department_col] == selected_department].copy()
    else:
        selected_department = "All employees"
        team = employee_value.copy()
        st.warning("No department column detected. Showing all employees for demo purposes.")

    with tab1:
        st.header("Team Overview")
        st.markdown(f"Team selected: **{selected_department}**")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Team size", f"{len(team):,}")
        col2.metric("Avg value proxy", safe_mean(team, "human_capital_value_proxy"))
        col3.metric("Avg learning signal", safe_mean(team, "learning_intensity_score"))
        col4.metric("Avg reliability", safe_mean(team, "kpi_reliability_score"))

        if "segment_name" in team.columns:
            seg_counts = team["segment_name"].value_counts().rename_axis("segment").reset_index(name="employees")
            fig = px.bar(seg_counts, x="segment", y="employees", title="Team AI segment distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(seg_counts, use_container_width=True)

    with tab2:
        st.header("Risk & Signals")
        risk_cols = [
            "display_employee",
            "segment_name",
            "risk_prediction_label",
            "absenteeism_risk_score",
            "learning_intensity_score",
            "sustainability_balance",
            "kpi_reliability_score",
            "low_data_flag",
            "recommended_action",
        ]
        risk_cols = [c for c in risk_cols if c in team.columns]

        if "risk_prediction_label" in team.columns:
            risk_counts = team["risk_prediction_label"].value_counts().rename_axis("risk").reset_index(name="employees")
            fig = px.bar(risk_counts, x="risk", y="employees", title="Predicted continuity-risk levels")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Employees requiring coaching attention")
        priority = team.copy()
        if "risk_prediction_label" in priority.columns:
            priority = priority[priority["risk_prediction_label"].isin(["High", "Medium"])]
        if "sustainability_balance" in priority.columns:
            priority = priority.sort_values("sustainability_balance", ascending=True)
        st.dataframe(priority[risk_cols].head(25), use_container_width=True)

        note(
            "<b>Manager guardrail:</b> this view is for coaching and workload support. It should trigger conversations, not sanctions.",
            "governance",
        )

    with tab3:
        st.header("Actions")
        st.subheader("Recommended management actions by profile")
        st.dataframe(segment_actions_df(), use_container_width=True)

        st.subheader("Team-level recommendation summary")
        team_recommendations = recommendation_df[
            recommendation_df["display_employee"].isin(team["display_employee"])
        ].copy() if "display_employee" in recommendation_df.columns else pd.DataFrame()

        if not team_recommendations.empty:
            show_recommendations(team_recommendations, "Team Recommended Actions")
        elif "recommended_action" in team.columns:
            action_summary = team["recommended_action"].value_counts().rename_axis("recommended_action").reset_index(name="employees")
            st.dataframe(action_summary, use_container_width=True)

        st.markdown(
            """
            **Practical coaching loop:**  
            1. Check data reliability.  
            2. Identify team-level pressure or development gaps.  
            3. Discuss context with employees.  
            4. Adjust workload, support, or training access.  
            5. Reassess indicators over time.
            """
        )


# --------------------------------------------------
# HR VIEW
# --------------------------------------------------
elif role == "HR":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Overview",
            "Value Explorer",
            "AI Segments",
            "Recommendations",
            "KPI Detail",
            "Document Intelligence",
            "Governance & Roadmap",
        ]
    )

    with tab1:
        st.header("Integrated Human Capital Overview")
        st.markdown("Cross-team view for workforce planning, governance, and strategic recommendations.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Employees mapped", f"{len(employee_value):,}")
        col2.metric("Average value proxy", safe_mean(employee_value, "human_capital_value_proxy"))
        col3.metric("Average reliability", safe_mean(employee_value, "kpi_reliability_score"))
        col4.metric("Training visibility", f"{int(employee_value['has_training_record'].sum()):,}" if "has_training_record" in employee_value.columns else "N/A")

        if "human_capital_value_proxy" in employee_value.columns:
            fig = px.histogram(employee_value, x="human_capital_value_proxy", nbins=40, title="Human Capital Value Proxy Distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "segment_name" in employee_value.columns:
            segment_counts = employee_value["segment_name"].value_counts().rename_axis("segment_name").reset_index(name="employees")
            fig = px.bar(segment_counts, x="segment_name", y="employees", title="Number of employees by AI segment")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        note("<b>Leadership use:</b> CACEIS leadership does not need individual-level views. HR can provide aggregated workforce-risk and value-creation summaries from this perspective.", "governance")

    with tab2:
        st.header("Value Explorer")
        filtered = employee_value.copy()
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_segments = st.multiselect("Filter by AI segment", sorted(filtered["segment_name"].dropna().unique()), default=sorted(filtered["segment_name"].dropna().unique()))
            filtered = filtered[filtered["segment_name"].isin(selected_segments)]

        with col2:
            if "low_data_flag" in filtered.columns:
                low_data_choice = st.selectbox("Data visibility", ["All", "Only low-visibility employees", "Exclude low-visibility employees"])
                if low_data_choice == "Only low-visibility employees":
                    filtered = filtered[filtered["low_data_flag"] == True]
                elif low_data_choice == "Exclude low-visibility employees":
                    filtered = filtered[filtered["low_data_flag"] == False]

        with col3:
            if department_col:
                departments = sorted(filtered[department_col].dropna().unique())
                selected_departments = st.multiselect("Filter by department/entity", departments, default=departments)
                filtered = filtered[filtered[department_col].isin(selected_departments)]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Selected employees", f"{len(filtered):,}")
        col2.metric("Avg value proxy", safe_mean(filtered, "human_capital_value_proxy"))
        col3.metric("Avg learning signal", safe_mean(filtered, "learning_intensity_score"))
        col4.metric("Avg continuity risk", safe_mean(filtered, "absenteeism_risk_score"))

        if {"learning_intensity_score", "human_capital_value_proxy", "segment_name"}.issubset(filtered.columns):
            fig = px.scatter(
                filtered,
                x="learning_intensity_score",
                y="human_capital_value_proxy",
                color="segment_name",
                hover_data=[c for c in ["display_employee", "performance_score", "absenteeism_risk_score", "kpi_reliability_score"] if c in filtered.columns],
                title="Learning intensity vs human capital value proxy",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "sustainability_balance" in filtered.columns:
            fig = px.histogram(filtered, x="sustainability_balance", nbins=30, color="segment_name", title="Sustainability balance distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        display_cols = [
            "display_employee",
            department_col,
            "segment_name",
            "risk_prediction_label",
            "human_capital_value_proxy",
            "reliability_adjusted_value_proxy",
            "kpi_reliability_score",
            "performance_score",
            "learning_intensity_score",
            "absenteeism_risk_score",
            "sustainability_balance",
            "recommended_action",
        ]
        display_cols = [c for c in display_cols if c and c in filtered.columns]
        st.dataframe(filtered[display_cols], use_container_width=True)

    with tab3:
        st.header("AI Segments")
        st.markdown("Clustering identifies broad behavioral profiles. Segments support investigation and action design, not individual verdicts.")
        st.dataframe(segment_actions_df(), use_container_width=True)

        metrics = ["human_capital_value_proxy", "reliability_adjusted_value_proxy", "performance_score", "learning_intensity_score", "absenteeism_risk_score", "sustainability_balance", "data_coverage_score", "kpi_reliability_score"]
        available_metrics = [c for c in metrics if c in employee_value.columns]
        if available_metrics:
            summary = employee_value.groupby("segment_name", as_index=False)[available_metrics].mean()
            counts = employee_value.groupby("segment_name", as_index=False).size().rename(columns={"size": "employees"})
            summary = counts.merge(summary, on="segment_name", how="left")
            st.dataframe(summary, use_container_width=True)
            fig = px.bar(summary, x="segment_name", y="human_capital_value_proxy", title="Average value proxy by segment")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

    with tab4:
        show_recommendations(recommendation_df, "Strategic Recommendation Layer")

    with tab5:
        st.header("KPI Detail")
        st.markdown("KPIs are observable signals. They require context, reliability checks, and human interpretation.")
        kpi_section = st.radio("Choose KPI view", ["HR & Performance", "Absenteeism / Continuity", "Learning"], horizontal=True)

        if kpi_section == "HR & Performance":
            col1, col2, col3 = st.columns(3)
            col1.metric("Employees", f"{len(hr_kpi):,}")
            col2.metric("Average performance", safe_mean(hr_kpi, "avg_performance", 2))
            col3.metric("Average talent progression", safe_mean(hr_kpi, "talent_progression_proxy", 2))
            if "avg_performance" in hr_kpi.columns:
                fig = px.histogram(hr_kpi, x="avg_performance", nbins=10, title="Average performance distribution")
                st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(hr_kpi, use_container_width=True)

        elif kpi_section == "Absenteeism / Continuity":
            col1, col2, col3 = st.columns(3)
            col1.metric("Employees", f"{len(absence_kpi):,}")
            col2.metric("Average absence days", safe_mean(absence_kpi, "absence_days", 2))
            col3.metric("Average continuity risk", safe_mean(absence_kpi, "absenteeism_risk_score", 2))
            if "absenteeism_risk_score" in absence_kpi.columns:
                fig = px.histogram(absence_kpi, x="absenteeism_risk_score", nbins=30, title="Absenteeism risk distribution")
                st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(absence_kpi, use_container_width=True)

        elif kpi_section == "Learning":
            col1, col2, col3 = st.columns(3)
            col1.metric("Employees", f"{len(training_kpi):,}")
            col2.metric("Average training hours", safe_mean(training_kpi, "training_hours", 2))
            col3.metric("Average learning intensity", safe_mean(training_kpi, "learning_intensity_score", 2))
            if "learning_intensity_score" in training_kpi.columns:
                fig = px.histogram(training_kpi, x="learning_intensity_score", nbins=30, title="Learning intensity distribution")
                st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(training_kpi, use_container_width=True)

    with tab6:
        show_document_intelligence()

    with tab7:
        st.header("Governance & Roadmap")
        st.subheader("Pipeline")
        st.markdown(
            """
            1. Clean separate HR, absence, training, and finance/FTE files.  
            2. Calculate KPI tables for each source.  
            3. Validate anonymized employee identifiers and merge safe sources.  
            4. Create a human capital value proxy and reliability-adjusted score.  
            5. Use AI segmentation and risk labelling to structure questions.  
            6. Add document intelligence from PDFs/PPTs/DOCX to contextualize structured indicators.  
            7. Export dashboard-ready outputs and prepare for Snowflake integration.
            """
        )
        st.subheader("Governance principles")
        st.markdown(
            """
            - Use anonymized / pseudonymized identifiers.  
            - Do not use outputs for automatic individual sanctions.  
            - Display reliability and data coverage before interpreting scores.  
            - Monitor bias in performance reviews and training access.  
            - Treat AI segments and risk labels as conversation starters.  
            - Keep humans in the loop for all HR decisions.
            """
        )
        st.subheader("Implementation roadmap")
        roadmap = pd.DataFrame(
            [
                {"Phase": "1. Prototype", "Focus": "Structured KPIs, value proxy, AI segmentation", "Owner": "Student/Data team"},
                {"Phase": "2. Evolved prototype", "Focus": "Document intelligence, recommendations, role-based views", "Owner": "HR + Data/AI"},
                {"Phase": "3. Pilot", "Focus": "Department-level testing, feedback loops, bias checks", "Owner": "HR + managers"},
                {"Phase": "4. Scale", "Focus": "Snowflake integration, governance workflows, model monitoring", "Owner": "Data/AI Admin + HR"},
            ]
        )
        st.dataframe(roadmap, use_container_width=True)


# --------------------------------------------------
# DATA / AI ADMIN VIEW
# --------------------------------------------------
elif role == "Data / AI Admin":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pipeline Health", "Data Quality", "Model Monitoring", "Recommendation Monitoring", "Document Pipeline"])

    with tab1:
        st.header("Pipeline Health")
        st.markdown("Admin view for the Data/AI team: monitor reproducibility, data availability, and output readiness.")

        output_checks = pd.DataFrame(
            [
                {"Output": "hr_kpi_table.csv", "Rows": len(hr_kpi), "Status": "Loaded" if not hr_kpi.empty else "Missing/empty"},
                {"Output": "absence_kpi_table.csv", "Rows": len(absence_kpi), "Status": "Loaded" if not absence_kpi.empty else "Missing/empty"},
                {"Output": "training_kpi_table.csv", "Rows": len(training_kpi), "Status": "Loaded" if not training_kpi.empty else "Missing/empty"},
                {"Output": "employee_value_table_v2.csv", "Rows": len(employee_value), "Status": "Loaded" if not employee_value.empty else "Missing/empty"},
                {"Output": "document_theme_summary.csv", "Rows": len(doc_theme), "Status": "Loaded" if not doc_theme.empty else "Missing/empty"},
                {"Output": "document_inventory.csv", "Rows": len(doc_inventory), "Status": "Loaded" if not doc_inventory.empty else "Missing/empty"},
                {"Output": "recommendation_table.csv", "Rows": len(recommendation_df), "Status": "Loaded" if not recommendation_df.empty else "Missing/empty"},
            ]
        )
        st.dataframe(output_checks, use_container_width=True)

    with tab2:
        st.header("Data Quality")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg data coverage", safe_mean(employee_value, "data_coverage_score"))
        col2.metric("Avg KPI reliability", safe_mean(employee_value, "kpi_reliability_score"))
        col3.metric("Low-data records", f"{int(employee_value['low_data_flag'].sum()):,}" if "low_data_flag" in employee_value.columns else "N/A")

        dq_cols = ["display_employee", department_col, "data_coverage_score", "kpi_reliability_score", "low_data_flag", "has_performance_record", "has_absence_record", "has_training_record"]
        dq_cols = [c for c in dq_cols if c and c in employee_value.columns]
        st.dataframe(employee_value[dq_cols].head(100), use_container_width=True)

        if "data_coverage_score" in employee_value.columns:
            fig = px.histogram(employee_value, x="data_coverage_score", nbins=20, title="Data coverage score distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

    with tab3:
        st.header("Model Monitoring")
        st.markdown("Monitor AI outputs for balance, interpretability, and responsible use.")

        if "segment_name" in employee_value.columns:
            seg_counts = employee_value["segment_name"].value_counts().rename_axis("segment_name").reset_index(name="employees")
            st.dataframe(seg_counts, use_container_width=True)
            fig = px.bar(seg_counts, x="segment_name", y="employees", title="AI segment distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "risk_prediction_label" in employee_value.columns:
            risk_counts = employee_value["risk_prediction_label"].value_counts().rename_axis("risk_prediction_label").reset_index(name="employees")
            st.dataframe(risk_counts, use_container_width=True)
            fig = px.bar(risk_counts, x="risk_prediction_label", y="employees", title="Risk label distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        note(
            "<b>Admin guardrail:</b> in a production system, this page would include model versioning, fairness checks, drift monitoring, and validation metrics.",
            "governance",
        )

    with tab4:
        st.header("Recommendation Monitoring")
        if recommendation_df.empty:
            st.warning("recommendation_table.csv is missing or empty.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Recommendations", f"{len(recommendation_df):,}")
            col2.metric("Priority levels", f"{recommendation_df['priority_level'].nunique():,}" if "priority_level" in recommendation_df.columns else "N/A")
            col3.metric("Target roles", f"{recommendation_df['role_target'].nunique():,}" if "role_target" in recommendation_df.columns else "N/A")

            if "priority_level" in recommendation_df.columns:
                priority_counts = recommendation_df["priority_level"].value_counts().rename_axis("priority_level").reset_index(name="profiles")
                fig = px.bar(priority_counts, x="priority_level", y="profiles", title="Recommendation priority distribution")
                st.plotly_chart(clean_chart(fig), use_container_width=True)

            if "role_target" in recommendation_df.columns:
                role_counts = recommendation_df["role_target"].value_counts().rename_axis("role_target").reset_index(name="profiles")
                st.dataframe(role_counts, use_container_width=True)

            show_recommendations(recommendation_df, "Full Recommendation Table")

    with tab5:
        show_document_intelligence()
