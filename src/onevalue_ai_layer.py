from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"

employee_path = OUTPUTS / "employee_value_table_v2.csv"
output_path = OUTPUTS / "onevalue_ai_insights.csv"

df = pd.read_csv(employee_path)

# --------------------------------------------------
# Compatibility checks
# --------------------------------------------------
if "display_employee" not in df.columns:
    df = df.reset_index(drop=True)
    df["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(df))]

if "segment_name" not in df.columns:
    if "ai_segment_label" in df.columns:
        df["segment_name"] = df["ai_segment_label"]
    else:
        df["segment_name"] = "Unclassified"

# --------------------------------------------------
# Create sustainability balance
# --------------------------------------------------
if {"learning_intensity_score", "absenteeism_risk_score"}.issubset(df.columns):
    df["sustainability_balance"] = (
        df["learning_intensity_score"] - df["absenteeism_risk_score"]
    )
else:
    df["sustainability_balance"] = np.nan

# --------------------------------------------------
# AI interpretation logic
# --------------------------------------------------
def interpret_profile(row):
    segment = str(row.get("segment_name", "Unclassified"))
    absence = row.get("absenteeism_risk_score", np.nan)
    learning = row.get("learning_intensity_score", np.nan)
    performance = row.get("performance_score", np.nan)
    reliability = row.get("kpi_reliability_score", np.nan)
    sustainability = row.get("sustainability_balance", np.nan)

    if pd.notna(reliability) and reliability < 0.5:
        return {
            "ai_signal": "Low visibility",
            "ai_interpretation": "The profile has limited data coverage, so conclusions should be avoided.",
            "recommended_experiment": "Improve HR, training, and review data completeness for this profile.",
            "learning_question": "Is this employee really low-signal, or are we missing important data?",
            "value_creation_hypothesis": "Better data quality will improve decision reliability.",
            "decision_owner": "HR / Data AI",
        }

    if pd.notna(absence) and pd.notna(performance) and absence > 0.7 and performance > 0.7:
        return {
            "ai_signal": "High contribution under pressure",
            "ai_interpretation": "The employee appears to contribute strongly while showing elevated continuity risk.",
            "recommended_experiment": "Test workload rebalancing or recovery support over the next review cycle.",
            "learning_question": "Is strong value being created sustainably?",
            "value_creation_hypothesis": "Reducing pressure may preserve contribution and lower future absence risk.",
            "decision_owner": "Manager / HR",
        }

    if pd.notna(performance) and pd.notna(learning) and performance > 0.7 and learning < 0.3:
        return {
            "ai_signal": "High performer with low development signal",
            "ai_interpretation": "The employee contributes strongly but has limited visible learning investment.",
            "recommended_experiment": "Offer targeted training, mentoring, or internal mobility.",
            "learning_question": "Are strong performers being developed for future value creation?",
            "value_creation_hypothesis": "Targeted development will increase future capability without reducing current performance.",
            "decision_owner": "Manager",
        }

    if pd.notna(sustainability) and sustainability < -0.3:
        return {
            "ai_signal": "Negative sustainability balance",
            "ai_interpretation": "Absence/continuity risk is higher than visible learning investment.",
            "recommended_experiment": "Review workload, role design, and recovery conditions.",
            "learning_question": "Which working conditions are creating unsustainable pressure?",
            "value_creation_hypothesis": "Improving work design may increase sustainable human capital value.",
            "decision_owner": "Manager / HR",
        }

    if pd.notna(learning) and learning > 0.7:
        return {
            "ai_signal": "Learning-intensive profile",
            "ai_interpretation": "The employee shows strong visible learning activity.",
            "recommended_experiment": "Track whether learning translates into future performance, mobility, or resilience.",
            "learning_question": "Which learning investments create measurable value?",
            "value_creation_hypothesis": "Learning intensity may predict future contribution if applied in role.",
            "decision_owner": "HR / Manager",
        }

    return {
        "ai_signal": "Stable baseline",
        "ai_interpretation": "The profile does not show a strong risk or opportunity signal.",
        "recommended_experiment": "Maintain regular development check-ins and monitor evolution.",
        "learning_question": "What small action could improve contribution, learning, or sustainability?",
        "value_creation_hypothesis": "Continuous small improvements can raise long-term human capital value.",
        "decision_owner": "Employee / Manager",
    }


insights = df.apply(interpret_profile, axis=1, result_type="expand")

final_df = pd.concat(
    [
        df[
            [
                c for c in [
                    "display_employee",
                    "segment_name",
                    "performance_score",
                    "learning_intensity_score",
                    "absenteeism_risk_score",
                    "kpi_reliability_score",
                    "human_capital_value_proxy",
                    "reliability_adjusted_value_proxy",
                    "sustainability_balance",
                ]
                if c in df.columns
            ]
        ],
        insights,
    ],
    axis=1,
)

final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ ONEValue AI insights created: {output_path}")
print(f"Shape: {final_df.shape}")
print(final_df.head())