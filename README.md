# 📊 CACEIS Human Capital Pipeline

## 🎯 Objective

This project transforms raw HR data into meaningful KPIs to support **human capital valuation** at CACEIS.

It combines:
- A **reproducible data pipeline**
- A **KPI framework**
- A **dashboard prototype**
- A **forward-looking AI and data architecture**

---

## 🧠 Concept

We adopt a **bottom-up approach**:

> Employees are not measured as costs —  
> value is created through behaviors, decisions, and interactions.

👉 Therefore:
- KPIs are **not value**
- KPIs are **proxies of underlying value drivers**

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
│ └── 03_eda.ipynb
│
├── src/ # Core pipeline logic
│ ├── data_cleaning.py
│ └── kpi_engineering.py
│
├── dashboard/ # Streamlit app
│ └── streamlit_app.py
│
├── outputs/ # Figures, results
├── docs/ # Technical documentation
│
├── README.md
└── requirements.txt

---

## 🔄 Data Pipeline

### 1. Data Cleaning
- Standardize formats
- Handle missing values
- Remove duplicates

### 2. Data Integration
- Merge datasets using `employee_id`
- Align time dimensions

### 3. KPI Engineering
We compute key indicators:

- Absenteeism Risk Score  
- Learning Intensity Score  
- Performance Consistency Score  
- Engagement Stability Index  
- Talent Progression Proxy  

### 4. Output
- Clean dataset  
- KPI table  
- Dashboard-ready data  

---

## 📊 Dashboard

The Streamlit dashboard allows:
- KPI exploration
- Team comparison
- Filtering by role, department, tenure

---

## 🤖 AI Approach (Next Step)

- Clustering → employee segmentation  
- Regression → performance drivers  
- Classification → risk prediction  

👉 AI is used to identify patterns, not replace human judgment.

---

## ⚠️ Limitations

Current data does not directly capture value creation.

Missing:
- Productivity data  
- Error/risk data  
- Collaboration data  
- Decision-level data  

---

## 🚀 Future Architecture (Snowflake)

Planned scalable architecture: HR Systems → Snowflake → KPI Tables → Dashboard → AI Models

---

## 🔑 Key Takeaway

> We are not building a KPI system.  
> We are designing a system where KPIs are by-products of value creation.

