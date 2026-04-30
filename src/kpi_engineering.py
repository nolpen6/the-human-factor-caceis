import pandas as pd
import numpy as np


def safe_rank_score(series: pd.Series, reverse: bool = False) -> pd.Series:
    """
    Converts a numeric column into a 0-1 percentile score.
    reverse=True means lower values get higher scores.
    """
    s = pd.to_numeric(series, errors="coerce")

    if s.notna().sum() == 0:
        return pd.Series(np.nan, index=series.index)

    score = s.rank(pct=True)

    if reverse:
        score = 1 - score

    return score


def build_absenteeism_kpi(
    absences: pd.DataFrame,
    employee_col: str,
    days_col: str = None,
    start_date_col: str = None,
    end_date_col: str = None
) -> pd.DataFrame:
    """
    KPI 1: Absenteeism Risk Score
    Based on absence frequency and duration.
    """

    df = absences.copy()

    if days_col and days_col in df.columns:
        df["absence_days"] = pd.to_numeric(df[days_col], errors="coerce")
    elif start_date_col and end_date_col:
        df[start_date_col] = pd.to_datetime(df[start_date_col], errors="coerce")
        df[end_date_col] = pd.to_datetime(df[end_date_col], errors="coerce")
        df["absence_days"] = (df[end_date_col] - df[start_date_col]).dt.days + 1
    else:
        df["absence_days"] = 1

    summary = df.groupby(employee_col).agg(
        absence_events=(employee_col, "count"),
        absence_days=("absence_days", "sum")
    ).reset_index()

    summary["absence_events_score"] = safe_rank_score(summary["absence_events"])
    summary["absence_days_score"] = safe_rank_score(summary["absence_days"])

    summary["absenteeism_risk_score"] = (
        0.4 * summary["absence_events_score"] +
        0.6 * summary["absence_days_score"]
    )

    return summary


def build_learning_kpi(
    training: pd.DataFrame,
    employee_col: str,
    training_id_col: str = None,
    duration_col: str = None,
    date_col: str = None
) -> pd.DataFrame:
    """
    KPI 2: Learning Intensity Score
    Based on number and duration of trainings.
    """

    df = training.copy()

    if duration_col and duration_col in df.columns:
        df["training_duration"] = pd.to_numeric(df[duration_col], errors="coerce")
    else:
        df["training_duration"] = 0

    agg_dict = {
        "training_count": (employee_col, "count"),
        "training_hours": ("training_duration", "sum")
    }

    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        agg_dict["last_training_date"] = (date_col, "max")

    summary = df.groupby(employee_col).agg(**agg_dict).reset_index()

    summary["training_count_score"] = safe_rank_score(summary["training_count"])
    summary["training_hours_score"] = safe_rank_score(summary["training_hours"])

    summary["learning_intensity_score"] = (
        0.5 * summary["training_count_score"] +
        0.5 * summary["training_hours_score"]
    )

    return summary


def build_performance_kpi(
    performance: pd.DataFrame,
    employee_col: str,
    score_col: str
) -> pd.DataFrame:
    """
    KPI 3: Performance Consistency Score
    Based on average performance and variation.
    """

    df = performance.copy()
    df[score_col] = pd.to_numeric(df[score_col], errors="coerce")

    summary = df.groupby(employee_col).agg(
        avg_performance=(score_col, "mean"),
        performance_std=(score_col, "std"),
        performance_reviews=(score_col, "count")
    ).reset_index()

    summary["performance_level_score"] = safe_rank_score(summary["avg_performance"])
    summary["performance_consistency_score"] = safe_rank_score(
        summary["performance_std"],
        reverse=True
    )

    summary["performance_consistency_score"] = summary[
        "performance_consistency_score"
    ].fillna(1)

    return summary


def build_engagement_kpi(
    engagement: pd.DataFrame,
    group_col: str,
    score_col: str,
    time_col: str = None
) -> pd.DataFrame:
    """
    KPI 4: Engagement Stability Index
    Usually calculated at team/department level if individual engagement is unavailable.
    """

    df = engagement.copy()
    df[score_col] = pd.to_numeric(df[score_col], errors="coerce")

    if time_col and time_col in df.columns:
        summary = df.groupby(group_col).agg(
            avg_engagement=(score_col, "mean"),
            engagement_std=(score_col, "std"),
            engagement_observations=(score_col, "count")
        ).reset_index()

        summary["engagement_stability_index"] = safe_rank_score(
            summary["engagement_std"],
            reverse=True
        )

    else:
        summary = df.groupby(group_col).agg(
            avg_engagement=(score_col, "mean"),
            engagement_observations=(score_col, "count")
        ).reset_index()

        summary["engagement_stability_index"] = safe_rank_score(
            summary["avg_engagement"]
        )

    return summary


def build_talent_progression_kpi(
    hr: pd.DataFrame,
    employee_col: str,
    promotion_col: str = None,
    role_change_col: str = None,
    tenure_col: str = None
) -> pd.DataFrame:
    """
    KPI 5: Talent Progression Proxy
    Based on promotions, role changes, or fallback to tenure.
    """

    df = hr.copy()

    summary = df[[employee_col]].drop_duplicates().copy()

    if promotion_col and promotion_col in df.columns:
        summary["promotion_count"] = pd.to_numeric(
            df[promotion_col],
            errors="coerce"
        ).fillna(0)

    else:
        summary["promotion_count"] = 0

    if role_change_col and role_change_col in df.columns:
        summary["role_change_count"] = pd.to_numeric(
            df[role_change_col],
            errors="coerce"
        ).fillna(0)

    else:
        summary["role_change_count"] = 0

    if tenure_col and tenure_col in df.columns:
        summary["tenure"] = pd.to_numeric(df[tenure_col], errors="coerce")
    else:
        summary["tenure"] = np.nan

    summary["talent_progression_raw"] = (
        summary["promotion_count"] +
        summary["role_change_count"]
    )

    if summary["talent_progression_raw"].sum() > 0:
        summary["talent_progression_proxy"] = safe_rank_score(
            summary["talent_progression_raw"]
        )
    else:
        summary["talent_progression_proxy"] = safe_rank_score(summary["tenure"])

    return summary