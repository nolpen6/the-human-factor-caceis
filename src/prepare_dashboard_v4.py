from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
OUTPUTS = BASE / "outputs"


def _safe_series(df: pd.DataFrame, col: str, default):
    if col in df.columns:
        return df[col]
    return pd.Series(default, index=df.index)


def _build_hr_kpi(employee_df: pd.DataFrame) -> pd.DataFrame:
    hr_df = pd.DataFrame(
        {
            "iug": _safe_series(employee_df, "employee_id", [f"EMP_{i + 1:05d}" for i in range(len(employee_df))]),
            "low_data_flag": _safe_series(employee_df, "low_data_flag", False),
            "avg_performance": _safe_series(employee_df, "avg_performance", pd.NA),
            "performance_std": _safe_series(employee_df, "performance_std", pd.NA),
            "performance_reviews": _safe_series(employee_df, "performance_reviews", pd.NA),
            "performance_consistency_score": _safe_series(employee_df, "performance_consistency_score", pd.NA),
            "talent_progression_proxy": _safe_series(employee_df, "talent_progression_proxy", pd.NA),
            "libelle_organisation_niveau_07": _safe_series(employee_df, "libelle_organisation_niveau_07", pd.NA),
        }
    )
    return hr_df


def _build_absence_kpi(employee_df: pd.DataFrame) -> pd.DataFrame:
    absence_df = pd.DataFrame(
        {
            "employee_code": _safe_series(employee_df, "employee_id", [f"EMP_{i + 1:05d}" for i in range(len(employee_df))]),
            "absence_events": _safe_series(employee_df, "absence_events", 0),
            "absence_days": _safe_series(employee_df, "absence_days", 0),
            "absence_events_score": _safe_series(employee_df, "absence_events_score", 0),
            "absence_days_score": _safe_series(employee_df, "absence_days_score", 0),
            "absenteeism_risk_score": _safe_series(employee_df, "absenteeism_risk_score", 0),
        }
    )
    return absence_df


def _build_training_kpi(employee_df: pd.DataFrame) -> pd.DataFrame:
    training_df = pd.DataFrame(
        {
            "employee_code": _safe_series(employee_df, "employee_id", [f"EMP_{i + 1:05d}" for i in range(len(employee_df))]),
            "training_count": _safe_series(employee_df, "training_count", 0),
            "training_hours": _safe_series(employee_df, "training_hours", 0),
            "training_count_score": _safe_series(employee_df, "training_count_score", 0),
            "training_hours_score": _safe_series(employee_df, "training_hours_score", 0),
            "learning_intensity_score": _safe_series(employee_df, "learning_intensity_score", 0),
        }
    )
    return training_df


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    required = [
        OUTPUTS / "hr_kpi_table.csv",
        OUTPUTS / "absence_kpi_table.csv",
        OUTPUTS / "training_kpi_table.csv",
    ]

    missing = [p for p in required if not p.exists() or p.stat().st_size == 0]
    if not missing:
        print("All required KPI files already exist. No preparation needed.")
        return

    employee_path = OUTPUTS / "employee_value_table_v2.csv"
    if not employee_path.exists() or employee_path.stat().st_size == 0:
        raise FileNotFoundError(
            "Missing outputs/employee_value_table_v2.csv. Cannot derive required KPI files."
        )

    employee_df = pd.read_csv(employee_path, encoding="utf-8-sig")
    if employee_df.empty:
        raise ValueError("outputs/employee_value_table_v2.csv is empty. Cannot prepare KPI files.")

    if required[0] in missing:
        hr_df = _build_hr_kpi(employee_df)
        hr_df.to_csv(required[0], index=False, encoding="utf-8-sig")
        print(f"Created {required[0].name}: {hr_df.shape}")

    if required[1] in missing:
        absence_df = _build_absence_kpi(employee_df)
        absence_df.to_csv(required[1], index=False, encoding="utf-8-sig")
        print(f"Created {required[1].name}: {absence_df.shape}")

    if required[2] in missing:
        training_df = _build_training_kpi(employee_df)
        training_df.to_csv(required[2], index=False, encoding="utf-8-sig")
        print(f"Created {required[2].name}: {training_df.shape}")

    print("Preparation complete. Dashboard v4 required files are available.")


if __name__ == "__main__":
    main()
