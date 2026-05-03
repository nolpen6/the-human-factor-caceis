from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"

employee_path = OUTPUTS / "employee_value_table_v2.csv"
output_path = OUTPUTS / "onevalue_ai_insights.csv"

df = pd.read_csv(employee_path)

if "display_employee" not in df.columns:
    df = df.reset_index(drop=True)
    df["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(df))]

if "segment_name" not in df.columns:
    if "ai_segment_label" in df.columns:
        df["segment_name"] = df["ai_segment_label"]
    else:
        df["segment_name"] = "Unclassified"

if "sustainability_balance" not in df.columns and {"learning_intensity_score", "absenteeism_risk_score"}.issubset(df.columns):
    df["sustainability_balance"] = df["learning_intensity_score"] - df["absenteeism_risk_score"]
elif "sustainability_balance" not in df.columns:
    df["sustainability_balance"] = np.nan


def interpret_profile(row):
    archetype = str(row.get("valuation_archetype", "Stable / Monitor"))

    if archetype == "Under-Observed Profile":
        return {
            "ai_signal": "Low interpretation confidence",
            "ai_interpretation": "Available data is too incomplete to interpret safely.",
            "recommended_experiment": "Validate identifier mapping and missing HR, training, review, and absence records.",
            "learning_question": "What important signals are missing from the current dataset?",
            "value_creation_hypothesis": "Improving data quality may reveal hidden contribution or risk.",
            "decision_owner": "HR / Data AI",
            "validation_needed": "Check source coverage, identifier mapping, and missing records before action.",
        }

    if archetype == "Value Under Pressure":
        return {
            "ai_signal": "High contribution under pressure",
            "ai_interpretation": "Contribution appears strong, but sustainability signals suggest possible pressure.",
            "recommended_experiment": "Test workload rebalancing or recovery support over the next review cycle.",
            "learning_question": "Does workload support improve sustainability without reducing contribution?",
            "value_creation_hypothesis": "Reducing pressure may preserve contribution while lowering future continuity risk.",
            "decision_owner": "Manager / HR",
            "validation_needed": "Validate with manager context, absence patterns, workload context, and employee feedback.",
        }

    if archetype == "Strong Contributor / Low Development":
        return {
            "ai_signal": "Strong contribution with low development signal",
            "ai_interpretation": "The profile shows contribution today but limited visible investment in future capability.",
            "recommended_experiment": "Offer targeted training, mentoring, or internal mobility and monitor learning uptake.",
            "learning_question": "Does targeted development increase future capability signals?",
            "value_creation_hypothesis": "Targeted development may increase future value potential.",
            "decision_owner": "Manager / Employee",
            "validation_needed": "Check whether training data is complete and whether the role requires formal training.",
        }

    if archetype == "Future Value Builder":
        return {
            "ai_signal": "Future value builder",
            "ai_interpretation": "The profile shows visible learning investment that may convert into future contribution.",
            "recommended_experiment": "Assign a mentor or stretch task to test whether learning converts into contribution.",
            "learning_question": "Which learning investments create measurable value in the role?",
            "value_creation_hypothesis": "Learning intensity may predict future contribution when applied in role.",
            "decision_owner": "Manager / Employee",
            "validation_needed": "Track follow-up contribution, mobility, or role impact over time.",
        }

    if archetype == "Sustainable Value Builder":
        return {
            "ai_signal": "Sustainable value conditions",
            "ai_interpretation": "Contribution, learning, and sustainability signals are jointly positive with sufficient reliability.",
            "recommended_experiment": "Identify enabling conditions and test whether they can support comparable teams.",
            "learning_question": "Which team or role conditions make value creation sustainable?",
            "value_creation_hypothesis": "Replicating enabling conditions may raise sustainable value potential elsewhere.",
            "decision_owner": "HR / Manager",
            "validation_needed": "Confirm context qualitatively before generalizing across teams.",
        }

    if archetype == "Low Learning Visibility":
        return {
            "ai_signal": "Low learning visibility",
            "ai_interpretation": "Visible learning activity is low; interpretation requires context.",
            "recommended_experiment": "Review training access, role requirements, and development planning.",
            "learning_question": "Is low learning due to access, role design, motivation, or missing data?",
            "value_creation_hypothesis": "Improving learning access or data capture may increase future value potential.",
            "decision_owner": "Employee / Manager / HR",
            "validation_needed": "Check training records and ask whether informal learning is invisible.",
        }

    return {
        "ai_signal": "Stable monitoring",
        "ai_interpretation": "The profile does not show a strong risk or opportunity signal from current data.",
        "recommended_experiment": "Maintain regular development check-ins and monitor signal evolution.",
        "learning_question": "What small action could improve contribution, learning, or sustainability?",
        "value_creation_hypothesis": "Continuous small improvements can raise long-term human capital value.",
        "decision_owner": "Employee / Manager",
        "validation_needed": "Continue checking data quality and context.",
    }

insights = df.apply(interpret_profile, axis=1, result_type="expand")

keep = [
    "display_employee", "segment_name", "valuation_archetype", "blue_line_question",
    "contribution_signal", "learning_future_value_signal", "sustainability_signal",
    "progression_signal", "interpretation_confidence", "sustainable_value_potential",
    "reliability_adjusted_value_potential", "interpretation_risk", "performance_score",
    "learning_intensity_score", "absenteeism_risk_score", "kpi_reliability_score",
    "human_capital_value_proxy", "reliability_adjusted_value_proxy", "sustainability_balance",
]

final_df = pd.concat([df[[c for c in keep if c in df.columns]], insights], axis=1)
final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ ONEValue AI insights created: {output_path}")
print(f"Shape: {final_df.shape}")
print(final_df.head())
