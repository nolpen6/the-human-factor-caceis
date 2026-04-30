from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"

# -----------------------------
# LOAD DATA
# -----------------------------
source_path = OUTPUTS / "employee_value_table_v2.csv"
output_path = OUTPUTS / "risk_prediction_table.csv"

df = pd.read_csv(source_path)

print("Loaded employee_value_table:", df.shape)

if df.empty:
    raise ValueError("❌ employee_value_table is empty")

# -----------------------------
# CREATE DISPLAY ID
# -----------------------------
df = df.reset_index(drop=True)
df["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(df))]

# -----------------------------
# CREATE RISK LABEL
# -----------------------------
q75 = df["absenteeism_risk_score"].quantile(0.75)
q40 = df["absenteeism_risk_score"].quantile(0.40)

def risk_label(x):
    if pd.isna(x):
        return "Unknown"
    if x >= q75:
        return "High"
    elif x >= q40:
        return "Medium"
    return "Low"

df["risk_prediction_label"] = df["absenteeism_risk_score"].apply(risk_label)

# -----------------------------
# CREATE RECOMMENDATIONS
# -----------------------------
def recommendation(row):
    segment = row.get("segment_name", "")
    risk = row.get("risk_prediction_label", "")
    low_data = row.get("low_data_flag", False)

    if low_data or segment == "Low Visibility Employees":
        return "Improve data completeness before interpretation."
    if risk == "High" or segment == "High Engagement / High Risk":
        return "Review workload and wellbeing."
    if segment == "High Performers / Low Development":
        return "Offer development opportunities."
    return "Maintain monitoring."

df["recommended_action"] = df.apply(recommendation, axis=1)

# -----------------------------
# SELECT FINAL COLUMNS
# -----------------------------
cols = [
    "display_employee",
    "segment_name",
    "risk_prediction_label",
    "absenteeism_risk_score",
    "learning_intensity_score",
    "performance_score",
    "kpi_reliability_score",
    "recommended_action",
]

cols = [c for c in cols if c in df.columns]

risk_df = df[cols].copy()

# -----------------------------
# SAVE FILE
# -----------------------------
risk_df.to_csv(output_path, index=False)

print("✅ File created:", output_path)
print("Shape:", risk_df.shape)
print(risk_df.head())