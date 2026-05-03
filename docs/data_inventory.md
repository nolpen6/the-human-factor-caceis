# 📦 Data Inventory — Human Capital Signals

## Objective

Map available datasets to the **value signals used in the dashboard**.

This is not just a data list — it explains:
- what each dataset measures
- how it is used in the pipeline
- what signal it produces
- what its limits are

---

## Value Dimensions (used in the dashboard)

| Dimension        | What it means                     | Example signal                    |
|----------------|----------------------------------|----------------------------------|
| Contribution    | Current observable impact        | performance_score                |
| Learning        | Future capability                | learning_intensity_score         |
| Sustainability  | Continuity / risk                | absenteeism_risk_score           |
| Reliability     | Data quality / completeness      | kpi_reliability_score            |

---

## Available Data Sources

### 1. HR Master Data

**Used for**
- joins and segmentation
- department / role context

**Feeds**
- grouping in dashboard
- comparison across teams

**Limitation**
- no behavioral signal

---

### 2. Performance Data

**Feeds**
- `performance_score`
- `performance_consistency_score`

**Used in**
- contribution signal
- manager view

**Limitations**
- subjective (bias)
- low frequency

---

### 3. Absenteeism Data

**Feeds**
- `absenteeism_risk_score`

**Used in**
- sustainability signal
- risk detection

**Limitations**
- lagging indicator
- does not explain cause

---

### 4. Training Data

**Feeds**
- `learning_intensity_score`

**Used in**
- development signal
- employee dashboard

**Limitations**
- measures participation, not skill
- no guarantee of application

---

## Derived Signals (from code)

| Signal                         | Meaning |
|------------------------------|--------|
| contribution_signal           | current contribution proxy |
| learning_future_value_signal  | development / future capability |
| sustainability_signal         | inverse of absence risk |
| interpretation_confidence     | data reliability |
| sustainable_value_potential   | combined signal |

---

## Key Gap (IMPORTANT FOR REPORT)

Missing but critical:
- workload / pressure data
- collaboration / network effects
- productivity / output metrics

👉 This explains why:

> The system estimates **value potential**, not actual value.

---

## Final Insight

> Data does not measure value.
> It captures signals that must be interpreted.

The system’s purpose is to:
- structure these signals
- support decisions
- highlight where human judgment is needed