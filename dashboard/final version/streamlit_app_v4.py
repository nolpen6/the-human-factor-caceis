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

# --------------------------------------------------
# BLUE-LINE VALUATION COMPATIBILITY
# --------------------------------------------------
def normalize_dashboard_series(series: pd.Series) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce")
    if series.notna().sum() == 0:
        return pd.Series(0.5, index=series.index)
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(0.5, index=series.index)
    return ((series - min_val) / (max_val - min_val)).fillna(0.5)

if "contribution_signal" not in employee_value.columns:
    employee_value["contribution_signal"] = normalize_dashboard_series(employee_value.get("performance_score", pd.Series(0.5, index=employee_value.index)))
if "learning_future_value_signal" not in employee_value.columns:
    employee_value["learning_future_value_signal"] = normalize_dashboard_series(employee_value.get("learning_intensity_score", pd.Series(0.5, index=employee_value.index)))
if "sustainability_signal" not in employee_value.columns:
    employee_value["sustainability_signal"] = 1 - normalize_dashboard_series(employee_value.get("absenteeism_risk_score", pd.Series(0.5, index=employee_value.index)))
if "progression_signal" not in employee_value.columns:
    employee_value["progression_signal"] = normalize_dashboard_series(employee_value.get("talent_progression_proxy", pd.Series(0.5, index=employee_value.index)))
if "interpretation_confidence" not in employee_value.columns:
    employee_value["interpretation_confidence"] = normalize_dashboard_series(employee_value.get("kpi_reliability_score", pd.Series(0.5, index=employee_value.index)))
if "sustainable_value_potential" not in employee_value.columns:
    employee_value["sustainable_value_potential"] = (
        0.35 * employee_value["contribution_signal"]
        + 0.30 * employee_value["learning_future_value_signal"]
        + 0.20 * employee_value["sustainability_signal"]
        + 0.15 * employee_value["progression_signal"]
    )
if "reliability_adjusted_value_potential" not in employee_value.columns:
    employee_value["reliability_adjusted_value_potential"] = employee_value["sustainable_value_potential"] * employee_value["interpretation_confidence"]
if "interpretation_risk" not in employee_value.columns:
    employee_value["interpretation_risk"] = employee_value["sustainable_value_potential"] * (1 - employee_value["interpretation_confidence"])
if "valuation_archetype" not in employee_value.columns:
    def dashboard_archetype(row):
        if row.get("interpretation_confidence", 0.5) < 0.4:
            return "Under-Observed Profile"
        if row.get("contribution_signal", 0.5) >= 0.65 and row.get("sustainability_signal", 0.5) < 0.45:
            return "Value Under Pressure"
        if row.get("contribution_signal", 0.5) >= 0.65 and row.get("learning_future_value_signal", 0.5) < 0.4:
            return "Strong Contributor / Low Development"
        if row.get("learning_future_value_signal", 0.5) >= 0.65 and row.get("contribution_signal", 0.5) < 0.55:
            return "Future Value Builder"
        if row.get("sustainable_value_potential", 0.5) >= 0.65 and row.get("sustainability_signal", 0.5) >= 0.55 and row.get("learning_future_value_signal", 0.5) >= 0.55:
            return "Sustainable Value Builder"
        if row.get("learning_future_value_signal", 0.5) < 0.4 and row.get("contribution_signal", 0.5) < 0.55:
            return "Low Learning Visibility"
        return "Stable / Monitor"
    employee_value["valuation_archetype"] = employee_value.apply(dashboard_archetype, axis=1)
if "blue_line_question" not in employee_value.columns:
    employee_value["blue_line_question"] = employee_value["valuation_archetype"].map({
        "Under-Observed Profile": "Do we have enough reliable data to interpret this profile safely?",
        "Value Under Pressure": "Is current contribution being created in a sustainable way?",
        "Strong Contributor / Low Development": "Are strong contributors receiving enough future-oriented development?",
        "Future Value Builder": "How can learning investment be converted into measurable contribution?",
        "Sustainable Value Builder": "What conditions are enabling sustainable value creation here?",
        "Low Learning Visibility": "Is low learning due to limited access, limited need, low motivation, or missing data?",
        "Stable / Monitor": "What should be monitored to sustain contribution and development over time?",
    }).fillna("What context should be validated before acting on this signal?")

# Backward-compatible names for old charts.
employee_value["human_capital_value_proxy"] = employee_value.get("human_capital_value_proxy", employee_value["sustainable_value_potential"])
employee_value["reliability_adjusted_value_proxy"] = employee_value.get("reliability_adjusted_value_proxy", employee_value["reliability_adjusted_value_potential"])

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
    for col, default in {
        "recommended_experiment": "Maintain regular check-ins and monitor signal evolution.",
        "expected_signal_change": "Stable or improved signals over the next review cycle.",
        "review_period": "1 quarter",
        "decision_owner": "Employee / Manager",
        "governance_guardrail": "Use indicators as learning prompts, not rankings.",
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



# --------------------------------------------------
# V4 HUMAN INPUT LOGS
# --------------------------------------------------
def get_outputs_dir() -> Path:
    """Return the same outputs folder used by the pipeline."""
    return Path(__file__).resolve().parents[2] / "outputs"


def classify_context_theme(text: str) -> str:
    """Very simple prototype theme classifier for employee/manager comments."""
    text = str(text).lower()
    if any(word in text for word in ["workload", "busy", "pressure", "stress", "overload", "capacity"]):
        return "Workload / sustainability"
    if any(word in text for word in ["training", "learn", "skill", "course", "upskill", "development"]):
        return "Learning / development"
    if any(word in text for word in ["client", "report", "deadline", "quality", "error", "risk", "control"]):
        return "Operational value / risk prevention"
    if any(word in text for word in ["team", "help", "collabor", "manager", "colleague"]):
        return "Collaboration / team support"
    if any(word in text for word in ["data", "missing", "wrong", "incorrect", "record"]):
        return "Data quality correction"
    return "General context"


def append_log_row(file_name: str, row: dict):
    """Append a row to a CSV file in outputs. Creates the file if needed."""
    outputs_dir = get_outputs_dir()
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / file_name
    new_row = pd.DataFrame([row])

    if path.exists() and path.stat().st_size > 0:
        existing = pd.read_csv(path)
        updated = pd.concat([existing, new_row], ignore_index=True)
    else:
        updated = new_row

    updated.to_csv(path, index=False)
    st.cache_data.clear()


def load_log(file_name: str) -> pd.DataFrame:
    """Load one of the V4 human input logs if it exists."""
    path = get_outputs_dir() / file_name
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path)
    return pd.DataFrame()


def show_context_summary(employee_log: pd.DataFrame, manager_log: pd.DataFrame):
    """Show how human input becomes structured context for the value tool."""
    st.subheader("How this input feeds the value tool")
    note(
        "<b>Important:</b> comments are not used to score or punish employees. "
        "They are converted into themes that help managers and HR interpret KPI signals with human context.",
        "governance",
    )

    combined = []
    if not employee_log.empty:
        temp = employee_log.copy()
        temp["source"] = "Employee input"
        combined.append(temp)
    if not manager_log.empty:
        temp = manager_log.copy()
        temp["source"] = "Manager note"
        combined.append(temp)

    if not combined:
        st.info("No human input has been saved yet in this demo session.")
        return

    context_df = pd.concat(combined, ignore_index=True)
    if "theme" in context_df.columns:
        theme_summary = (
            context_df.groupby(["source", "theme"], as_index=False)
            .size()
            .rename(columns={"size": "entries"})
            .sort_values("entries", ascending=False)
        )
        st.dataframe(theme_summary, use_container_width=True, hide_index=True)




# --------------------------------------------------
# CACEIS VALUE LENS HELPERS
# --------------------------------------------------
def derive_value_lens(row: pd.Series) -> str:
    archetype = str(row.get("valuation_archetype", ""))
    absence = row.get("absenteeism_risk_score", 0)
    learning = row.get("learning_future_value_signal", row.get("learning_intensity_score", 0))
    reliability = row.get("interpretation_confidence", row.get("kpi_reliability_score", 0))
    contribution = row.get("contribution_signal", row.get("performance_score", 0))

    if pd.notna(reliability) and reliability < 0.4:
        return "Data reliability / auditability"
    if "Pressure" in archetype or (pd.notna(absence) and absence >= 0.7):
        return "Operational continuity and workload sustainability"
    if pd.notna(learning) and learning < 0.35:
        return "Future capability and reskilling"
    if pd.notna(contribution) and contribution >= 0.65:
        return "Current contribution and knowledge retention"
    return "Standard workforce monitoring"

def usefulness_answer(role: str) -> pd.DataFrame:
    rows = {
        "Employee": [
            ("What does the data say about me?", "Shows my own contribution, learning, sustainability, and data visibility signals."),
            ("What should I discuss with my manager?", "Turns signals into questions for development, workload, and invisible contribution."),
            ("Can I correct missing context?", "Lets me add context, decisions, expected outcomes, and data-correction notes."),
        ],
        "Manager": [
            ("Who may need support first?", "Highlights profiles with pressure, low learning visibility, or low data confidence."),
            ("What should I do next?", "Suggests experiments such as workload review, targeted training, or data validation."),
            ("Am I improving team conditions?", "Tracks sustainability, learning, reliability, and archetype distribution over time."),
        ],
        "HR": [
            ("Where are workforce risks concentrated?", "Aggregates continuity, learning, sustainability, and data quality signals by entity."),
            ("Can we trust the model output?", "Separates value potential from interpretation confidence and flags weak evidence."),
            ("What policy action is needed?", "Identifies whether the issue is capability, workload, data quality, or governance."),
        ],
        "Product Owner": [
            ("Is the product ready to deploy?", "Checks output readiness, model maturity, missing data, and governance controls."),
            ("Is the valuation model responsible?", "Monitors proxy logic, interpretation risk, archetype balance, and limitations."),
            ("What should be built next?", "Maps gaps to future data sources, validation, and production roadmap."),
        ],
    }
    return pd.DataFrame(rows.get(role, []), columns=["Question", "Dashboard answer"])

def show_caceis_value_lens(df: pd.DataFrame, title: str = "CACEIS value lens"):
    st.subheader(title)
    if df.empty:
        st.info("No data available for this value lens.")
        return
    work = df.copy()
    if "caceis_value_lens" not in work.columns:
        work["caceis_value_lens"] = work.apply(derive_value_lens, axis=1)
    lens_summary = (
        work["caceis_value_lens"]
        .value_counts()
        .rename_axis("CACEIS question")
        .reset_index(name="Profiles")
    )
    st.dataframe(lens_summary, use_container_width=True, hide_index=True)
    fig = px.bar(lens_summary, x="CACEIS question", y="Profiles", title="What business question does each signal support?")
    st.plotly_chart(clean_chart(fig), use_container_width=True)


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
        show_caceis_value_lens(employee_value, "CACEIS workforce value lens")

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
# EMPLOYEE-FACING EXPLANATION HELPERS
# --------------------------------------------------
def score_band(value):
    """Plain-language banding for 0-1 prototype signals."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "Not available"
    if value >= 0.70:
        return "High"
    if value >= 0.40:
        return "Medium"
    return "Low"


def info_expander(title: str, body: str):
    """Small clickable info block for score cards. Streamlit metric help tooltips are easy to miss."""
    with st.expander(f"ℹ️ {title}", expanded=False):
        st.markdown(body)


def signal_text(emp: pd.Series, primary_col: str, fallback_col: str | None = None) -> str:
    """Return a score with plain-language band for employee-facing display."""
    value = emp.get(primary_col, None)
    if pd.isna(value) and fallback_col:
        value = emp.get(fallback_col, None)
    return f"{safe_value(pd.Series({primary_col: value}), primary_col)} · {score_band(value)}"


def employee_signal_explanation(emp: pd.Series) -> pd.DataFrame:
    """Visible explanation table for employee-facing signals."""
    learning = emp.get("learning_future_value_signal", emp.get("learning_intensity_score", None))
    contribution = emp.get("contribution_signal", emp.get("performance_score", None))
    sustainability = emp.get("sustainability_signal", None)
    reliability = emp.get("interpretation_confidence", emp.get("kpi_reliability_score", None))
    absence = emp.get("absenteeism_risk_score", None)

    return pd.DataFrame([
        {
            "Signal": "Development signal",
            "Your score": safe_value(emp, "learning_future_value_signal") if "learning_future_value_signal" in emp.index else safe_value(emp, "learning_intensity_score"),
            "Level": score_band(learning),
            "What it means": "How much visible training/development activity appears in the data. Low does not mean low talent; it may mean training is missing, informal, or not yet recorded.",
            "Good next question": "What skill or learning opportunity should I prioritize next?",
        },
        {
            "Signal": "Contribution signal",
            "Your score": safe_value(emp, "contribution_signal") if "contribution_signal" in emp.index else safe_value(emp, "performance_score"),
            "Level": score_band(contribution),
            "What it means": "A proxy based mainly on available review/performance information. It should be discussed with concrete examples because reviews can be incomplete or biased.",
            "Good next question": "Which parts of my work create the most value for my team?",
        },
        {
            "Signal": "Sustainability signal",
            "Your score": safe_value(emp, "sustainability_signal"),
            "Level": score_band(sustainability),
            "What it means": "A continuity signal derived from absence/PTO-risk patterns. Higher usually means lower observed continuity pressure. It is not a wellbeing diagnosis.",
            "Good next question": "Is my current workload sustainable?",
        },
        {
            "Signal": "Absence / continuity risk",
            "Your score": safe_value(emp, "absenteeism_risk_score"),
            "Level": score_band(absence),
            "What it means": "Higher means more observed absence/continuity pressure in the data. This needs human context before any interpretation.",
            "Good next question": "Is there context missing behind my absence/PTO pattern?",
        },
        {
            "Signal": "Data visibility",
            "Your score": safe_value(emp, "interpretation_confidence") if "interpretation_confidence" in emp.index else safe_value(emp, "kpi_reliability_score"),
            "Level": score_band(reliability),
            "What it means": "How complete the available data is. Low visibility means the dashboard should not be trusted strongly yet.",
            "Good next question": "Are my review, training, or HR records complete?",
        },
    ])


def employee_plain_language_summary(emp: pd.Series) -> dict:
    """Create a practical employee-facing summary from selected employee data."""
    learning = emp.get("learning_future_value_signal", emp.get("learning_intensity_score", None))
    contribution = emp.get("contribution_signal", emp.get("performance_score", None))
    sustainability = emp.get("sustainability_signal", None)
    reliability = emp.get("interpretation_confidence", emp.get("kpi_reliability_score", None))
    absence = emp.get("absenteeism_risk_score", None)

    learning_band = score_band(learning)
    contribution_band = score_band(contribution)
    sustainability_band = score_band(sustainability)
    reliability_band = score_band(reliability)
    absence_band = score_band(absence)

    if reliability_band == "Low":
        situation = "The dashboard does not have enough reliable data to say much yet."
        worry = "Do not over-interpret these results. The main issue is data completeness, not your performance."
        next_step = "Check whether your training, review, absence/PTO, or HR records are missing or outdated."
    elif absence_band == "High" or sustainability_band == "Low":
        situation = "Your data suggests possible workload, recovery, or continuity pressure."
        worry = "This is not a judgment, but it is worth discussing context before pressure turns into a bigger issue."
        next_step = "Prepare a conversation about workload, recovery, priorities, or support needs."
    elif learning_band == "Low" and contribution_band in ["Medium", "High"]:
        situation = "You appear to have visible contribution, but low recorded development activity."
        worry = "This is not a problem by itself. It means your next useful conversation is about future growth."
        next_step = "Identify one training, mentoring, mobility, or upskilling opportunity to discuss with your manager."
    elif contribution_band == "Low" and learning_band in ["Medium", "High"]:
        situation = "You have visible learning activity, but it may not yet appear as contribution in the available data."
        worry = "No immediate conclusion should be drawn. The key is to connect learning to concrete work outcomes."
        next_step = "Ask how your recent learning can be applied to a project, process, or client deliverable."
    else:
        situation = "Your signals look broadly stable based on the available data."
        worry = "No major red flag appears from the current dashboard view."
        next_step = "Use your next check-in to confirm priorities, development goals, and any missing context."

    return {
        "situation": situation,
        "worry": worry,
        "next_step": next_step,
        "manager_questions": [
            "What skill should I build before my next review?",
            "Which part of my work creates the most value for the team?",
            "Is any important work or informal learning missing from the data?",
            "Is my workload sustainable for the next review cycle?",
        ],
    }



def employee_manager_questions(emp: pd.Series) -> pd.DataFrame:
    """Generate manager questions from this employee's actual signals instead of hard-coding them."""
    learning = emp.get("learning_future_value_signal", emp.get("learning_intensity_score", None))
    contribution = emp.get("contribution_signal", emp.get("performance_score", None))
    sustainability = emp.get("sustainability_signal", None)
    reliability = emp.get("interpretation_confidence", emp.get("kpi_reliability_score", None))
    absence = emp.get("absenteeism_risk_score", None)
    balance = emp.get("sustainability_balance", None)
    archetype = str(emp.get("valuation_archetype", emp.get("segment_name", "")))

    rows = []

    def add(priority, theme, question, why):
        rows.append({
            "Priority": priority,
            "Theme": theme,
            "Question to ask": question,
            "Why this question appears": why,
        })

    if pd.notna(reliability) and reliability < 0.5:
        add(
            "High",
            "Data quality",
            "Are my review, training, absence/PTO, or HR records complete and up to date?",
            "Your data visibility is low, so the dashboard should not be strongly interpreted yet.",
        )

    if pd.notna(learning) and learning < 0.3:
        add(
            "High",
            "Development",
            "Which skill, training, mentoring, or mobility opportunity should I prioritize next?",
            "Your visible learning/development signal is low compared with the available scale.",
        )
        add(
            "Medium",
            "Missing context",
            "Is any informal learning, project-based learning, or on-the-job development missing from the data?",
            "Low learning can mean missing records, not low effort or low potential.",
        )

    if pd.notna(contribution) and contribution < 0.4:
        add(
            "High",
            "Contribution clarity",
            "What concrete outcomes or responsibilities should I focus on to increase my visible contribution?",
            "Your contribution signal is currently low or unclear in the available data.",
        )
    elif pd.notna(contribution) and contribution >= 0.65:
        add(
            "Medium",
            "Contribution leverage",
            "Which parts of my work create the most value for the team, and how can I protect or grow them?",
            "Your contribution signal is relatively strong, so the useful question is how to sustain and develop it.",
        )

    if (pd.notna(absence) and absence >= 0.6) or (pd.notna(sustainability) and sustainability < 0.45) or (pd.notna(balance) and balance < 0):
        add(
            "High",
            "Workload / sustainability",
            "Is my current workload, recovery rhythm, or prioritization sustainable for the next review cycle?",
            "Your sustainability or absence/continuity signal suggests this deserves context and discussion.",
        )

    if "Under-Observed" in archetype or "Low Visibility" in archetype:
        add(
            "High",
            "Visibility",
            "What important work, training, or contribution is not visible in the current dashboard?",
            "Your profile appears under-observed, so improving visibility is the first useful step.",
        )

    if "Future Value Builder" in archetype:
        add(
            "Medium",
            "Applying learning",
            "How can I apply my learning to a concrete project, process improvement, or client deliverable?",
            "Your learning signal is stronger than your current contribution signal, so conversion into applied impact is the key topic.",
        )

    if not rows:
        add(
            "Medium",
            "Next growth step",
            "What should be my main development or contribution priority before the next review?",
            "No strong alert appears, so the best use is regular development planning.",
        )
        add(
            "Low",
            "Context check",
            "Is there anything important about my work that the dashboard does not capture?",
            "Even stable signals can miss informal work, collaboration, or context.",
        )

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    return pd.DataFrame(rows).drop_duplicates("Question to ask").sort_values(
        by="Priority",
        key=lambda s: s.map(priority_order).fillna(9),
    )

def show_employee_score_dictionary():
    st.subheader("Score dictionary")
    st.markdown("These explanations are always visible because hover tooltips are easy to miss.")
    st.dataframe(
        pd.DataFrame([
            {"Score": "Development signal", "Meaning": "Visible training and learning activity.", "Important caution": "Low can mean missing or informal learning, not low ability."},
            {"Score": "Contribution signal", "Meaning": "Available review/performance-related signal.", "Important caution": "Reviews can be incomplete or biased; use examples and manager context."},
            {"Score": "Sustainability signal", "Meaning": "Continuity signal based on absence/PTO-risk patterns. Higher is generally better.", "Important caution": "This is not a health, burnout, or wellbeing diagnosis."},
            {"Score": "Learning vs pressure balance", "Meaning": "Learning intensity minus absenteeism risk.", "Important caution": "Positive = learning signal is stronger than risk. Negative = risk is stronger than visible learning."},
            {"Score": "Data visibility", "Meaning": "How complete the available records are.", "Important caution": "Low visibility means do not make strong conclusions."},
        ]),
        use_container_width=True,
        hide_index=True,
    )



def show_manager_score_dictionary():
    st.subheader("Manager score dictionary")
    st.markdown("These explanations are visible because hover tooltips are easy to miss during a demo.")
    st.dataframe(
        pd.DataFrame([
            {
                "Score / box": "Team size",
                "What it tells a manager": "How many employees are visible in this manager workspace.",
                "How to use it": "Use it as context only; small teams can make averages unstable.",
            },
            {
                "Score / box": "Avg sustainable value potential",
                "What it tells a manager": "A combined team signal from contribution, learning, sustainability, and progression.",
                "How to use it": "Use it to identify team-level patterns, not to rank employees.",
            },
            {
                "Score / box": "Avg future value signal",
                "What it tells a manager": "Average visible learning and development activity across the team.",
                "How to use it": "Low values should trigger questions about training access, informal learning, and development planning.",
            },
            {
                "Score / box": "Avg interpretation confidence",
                "What it tells a manager": "How complete/reliable the available team data is.",
                "How to use it": "If this is low, validate data before acting on the signals.",
            },
            {
                "Score / box": "High continuity-risk profiles",
                "What it tells a manager": "Number of team members with elevated absence/continuity risk labels.",
                "How to use it": "Start workload, staffing, recovery, or context conversations. Do not treat it as blame.",
            },
            {
                "Score / box": "Learning vs pressure balance",
                "What it tells a manager": "Learning intensity minus absenteeism risk.",
                "How to use it": "Negative values suggest pressure/risk is stronger than visible development activity.",
            },
        ]),
        use_container_width=True,
        hide_index=True,
    )


def manager_team_plain_language_summary(team_df: pd.DataFrame) -> dict:
    """Generate a practical manager-facing team summary from team-level signals."""
    if team_df.empty:
        return {
            "situation": "No team data is available.",
            "risk": "No interpretation is possible.",
            "next_step": "Check the manager-to-department mapping and available data files.",
        }

    avg_learning = pd.to_numeric(team_df.get("learning_future_value_signal", team_df.get("learning_intensity_score", pd.Series(dtype=float))), errors="coerce").mean()
    avg_contribution = pd.to_numeric(team_df.get("contribution_signal", team_df.get("performance_score", pd.Series(dtype=float))), errors="coerce").mean()
    avg_sustainability = pd.to_numeric(team_df.get("sustainability_signal", pd.Series(dtype=float)), errors="coerce").mean()
    avg_confidence = pd.to_numeric(team_df.get("interpretation_confidence", team_df.get("kpi_reliability_score", pd.Series(dtype=float))), errors="coerce").mean()
    high_risk_share = (team_df.get("risk_prediction_label", pd.Series(dtype=str)).astype(str).eq("High")).mean() if "risk_prediction_label" in team_df.columns else 0
    low_data_share = pd.to_numeric(team_df.get("low_data_flag", pd.Series(False, index=team_df.index)), errors="coerce").fillna(0).astype(bool).mean() if "low_data_flag" in team_df.columns else 0

    if pd.notna(avg_confidence) and avg_confidence < 0.5:
        situation = "Your first management issue is data quality, not performance. The team signals are not reliable enough for strong interpretation."
        risk = "Risk of misreading the team because some records are missing or incomplete."
        next_step = "Validate HR, training, review, and absence records before drawing conclusions."
    elif high_risk_share >= 0.25 or (pd.notna(avg_sustainability) and avg_sustainability < 0.45):
        situation = "The team may be delivering under pressure. The main management topic is sustainability and continuity."
        risk = "If ignored, this can become absence, disengagement, operational disruption, or loss of knowledge."
        next_step = "Review workload distribution, deadlines, recovery capacity, and whether support is needed."
    elif pd.notna(avg_learning) and avg_learning < 0.35 and pd.notna(avg_contribution) and avg_contribution >= 0.5:
        situation = "The team appears to contribute, but visible learning/development activity is low."
        risk = "Current delivery may be okay, but future capability could weaken if skills are not refreshed."
        next_step = "Identify one training, mentoring, or upskilling priority for the team."
    elif pd.notna(avg_learning) and avg_learning >= 0.6 and pd.notna(avg_contribution) and avg_contribution < 0.5:
        situation = "The team shows learning activity, but it may not yet be converting into visible contribution."
        risk = "Training investment may not translate into operational value unless applied to real work."
        next_step = "Connect learning to concrete projects, process improvements, or client deliverables."
    elif low_data_share >= 0.25:
        situation = "A significant part of the team is under-observed in the available data."
        risk = "Important work, informal learning, or context may be invisible."
        next_step = "Use manager notes and employee context inputs to fill the interpretation gap."
    else:
        situation = "The team signals look broadly stable based on the available data."
        risk = "No single major alert dominates the dashboard."
        next_step = "Use the dashboard to prepare regular check-ins and monitor changes over time."

    return {"situation": situation, "risk": risk, "next_step": next_step}


def manager_dynamic_questions(team_df: pd.DataFrame) -> pd.DataFrame:
    """Generate manager questions based on the actual team signals instead of hard-coding generic bullets."""
    rows = []

    def add(priority, theme, question, why):
        rows.append({
            "Priority": priority,
            "Theme": theme,
            "Manager question": question,
            "Why this appears": why,
        })

    if team_df.empty:
        add("High", "Data availability", "Why is no team data mapped to this manager?", "The manager workspace has no employee rows.")
        return pd.DataFrame(rows)

    avg_learning = pd.to_numeric(team_df.get("learning_future_value_signal", team_df.get("learning_intensity_score", pd.Series(dtype=float))), errors="coerce").mean()
    avg_contribution = pd.to_numeric(team_df.get("contribution_signal", team_df.get("performance_score", pd.Series(dtype=float))), errors="coerce").mean()
    avg_sustainability = pd.to_numeric(team_df.get("sustainability_signal", pd.Series(dtype=float)), errors="coerce").mean()
    avg_confidence = pd.to_numeric(team_df.get("interpretation_confidence", team_df.get("kpi_reliability_score", pd.Series(dtype=float))), errors="coerce").mean()
    avg_balance = pd.to_numeric(team_df.get("sustainability_balance", pd.Series(dtype=float)), errors="coerce").mean()
    high_risk_count = int(team_df.get("risk_prediction_label", pd.Series(dtype=str)).astype(str).eq("High").sum()) if "risk_prediction_label" in team_df.columns else 0
    low_data_count = int(pd.to_numeric(team_df.get("low_data_flag", pd.Series(False, index=team_df.index)), errors="coerce").fillna(0).astype(bool).sum()) if "low_data_flag" in team_df.columns else 0

    if pd.notna(avg_confidence) and avg_confidence < 0.5:
        add("High", "Data reliability", "Which team records are missing or unreliable before I act on these signals?", "Average interpretation confidence is low.")
    if low_data_count > 0:
        add("High", "Visibility", "Which employees or activities are under-observed in the current data?", f"{low_data_count} team profile(s) have low-data flags.")
    if high_risk_count > 0:
        add("High", "Continuity / workload", "Which workload, deadline, staffing, or recovery factors could explain the high-risk profiles?", f"{high_risk_count} team profile(s) show high continuity-risk labels.")
    if pd.notna(avg_sustainability) and avg_sustainability < 0.45:
        add("High", "Sustainability", "Is the team creating value in a way that can be sustained next quarter?", "Average sustainability signal is low.")
    if pd.notna(avg_balance) and avg_balance < 0:
        add("High", "Learning vs pressure", "Is pressure stronger than development investment for this team?", "Average learning-vs-pressure balance is negative.")
    if pd.notna(avg_learning) and avg_learning < 0.35:
        add("Medium", "Development", "Does the team have enough access to training, mentoring, or stretch assignments?", "Average future value/development signal is low.")
    if pd.notna(avg_contribution) and avg_contribution < 0.45:
        add("Medium", "Contribution clarity", "Are team priorities and expected outcomes clear enough?", "Average contribution signal is low or unclear.")
    if pd.notna(avg_learning) and avg_learning >= 0.6 and pd.notna(avg_contribution) and avg_contribution < 0.5:
        add("Medium", "Learning conversion", "How can recent learning be converted into concrete process or client-delivery improvements?", "Learning signal is stronger than contribution signal.")

    if "valuation_archetype" in team_df.columns:
        archetypes = set(team_df["valuation_archetype"].dropna().astype(str))
        if any("Value Under Pressure" in a for a in archetypes):
            add("High", "Value under pressure", "Who may be contributing strongly but under unsustainable pressure?", "At least one team member is classified as Value Under Pressure.")
        if any("Strong Contributor / Low Development" in a for a in archetypes):
            add("Medium", "Future capability", "Which strong contributors need targeted development to protect future value?", "At least one team member has strong contribution but low development signal.")
        if any("Under-Observed" in a for a in archetypes):
            add("High", "Data/context", "What context should I add before HR interprets these profiles?", "At least one profile is under-observed.")

    if not rows:
        add("Medium", "Regular management", "What is the team’s main development or delivery priority before the next review?", "No major alert dominates, so use the tool for proactive check-ins.")
        add("Low", "Context", "What important team work is not captured by the current structured data?", "Dashboards can miss informal work, collaboration, and client support.")

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    return pd.DataFrame(rows).drop_duplicates("Manager question").sort_values(
        by="Priority",
        key=lambda s: s.map(priority_order).fillna(9),
    )


def manager_employee_coaching_questions(emp: pd.Series) -> pd.DataFrame:
    """Generate coaching questions for one selected employee in the manager drill-down."""
    # Reuse the employee question generator but adjust labels to manager language.
    q = employee_manager_questions(emp).copy()
    if q.empty:
        return q
    q = q.rename(columns={"Question to ask": "Coaching question", "Why this question appears": "Why this appears"})
    q["Coaching question"] = q["Coaching question"].str.replace("Are my", "Are this employee's", regex=False)
    q["Coaching question"] = q["Coaching question"].str.replace("What skill should I", "What skill should this employee", regex=False)
    q["Coaching question"] = q["Coaching question"].str.replace("Which part of my work", "Which part of this employee's work", regex=False)
    q["Coaching question"] = q["Coaching question"].str.replace("Is my", "Is this employee's", regex=False)
    q["Coaching question"] = q["Coaching question"].str.replace("How can I", "How can this employee", regex=False)
    q["Coaching question"] = q["Coaching question"].str.replace("What concrete outcomes or responsibilities should I", "What concrete outcomes or responsibilities should this employee", regex=False)
    return q


# --------------------------------------------------
# EMPLOYEE VIEW
# --------------------------------------------------
if role == "Employee":
    tab1, tab2, tab3, tab4 = st.tabs(["My Situation", "My Next Steps", "Add Context", "Help & FAQ"])

    selected_employee = user["id"]
    employee_match = employee_value[employee_value["display_employee"] == selected_employee]

    if employee_match.empty:
        emp = None
        st.warning(f"No profile found for {selected_employee}. Check the demo user mapping.")
    else:
        emp = employee_match.iloc[0]

    with tab1:
        st.header("My Situation")
        st.markdown("This page translates your own signals into plain-language guidance. Scores are not judgments; they are prompts for a conversation.")

        if emp is None:
            st.warning("No employee profile found in the integrated table.")
        else:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("My development signal", safe_value(emp, "learning_future_value_signal"))
                info_expander(
                    "What is this?",
                    "Visible training and development activity found in the data. A low score can mean formal training is low, informal learning is not recorded, or the data is incomplete. It is not a measure of talent."
                )

            with col2:
                st.metric("My contribution signal", safe_value(emp, "contribution_signal"))
                info_expander(
                    "What is this?",
                    "A proxy based mainly on available annual review/performance information. It should be discussed with concrete examples because reviews can be subjective, incomplete, or biased."
                )

            with col3:
                st.metric("My sustainability signal", safe_value(emp, "sustainability_signal"))
                info_expander(
                    "What is this?",
                    "A continuity signal based on absence/PTO-risk patterns. Higher usually means lower observed continuity pressure. It is not a health, burnout, or wellbeing diagnosis."
                )

            with col4:
                st.metric("My data visibility", safe_value(emp, "interpretation_confidence"))
                info_expander(
                    "What is this?",
                    "How complete and reliable the available records are. If this is low, the dashboard should not be used to make strong conclusions about you."
                )

            summary = employee_plain_language_summary(emp)

            st.subheader("What this means")
            soft_card("Current situation", summary["situation"])
            soft_card("Should I worry?", summary["worry"])
            soft_card("Recommended next step", summary["next_step"])

            with st.expander("See exactly what each score means", expanded=True):
                st.dataframe(employee_signal_explanation(emp), use_container_width=True, hide_index=True)

            st.subheader("My profile summary")

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:
                soft_card(
                    "My team / entity",
                    str(safe_value(emp, department_col)) if department_col else "Not available"
                )
                info_expander("Why show this?", "Your team/entity gives context. Scores should be compared and discussed within role and team context, not in isolation.")

            with summary_col2:
                soft_card(
                    "My current situation",
                    str(safe_value(emp, "valuation_archetype"))
                )
                info_expander("What does this label mean?", "This is a plain grouping used to guide conversation. It is not a ranking, grade, or HR decision.")

            with summary_col3:
                soft_card(
                    "Question to discuss",
                    str(safe_value(emp, "blue_line_question"))
                )
                info_expander("Why this question?", "The question points to the next human conversation: what context is missing, what should be developed, or what support may be useful.")

            value_col1, value_col2, value_col3 = st.columns(3)

            with value_col1:
                soft_card(
                    "Overall signal",
                    str(safe_value(emp, "sustainable_value_potential"))
                )
                info_expander("What is this?", "A combined prototype signal from contribution, learning, sustainability, and progression. It is kept visible for transparency, but it should not be read as your personal value.")

            with value_col2:
                soft_card(
                    "Confidence-adjusted signal",
                    str(safe_value(emp, "reliability_adjusted_value_potential"))
                )
                info_expander("What is this?", "The overall signal reduced when data visibility is incomplete. If the data is weaker, the interpretation should be weaker too.")

            with value_col3:
                soft_card(
                    "Learning vs pressure balance",
                    str(safe_value(emp, "sustainability_balance"))
                )
                info_expander("What is this?", "Formula: learning intensity score minus absenteeism risk score. Positive means visible learning is stronger than continuity pressure. Negative means continuity pressure is stronger than visible learning. It is not a diagnosis.")

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
        st.header("My Next Steps")

        if emp is not None:
            st.markdown(
                "This page combines your employee-specific scores with general coaching guidance. The scores update by employee; the action plan is a reusable checklist."
            )
            with st.expander("Which parts are employee-specific?", expanded=True):
                st.markdown(
                    """
                    **Employee-specific:** the numeric scores, current situation, recommended next step, data visibility, and any saved context.  
                    **General guidance:** the checklist and example questions are reusable prompts for a review conversation.
                    """
                )

            dev_col1, dev_col2, dev_col3 = st.columns(3)

            with dev_col1:
                soft_card(
                    "Current development signal",
                    f"Learning score: {safe_value(emp, 'learning_intensity_score')}"
                )
                info_expander("What should I do with this?", "Use this to check whether your formal learning and training activity is visible. If it is low but you learned informally, add context or discuss it in your review.")

            with dev_col2:
                soft_card(
                    "Review preparation",
                    f"Annual review signal: {safe_value(emp, 'performance_score')}"
                )
                info_expander("What should I do with this?", "Use this as a prompt to prepare examples of your work. It should not replace the actual review conversation.")

            with dev_col3:
                soft_card(
                    "Sustainability check",
                    f"Learning vs pressure balance: {safe_value(emp, 'sustainability_balance')}"
                )
                info_expander("What should I do with this?", "Use this to discuss whether your current workload and recovery rhythm are sustainable. A negative score means this deserves context, not blame.")

            note(
                "<b>What is the sustainability balance?</b> In this prototype it equals <b>learning intensity score minus absenteeism risk score</b>. "
                "A negative value means observed absence/continuity pressure is higher than visible learning activity. "
                "It is not a health diagnosis and should always be discussed with context.",
                "governance",
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
            st.markdown(
                "These questions are generated from this employee profile's actual signals, not hard-coded. "
                "Use them to prepare a focused review conversation."
            )
            manager_questions_df = employee_manager_questions(emp)
            st.dataframe(manager_questions_df, use_container_width=True, hide_index=True)
            with st.expander("ℹ️ How are these questions generated?", expanded=False):
                st.markdown(
                    """
                    The dashboard checks this employee's data visibility, learning/development signal, contribution signal, 
                    absence/continuity risk, sustainability signal, sustainability balance, and valuation archetype. 
                    It then selects the most relevant questions for the manager conversation.
                    """
                )

            note(
                "<b>Your development drives value:</b> value is not only performance—it comes from learning, contribution, and sustainability over time. "
                "Use this view to shape your next step.",
                "governance",
            )


    with tab3:
        st.header("Add Context to My Profile")
        st.markdown(
            "Use this page when the dashboard is missing something important: informal learning, invisible work, workload pressure, a data issue, or a question for your manager/HR. "
            "This context helps explain signals; it is not used as a score."
        )

        if emp is None:
            st.warning("No employee profile found, so inputs cannot be linked safely.")
        else:
            with st.form("employee_context_form"):
                input_type = st.selectbox(
                    "What type of input is this?",
                    [
                        "Question for manager/HR",
                        "Workload or capacity context",
                        "Decision or action I took",
                        "Learning or development need",
                        "Process improvement idea",
                        "Data correction",
                        "Recognition / invisible contribution",
                    ],
                )
                employee_comment = st.text_area(
                    "What do you want to add?",
                    placeholder="Example: I supported an urgent client reporting task while two colleagues were absent.",
                )
                decision_taken = st.text_area(
                    "Optional: what decision/action did you take?",
                    placeholder="Example: I prioritized client reporting before internal admin tasks.",
                )
                expected_outcome = st.text_area(
                    "Optional: what did you expect would happen?",
                    placeholder="Example: The report would be delivered on time with fewer client escalations.",
                )
                actual_outcome = st.text_area(
                    "Optional: what actually happened?",
                    placeholder="Example: The report was delivered on time, but my workload increased.",
                )
                submitted = st.form_submit_button("Save my input")

            if submitted:
                full_text = " ".join([employee_comment, decision_taken, expected_outcome, actual_outcome])
                if not full_text.strip():
                    st.warning("Please write at least one comment before saving.")
                else:
                    append_log_row(
                        "employee_context_log.csv",
                        {
                            "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "display_employee": selected_employee,
                            "department": safe_value(emp, department_col) if department_col else "Not available",
                            "input_type": input_type,
                            "employee_comment": employee_comment,
                            "decision_taken": decision_taken,
                            "expected_outcome": expected_outcome,
                            "actual_outcome": actual_outcome,
                            "theme": classify_context_theme(full_text),
                            "status": "Submitted",
                        },
                    )
                    st.success("Input saved. In V4, this becomes contextual evidence for learning and support.")

            employee_log = load_log("employee_context_log.csv")
            my_log = employee_log[employee_log["display_employee"] == selected_employee] if not employee_log.empty and "display_employee" in employee_log.columns else pd.DataFrame()

            st.subheader("My saved inputs")
            if my_log.empty:
                st.info("No saved inputs yet for this employee.")
            else:
                st.dataframe(my_log.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

            show_context_summary(my_log, pd.DataFrame())



    with tab4:
        st.header("Help & FAQ")
        st.markdown("A short guide for using the employee dashboard without over-reading the numbers.")

        faq_items = [
            (
                "What is the point of this tool for me?",
                "It helps you prepare better conversations: what development to ask for, whether your data is complete, what context is missing, and whether workload or recovery should be discussed."
            ),
            (
                "Are these scores my evaluation?",
                "No. They are prototype signals from available HR, training, review, and absence/PTO data. They should start a conversation, not replace one."
            ),
            (
                "What should I look at first?",
                "Start with the plain-language boxes under 'What this means'. Then check data visibility. Only then look at individual scores."
            ),
            (
                "What does a low development signal mean?",
                "It means little formal learning is visible in the available data. It could also mean informal learning is missing from records, so you should add context or ask about training options."
            ),
            (
                "What does sustainability mean here?",
                "It is a continuity/workload proxy, not a health diagnosis. The balance shown in the dashboard is learning intensity minus absence/continuity risk."
            ),
            (
                "When should I use Add Context?",
                "Use it when the dashboard misses something important: invisible work, informal training, workload pressure, data errors, or a question for HR/manager."
            ),
        ]

        for question, answer in faq_items:
            with st.expander(f"ℹ️ {question}", expanded=False):
                st.markdown(answer)

        st.subheader("Score dictionary")
        show_employee_score_dictionary()

        note(
            "<b>Best use:</b> treat this as a preparation tool for a check-in: what is accurate, what is missing, and what should I develop next?",
            "governance",
        )

# --------------------------------------------------
# MANAGER VIEW
# --------------------------------------------------
elif role == "Manager":
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Team Dashboard",
        "Employee Drill-Down",
        "Team Signals",
        "Manager Notes",
        "Action Plan",
        "Help & FAQ",
    ])

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
        st.subheader("What this helps me answer")
        st.dataframe(usefulness_answer("Manager"), use_container_width=True, hide_index=True)

        st.markdown(
            "This dashboard summarizes your team’s value signals, learning visibility, reliability, and continuity risks. "
            "Use it to support coaching conversations and team development decisions."
        )

        team_summary = manager_team_plain_language_summary(team)
        st.subheader("Manager interpretation")
        s1, s2, s3 = st.columns(3)
        with s1:
            soft_card("What the dashboard sees", team_summary["situation"])
            with st.expander("ℹ️ Why this appears", expanded=False):
                st.markdown("This is generated from team averages for learning, contribution, sustainability, interpretation confidence, high-risk labels, and low-data flags.")
        with s2:
            soft_card("Main management risk", team_summary["risk"])
            with st.expander("ℹ️ How to use this", expanded=False):
                st.markdown("Use this as a prompt for context checks. It is not an automatic diagnosis of team performance or wellbeing.")
        with s3:
            soft_card("Recommended next step", team_summary["next_step"])
            with st.expander("ℹ️ What to do next", expanded=False):
                st.markdown("Turn the signal into a concrete conversation or experiment: validate data, review workload, identify training access, or add missing context.")

        st.subheader("Team-level questions to investigate")
        st.dataframe(manager_dynamic_questions(team), use_container_width=True, hide_index=True)
        with st.expander("ℹ️ How these questions are generated", expanded=False):
            st.markdown(
                "The questions are generated from the team’s actual signals: data reliability, learning/development signal, contribution signal, sustainability signal, high-risk labels, low-data flags, and valuation archetypes."
            )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Team size",
            f"{len(team):,}",
            help="Number of employees currently visible in this manager workspace."
        )

        col2.metric(
            "Avg sustainable value potential",
            safe_mean(team, "sustainable_value_potential"),
            help="Average bottom-up value proxy for the team. This is not a financial valuation; it combines available human capital signals."
        )

        col3.metric(
            "Avg future value signal",
            safe_mean(team, "learning_future_value_signal"),
            help="Average visible training and development activity across the team."
        )

        col4.metric(
            "Avg interpretation confidence",
            safe_mean(team, "interpretation_confidence"),
            help="Average confidence in the available data. Lower reliability means signals should be interpreted carefully."
        )

        with st.expander("ℹ️ What do these team scores mean?", expanded=False):
            show_manager_score_dictionary()

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

        with st.expander("ℹ️ How to read the team snapshot", expanded=False):
            st.markdown(
                "**Main team profile** shows the most common AI segment in your team. "
                "**High continuity-risk profiles** indicates how many employees may need workload, recovery, or context review. "
                "**Low-data profiles** indicates where the dashboard may be missing important records or context."
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

        st.subheader("Team Blue-Line valuation archetypes")
        if "valuation_archetype" in team.columns:
            team_archetypes = (
                team["valuation_archetype"]
                .value_counts()
                .rename_axis("Valuation archetype")
                .reset_index(name="Employees")
            )
            fig = px.bar(
                team_archetypes,
                x="Valuation archetype",
                y="Employees",
                title="Team Blue-Line valuation archetypes",
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(team_archetypes, use_container_width=True, hide_index=True)

        show_caceis_value_lens(team, "Team CACEIS value lens")

        note(
            "<b>How to use this view:</b> read team signals as prompts for support and development. "
            "They are not a ranking of employees or a substitute for manager judgment.",
            "governance",
        )


    with tab2:
        st.header("Employee Drill-Down")
        st.markdown(
            "Select one employee to see a more granular profile. This keeps the team overview, but also allows coaching at individual level."
        )

        if team.empty:
            st.warning("No team data available.")
        else:
            selected_team_employee = st.selectbox(
                "Select an employee",
                sorted(team["display_employee"].dropna().unique()),
            )
            employee_detail = team[team["display_employee"] == selected_team_employee].iloc[0]

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Contribution signal", safe_value(employee_detail, "contribution_signal") if "contribution_signal" in employee_detail.index else safe_value(employee_detail, "performance_score"))
            c2.metric("Development signal", safe_value(employee_detail, "learning_future_value_signal") if "learning_future_value_signal" in employee_detail.index else safe_value(employee_detail, "learning_intensity_score"))
            c3.metric("Absence / continuity risk", safe_value(employee_detail, "absenteeism_risk_score"))
            c4.metric("Data confidence", safe_value(employee_detail, "interpretation_confidence") if "interpretation_confidence" in employee_detail.index else safe_value(employee_detail, "kpi_reliability_score"))

            with st.expander("ℹ️ What do these employee drill-down scores mean?", expanded=False):
                st.dataframe(
                    pd.DataFrame([
                        {"Score": "Contribution signal", "Meaning": "Available review/performance-related signal.", "Manager use": "Ask for examples and context before interpreting."},
                        {"Score": "Development signal", "Meaning": "Visible learning and training activity.", "Manager use": "Check training access, informal learning, and development plan."},
                        {"Score": "Absence / continuity risk", "Meaning": "Absence/PTO-related continuity proxy.", "Manager use": "Discuss workload and context; do not treat it as blame."},
                        {"Score": "Data confidence", "Meaning": "Completeness/reliability of available records.", "Manager use": "Low confidence means validate records before acting."},
                    ]),
                    use_container_width=True,
                    hide_index=True,
                )

            st.subheader("Profile interpretation")
            p1, p2, p3 = st.columns(3)
            with p1:
                soft_card("Current situation", str(safe_value(employee_detail, "valuation_archetype")) if "valuation_archetype" in employee_detail.index else str(safe_value(employee_detail, "segment_name")))
                with st.expander("ℹ️ What this means", expanded=False):
                    st.markdown("This is an interpretation category, not a ranking. It helps decide what kind of conversation or support may be useful.")
            with p2:
                soft_card("Continuity label", str(safe_value(employee_detail, "risk_prediction_label")))
                with st.expander("ℹ️ What this means", expanded=False):
                    st.markdown("This label is based on absence/continuity patterns. It should trigger context review, not conclusions.")
            with p3:
                soft_card("Recommended manager experiment", str(safe_value(employee_detail, "recommended_action")))
                with st.expander("ℹ️ What this means", expanded=False):
                    st.markdown("Treat this as a small management experiment or coaching prompt. Validate context with the employee first.")

            st.subheader("Coaching questions generated from this employee's data")
            st.dataframe(manager_employee_coaching_questions(employee_detail), use_container_width=True, hide_index=True)
            with st.expander("ℹ️ How these coaching questions are generated", expanded=False):
                st.markdown(
                    "Questions are generated from this employee's visible development, contribution, absence/continuity risk, sustainability, data confidence, and valuation archetype."
                )

            employee_log = load_log("employee_context_log.csv")
            manager_log = load_log("manager_context_log.csv")
            employee_inputs = employee_log[employee_log["display_employee"] == selected_team_employee] if not employee_log.empty and "display_employee" in employee_log.columns else pd.DataFrame()
            manager_notes = manager_log[manager_log["display_employee"] == selected_team_employee] if not manager_log.empty and "display_employee" in manager_log.columns else pd.DataFrame()

            st.subheader("Employee context inputs")
            if employee_inputs.empty:
                st.info("No employee context inputs saved for this employee yet.")
            else:
                st.dataframe(employee_inputs.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

            st.subheader("Manager notes for this employee")
            if manager_notes.empty:
                st.info("No manager notes saved for this employee yet.")
            else:
                st.dataframe(manager_notes.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

            note(
                "<b>How to read this:</b> the drill-down combines quantitative signals with human context. "
                "It should support a coaching conversation, not produce an automatic judgment.",
                "governance",
            )

    with tab4:
        st.header("Manager Notes")
        st.markdown(
            "Managers can add structured context when the data alone is incomplete. These notes become qualitative evidence for HR and the value tool."
        )

        if team.empty:
            st.warning("No team data available.")
        else:
            with st.form("manager_note_form"):
                note_employee = st.selectbox(
                    "Employee concerned",
                    sorted(team["display_employee"].dropna().unique()),
                    key="manager_note_employee",
                )
                note_type = st.selectbox(
                    "Type of note",
                    [
                        "Coaching",
                        "Workload / capacity",
                        "Training need",
                        "Data correction",
                        "Recognition / invisible work",
                        "Risk or context",
                        "Follow-up with HR",
                    ],
                )
                manager_note = st.text_area(
                    "Manager comment",
                    placeholder="Example: This employee absorbed extra reporting work during a peak period; absence signal should be interpreted with context.",
                )
                follow_up_needed = st.selectbox("Follow-up needed?", ["No", "Yes"])
                submitted_note = st.form_submit_button("Save manager note")

            if submitted_note:
                if not manager_note.strip():
                    st.warning("Please write a note before saving.")
                else:
                    append_log_row(
                        "manager_context_log.csv",
                        {
                            "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "manager_department": selected_department,
                            "display_employee": note_employee,
                            "note_type": note_type,
                            "manager_note": manager_note,
                            "theme": classify_context_theme(manager_note),
                            "follow_up_needed": follow_up_needed,
                            "status": "Submitted",
                        },
                    )
                    st.success("Manager note saved. It can now be reviewed as context, not as a score.")

            manager_log = load_log("manager_context_log.csv")
            team_notes = manager_log[manager_log["display_employee"].isin(team["display_employee"])] if not manager_log.empty and "display_employee" in manager_log.columns else pd.DataFrame()
            st.subheader("Saved notes for my team")
            if team_notes.empty:
                st.info("No manager notes saved for this team yet.")
            else:
                st.dataframe(team_notes.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

            employee_log = load_log("employee_context_log.csv")
            team_employee_inputs = employee_log[employee_log["display_employee"].isin(team["display_employee"])] if not employee_log.empty and "display_employee" in employee_log.columns else pd.DataFrame()
            show_context_summary(team_employee_inputs, team_notes)

    with tab3:
        st.header("Team Signals")

        st.markdown(
            "This view helps identify where the team may need support: workload balance, learning access, data reliability, or coaching attention."
        )

        with st.expander("ℹ️ How to use Team Signals", expanded=False):
            st.markdown(
                "Start with the distributions, then inspect the coaching list. "
                "A high-risk or negative balance signal should lead to a conversation about workload, deadlines, support, or missing context — not automatic judgment."
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
                    labels={"sustainability_balance": "Learning vs pressure balance"},
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

    with tab5:
        st.header("Team Action Plan")

        st.markdown(
            "This section translates team signals into practical management actions."
        )

        with st.expander("ℹ️ How this action plan is generated", expanded=False):
            st.markdown(
                "The first table is generated from your team’s actual signals. The second table summarizes recommendation outputs when available. "
                "Actions should be treated as experiments: try a support action, observe whether signals improve, and add context."
            )

        st.subheader("Dynamic management questions and experiments")
        dynamic_manager_questions = manager_dynamic_questions(team)
        action_plan = dynamic_manager_questions.rename(
            columns={
                "Manager question": "Management question / experiment",
                "Why this appears": "Signal behind it",
            }
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

    with tab6:
        st.header("Manager Help & FAQ")
        st.markdown("Use this tab when presenting the manager view or when a manager asks what to do with the signals.")

        manager_faq_items = [
            (
                "What is the manager supposed to understand first?",
                "Start with the plain-language Manager interpretation on the Team Dashboard. It tells you whether the main topic is data quality, workload sustainability, development, learning conversion, or regular monitoring."
            ),
            (
                "Are employees being ranked?",
                "No. The manager view should not be used as a ranking tool. It shows coaching and context signals to help managers support the team."
            ),
            (
                "What should I do with a high continuity-risk profile?",
                "Treat it as a prompt to ask about workload, recovery, staffing, deadlines, role constraints, or missing context. Do not treat it as employee fault."
            ),
            (
                "What should I do with a low development signal?",
                "Check whether the employee had access to training, mentoring, mobility, or project-based learning. Also check whether informal learning is missing from records."
            ),
            (
                "What does interpretation confidence mean?",
                "It tells you whether the available records are complete enough to interpret. Low confidence means validate the data before making decisions."
            ),
            (
                "How should manager notes be used?",
                "Use notes to add context that structured data misses: invisible work, peak workload, data errors, training needs, support needs, or recognition."
            ),
            (
                "What is the real added value for a manager?",
                "It helps turn scattered HR signals into concrete coaching questions and small management experiments: validate data, rebalance work, improve training access, and monitor whether conditions improve."
            ),
        ]

        for question, answer in manager_faq_items:
            with st.expander(f"ℹ️ {question}", expanded=False):
                st.markdown(answer)

        show_manager_score_dictionary()

        st.subheader("Manager workflow")
        st.dataframe(
            pd.DataFrame([
                {"Step": "1. Read the interpretation", "Manager action": "Identify whether the main issue is data quality, workload, development, or monitoring."},
                {"Step": "2. Check confidence", "Manager action": "If data confidence is low, validate records before interpreting."},
                {"Step": "3. Review team questions", "Manager action": "Use generated questions to prepare team or individual check-ins."},
                {"Step": "4. Add context", "Manager action": "Use Manager Notes when structured data misses important information."},
                {"Step": "5. Run a small experiment", "Manager action": "Try a workload, training, mentoring, or data-quality action and monitor changes."},
            ]),
            use_container_width=True,
            hide_index=True,
        )

        note(
            "<b>Manager principle:</b> the dashboard should help managers improve the work system around people — not mechanically evaluate people.",
            "governance",
        )


# --------------------------------------------------
# HR VIEW
# --------------------------------------------------
elif role == "HR":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Action Center",
            "Blue-Line Valuation",
            "Workforce Explorer",
            "Employee / Team Drill-Down",
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
        st.subheader("What this helps HR answer")
        st.dataframe(usefulness_answer("HR"), use_container_width=True, hide_index=True)

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
        st.header("Blue-Line Valuation")
        st.markdown(
            """
            This view estimates **sustainable value potential** from observable signals.
            It does not measure employee worth. KPIs are treated as indicators of value drivers, not as value itself.
            """
        )
        note(
            "<b>Blue-Line principle:</b> indicators are not the objective. They are learning signals that help CACEIS understand which conditions may create, sustain, or destroy long-term value.",
            "governance",
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg contribution signal", safe_mean(employee_value, "contribution_signal"))
        col2.metric("Avg future value signal", safe_mean(employee_value, "learning_future_value_signal"))
        col3.metric("Avg sustainability signal", safe_mean(employee_value, "sustainability_signal"))
        col4.metric("Avg interpretation confidence", safe_mean(employee_value, "interpretation_confidence"))

        st.subheader("Valuation archetype distribution")
        archetype_counts = (
            employee_value["valuation_archetype"]
            .value_counts()
            .rename_axis("Valuation archetype")
            .reset_index(name="Employees")
        )
        fig = px.bar(archetype_counts, x="Valuation archetype", y="Employees", title="Distribution of Blue-Line valuation archetypes")
        st.plotly_chart(clean_chart(fig), use_container_width=True)
        st.dataframe(archetype_counts, use_container_width=True, hide_index=True)

        st.subheader("Value potential vs interpretation confidence")
        fig = px.scatter(
            employee_value,
            x="sustainable_value_potential",
            y="interpretation_confidence",
            color="valuation_archetype",
            hover_data=[c for c in ["display_employee", department_col, "blue_line_question", "interpretation_risk"] if c and c in employee_value.columns],
            title="Sustainable value potential must be interpreted with data confidence",
        )
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Valuation explanation table")
        explanation_cols = [
            "display_employee", department_col, "valuation_archetype", "blue_line_question",
            "contribution_signal", "learning_future_value_signal", "sustainability_signal",
            "progression_signal", "sustainable_value_potential", "interpretation_confidence",
            "reliability_adjusted_value_potential", "interpretation_risk",
        ]
        explanation_cols = [c for c in explanation_cols if c and c in employee_value.columns]
        st.dataframe(employee_value[explanation_cols], use_container_width=True, hide_index=True)
        note(
            "<b>Interpretation rule:</b> a high value potential with low confidence is not a strong conclusion. It is a prompt to improve data quality or validate context.",
            "warning",
        )

    with tab3:
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
    # TAB 3 — EMPLOYEE / TEAM DRILL-DOWN
    # --------------------------------------------------
    with tab4:
        st.header("Employee / Team Drill-Down")
        st.markdown("HR can inspect one department or one employee while still seeing employee and manager context logs.")

        drill_df = employee_value.copy()
        if department_col:
            departments = sorted(drill_df[department_col].dropna().unique())
            selected_hr_department = st.selectbox("Select department/entity", ["All"] + departments)
            if selected_hr_department != "All":
                drill_df = drill_df[drill_df[department_col] == selected_hr_department]

        selected_hr_employee = st.selectbox("Select employee", sorted(drill_df["display_employee"].dropna().unique()))
        hr_emp = drill_df[drill_df["display_employee"] == selected_hr_employee].iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Value proxy", safe_value(hr_emp, "human_capital_value_proxy"))
        c2.metric("Learning", safe_value(hr_emp, "learning_intensity_score"))
        c3.metric("Continuity risk", safe_value(hr_emp, "absenteeism_risk_score"))
        c4.metric("Reliability", safe_value(hr_emp, "kpi_reliability_score"))

        st.subheader("Individual signal summary")
        signal_cols = ["display_employee", department_col, "segment_name", "risk_prediction_label", "recommended_action", "data_coverage_score", "kpi_reliability_score", "sustainability_balance"]
        signal_cols = [c for c in signal_cols if c and c in employee_value.columns]
        st.dataframe(pd.DataFrame([hr_emp[signal_cols]]), use_container_width=True, hide_index=True)

        employee_log = load_log("employee_context_log.csv")
        manager_log = load_log("manager_context_log.csv")
        emp_inputs = employee_log[employee_log["display_employee"] == selected_hr_employee] if not employee_log.empty and "display_employee" in employee_log.columns else pd.DataFrame()
        mgr_notes = manager_log[manager_log["display_employee"] == selected_hr_employee] if not manager_log.empty and "display_employee" in manager_log.columns else pd.DataFrame()

        st.subheader("Employee inputs")

        if not emp_inputs.empty:
            st.dataframe(
                emp_inputs.sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No employee inputs for this employee yet.")

        st.subheader("Manager notes")

        if not mgr_notes.empty:
            st.dataframe(
                mgr_notes.sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No manager notes for this employee yet.")

        show_context_summary(emp_inputs, mgr_notes)

    # TAB 4 — AI INSIGHTS
    # --------------------------------------------------
    with tab5:
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
    # TAB 5 — DATA & DOCUMENTS
    # --------------------------------------------------
    with tab6:
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
    # TAB 6 — USAGE & PRINCIPLES
    # --------------------------------------------------
    with tab7:
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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "System Health",
            "Valuation Model",
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
        st.subheader("What this helps Product Owners answer")
        st.dataframe(usefulness_answer("Product Owner"), use_container_width=True, hide_index=True)

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
                {
                    "Output": "employee_context_log.csv",
                    "Purpose": "V4 employee questions, decisions, and context inputs",
                    "Rows": len(load_log("employee_context_log.csv")),
                    "Status": "Loaded" if not load_log("employee_context_log.csv").empty else "Optional / no entries yet",
                },
                {
                    "Output": "manager_context_log.csv",
                    "Purpose": "V4 manager comments and contextual notes",
                    "Rows": len(load_log("manager_context_log.csv")),
                    "Status": "Loaded" if not load_log("manager_context_log.csv").empty else "Optional / no entries yet",
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
                    "Command": 'python -m streamlit run "dashboard/final version/streamlit_app_v4.py"',
                    "Expected output": "Launch dashboard",
                },
            ]
        )

        st.dataframe(run_order, use_container_width=True, hide_index=True)

    # --------------------------------------------------
    # TAB 2 — VALUATION MODEL
    # --------------------------------------------------
    with tab2:
        st.header("Valuation Model Monitoring")
        st.markdown(
            """
            Monitor whether the Blue-Line valuation framework is usable, reliable, and responsible.
            The objective is not score production; it is explainable, confidence-aware decision support.
            """
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg value potential", safe_mean(employee_value, "sustainable_value_potential"))
        col2.metric("Avg adjusted potential", safe_mean(employee_value, "reliability_adjusted_value_potential"))
        col3.metric("Avg interpretation risk", safe_mean(employee_value, "interpretation_risk"))
        col4.metric("Archetypes detected", f"{employee_value['valuation_archetype'].nunique():,}" if "valuation_archetype" in employee_value.columns else "N/A")

        st.subheader("Model input dimensions")
        dimension_cols = ["contribution_signal", "learning_future_value_signal", "sustainability_signal", "progression_signal", "interpretation_confidence"]
        available_dimension_cols = [c for c in dimension_cols if c in employee_value.columns]
        if available_dimension_cols:
            dimension_summary = pd.DataFrame({
                "Dimension": available_dimension_cols,
                "Average score": [round(employee_value[c].mean(), 3) for c in available_dimension_cols],
                "Minimum": [round(employee_value[c].min(), 3) for c in available_dimension_cols],
                "Maximum": [round(employee_value[c].max(), 3) for c in available_dimension_cols],
                "Missing values": [int(employee_value[c].isna().sum()) for c in available_dimension_cols],
            })
            st.dataframe(dimension_summary, use_container_width=True, hide_index=True)
            fig = px.bar(dimension_summary, x="Dimension", y="Average score", title="Average valuation model input dimensions")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        st.subheader("Interpretation risk monitoring")
        fig = px.histogram(employee_value, x="interpretation_risk", nbins=25, title="Distribution of interpretation risk")
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        if department_col and "valuation_archetype" in employee_value.columns:
            st.subheader("Valuation archetype by department")
            archetype_department = employee_value.groupby([department_col, "valuation_archetype"]).size().reset_index(name="Employees")
            fig = px.bar(archetype_department, x=department_col, y="Employees", color="valuation_archetype", title="Valuation archetypes by department/entity")
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(archetype_department, use_container_width=True, hide_index=True)

        st.subheader("Model limitations")
        limitations = pd.DataFrame([
            {"Limitation": "Indicators are proxies", "Implication": "The model estimates sustainable value potential; it does not directly measure financial value.", "Control": "Show dimension scores and interpretation confidence."},
            {"Limitation": "Performance reviews may be biased", "Implication": "Contribution signal may reflect review process bias.", "Control": "Monitor rating distributions by team and manager if data becomes available."},
            {"Limitation": "Absence data is a lagging signal", "Implication": "Burnout or disengagement may appear before absence increases.", "Control": "Add workload, engagement, and recovery indicators in future versions."},
            {"Limitation": "No supervised outcome labels yet", "Implication": "Risk labels are not validated predictive models.", "Control": "Treat AI outputs as segmentation and hypothesis generation, not prediction."},
            {"Limitation": "Low data coverage", "Implication": "Some profiles cannot be interpreted safely.", "Control": "Use interpretation confidence and block strong conclusions below threshold."},
        ])
        st.dataframe(limitations, use_container_width=True, hide_index=True)
        note("<b>Product Owner rule:</b> assess valuation by reliability, explainability, bias risk, and usefulness for learning — not by score production alone.", "governance")

    # --------------------------------------------------
    # TAB 3 — DATA QUALITY
    # --------------------------------------------------
    with tab3:
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
    with tab4:
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
    with tab5:
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
    with tab6:
        st.header("Document Pipeline")
        st.markdown(
            "Monitor unstructured document processing and theme extraction."
        )

        show_document_intelligence()