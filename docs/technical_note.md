# 🧠 Technical Note — Human Capital Valuation Prototype

## 💭 Objective

This document explains how raw HR data is transformed into:

* behavioral KPIs
* an integrated employee dataset
* a human capital value proxy
* AI-based segmentation

---

## 🔄 Pipeline Overview

The system follows a 5-step pipeline:

1. Data cleaning
2. KPI engineering
3. Data integration
4. Value proxy construction
5. AI segmentation

---

## 🧹 1. Data Cleaning

Key steps:

* standardization of identifiers
* missing value handling
* consistency checks across datasets

👉 Goal: ensure datasets can be merged reliably

---

## 📊 2. KPI Engineering

We transform raw variables into interpretable indicators:

| KPI                | Interpretation       |
| ------------------ | -------------------- |
| Performance Score  | Current contribution |
| Learning Intensity | Future capability    |
| Absenteeism Risk   | Sustainability risk  |
| Talent Progression | Growth trajectory    |

👉 Important:

> KPIs are **proxies**, not direct measures of value

---

## 🔗 3. Data Integration

All datasets are merged at the employee level.

We introduce:

* `data_coverage_score` → how complete the data is
* `kpi_reliability_score` → how trustworthy the signals are

👉 This prevents:

* misinterpreting missing data as low performance

---

## 💎 4. Value Proxy Construction

We define a composite score:

Value ≈

* Performance
* Learning
* Talent progression
  − Absenteeism risk

Adjusted by:

* data reliability

👉 This is:

* **not financial value**
* a **decision-support indicator**

---

## 🤖 5. AI Segmentation

We apply clustering to group employees based on KPIs.

### Objective

* identify patterns
* structure decision-making

### Output segments

* Low Information
* Engaged but At Risk
* High Performers

👉 Important:

> Segments are **exploratory**, not prescriptive.

---

## ⚠️ Methodological Limits

* No direct link to financial output
* KPIs rely on imperfect proxies
* clustering depends on data quality
* risk of bias in performance evaluations

---

## 🧠 Design Philosophy

This system follows three principles:

### 1. Interpretability over complexity

Simple, explainable indicators

### 2. Human-centered approach

Focus on behavior, not just metrics

### 3. Decision support, not automation

The model supports discussion — not replaces it

---

## 🧩 Final Insight

> The objective is not to measure human capital perfectly,
> but to build a system that makes **better decisions possible**.
