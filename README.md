# 📊 The Human Factor @CACEIS
### Turning people into value — beyond spreadsheets

---

## 💭 Why this project?

In most organizations, people appear in dashboards as costs, headcounts, or scores.

But humans are not static resources.

They are:
- evolving
- learning
- interacting
- burning out
- amplifying each other’s performance

This project explores a simple but powerful idea:
>> Value is not just created by what people do — but by how they behave, adapt, and sustain performance over time.**

---

## 🧠 Our Approach

We designed a bottom-up, human-centered framework to approximate human capital value.

**3-Layer System**

1. Human Signals (Raw Data)
HR, absenteeism, training, performance, and workforce structure

2. Behavioral KPIs (Interpretation Layer)
Proxies capturing:
- engagement
- learning dynamics
- productivity patterns
- early risk signals

3. AI Layer (Structuring Insight)
- employee segmentation
- pattern detection
- decision-support insights

Important principle: **KPIs are not value — they are signals of underlying behaviors.**

---

## 🏗️ Project Structure

caceis-human-capital-pipeline/
│
├── data/
│ ├── raw/ # Original data (not tracked)
│ └── clean/ # Processed datasets
│
├── notebooks/ # Analysis workflow
│ ├── 01_cleaning.ipynb
│ ├── 02_kpis.ipynb
│ ├── 03_eda.ipynb
│ ├── 04_integrated_value_ai.ipynb
│
├── src/ # Core pipeline logic
│ ├── data_cleaning.py
│ ├── kpi_engineering.py
│ ├── 04_integrated_value_ai.py
│
├── dashboard/ # Streamlit app
│ ├── streamlit_app_v1.py
│ └── streamlit_app_v2.py
│
├── outputs/ # Results
│ ├── hr_kpi_table.csv
│ ├── absence_kpi_table.csv
│ ├── training_kpi_table.csv
│ ├── employee_value_table_v2.csv
│ ├── department_value_summary_v2.csv
│ ├── ai_segment_summary_v2.csv
│
├── docs/
│ ├── data_inventory.md
│ ├── technical_note.md
│
├── README.md
└── requirements.txt

---

## 🔄 Data Pipeline

### 1. 🧹 Data Cleaning

* Standardization across datasets
* Missing value handling
* Consistency checks

### 2. 📊 KPI Engineering

We construct behavioral indicators such as:
- Absenteeism Risk Score
- Learning Intensity Score
- Performance Score
- Talent Progression Proxy

These capture **how employees behave**, not just what they produce.

---

### 3. 🔗 Data Integration

All datasets are merged at the employee level.
We introduce:

* `data_coverage_score`
* `kpi_reliability_score`

👉 This step is critical to distinguish:

* true low performance
* vs. missing or unreliable data
---

### 4. 💎 Human Capital Value Proxy

We define a first approximation of value by combining:

* performance
* learning
* progression
* risk (negative contribution)

We also compute a reliability-adjusted value score.

---

### 5. 🤖 AI Segmentation

We apply clustering to group employees into profiles:

* Low Visibility Employees
* High Engagement, High Risk
* High Performers

The goal is not prediction, but **understanding patterns in human behavior.**

---

### 6. 📦 Output

* Integrated employee dataset
* Value proxy scores
* Reliability indicators
* Segment-level summaries
* Dashboard-ready tables

---

## 🌷 Dashboard Experience

The Streamlit dashboard allows:

* Exploration of employee-level signals
* Visualization of KPIs
* Behavioral segmentation
* Identification of risk patterns (e.g. burnout proxies)

Designed to be intuitive, human-centered, and decision-oriented.

---

## 🤖 Role of AI

AI is used to:

* structure complexity
* reveal hidden patterns
* support decision-making

It does **not replace human judgment** — it enhances it.

---

## ⚠️ Limitations

* No direct productivity or financial output data
* Performance data is limited (often one review per employee)
* KPIs remain proxies, not direct measures of value
* Data coverage impacts reliability

---

## 🚀 Target Architecture (Snowflake)

Future scalable system:

HR Systems → Data Warehouse (e.g. Snowflake) → KPI Layer → Value Layer → Dashboard → AI Models

---

## 🌸 Philosophy

We believe:
>> Human capital value is not static. It emerges from behavior, context, and time.

And therefore:
>> The goal is not to measure value perfectly — but to build better systems to understand it.

---

## 👩‍💻 Team

Anna Mika
Nolwenn Montillot
Emma Lou Villaret
Hannah Zilesch

---

## ⚠️ Note

All data used in this project is anonymized or simulated for academic purposes.