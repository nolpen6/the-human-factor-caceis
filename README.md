# 📊 ONEValue @CACEIS
### From KPI Dashboard to Human Capital Value System

---

## 💭 Why this project?

In most organizations, people appear in dashboards as costs, headcounts, or scores.

But humans are not static resources.

They are:
- learn
- adapt
- collaborate
- take decisions
- experience workload and recovery cycles

This project explores a core idea:
>> Value is created through behaviors and decisions — not just outcomes.

---

## 🧠 Our Approach

We move from a KPI dashboard to a value-creation system.

**3-Layer System**

1. Behavioral Layer (NEW CORE)
- decisions taken
- actions performed
- employee inputs
- manager context
- learning loops

2. Indicator Layer (KPIs)
- performance
- absenteeism
- learning
- progression

3. Value Layer (AI & Interpretation)
- segmentation
- pattern detection
- decision-support recommendations

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

---

## 🔵 Blue-Line Valuation Methodology

The latest dashboard version follows the INSEAD Blue-Line logic: **indicators are not value itself**. KPIs are observable signals that help CACEIS learn which human-capital conditions may create, sustain, or destroy long-term value.

This project therefore does **not** calculate the financial value of an individual employee. It estimates **sustainable value potential** from observable, reliability-adjusted indicators.

### Valuation dimensions

| Dimension | Meaning | Current data used |
|---|---|---|
| Contribution Signal | Observable current contribution | Performance score and performance-related fields |
| Learning / Future Value Signal | Future capability development | Training count, training hours, learning intensity |
| Sustainability Signal | Durability of contribution | Absenteeism / continuity risk, inverted so higher is better |
| Progression Signal | Growth and internal development potential | Talent progression proxy where available |
| Interpretation Confidence | How safely the signals can be interpreted | Data coverage and KPI reliability |

### Sustainable Value Potential

The prototype uses a transparent weighted model:

```text
Sustainable Value Potential =
35% Contribution Signal
+ 30% Learning / Future Value Signal
+ 20% Sustainability Signal
+ 15% Progression Signal
```

The model then applies reliability awareness:

```text
Reliability-Adjusted Value Potential =
Sustainable Value Potential × Interpretation Confidence
```

```text
Interpretation Risk =
Sustainable Value Potential × (1 - Interpretation Confidence)
```

A high value potential with weak confidence is therefore **not** treated as a strong conclusion. It becomes a prompt to improve data quality or validate context.

### Valuation archetypes

Instead of ranking employees, the dashboard assigns human-centered archetypes:

- Sustainable Value Builder
- Value Under Pressure
- Strong Contributor / Low Development
- Future Value Builder
- Low Learning Visibility
- Under-Observed Profile
- Stable / Monitor

These archetypes are used to generate **Blue-Line questions** and **recommended experiments**, not automatic decisions.

---

## 🧪 Recommendation and Experiment Engine

The recommendation layer has been upgraded from “recommended actions” to **recommended experiments**.

Each recommendation now includes:

- key signal
- human question
- recommended experiment
- expected signal change
- review period
- decision owner
- governance guardrail

Example:

| Archetype | Blue-Line question | Recommended experiment |
|---|---|---|
| Value Under Pressure | Is current contribution being created sustainably? | Run a workload and recovery review, then test a targeted workload rebalance |
| Strong Contributor / Low Development | Are strong contributors receiving enough future-oriented development? | Offer targeted training, mentoring, or mobility and monitor learning uptake |
| Under-Observed Profile | Do we have enough reliable data to interpret safely? | Validate missing HR, performance, absence, and training records |

This follows the project principle: **the goal is not to manage KPIs directly, but to learn which decisions and working conditions raise sustainable value.**

---

## 🧭 Dashboard V4 Enhancements

The Streamlit dashboard now includes:

- Blue-Line valuation fields
- valuation archetypes
- interpretation confidence
- interpretation risk
- recommended experiments
- AI hypotheses and validation needs
- employee and manager context logs
- HR Blue-Line Valuation tab
- Product Owner Valuation Model Monitoring tab

The dashboard remains role-based:

| Role | Main use |
|---|---|
| Employee | Understand own contribution, learning, sustainability, data visibility, and questions to discuss |
| Manager | Coach teams using signals, context, and experiments |
| HR | Monitor workforce patterns, reliability, sustainability, and governance |
| Product Owner | Monitor model maturity, data quality, outputs, and deployment readiness |

---

## 🌍 Future External Data Enrichment

To strengthen the valuation framework, future versions should integrate external data sources.

| External source | Example use | How it improves valuation |
|---|---|---|
| Market salary benchmarks | Compensation surveys | Contextualizes retention and replacement risk |
| Skill databases | ESCO, O*NET, skills taxonomies | Maps current roles to future skill requirements |
| Labor market demand | Job postings, hiring trends | Identifies scarce or strategically critical roles |
| Sector trends | Financial services workforce trends | Anticipates changing capability needs |
| Training benchmarks | Certification and learning market data | Evaluates whether training investment matches market evolution |
| Regulatory trends | Compliance and financial regulation updates | Anticipates future risk and compliance skill needs |
| Wellbeing benchmarks | Occupational health benchmarks | Contextualizes absence and sustainability signals |
| Technology trends | AI, automation, fund administration tools | Identifies reskilling and automation exposure |

External data would not replace internal HR data. It would contextualize it. For example, a low learning signal is more concerning if the employee’s role is in a fast-changing skill area with strong external labor-market demand.

---

## ✅ Governance Reminder

The platform must not be used for automatic employee ranking, sanctions, or final HR decisions. It is a decision-support and learning system. Every output should be interpreted with:

- data reliability
- employee and manager context
- bias checks
- human review
- GDPR and privacy safeguards
