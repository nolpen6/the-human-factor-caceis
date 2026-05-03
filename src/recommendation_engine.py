from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"

source_path = OUTPUTS / "employee_value_table_v2.csv"
risk_path = OUTPUTS / "risk_prediction_table.csv"
output_path = OUTPUTS / "recommendation_table.csv"

employee_df = pd.read_csv(source_path)

if risk_path.exists() and risk_path.stat().st_size > 0:
    risk_df = pd.read_csv(risk_path)
else:
    risk_df = pd.DataFrame()

employee_df = employee_df.reset_index(drop=True)

if "display_employee" not in employee_df.columns:
    employee_df["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(employee_df))]

if not risk_df.empty and "display_employee" in risk_df.columns:
    keep_cols = [c for c in ["display_employee", "risk_prediction_label", "recommended_action"] if c in risk_df.columns]
    employee_df = employee_df.merge(risk_df[keep_cols], on="display_employee", how="left", suffixes=("", "_risk"))

if "risk_prediction_label" not in employee_df.columns and "absenteeism_risk_score" in employee_df.columns:
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
    archetype = str(row.get("valuation_archetype", "Stable / Monitor"))
    risk = str(row.get("risk_prediction_label", "Unknown"))
    low_data = bool(row.get("low_data_flag", False))

    if archetype == "Under-Observed Profile" or low_data:
        return {
            "key_signal": "Low interpretation confidence",
            "recommendation": "Validate missing records before interpreting this profile.",
            "recommended_experiment": "Validate HR, performance, absence, and training records before interpretation.",
            "expected_signal_change": "Higher data coverage and interpretation confidence.",
            "review_period": "2-4 weeks",
            "priority_level": "Medium",
            "role_target": "HR / Data AI",
            "decision_owner": "HR / Data AI",
            "human_question": "Do we have enough reliable data to interpret this profile safely?",
            "governance_guardrail": "Do not use this profile for individual decisions until reliability improves.",
        }

    if archetype == "Value Under Pressure" or risk == "High":
        return {
            "key_signal": "Value under pressure",
            "recommendation": "Review workload, recovery balance, and wellbeing support.",
            "recommended_experiment": "Run a workload and recovery review, then test a targeted workload rebalance.",
            "expected_signal_change": "Lower continuity risk and improved sustainability signal.",
            "review_period": "4-8 weeks",
            "priority_level": "High",
            "role_target": "Manager / HR",
            "decision_owner": "Manager / HR",
            "human_question": "Is current contribution being created in a sustainable way?",
            "governance_guardrail": "Use this as a wellbeing and continuity prompt, not a performance judgment.",
        }

    if archetype == "Strong Contributor / Low Development":
        return {
            "key_signal": "Strong contribution but limited development signal",
            "recommendation": "Offer targeted development opportunities while protecting current contribution.",
            "recommended_experiment": "Offer one targeted training, mentoring, or mobility opportunity and monitor learning uptake.",
            "expected_signal_change": "Higher future value signal without reducing contribution.",
            "review_period": "1 quarter",
            "priority_level": "Medium",
            "role_target": "Manager / Employee",
            "decision_owner": "Manager / Employee",
            "human_question": "Are strong contributors receiving enough future-oriented development?",
            "governance_guardrail": "Do not assume low learning means low motivation; check access and role context.",
        }

    if archetype == "Future Value Builder":
        return {
            "key_signal": "High learning signal with future value potential",
            "recommendation": "Convert learning into contribution through mentoring or a stretch assignment.",
            "recommended_experiment": "Assign a mentor or stretch project to test whether learning converts into contribution.",
            "expected_signal_change": "Improved contribution and progression signals.",
            "review_period": "1 quarter",
            "priority_level": "Medium",
            "role_target": "Manager / Employee",
            "decision_owner": "Manager / Employee",
            "human_question": "How can learning investment be converted into measurable contribution?",
            "governance_guardrail": "Support conversion of learning into contribution; do not penalize current lower contribution.",
        }

    if archetype == "Sustainable Value Builder":
        return {
            "key_signal": "Sustainable value conditions",
            "recommendation": "Identify enabling conditions and replicate them carefully across comparable teams.",
            "recommended_experiment": "Document what enables this profile and test one condition in a comparable team.",
            "expected_signal_change": "Stable or improved sustainable value potential across similar profiles.",
            "review_period": "1 quarter",
            "priority_level": "Low",
            "role_target": "HR / Manager",
            "decision_owner": "HR / Manager",
            "human_question": "What conditions are enabling sustainable value creation here?",
            "governance_guardrail": "Do not overburden high-performing profiles; protect sustainability.",
        }

    if archetype == "Low Learning Visibility":
        return {
            "key_signal": "Low learning visibility",
            "recommendation": "Review training access and development planning.",
            "recommended_experiment": "Review training access and define one development action with employee and manager.",
            "expected_signal_change": "Clearer learning signal and improved development visibility.",
            "review_period": "1 quarter",
            "priority_level": "Low",
            "role_target": "Employee / Manager / HR",
            "decision_owner": "Employee / Manager / HR",
            "human_question": "Is low learning due to limited access, limited need, low motivation, or missing data?",
            "governance_guardrail": "Low learning visibility is not proof of low capability.",
        }

    return {
        "key_signal": "Stable monitoring",
        "recommendation": "Maintain regular development check-ins and continue monitoring signals.",
        "recommended_experiment": "Maintain regular check-ins and monitor contribution, learning, and sustainability evolution.",
        "expected_signal_change": "Stable or improved signals over the next review cycle.",
        "review_period": "1 quarter",
        "priority_level": "Low",
        "role_target": "Employee / Manager",
        "decision_owner": "Employee / Manager",
        "human_question": "What should be monitored to sustain contribution and development over time?",
        "governance_guardrail": "Use indicators as learning prompts, not rankings.",
    }



def derive_caceis_value_lens(row):
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

employee_df["caceis_value_lens"] = employee_df.apply(derive_caceis_value_lens, axis=1)

recommendations = employee_df.apply(build_recommendation, axis=1, result_type="expand")

keep = [
    "display_employee", "segment_name", "valuation_archetype", "blue_line_question",
    "risk_prediction_label", "contribution_signal", "learning_future_value_signal",
    "sustainability_signal", "progression_signal", "interpretation_confidence",
    "sustainable_value_potential", "reliability_adjusted_value_potential", "interpretation_risk",
    "absenteeism_risk_score", "learning_intensity_score", "performance_score",
    "kpi_reliability_score", "human_capital_value_proxy", "reliability_adjusted_value_proxy",
]

final_df = pd.concat([employee_df[[c for c in keep if c in employee_df.columns]], recommendations], axis=1)
final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ recommendation_table.csv created: {output_path}")
print(f"Shape: {final_df.shape}")
print(final_df.head())
