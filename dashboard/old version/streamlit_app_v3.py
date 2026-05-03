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
    page_title="ONEValue @CACEIS",
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
    project_root = Path(__file__).resolve().parents[2]
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

    onevalue_ai_path = outputs_dir / "onevalue_ai_insights.csv"
    onevalue_ai_df = (
        pd.read_csv(onevalue_ai_path)
        if onevalue_ai_path.exists() and onevalue_ai_path.stat().st_size > 0
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
        onevalue_ai_df,
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
    onevalue_ai_df,
) = load_data()


# --------------------------------------------------
# BASIC CLEANUP / COMPATIBILITY
# --------------------------------------------------
if "segment_name" not in employee_value.columns:
    if "ai_segment_label" in employee_value.columns:
        employee_value["segment_name"] = employee_value["ai_segment_label"]
    elif "ai_segment" in employee_value.columns:
        employee_value["segment_name"] = "AI Segment " + employee_value["ai_segment"].astype(str)
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
    st.markdown("## ONEValue")
    st.markdown(
    """
    <p class="small-muted">
    A decision-based human capital system that links employee actions, learning, and risk to value creation.
    </p>
    """,
    unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("### Platform principles")
    st.markdown(
    """
    - **Start with signals, not conclusions**  
    - **Interpret value through context, not scores**  
    - **Focus on decisions and behaviors, not outcomes alone**  
    - **Use AI to identify patterns, not to judge individuals**  
    - **Always validate signals before acting**
    """
    )
    st.divider()
    st.caption("Human Capital Intelligence Prototype · Built for CACEIS")


# --------------------------------------------------
# HEADER + AUTHENTICATION (DEMO)
# --------------------------------------------------
st.title("ONEValue by CACEIS")
st.caption(
    "A human capital intelligence platform inspired by the ONE CACEIS culture: care, growth, responsibility, and learning."
)

# Pick two employee demo accounts with the strongest data coverage.
employee_demo_accounts = (
    employee_value.sort_values(
        by=["data_coverage_score", "kpi_reliability_score"],
        ascending=False,
    )
    .head(2)["display_employee"]
    .tolist()
    if {"data_coverage_score", "kpi_reliability_score", "display_employee"}.issubset(employee_value.columns)
    else employee_value["display_employee"].head(2).tolist()
)

# Pick two manager demo accounts with the largest teams.
if department_col:
    manager_demo_departments = (
        employee_value.groupby(department_col)
        .size()
        .sort_values(ascending=False)
        .head(2)
        .index
        .tolist()
    )
else:
    manager_demo_departments = []

USERS = {
    "emp_001": {
        "role": "Employee",
        "id": employee_demo_accounts[0] if len(employee_demo_accounts) > 0 else "Employee P-001",
    },
    "emp_002": {
        "role": "Employee",
        "id": employee_demo_accounts[1] if len(employee_demo_accounts) > 1 else "Employee P-002",
    },
    "mgr_001": {
        "role": "Manager",
        "department": manager_demo_departments[0] if len(manager_demo_departments) > 0 else None,
    },
    "mgr_002": {
        "role": "Manager",
        "department": manager_demo_departments[1] if len(manager_demo_departments) > 1 else None,
    },
    "hr_001": {"role": "HR"},
    "admin_001": {"role": "Product Owner"},
}

with st.sidebar:
    st.markdown("### Access")

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user:
    current_login = st.session_state.logged_in_user
    current_user = USERS[current_login]

    st.sidebar.success(f"Signed in as: {current_login} ({current_user['role']})")

    if st.sidebar.button("Sign out"):
        st.session_state.logged_in_user = None
        st.rerun()

    user = USERS[st.session_state.logged_in_user]
    role = user["role"]

    # --------------------------------------------------
    # ROLE-AWARE HEADER AFTER SIGN-IN
    # --------------------------------------------------
    if role == "Employee":
        user_name = user.get("id", "Employee")

        note(
            f"<b>Hello {user_name}.</b> This workspace helps you track your development, annual review signals, training visibility, PTO/absence balance, and value contribution over time.",
            "soft",
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            soft_card(
                "My development",
                "Review training participation, learning intensity, and future capability signals.",
            )

        with col_b:
            soft_card(
                "My annual review signals",
                "Track performance consistency, progression indicators, and data reliability before drawing conclusions.",
            )

        with col_c:
            soft_card(
                "My sustainable value",
                "Understand how contribution, learning, and absence/PTO signals combine into a bottom-up value profile.",
            )

    elif role == "Manager":
        manager_department = user.get("department", "your team")
        note(
            f"<b>Hello Manager.</b> You are viewing <b>{manager_department}</b>. This workspace helps you support your team, identify coaching needs, and understand value creation without ranking employees mechanically.",
            "soft",
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            soft_card(
                "Team signals",
                "View team-level learning, performance, reliability, and continuity-risk patterns.",
            )
        with col_b:
            soft_card(
                "Coaching priorities",
                "Identify where support, workload review, or training access may be needed.",
            )
        with col_c:
            soft_card(
                "Sustainable value creation",
                "Understand how team behaviors and indicators connect to long-term human capital value.",
            )

    elif role == "HR":
        note(
            "<b>Hello HR.</b> This workspace helps monitor workforce patterns, data quality, AI segments, and strategic recommendations across the organization.",
            "soft",
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            soft_card(
                "Workforce patterns",
                "Analyze value, learning, absenteeism, and development signals across teams.",
            )
        with col_b:
            soft_card(
                "Governance",
                "Check data reliability, bias risks, and responsible use of employee indicators.",
            )
        with col_c:
            soft_card(
                "Strategic actions",
                "Use recommendations to guide workforce planning and capability development.",
            )

    elif role == "Product Owner":
        note(
            "<b>Hello Product Owner.</b> This workspace helps monitor pipeline health, model behavior, recommendation quality, and deployment readiness.",
            "soft",
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            soft_card(
                "Pipeline health",
                "Check whether KPI, recommendation, and document intelligence outputs are loaded correctly.",
            )
        with col_b:
            soft_card(
                "Model monitoring",
                "Track AI segments, risk labels, and data coverage before operational use.",
            )
        with col_c:
            soft_card(
                "Responsible deployment",
                "Validate governance, access control, and audit readiness.",
            )

    st.caption(
        "Built by Anna Mika, Nolwenn Montillot, Emma Lou Villaret, and Hannah Zilesch · CACEIS x Albert School Alberthon"
    )

else:
    login = st.sidebar.text_input("Enter demo login ID")

    if login in USERS:
        st.session_state.logged_in_user = login
        st.rerun()

    note(
        "<b>Welcome.</b> The platform adapts to your role: employees track development, managers act on team signals, HR analyzes workforce patterns, and product owners oversee system performance.",
        "soft",
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        soft_card(
            "From behavior to value",
            "The platform captures employee actions, learning, and signals to understand how value is actually created over time.",
        )

    with col_b:
        soft_card(
            "Signals, not scores",
            "KPIs are treated as indicators, not truth. They help identify patterns, risks, and opportunities—not rank individuals.",
        )

    with col_c:
        soft_card(
            "Decision support system",
            "AI highlights segments, risks, and recommendations so managers and HR can act earlier and more effectively.",
        )

    st.caption(
        "Built by Anna Mika, Nolwenn Montillot, Emma Lou Villaret, and Hannah Zilesch · CACEIS x Albert School Alberthon"
    )

    st.markdown("## Sign in required")
    st.info("Enter a demo login ID in the sidebar to unlock your workspace.")

    st.markdown("### Demo login IDs")

    emp_col, mgr_col, other_col, spacer = st.columns([1, 1, 1, 3])

    with emp_col:
        st.markdown("**Employees**")
        st.markdown("`emp_001`")
        st.markdown("`emp_002`")

    with mgr_col:
        st.markdown("**Managers**")
        st.markdown("`mgr_001`")
        st.markdown("`mgr_002`")

    with other_col:
        st.markdown("**Other roles**")
        st.markdown("`hr_001`")
        st.markdown("`admin_001`")

    note(
        "<b>Access control:</b> users only see the data required for their role. Production systems would enforce this through secure authentication.",
        "governance",
    )

    st.stop()


# --------------------------------------------------
# EMPLOYEE VIEW
# --------------------------------------------------
if role == "Employee":
    tab1, tab2 = st.tabs(["My Value Dashboard", "My Development"])

    selected_employee = user["id"]
    employee_match = employee_value[employee_value["display_employee"] == selected_employee]

    if employee_match.empty:
        emp = None
        st.warning(f"No profile found for {selected_employee}. Check the demo user mapping.")
    else:
        emp = employee_match.iloc[0]

    with tab1:
        st.header("My Personal Value Dashboard")

        if emp is None:
            st.warning("No employee profile found in the integrated table.")
        else:
            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Learning signal",
                safe_value(emp, "learning_intensity_score"),
                help="Visible training and development activity. This is a proxy for learning investment, not a measure of talent."
            )

            col2.metric(
                "Annual review signal",
                safe_value(emp, "performance_score"),
                help="Available annual review or performance information. Reviews should be interpreted with context because they can be incomplete or biased."
            )

            col3.metric(
                "PTO / absence balance",
                safe_value(emp, "absenteeism_risk_score"),
                help="Absence/PTO-related pattern used as a continuity and wellbeing signal. This is not a judgment."
            )

            col4.metric(
                "Data reliability",
                safe_value(emp, "kpi_reliability_score"),
                help="How complete and reliable the available data is. Low reliability means insights should be interpreted carefully."
            )

            st.subheader("My profile summary")

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                soft_card(
                    "My team / entity",
                    str(safe_value(emp, department_col)) if department_col else "Not available"
                )

            with summary_col2:
                soft_card(
                    "My current profile",
                    str(safe_value(emp, "segment_name"))
                )

            with summary_col3:
                soft_card(
                    "Current continuity label",
                    str(safe_value(emp, "risk_prediction_label"))
                )

            value_col1, value_col2, value_col3 = st.columns(3)

            with value_col1:
                soft_card(
                    "Value contribution proxy",
                    str(safe_value(emp, "human_capital_value_proxy"))
                )

            with value_col2:
                soft_card(
                    "Reliability-adjusted value",
                    str(safe_value(emp, "reliability_adjusted_value_proxy"))
                )

            with value_col3:
                soft_card(
                    "Sustainability balance",
                    str(safe_value(emp, "sustainability_balance"))
                )

            st.subheader("Recommended focus")

            employee_segment = str(emp.get("segment_name", ""))
            employee_risk = str(emp.get("risk_prediction_label", ""))
            learning_score = emp.get("learning_intensity_score", None)
            reliability_score = emp.get("kpi_reliability_score", None)

            if employee_segment == "High Performers / Low Development":
                employee_focus = (
                    "You show a strong contribution signal, but your visible development activity is limited. "
                    "A useful next step is to discuss targeted training, mobility, or upskilling opportunities."
                )
            elif employee_segment == "High Engagement / High Risk" or employee_risk == "High":
                employee_focus = (
                    "Your profile suggests strong activity combined with possible pressure. "
                    "A useful next step is to discuss workload, recovery balance, and support needs with your manager."
                )
            elif employee_segment == "Low Visibility Employees":
                employee_focus = (
                    "Some parts of your profile are not fully visible in the available data. "
                    "A useful next step is to check whether your training, contribution, or recent work is being captured correctly."
                )
            elif pd.notna(learning_score) and learning_score < 0.3:
                employee_focus = (
                    "Your learning signal is currently low. "
                    "A useful next step is to identify one relevant training or development opportunity for the next review cycle."
                )
            elif pd.notna(reliability_score) and reliability_score < 0.5:
                employee_focus = (
                    "Some insights are based on incomplete information. "
                    "A useful next step is to review whether your HR, training, and review records are up to date."
                )
            else:
                employee_focus = (
                    "Your current signals appear stable. "
                    "A useful next step is to maintain regular development conversations and define your next growth objective."
                )

            st.info(employee_focus)

            note(
                "<b>Your data rights:</b> this workspace uses your personal HR, training, review, and absence/PTO data to provide development-oriented insights. "
                "These insights are provided for transparency and development support. They are not used for automatic evaluation, ranking, or disciplinary decisions. "
                "For full details, see the employee data policy and consent framework below.",
                "governance",
            )

            with st.expander("View employee data policy and consent framework"):
                st.markdown(
                    """
                    **1. Purpose of data use**  
                    This workspace uses HR, training, annual review, and absence/PTO data to support employee development, workforce planning, and organizational learning.

                    **2. Employee transparency**  
                    Employees can view the signals derived from their own data. These signals are designed to support understanding, not to define individual worth.

                    **3. Responsible use**  
                    Data and AI outputs must not be used for automatic performance evaluation, employee ranking, or disciplinary action without human review.

                    **4. Data reliability and limitations**  
                    Indicators depend on data completeness and quality. Missing, outdated, or biased data may affect interpretation.

                    **5. Consent and governance**  
                    In a production system, employees would be informed of data usage policies, consent mechanisms, and internal HR governance rules. Processing would follow GDPR principles and company data policies.

                    **6. Human-in-the-loop principle**  
                    Managers and HR remain responsible for decisions. AI-generated signals are decision-support prompts, not final judgments.

                    ---
                    _Prototype policy notice for demonstration purposes._
                    """
                )

    with tab2:
        st.header("My Development Plan")

        if emp is not None:
            st.markdown(
                "This view translates your signals into practical questions and next steps for your next review cycle."
            )

            dev_col1, dev_col2, dev_col3 = st.columns(3)

            with dev_col1:
                soft_card(
                    "Current development signal",
                    f"Learning score: {safe_value(emp, 'learning_intensity_score')}"
                )

            with dev_col2:
                soft_card(
                    "Review preparation",
                    f"Annual review signal: {safe_value(emp, 'performance_score')}"
                )

            with dev_col3:
                soft_card(
                    "Sustainability check",
                    f"Balance score: {safe_value(emp, 'sustainability_balance')}"
                )

            st.subheader("Recommended next step")
            st.info(employee_focus)

            st.subheader("Suggested action plan")

            action_plan = pd.DataFrame(
                [
                    {
                        "Step": "1. Validate my data",
                        "Why it matters": "Make sure training, annual review, and absence/PTO records reflect reality.",
                        "Suggested action": "Check whether anything important is missing or outdated.",
                    },
                    {
                        "Step": "2. Prepare my review",
                        "Why it matters": "Annual review signals need context, examples, and discussion.",
                        "Suggested action": "List concrete achievements, skills developed, and contribution examples.",
                    },
                    {
                        "Step": "3. Choose one development priority",
                        "Why it matters": "Value grows through learning, not only current performance.",
                        "Suggested action": "Select one training, mentoring, mobility, or upskilling opportunity.",
                    },
                    {
                        "Step": "4. Discuss sustainability",
                        "Why it matters": "Sustained value depends on workload, recovery, and long-term engagement.",
                        "Suggested action": "Raise workload or support needs if the current pace feels difficult to maintain.",
                    },
                ]
            )

            st.dataframe(action_plan, use_container_width=True, hide_index=True)

            st.subheader("Questions for my manager")

            q1, q2 = st.columns(2)

            with q1:
                st.markdown(
                    """
                    **Development**
                    - What skills should I build before my next review?
                    - Which training would be most useful for my role?
                    - Are there mentoring or mobility opportunities?
                    """
                )

            with q2:
                st.markdown(
                    """
                    **Value and sustainability**
                    - Which parts of my contribution create the most value?
                    - Is any important work invisible in the current data?
                    - Is my workload sustainable over the next review cycle?
                    """
                )

            note(
                "<b>Your development drives value:</b> value is not only performance—it comes from learning, contribution, and sustainability over time. "
                "Use this view to shape your next step.",
                "governance",
            )

# --------------------------------------------------
# MANAGER VIEW
# --------------------------------------------------
elif role == "Manager":
    tab1, tab2, tab3 = st.tabs(["Team Dashboard", "Team Signals", "Action Plan"])

    if department_col:
        selected_department = user["department"]
        team = employee_value[employee_value[department_col] == selected_department].copy()

        if team.empty:
            st.warning(
                f"No employees found for manager department: {selected_department}. "
                "Check the demo user mapping or department names in the data."
            )
    else:
        selected_department = "No department detected"
        team = pd.DataFrame()
        st.error("No department column detected. Manager access cannot be safely simulated.")
        st.stop()

    with tab1:
        st.header(f"Hello Manager of {selected_department}")

        st.markdown(
            "This dashboard summarizes your team’s value signals, learning visibility, reliability, and continuity risks. "
            "Use it to support coaching conversations and team development decisions."
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Team size",
            f"{len(team):,}",
            help="Number of employees currently visible in this manager workspace."
        )

        col2.metric(
            "Avg value proxy",
            safe_mean(team, "human_capital_value_proxy"),
            help="Average bottom-up value proxy for the team. This is not a financial valuation; it combines available human capital signals."
        )

        col3.metric(
            "Avg learning signal",
            safe_mean(team, "learning_intensity_score"),
            help="Average visible training and development activity across the team."
        )

        col4.metric(
            "Avg data reliability",
            safe_mean(team, "kpi_reliability_score"),
            help="Average confidence in the available data. Lower reliability means signals should be interpreted carefully."
        )

        st.subheader("Team profile snapshot")

        snapshot_col1, snapshot_col2, snapshot_col3 = st.columns(3)

        if "risk_prediction_label" in team.columns:
            high_risk_count = int((team["risk_prediction_label"] == "High").sum())
        else:
            high_risk_count = "N/A"

        if "segment_name" in team.columns:
            main_segment = team["segment_name"].mode().iloc[0] if not team["segment_name"].mode().empty else "N/A"
        else:
            main_segment = "N/A"

        if "low_data_flag" in team.columns:
            low_data_count = int(team["low_data_flag"].sum())
        else:
            low_data_count = "N/A"

        with snapshot_col1:
            soft_card(
                "Main team profile",
                str(main_segment)
            )

        with snapshot_col2:
            soft_card(
                "High continuity-risk profiles",
                str(high_risk_count)
            )

        with snapshot_col3:
            soft_card(
                "Low-data profiles",
                str(low_data_count)
            )

        st.subheader("Team segment distribution")

        if "segment_name" in team.columns:
            seg_counts = (
                team["segment_name"]
                .value_counts()
                .rename_axis("Team profile")
                .reset_index(name="Employees")
            )

            fig = px.bar(
                seg_counts,
                x="Team profile",
                y="Employees",
                title="How the team is distributed across AI-generated profiles",
                labels={"Team profile": "Team profile", "Employees": "Employees"},
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

            st.dataframe(seg_counts, use_container_width=True, hide_index=True)

        note(
            "<b>How to use this view:</b> read team signals as prompts for support and development. "
            "They are not a ranking of employees or a substitute for manager judgment.",
            "governance",
        )

    with tab2:
        st.header("Team Signals")

        st.markdown(
            "This view helps identify where the team may need support: workload balance, learning access, data reliability, or coaching attention."
        )

        signal_col1, signal_col2 = st.columns(2)

        with signal_col1:
            if "risk_prediction_label" in team.columns:
                risk_counts = (
                    team["risk_prediction_label"]
                    .value_counts()
                    .rename_axis("Continuity label")
                    .reset_index(name="Employees")
                )

                fig = px.bar(
                    risk_counts,
                    x="Continuity label",
                    y="Employees",
                    title="Continuity-risk distribution",
                    labels={"Continuity label": "Continuity label", "Employees": "Employees"},
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)

        with signal_col2:
            if "sustainability_balance" in team.columns:
                fig = px.histogram(
                    team,
                    x="sustainability_balance",
                    nbins=25,
                    title="Sustainability balance distribution",
                    labels={"sustainability_balance": "Sustainability balance"},
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Coaching attention list")

        priority = team.copy()

        if "risk_prediction_label" in priority.columns:
            priority = priority[priority["risk_prediction_label"].isin(["High", "Medium"])]

        if "sustainability_balance" in priority.columns:
            priority = priority.sort_values("sustainability_balance", ascending=True)

        coaching_cols = [
            "display_employee",
            "segment_name",
            "risk_prediction_label",
            "learning_intensity_score",
            "absenteeism_risk_score",
            "sustainability_balance",
            "kpi_reliability_score",
            "recommended_action",
        ]
        coaching_cols = [c for c in coaching_cols if c in priority.columns]

        if priority.empty:
            st.success("No high-priority coaching alerts detected for this team.")
        else:
            st.dataframe(priority[coaching_cols].head(15), use_container_width=True, hide_index=True)

        note(
            "<b>Manager responsibility:</b> these signals should trigger conversations, not conclusions. "
            "Before acting, check context, workload, role constraints, and data reliability.",
            "governance",
        )

    with tab3:
        st.header("Team Action Plan")

        st.markdown(
            "This section translates team signals into practical management actions."
        )

        st.subheader("Recommended management actions by team profile")

        action_plan = pd.DataFrame(
            [
                {
                    "Team signal": "Low information / low learning",
                    "What it may mean": "Some employees have limited visible training, review, or contribution data.",
                    "Manager action": "Check whether work, training, or development activity is being captured correctly.",
                },
                {
                    "Team signal": "High performers / low development",
                    "What it may mean": "Strong contribution but limited visible learning investment.",
                    "Manager action": "Protect performance while offering targeted training, mentoring, or mobility options.",
                },
                {
                    "Team signal": "Engaged but at risk",
                    "What it may mean": "Strong activity combined with possible workload or continuity pressure.",
                    "Manager action": "Review workload, recovery balance, and support needs before pressure becomes attrition or absence.",
                },
            ]
        )

        st.dataframe(action_plan, use_container_width=True, hide_index=True)

        st.subheader("Team-level recommendation summary")

        team_recommendations = (
            recommendation_df[
                recommendation_df["display_employee"].isin(team["display_employee"])
            ].copy()
            if "display_employee" in recommendation_df.columns
            else pd.DataFrame()
        )

        if not team_recommendations.empty and "recommendation" in team_recommendations.columns:
            action_summary = (
                team_recommendations["recommendation"]
                .value_counts()
                .rename_axis("Recommended action")
                .reset_index(name="Employees")
            )

            st.dataframe(action_summary, use_container_width=True, hide_index=True)
        elif "recommended_action" in team.columns:
            action_summary = (
                team["recommended_action"]
                .value_counts()
                .rename_axis("Recommended action")
                .reset_index(name="Employees")
            )
            st.dataframe(action_summary, use_container_width=True, hide_index=True)

        st.subheader("Practical coaching loop")

        loop_col1, loop_col2, loop_col3, loop_col4 = st.columns(4)

        with loop_col1:
            soft_card("1. Check reliability", "Confirm whether the data is complete enough to interpret.")

        with loop_col2:
            soft_card("2. Identify pattern", "Look for workload, learning, or development gaps.")

        with loop_col3:
            soft_card("3. Discuss context", "Use the signal as a starting point with employees.")

        with loop_col4:
            soft_card("4. Act and reassess", "Adjust support, training, or workload, then monitor evolution.")

        note(
            "<b>Bottom-up value:</b> managers create value by improving the conditions that allow employees to learn, contribute, and sustain performance over time.",
            "governance",
        )


# --------------------------------------------------
# HR VIEW
# --------------------------------------------------
elif role == "HR":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Action Center",
            "Workforce Explorer",
            "AI Insights",
            "Data & Documents",
            "Usage & Principles",
        ]
    )

    # --------------------------------------------------
    # CREATE HR PRIORITY DATAFRAME ONCE
    # --------------------------------------------------
    hr_priority = employee_value.copy()

    if "sustainability_balance" not in hr_priority.columns:
        if {"learning_intensity_score", "absenteeism_risk_score"}.issubset(hr_priority.columns):
            hr_priority["sustainability_balance"] = (
                hr_priority["learning_intensity_score"] - hr_priority["absenteeism_risk_score"]
            )

    high_continuity_risk = (
        hr_priority["absenteeism_risk_score"] >= hr_priority["absenteeism_risk_score"].quantile(0.75)
        if "absenteeism_risk_score" in hr_priority.columns
        else pd.Series(False, index=hr_priority.index)
    )

    low_reliability = (
        hr_priority["kpi_reliability_score"] < 0.5
        if "kpi_reliability_score" in hr_priority.columns
        else pd.Series(False, index=hr_priority.index)
    )

    negative_sustainability = (
        hr_priority["sustainability_balance"] < 0
        if "sustainability_balance" in hr_priority.columns
        else pd.Series(False, index=hr_priority.index)
    )

    low_learning = (
        hr_priority["learning_intensity_score"] < 0.3
        if "learning_intensity_score" in hr_priority.columns
        else pd.Series(False, index=hr_priority.index)
    )

    hr_priority["priority_reason"] = "Standard monitoring"
    hr_priority.loc[low_reliability, "priority_reason"] = "Low data reliability"
    hr_priority.loc[low_learning, "priority_reason"] = "Low learning investment"
    hr_priority.loc[negative_sustainability, "priority_reason"] = "Negative sustainability balance"
    hr_priority.loc[high_continuity_risk, "priority_reason"] = "High continuity risk"

    hr_priority["priority_level"] = "Low"
    hr_priority.loc[low_learning | low_reliability, "priority_level"] = "Medium"
    hr_priority.loc[high_continuity_risk | negative_sustainability, "priority_level"] = "High"

    hr_priority["priority_score"] = hr_priority["priority_level"].map(
        {"High": 3, "Medium": 2, "Low": 1}
    )

    sort_cols = ["priority_score"]
    ascending_rules = [False]

    if "absenteeism_risk_score" in hr_priority.columns:
        sort_cols.append("absenteeism_risk_score")
        ascending_rules.append(False)

    if "sustainability_balance" in hr_priority.columns:
        sort_cols.append("sustainability_balance")
        ascending_rules.append(True)

    hr_priority = hr_priority.sort_values(by=sort_cols, ascending=ascending_rules)

    # --------------------------------------------------
    # TAB 1 — ACTION CENTER
    # --------------------------------------------------
    with tab1:
        st.header("HR Action Center")
        st.markdown(
            "This page answers the main HR question: **who needs attention, why, and what should be done next?**"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Employees mapped", f"{len(employee_value):,}")
        col2.metric(
            "High-priority profiles",
            f"{int((hr_priority['priority_level'] == 'High').sum()):,}"
        )
        col3.metric("High continuity risk", f"{int(high_continuity_risk.sum()):,}")
        col4.metric("Low reliability", f"{int(low_reliability.sum()):,}")

        st.subheader("Top profiles requiring attention")

        priority_cols = [
            "display_employee",
            department_col,
            "segment_name",
            "priority_level",
            "priority_reason",
            "absenteeism_risk_score",
            "learning_intensity_score",
            "sustainability_balance",
            "performance_score",
            "kpi_reliability_score",
            "recommended_action",
        ]

        priority_cols = [c for c in priority_cols if c and c in hr_priority.columns]

        st.dataframe(
            hr_priority[priority_cols].head(30),
            use_container_width=True,
            hide_index=True
        )

        note(
            "<b>How to use this table:</b> these are not automatic HR decisions. "
            "They are profiles that deserve context checking, manager discussion, or data validation.",
            "governance",
        )

        st.subheader("Why profiles are flagged")

        reason_summary = (
            hr_priority["priority_reason"]
            .value_counts()
            .rename_axis("Priority reason")
            .reset_index(name="Employees")
        )

        fig = px.bar(
            reason_summary,
            x="Priority reason",
            y="Employees",
            title="Priority reason breakdown",
        )
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Recommendation summary")

        if not recommendation_df.empty and "recommendation" in recommendation_df.columns:
            rec_summary = (
                recommendation_df["recommendation"]
                .value_counts()
                .rename_axis("Recommendation")
                .reset_index(name="Profiles")
            )

            fig = px.bar(
                rec_summary.head(10),
                x="Profiles",
                y="Recommendation",
                orientation="h",
                title="Most frequent recommended actions",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(rec_summary, use_container_width=True, hide_index=True)
        else:
            st.warning("No recommendation table available.")

    # --------------------------------------------------
    # TAB 2 — WORKFORCE EXPLORER
    # --------------------------------------------------
    with tab2:
        st.header("Workforce Explorer")
        st.markdown(
            "Use this view to explore workforce patterns by segment, department, reliability, learning, and value proxy."
        )

        filtered = employee_value.copy()

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_segments = st.multiselect(
                "Filter by AI segment",
                sorted(filtered["segment_name"].dropna().unique()),
                default=sorted(filtered["segment_name"].dropna().unique())
            )
            filtered = filtered[filtered["segment_name"].isin(selected_segments)]

        with col2:
            if "low_data_flag" in filtered.columns:
                low_data_choice = st.selectbox(
                    "Data visibility",
                    ["All", "Only low-visibility employees", "Exclude low-visibility employees"]
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
                    default=departments
                )
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
                hover_data=[
                    c for c in [
                        "display_employee",
                        "performance_score",
                        "absenteeism_risk_score",
                        "kpi_reliability_score",
                    ]
                    if c in filtered.columns
                ],
                title="Learning intensity vs human capital value proxy",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "sustainability_balance" in filtered.columns:
            fig = px.histogram(
                filtered,
                x="sustainability_balance",
                nbins=30,
                color="segment_name",
                title="Sustainability balance distribution",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("AI segment summary")

        metrics = [
            "human_capital_value_proxy",
            "reliability_adjusted_value_proxy",
            "performance_score",
            "learning_intensity_score",
            "absenteeism_risk_score",
            "sustainability_balance",
            "data_coverage_score",
            "kpi_reliability_score",
        ]

        available_metrics = [c for c in metrics if c in employee_value.columns]

        if available_metrics:
            summary = employee_value.groupby("segment_name", as_index=False)[available_metrics].mean()
            counts = (
                employee_value.groupby("segment_name", as_index=False)
                .size()
                .rename(columns={"size": "employees"})
            )
            summary = counts.merge(summary, on="segment_name", how="left")
            st.dataframe(summary, use_container_width=True, hide_index=True)

        st.subheader("Filtered employee profiles")

        filtered = filtered.merge(
            hr_priority[
                [
                    c for c in [
                        "display_employee",
                        "priority_level",
                        "priority_reason",
                    ]
                    if c in hr_priority.columns
                ]
            ],
            on="display_employee",
            how="left"
        )

        display_cols = [
            "display_employee",
            department_col,
            "segment_name",
            "priority_level",
            "priority_reason",
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

        st.dataframe(
            filtered[display_cols],
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # TAB 3 — AI INSIGHTS
    # --------------------------------------------------
    with tab3:
        st.header("AI Insights")
        st.markdown(
            """
            This tab combines AI segments, ONEValue signals, and value-creation experiments.
            The goal is not to judge employees, but to identify patterns that CACEIS can learn from.
            """
        )

        if onevalue_ai_df.empty:
            st.warning("ONEValue AI insights not found. Run `python src/onevalue_ai_layer.py` first.")
        else:
            col1, col2, col3 = st.columns(3)

            col1.metric("AI insights", f"{len(onevalue_ai_df):,}")
            col2.metric(
                "AI signal types",
                f"{onevalue_ai_df['ai_signal'].nunique():,}"
                if "ai_signal" in onevalue_ai_df.columns
                else "N/A"
            )
            col3.metric(
                "Decision owners",
                f"{onevalue_ai_df['decision_owner'].nunique():,}"
                if "decision_owner" in onevalue_ai_df.columns
                else "N/A"
            )

            if "ai_signal" in onevalue_ai_df.columns:
                signal_summary = (
                    onevalue_ai_df["ai_signal"]
                    .value_counts()
                    .rename_axis("AI signal")
                    .reset_index(name="Profiles")
                )

                fig = px.bar(
                    signal_summary,
                    x="AI signal",
                    y="Profiles",
                    title="ONEValue AI signal distribution",
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)
                st.dataframe(signal_summary, use_container_width=True, hide_index=True)

            st.subheader("High-priority AI experiments")

            high_priority_signals = [
                "High contribution under pressure",
                "Negative sustainability balance",
                "High performer with low development signal",
            ]

            ai_priority = onevalue_ai_df[
                onevalue_ai_df["ai_signal"].isin(high_priority_signals)
            ].copy()

            if ai_priority.empty:
                st.success("No high-priority AI experiments detected.")
            else:
                ai_priority_cols = [
                    "display_employee",
                    "segment_name",
                    "ai_signal",
                    "ai_interpretation",
                    "recommended_experiment",
                    "learning_question",
                    "decision_owner",
                ]

                ai_priority_cols = [c for c in ai_priority_cols if c in ai_priority.columns]

                st.dataframe(
                    ai_priority[ai_priority_cols].head(30),
                    use_container_width=True,
                    hide_index=True
                )

            st.subheader("All value-creation experiments")

            experiment_cols = [
                "display_employee",
                "segment_name",
                "ai_signal",
                "ai_interpretation",
                "recommended_experiment",
                "learning_question",
                "value_creation_hypothesis",
                "decision_owner",
            ]

            experiment_cols = [c for c in experiment_cols if c in onevalue_ai_df.columns]

            st.dataframe(
                onevalue_ai_df[experiment_cols],
                use_container_width=True,
                hide_index=True
            )

            note(
                "<b>Blue-line logic:</b> the goal is not to manage the indicator directly. "
                "The goal is to test which actions and working conditions improve sustainable value creation.",
                "governance",
            )

    # --------------------------------------------------
    # TAB 4 — DATA & DOCUMENTS
    # --------------------------------------------------
    with tab4:
        st.header("Data & Documents")
        st.markdown(
            "This tab combines KPI audit, data quality checks, and document intelligence."
        )

        st.subheader("Data quality snapshot")

        col1, col2, col3 = st.columns(3)

        col1.metric("Avg data coverage", safe_mean(employee_value, "data_coverage_score"))
        col2.metric("Avg KPI reliability", safe_mean(employee_value, "kpi_reliability_score"))
        col3.metric(
            "Low-data records",
            f"{int(employee_value['low_data_flag'].sum()):,}"
            if "low_data_flag" in employee_value.columns
            else "N/A"
        )

        if "data_coverage_score" in employee_value.columns:
            fig = px.histogram(
                employee_value,
                x="data_coverage_score",
                nbins=20,
                title="Data coverage score distribution",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("KPI audit")

        kpi_section = st.radio(
            "Choose KPI table",
            ["HR & Performance", "Absenteeism / Continuity", "Learning"],
            horizontal=True
        )

        if kpi_section == "HR & Performance":
            st.dataframe(hr_kpi, use_container_width=True)

        elif kpi_section == "Absenteeism / Continuity":
            st.dataframe(absence_kpi, use_container_width=True)

        elif kpi_section == "Learning":
            st.dataframe(training_kpi, use_container_width=True)

        st.divider()

        show_document_intelligence()

    # --------------------------------------------------
    # TAB 5 — USAGE & PRINCIPLES
    # --------------------------------------------------
    with tab5:
        st.header("Usage & Principles")

        st.subheader("What this tool does")
        st.markdown(
            """
            - Identifies workforce patterns using HR, absence, training, and performance data  
            - Highlights profiles that may require attention  
            - Translates signals into recommended actions and learning questions  
            - Supports HR and managers in decision-making  
            """
        )

        st.subheader("What this tool does NOT do")
        st.markdown(
            """
            - It does not evaluate employees automatically  
            - It does not replace HR or managerial judgment  
            - It does not produce final decisions  
            - It does not directly measure value creation; it uses proxy signals  
            """
        )

        st.subheader("How HR should use this dashboard")
        st.markdown(
            """
            1. Start from the **Action Center** to identify priority profiles  
            2. Use the **Workforce Explorer** to understand patterns and context  
            3. Use **AI Insights** to explore recommended actions and experiments  
            4. Check **Data & Documents** to validate reliability before acting  
            """
        )

        st.subheader("Key principles")

        st.markdown(
            """
            - Use anonymized / pseudonymized data  
            - Do not use outputs for automatic sanctions  
            - Always check data reliability before interpreting results  
            - Treat AI outputs as signals, not truths  
            - Keep humans in the loop for all decisions  
            """
        )

        note(
            "<b>Important:</b> This system is a decision-support tool. "
            "It helps identify where attention may be needed, but final decisions always require human judgment.",
            "governance",
        )


# --------------------------------------------------
# PRODUCT OWNER / ADMIN VIEW
# --------------------------------------------------
elif role == "Product Owner":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "System Health",
            "Data Quality",
            "AI Monitoring",
            "Governance & Roadmap",
            "Document Pipeline",
        ]
    )

    # --------------------------------------------------
    # TAB 1 — SYSTEM HEALTH
    # --------------------------------------------------
    with tab1:
        st.header("System Health")
        st.markdown(
            "Product Owner view for monitoring pipeline readiness, generated outputs, and deployment completeness."
        )

        output_checks = pd.DataFrame(
            [
                {
                    "Output": "hr_kpi_table.csv",
                    "Purpose": "HR and performance KPI source",
                    "Rows": len(hr_kpi),
                    "Status": "Loaded" if not hr_kpi.empty else "Missing/empty",
                },
                {
                    "Output": "absence_kpi_table.csv",
                    "Purpose": "Absenteeism / continuity KPI source",
                    "Rows": len(absence_kpi),
                    "Status": "Loaded" if not absence_kpi.empty else "Missing/empty",
                },
                {
                    "Output": "training_kpi_table.csv",
                    "Purpose": "Learning intensity KPI source",
                    "Rows": len(training_kpi),
                    "Status": "Loaded" if not training_kpi.empty else "Missing/empty",
                },
                {
                    "Output": "employee_value_table_v2.csv",
                    "Purpose": "Integrated employee-level value table",
                    "Rows": len(employee_value),
                    "Status": "Loaded" if not employee_value.empty else "Missing/empty",
                },
                {
                    "Output": "recommendation_table.csv",
                    "Purpose": "Recommended actions and human questions",
                    "Rows": len(recommendation_df),
                    "Status": "Loaded" if not recommendation_df.empty else "Missing/empty",
                },
                {
                    "Output": "onevalue_ai_insights.csv",
                    "Purpose": "AI-generated signals, experiments, and learning questions",
                    "Rows": len(onevalue_ai_df),
                    "Status": "Loaded" if not onevalue_ai_df.empty else "Missing/empty",
                },
                {
                    "Output": "document_theme_summary.csv",
                    "Purpose": "Unstructured document theme extraction",
                    "Rows": len(doc_theme),
                    "Status": "Loaded" if not doc_theme.empty else "Missing/empty",
                },
                {
                    "Output": "document_inventory.csv",
                    "Purpose": "Document inventory and source tracking",
                    "Rows": len(doc_inventory),
                    "Status": "Loaded" if not doc_inventory.empty else "Missing/empty",
                },
            ]
        )

        loaded_count = int((output_checks["Status"] == "Loaded").sum())
        total_count = len(output_checks)

        col1, col2, col3 = st.columns(3)

        col1.metric("Pipeline outputs loaded", f"{loaded_count}/{total_count}")
        col2.metric("Employees mapped", f"{len(employee_value):,}")
        col3.metric(
            "Deployment readiness",
            "Ready" if loaded_count == total_count else "Incomplete"
        )

        st.subheader("Output readiness checklist")
        st.dataframe(output_checks, use_container_width=True, hide_index=True)

        if loaded_count < total_count:
            st.warning(
                "Some expected outputs are missing or empty. Re-run the pipeline scripts before using the dashboard for a final demo."
            )
        else:
            st.success("All expected outputs are loaded.")

        st.subheader("Recommended run order")

        run_order = pd.DataFrame(
            [
                {
                    "Step": 1,
                    "Command": "python src/integrated_value_ai.py",
                    "Expected output": "employee_value_table_v2.csv, department_value_summary_v2.csv, ai_segment_summary_v2.csv",
                },
                {
                    "Step": 2,
                    "Command": "python src/risk_prediction.py",
                    "Expected output": "risk_prediction_table.csv",
                },
                {
                    "Step": 3,
                    "Command": "python src/recommendation_engine.py",
                    "Expected output": "recommendation_table.csv",
                },
                {
                    "Step": 4,
                    "Command": "python src/onevalue_ai_layer.py",
                    "Expected output": "onevalue_ai_insights.csv",
                },
                {
                    "Step": 5,
                    "Command": "python src/document_theme_extraction.py",
                    "Expected output": "document_theme_summary.csv, document_inventory.csv",
                },
                {
                    "Step": 6,
                    "Command": 'python -m streamlit run "dashboard/final version/streamlit_app_v3.py"',
                    "Expected output": "Launch dashboard",
                },
            ]
        )

        st.dataframe(run_order, use_container_width=True, hide_index=True)

    # --------------------------------------------------
    # TAB 2 — DATA QUALITY
    # --------------------------------------------------
    with tab2:
        st.header("Data Quality")
        st.markdown(
            "This view checks whether the data is complete and reliable enough to support interpretation."
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Avg data coverage", safe_mean(employee_value, "data_coverage_score"))
        col2.metric("Avg KPI reliability", safe_mean(employee_value, "kpi_reliability_score"))
        col3.metric(
            "Low-data records",
            f"{int(employee_value['low_data_flag'].sum()):,}"
            if "low_data_flag" in employee_value.columns
            else "N/A"
        )
        col4.metric(
            "Training records visible",
            f"{int(employee_value['has_training_record'].sum()):,}"
            if "has_training_record" in employee_value.columns
            else "N/A"
        )

        st.subheader("Coverage by data source")

        coverage_rows = []

        for col, label in [
            ("has_performance_record", "Performance"),
            ("has_absence_record", "Absence"),
            ("has_training_record", "Training"),
        ]:
            if col in employee_value.columns:
                coverage_rows.append(
                    {
                        "Data source": label,
                        "Records available": int(employee_value[col].sum()),
                        "Coverage share": round(employee_value[col].mean(), 3),
                    }
                )

        if coverage_rows:
            coverage_df = pd.DataFrame(coverage_rows)
            st.dataframe(coverage_df, use_container_width=True, hide_index=True)

            fig = px.bar(
                coverage_df,
                x="Data source",
                y="Coverage share",
                title="Data coverage by source",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Low-reliability records")

        dq_cols = [
            "display_employee",
            department_col,
            "data_coverage_score",
            "kpi_reliability_score",
            "low_data_flag",
            "has_performance_record",
            "has_absence_record",
            "has_training_record",
        ]

        dq_cols = [c for c in dq_cols if c and c in employee_value.columns]

        if "kpi_reliability_score" in employee_value.columns:
            low_reliability_df = employee_value.sort_values(
                "kpi_reliability_score",
                ascending=True
            )
            st.dataframe(
                low_reliability_df[dq_cols].head(100),
                use_container_width=True,
                hide_index=True
            )

        if "data_coverage_score" in employee_value.columns:
            fig = px.histogram(
                employee_value,
                x="data_coverage_score",
                nbins=20,
                title="Data coverage score distribution",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        note(
            "<b>Product implication:</b> low data reliability should block strong interpretation. "
            "The platform should surface reliability before recommending action.",
            "governance",
        )

    # --------------------------------------------------
    # TAB 3 — AI MONITORING
    # --------------------------------------------------
    with tab3:
        st.header("AI Monitoring")
        st.markdown(
            "Monitor AI outputs for balance, interpretability, usefulness, and responsible deployment readiness."
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "AI segments",
            f"{employee_value['segment_name'].nunique():,}"
            if "segment_name" in employee_value.columns
            else "N/A"
        )

        col2.metric(
            "AI insight rows",
            f"{len(onevalue_ai_df):,}"
            if not onevalue_ai_df.empty
            else "0"
        )

        col3.metric(
            "Recommendation rows",
            f"{len(recommendation_df):,}"
            if not recommendation_df.empty
            else "0"
        )

        if "segment_name" in employee_value.columns:
            st.subheader("AI segment distribution")

            seg_counts = (
                employee_value["segment_name"]
                .value_counts()
                .rename_axis("AI segment")
                .reset_index(name="Employees")
            )

            st.dataframe(seg_counts, use_container_width=True, hide_index=True)

            fig = px.bar(
                seg_counts,
                x="AI segment",
                y="Employees",
                title="AI segment distribution",
            )

            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if not onevalue_ai_df.empty and "ai_signal" in onevalue_ai_df.columns:
            st.subheader("ONEValue AI signal distribution")

            signal_counts = (
                onevalue_ai_df["ai_signal"]
                .value_counts()
                .rename_axis("AI signal")
                .reset_index(name="Profiles")
            )

            st.dataframe(signal_counts, use_container_width=True, hide_index=True)

            fig = px.bar(
                signal_counts,
                x="AI signal",
                y="Profiles",
                title="ONEValue AI signal distribution",
            )

            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if not recommendation_df.empty and "priority_level" in recommendation_df.columns:
            st.subheader("Recommendation priority distribution")

            priority_counts = (
                recommendation_df["priority_level"]
                .value_counts()
                .rename_axis("Priority level")
                .reset_index(name="Profiles")
            )

            st.dataframe(priority_counts, use_container_width=True, hide_index=True)

            fig = px.bar(
                priority_counts,
                x="Priority level",
                y="Profiles",
                title="Recommendation priority distribution",
            )

            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Model maturity assessment")

        maturity = pd.DataFrame(
            [
                {
                    "AI component": "KMeans segmentation",
                    "Current status": "Implemented",
                    "Method": "Unsupervised learning",
                    "Limitation": "Finds patterns but does not predict future outcomes",
                    "Next improvement": "Validate segments with HR experts and longitudinal outcomes",
                },
                {
                    "AI component": "Continuity-risk label",
                    "Current status": "Implemented as rule-based label",
                    "Method": "Quantile-based scoring",
                    "Limitation": "Not a trained supervised model",
                    "Next improvement": "Train model if future long-absence or attrition labels become available",
                },
                {
                    "AI component": "Recommendation engine",
                    "Current status": "Implemented",
                    "Method": "Business rules + signal interpretation",
                    "Limitation": "Recommendations are not yet validated against outcomes",
                    "Next improvement": "Track accepted actions and outcome changes",
                },
                {
                    "AI component": "ONEValue AI experiments",
                    "Current status": "Implemented",
                    "Method": "Signal-to-hypothesis logic",
                    "Limitation": "No live manager/employee feedback loop yet",
                    "Next improvement": "Add decision logging and experiment tracking",
                },
                {
                    "AI component": "Document intelligence",
                    "Current status": "Implemented as keyword extraction",
                    "Method": "Theme detection",
                    "Limitation": "Counts terms, but does not yet summarize meaning deeply",
                    "Next improvement": "Use NLP summarization and link themes to departments",
                },
            ]
        )

        st.dataframe(maturity, use_container_width=True, hide_index=True)

        note(
            "<b>Admin guardrail:</b> current AI outputs are pattern-detection and decision-support tools. "
            "They should not be presented as fully validated predictive models.",
            "governance",
        )

    # --------------------------------------------------
    # TAB 4 — GOVERNANCE & ROADMAP
    # --------------------------------------------------
    with tab4:
        st.header("Governance & Roadmap")
        st.markdown(
            "This tab explains how the platform should evolve from prototype to responsible production system."
        )

        st.subheader("What this system does today")

        st.markdown(
            """
            - Uses structured HR, performance, absence, and training data.  
            - Creates KPI signals, not final judgments.  
            - Builds a reliability-adjusted human capital value proxy.  
            - Uses AI segmentation to identify broad workforce patterns.  
            - Uses ONEValue AI to translate signals into experiments and learning questions.  
            """
        )

        st.subheader("What this system does not do yet")

        st.markdown(
            """
            - It does not take live input from employees or managers yet.  
            - It does not train a supervised prediction model yet because no true future outcome label is available.  
            - It does not automatically rank, sanction, or evaluate employees.  
            - It does not directly measure value creation; it estimates proxy signals.  
            """
        )

        st.subheader("How new data would be integrated")

        st.markdown(
            """
            1. New data source is added, for example collaboration, workload, operational quality, engagement, or mobility data.  
            2. The source is cleaned and standardized.  
            3. Employee or team identifiers are mapped safely.  
            4. Data quality and coverage are scored.  
            5. New features are engineered.  
            6. The features either enrich the current KPI layer or feed the AI layer.  
            7. If historical outcomes become available, CACEIS can train supervised models.  
            """
        )

        st.subheader("Future supervised AI layer")

        st.markdown(
            """
            If CACEIS provides historical outcomes, the system could train models for:

            - long absence risk  
            - attrition risk  
            - performance drop risk  
            - learning-to-performance impact  
            - internal mobility success  
            - operational error reduction  
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
            - Use experiments to learn which actions create sustainable value.  
            """
        )

        st.subheader("Implementation roadmap")

        roadmap = pd.DataFrame(
            [
                {
                    "Phase": "1. Prototype",
                    "Focus": "Structured KPIs, value proxy, AI segmentation",
                    "Owner": "Student/Data team",
                },
                {
                    "Phase": "2. Evolved prototype",
                    "Focus": "Document intelligence, recommendations, role-based views, ONEValue AI experiments",
                    "Owner": "HR + Data/AI",
                },
                {
                    "Phase": "3. Pilot",
                    "Focus": "Department-level testing, manager feedback loops, bias checks",
                    "Owner": "HR + managers",
                },
                {
                    "Phase": "4. Scale",
                    "Focus": "Snowflake integration, governance workflows, supervised model monitoring",
                    "Owner": "Product Owner + HR",
                },
            ]
        )

        st.dataframe(roadmap, use_container_width=True, hide_index=True)

        st.subheader("Target architecture")

        architecture = pd.DataFrame(
            [
                {
                    "Layer": "Data ingestion",
                    "Role": "Collect HR, absence, training, documents, and future operational data",
                    "Future owner": "Data / IT",
                },
                {
                    "Layer": "Data quality",
                    "Role": "Validate missingness, coverage, identifiers, and reliability",
                    "Future owner": "Data / HR governance",
                },
                {
                    "Layer": "KPI engineering",
                    "Role": "Transform raw data into interpretable signals",
                    "Future owner": "Data / HR analytics",
                },
                {
                    "Layer": "AI layer",
                    "Role": "Detect segments, generate hypotheses, and support future predictions",
                    "Future owner": "Data Science / AI",
                },
                {
                    "Layer": "Decision layer",
                    "Role": "Log manager actions, employee feedback, experiments, and outcomes",
                    "Future owner": "HR / Managers",
                },
                {
                    "Layer": "Governance layer",
                    "Role": "Ensure privacy, fairness, auditability, and human-in-the-loop use",
                    "Future owner": "HR / Legal / Compliance",
                },
            ]
        )

        st.dataframe(architecture, use_container_width=True, hide_index=True)

    # --------------------------------------------------
    # TAB 5 — DOCUMENT PIPELINE
    # --------------------------------------------------
    with tab5:
        st.header("Document Pipeline")
        st.markdown(
            "Monitor unstructured document processing and theme extraction."
        )

        show_document_intelligence()