
"""
04_integrated_value_ai.py

Builds an integrated employee-level human capital value table from the three KPI outputs:
- hr_kpi_table.csv
- absence_kpi_table.csv
- training_kpi_table.csv

This file intentionally uses only the provided output files. It ignores any zip/project folder.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "outputs"# change to Path("data/processed") if needed


def load_inputs(data_dir: Path = DATA_DIR):
    hr = pd.read_csv(data_dir / "hr_kpi_table.csv", encoding="utf-8-sig")
    absence = pd.read_csv(data_dir / "absence_kpi_table.csv", encoding="utf-8-sig")
    training = pd.read_csv(data_dir / "training_kpi_table.csv", encoding="utf-8-sig")

    hr = hr.rename(columns={"iug": "employee_id"})
    absence = absence.rename(columns={"employee_code": "employee_id"})
    training = training.rename(columns={"employee_code": "employee_id"})

    hr["low_data_flag"] = (
        hr["low_data_flag"]
        .fillna(False)
        .astype(str)
        .str.lower()
        .eq("true")
    )

    return hr, absence, training


def build_employee_value_table(hr: pd.DataFrame, absence: pd.DataFrame, training: pd.DataFrame):
    employee = (
        hr.merge(absence, on="employee_id", how="left", indicator="absence_merge_status")
          .merge(training, on="employee_id", how="left", indicator="training_merge_status")
    )

    employee["has_absence_record"] = employee["absence_merge_status"].eq("both")
    employee["has_training_record"] = employee["training_merge_status"].eq("both")
    employee["has_performance_record"] = employee["avg_performance"].notna()

    # Interpretation for this prototype:
    # Missing absence/training rows mean "not observed in the corresponding source".
    # We set the quantitative KPI to 0 but preserve coverage flags so users know what is missing.
    zero_fill_cols = [
        "absence_events", "absence_days", "absence_events_score", "absence_days_score",
        "absenteeism_risk_score", "training_count", "training_hours",
        "training_count_score", "training_hours_score", "learning_intensity_score",
    ]
    for col in zero_fill_cols:
        employee[col] = employee[col].fillna(0)

    # Normalize performance to 0-1 assuming avg_performance has max observed scale of 5.
    employee["performance_score"] = employee["avg_performance"] / 5
    employee["performance_score"] = employee["performance_score"].fillna(
        employee["performance_score"].median()
    )

    employee["talent_progression_proxy"] = employee["talent_progression_proxy"].fillna(
        employee["talent_progression_proxy"].median()
    )

    employee["data_coverage_score"] = employee[
        ["has_absence_record", "has_training_record", "has_performance_record"]
    ].mean(axis=1)

    employee["kpi_reliability_score"] = np.where(
        employee["low_data_flag"], 0.5, 1.0
    ) * employee["data_coverage_score"]

    # Human Capital Value Proxy:
    # This is NOT a financial valuation. It is a normalized proxy connecting available KPIs to value drivers.
    employee["human_capital_value_proxy"] = (
        0.35 * employee["performance_score"]
        + 0.25 * employee["talent_progression_proxy"]
        + 0.20 * employee["learning_intensity_score"]
        + 0.20 * (1 - employee["absenteeism_risk_score"])
    )

    # Penalize the proxy when KPI reliability is low.
    employee["reliability_adjusted_value_proxy"] = (
        employee["human_capital_value_proxy"] * (0.5 + 0.5 * employee["kpi_reliability_score"])
    )

    return employee


def add_decision_flags(employee: pd.DataFrame):
    high_absence_cutoff = employee["absenteeism_risk_score"].quantile(0.80)
    high_learning_cutoff = employee["learning_intensity_score"].quantile(0.80)
    low_learning_cutoff = employee["learning_intensity_score"].quantile(0.20)
    high_perf_cutoff = employee["performance_score"].quantile(0.80)
    low_value_cutoff = employee["reliability_adjusted_value_proxy"].quantile(0.20)
    high_value_cutoff = employee["reliability_adjusted_value_proxy"].quantile(0.80)

    employee["risk_flag"] = np.select(
        [
            employee["absenteeism_risk_score"].ge(high_absence_cutoff),
            employee["reliability_adjusted_value_proxy"].le(low_value_cutoff),
            employee["low_data_flag"],
        ],
        ["High absenteeism risk", "Low value proxy", "Low KPI reliability"],
        default="No major risk flag",
    )

    employee["opportunity_flag"] = np.select(
        [
            employee["performance_score"].ge(high_perf_cutoff)
            & employee["learning_intensity_score"].le(low_learning_cutoff),
            employee["learning_intensity_score"].ge(high_learning_cutoff)
            & employee["performance_score"].lt(high_perf_cutoff),
            employee["reliability_adjusted_value_proxy"].ge(high_value_cutoff),
        ],
        [
            "High performer with low learning investment",
            "Learning investment to monitor for future impact",
            "High value proxy",
        ],
        default="Standard monitoring",
    )

    return employee


def add_ai_segments(employee: pd.DataFrame, n_clusters: int = 4):
    features = [
        "performance_score",
        "talent_progression_proxy",
        "learning_intensity_score",
        "absenteeism_risk_score",
        "kpi_reliability_score",
    ]

    X = employee[features].replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())

    X_scaled = StandardScaler().fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    employee["ai_segment"] = kmeans.fit_predict(X_scaled)

    silhouette = silhouette_score(X_scaled, employee["ai_segment"])

    cluster_summary = employee.groupby("ai_segment")[
        features + ["human_capital_value_proxy"]
    ].mean()

    cluster_names = {}
    for cluster, row in cluster_summary.iterrows():
        if row["absenteeism_risk_score"] >= cluster_summary["absenteeism_risk_score"].quantile(0.75):
            cluster_names[cluster] = "Operational continuity risk"
        elif row["learning_intensity_score"] >= cluster_summary["learning_intensity_score"].quantile(0.75):
            cluster_names[cluster] = "Learning-intensive profile"
        elif row["human_capital_value_proxy"] >= cluster_summary["human_capital_value_proxy"].quantile(0.75):
            cluster_names[cluster] = "High value proxy profile"
        else:
            cluster_names[cluster] = "Stable baseline profile"

    employee["ai_segment_label"] = employee["ai_segment"].map(cluster_names)
    employee["segment_name"] = employee["ai_segment_label"]

    return employee, cluster_summary, silhouette


def build_department_summary(employee: pd.DataFrame):
    dept_col = "libelle_organisation_niveau_07"

    return (
        employee.groupby(dept_col, dropna=False)
        .agg(
            employees=("employee_id", "nunique"),
            avg_value_proxy=("human_capital_value_proxy", "mean"),
            avg_reliability_adjusted_value=("reliability_adjusted_value_proxy", "mean"),
            avg_absenteeism_risk=("absenteeism_risk_score", "mean"),
            avg_learning_intensity=("learning_intensity_score", "mean"),
            avg_kpi_reliability=("kpi_reliability_score", "mean"),
            high_absence_risk_share=("risk_flag", lambda s: (s == "High absenteeism risk").mean()),
        )
        .reset_index()
        .sort_values("employees", ascending=False)
    )


def main():
    hr, absence, training = load_inputs(DATA_DIR)

    print("Input tables")
    print(f"HR KPI table: {hr.shape}")
    print(f"Absence KPI table: {absence.shape}")
    print(f"Training KPI table: {training.shape}")
    print()
    print("ID overlap validation")
    print(f"HR ∩ Absence: {len(set(hr['employee_id']) & set(absence['employee_id']))}")
    print(f"HR ∩ Training: {len(set(hr['employee_id']) & set(training['employee_id']))}")
    print(f"All three: {len(set(hr['employee_id']) & set(absence['employee_id']) & set(training['employee_id']))}")

    employee = build_employee_value_table(hr, absence, training)
    employee = add_decision_flags(employee)
    employee, cluster_summary, silhouette = add_ai_segments(employee)
    department_summary = build_department_summary(employee)

    employee.to_csv(DATA_DIR / "employee_value_table_v2.csv", index=False, encoding="utf-8-sig")
    department_summary.to_csv(DATA_DIR / "department_value_summary_v2.csv", index=False, encoding="utf-8-sig")
    cluster_summary.to_csv(DATA_DIR / "ai_segment_summary_v2.csv", encoding="utf-8-sig")

    print()
    print("Generated outputs")
    print(f"employee_value_table_v2.csv: {employee.shape}")
    print(f"department_value_summary_v2.csv: {department_summary.shape}")
    print(f"ai_segment_summary_v2.csv: {cluster_summary.shape}")
    print(f"KMeans silhouette score: {silhouette:.3f}")


if __name__ == "__main__":
    main()
