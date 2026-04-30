from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"

source_path = OUTPUTS / "employee_value_table_v2.csv"
risk_path = OUTPUTS / "risk_prediction_table.csv"
output_path = OUTPUTS / "recommendation_table.csv"

employee_df = pd.read_csv(source_path)

# Use risk table if available and non-empty
if risk_path.exists() and risk_path.stat().st_size > 0:
    risk_df = pd.read_csv(risk_path)
else:
    risk_df = pd.DataFrame()

employee_df = employee_df.reset_index(drop=True)

if "display_employee" not in employee_df.columns:
    employee_df["display_employee"] = [
        f"Employee P-{i+1:03d}" for i in range(len(employee_df))
    ]

# If risk labels already exist in risk table, merge them by display_employee
if not risk_df.empty and "display_employee" in risk_df.columns:
    keep_cols = [
        c for c in [
            "display_employee",
            "risk_prediction_label",
            "recommended_action",
        ]
        if c in risk_df.columns
    ]

    employee_df = employee_df.merge(
        risk_df[keep_cols],
        on="display_employee",
        how="left",
        suffixes=("", "_risk"),
    )

# Fallback risk label if missing
if "risk_prediction_label" not in employee_df.columns:
    q75 = employee_df["absenteeism_risk_score"].quantile(0.75)
    q40 = employee_df["absenteeism_risk_score"].quantile(0.40)

    def make_risk_label(x):
        if pd.isna(x):
            return "Unknown"
        if x >= q75:
            return "High"
        if x >= q40:
            return "Medium"
        return "Low"

    employee_df["risk_prediction_label"] = employee_df["absenteeism_risk_score"].apply(make_risk_label)


def build_recommendation(row):
    segment = str(row.get("segment_name", "Unclassified"))
    risk = str(row.get("risk_prediction_label", "Unknown"))
    low_data = bool(row.get("low_data_flag", False))

    absenteeism = row.get("absenteeism_risk_score", None)
    learning = row.get("learning_intensity_score", None)
    performance = row.get("performance_score", None)
    reliability = row.get("kpi_reliability_score", None)
    sustainability = None

    if pd.notna(learning) and pd.notna(absenteeism):
        sustainability = learning - absenteeism

    if low_data or segment == "Low Visibility Employees":
        return {
            "key_signal": "Low data visibility",
            "recommendation": "Improve data completeness before interpreting this profile.",
            "priority_level": "Medium",
            "role_target": "HR / Data AI",
            "human_question": "Are we missing important data, or is this employee outside tracked systems?",
        }

    if risk == "High" or segment == "High Engagement / High Risk":
        return {
            "key_signal": "High continuity risk",
            "recommendation": "Review workload, recovery balance, and wellbeing support.",
            "priority_level": "High",
            "role_target": "Manager / HR",
            "human_question": "Is this a motivated employee or team under unsustainable pressure?",
        }

    if segment == "High Performers / Low Development":
        return {
            "key_signal": "Strong contribution but limited development signal",
            "recommendation": "Offer targeted development opportunities and protect long-term capability.",
            "priority_level": "Medium",
            "role_target": "Manager",
            "human_question": "Are strong performers being stretched without enough future skill investment?",
        }

    if sustainability is not None and pd.notna(sustainability) and sustainability < 0:
        return {
            "key_signal": "Negative sustainability balance",
            "recommendation": "Discuss recovery, workload, and whether current effort is sustainable.",
            "priority_level": "High",
            "role_target": "Manager",
            "human_question": "Is value being created in a way that may not be sustainable over time?",
        }

    if pd.notna(reliability) and reliability < 0.5:
        return {
            "key_signal": "Low KPI reliability",
            "recommendation": "Validate data sources before using this profile for decisions.",
            "priority_level": "Medium",
            "role_target": "HR / Data AI",
            "human_question": "Can this signal be trusted enough to guide action?",
        }

    if pd.notna(learning) and learning < 0.3:
        return {
            "key_signal": "Low learning intensity",
            "recommendation": "Explore relevant training, mobility, or upskilling opportunities.",
            "priority_level": "Low",
            "role_target": "Employee / Manager",
            "human_question": "What future capability should be developed next?",
        }

    return {
        "key_signal": "Stable profile",
        "recommendation": "Maintain regular development check-ins and continue monitoring signals.",
        "priority_level": "Low",
        "role_target": "Employee / Manager",
        "human_question": "How can current contribution and learning be sustained?",
    }


recommendations = employee_df.apply(build_recommendation, axis=1, result_type="expand")

final_df = pd.concat(
    [
        employee_df[
            [
                c for c in [
                    "display_employee",
                    "segment_name",
                    "risk_prediction_label",
                    "absenteeism_risk_score",
                    "learning_intensity_score",
                    "performance_score",
                    "kpi_reliability_score",
                    "human_capital_value_proxy",
                    "reliability_adjusted_value_proxy",
                ]
                if c in employee_df.columns
            ]
        ],
        recommendations,
    ],
    axis=1,
)

final_df.to_csv(output_path, index=False)

print(f"✅ recommendation_table.csv created: {output_path}")
print(f"Shape: {final_df.shape}")
print(final_df.head())