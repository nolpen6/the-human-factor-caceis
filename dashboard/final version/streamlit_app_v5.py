from pathlib import Path
import html

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

px.defaults.template = "plotly_white"

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ONEValue · CACEIS",
    page_icon="🧭",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — injected once at startup
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..700,0..1,-50..200&display=swap');

/* ── Reset all font feature settings globally to prevent icon code rendering ── */
* {
  font-family: 'DM Sans', system-ui, -apple-system, sans-serif !important;
  font-variant: normal !important;
  font-variant-numeric: normal !important;
  font-variant-ligatures: none !important;
  text-rendering: geometricPrecision !important;
  -webkit-font-smoothing: subpixel-antialiased !important;
}

/* ── Design tokens ── */
:root {
  --bg:          #f0f4f8;
  --surface:     #ffffff;
  --surface-2:   #f8fafc;
  --border:      #e2e8f0;
  --border-2:    #cbd5e1;

  --text:        #0f172a;
  --text-2:      #334155;
  --text-3:      #64748b;
  --text-4:      #94a3b8;

  --primary:     #0d9488;
  --primary-dk:  #0f766e;
  --primary-lt:  #ccfbf1;
  --primary-bg:  #f0fdfa;

  --indigo:      #4f46e5;
  --indigo-lt:   #e0e7ff;

  --success:     #059669;
  --success-lt:  #d1fae5;
  --warn:        #d97706;
  --warn-lt:     #fef3c7;
  --danger:      #dc2626;
  --danger-lt:   #fee2e2;

  --sidebar-bg:  #0f172a;
  --sidebar-2:   #1e293b;

  --radius-sm:   8px;
  --radius:      12px;
  --radius-lg:   16px;
  --shadow-sm:   0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.06);
  --shadow:      0 4px 12px rgba(15,23,42,.10), 0 2px 4px rgba(15,23,42,.06);
  --shadow-lg:   0 10px 30px rgba(15,23,42,.12), 0 4px 8px rgba(15,23,42,.08);

  font-family: 'DM Sans', system-ui, sans-serif;
  color-scheme: light;
}

/* ── Base overrides ── */
.stApp,
section.main,
div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', system-ui, sans-serif !important;
}

h1,h2,h3,h4,h5,h6,p,li,span,label,div {
  color: var(--text) !important;
  font-family: 'DM Sans', system-ui, sans-serif !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  border-right: 1px solid var(--sidebar-2) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f8fafc !important; }
[data-testid="stSidebar"] .stDivider { border-color: var(--sidebar-2) !important; }
/* Sidebar input labels and buttons darker for visibility */
[data-testid="stSidebar"] label { color: #1e293b !important; }

/* Sign out button styling: white with black text normally, navy with white text on hover/active */
[data-testid="stSidebar"] button[data-testid^="stBaseButton"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid rgba(226,232,240,0.6) !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] button[data-testid^="stBaseButton"] * { color: #0f172a !important; }
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:active {
    background-color: #1e3a8a !important;
    color: #ffffff !important;
    border-color: #1e3a8a !important;
}
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover *,
[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:active * { color: #ffffff !important; }

/* Sidebar input placeholder / helper text (inside input) — make noticeably darker */
[data-testid="stSidebar"] input::placeholder,
[data-testid="stSidebar"] input::-webkit-input-placeholder { color: #475569 !important; opacity: 1 !important; }
[data-testid="stSidebar"] input:-ms-input-placeholder { color: #475569 !important; }

/* Sidebar helper small text (external helper) */
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] small * { color: #0f172a !important; }

/* ── Tabs ── */
button[data-baseweb="tab"] {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.88rem !important;
  color: var(--text-3) !important;
  letter-spacing: 0.01em;
  border: 1px solid transparent !important;
  border-radius: 6px !important;
  transition: all 0.2s ease;
  background: transparent !important;
  padding: 0.5rem 1rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
  color: var(--text) !important;
  border: 1px solid var(--border-2) !important;
  background: transparent !important;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-weight: 700 !important;
  font-size: 1.6rem !important;
  font-family: 'DM Mono', monospace !important;
}
[data-testid="stMetricLabel"] {
  color: var(--text-3) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

/* ── Select / multiselect ── */
div[data-baseweb="select"] > div {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-sm) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
}
ul[role="listbox"],div[role="listbox"],div[data-baseweb="popover"] {
  background-color: var(--surface) !important;
}
li[role="option"],div[role="option"] {
  background-color: var(--surface) !important;
  color: var(--text) !important;
}
li[role="option"]:hover,div[role="option"]:hover {
  background-color: var(--primary-bg) !important;
}
input,textarea {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  border-radius: var(--radius-sm) !important;
}

/* ── Plotly charts ── */
div[data-testid="stPlotlyChart"] {
  background-color: var(--surface) !important;
  border-radius: var(--radius) !important;
  border: 1px solid var(--border) !important;
  padding: 0.5rem;
  box-shadow: var(--shadow-sm);
}

/* ── DataFrames ── */
[data-testid="stDataFrame"],[data-testid="stTable"] {
  background-color: var(--surface) !important;
  border-radius: var(--radius) !important;
  border: 1px solid var(--border) !important;
  overflow: hidden;
}

/* ── ─────────────────────────── ── */
/* ── CUSTOM COMPONENTS            ── */
/* ── ─────────────────────────── ── */

/* Stat Card — used in key metrics rows */
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem 1rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  transition: box-shadow .2s, border-color .2s;
      min-height: 160px;
      justify-content: space-between;
}
.stat-card--mid {
    justify-content: flex-start;
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.stat-card--mid .stat-value {
    margin-top: 1.4rem;
}
.stat-card:hover {
  box-shadow: var(--shadow);
  border-color: var(--border-2);
}
.stat-card-accent { border-top: 3px solid var(--primary); }
.stat-card-accent-warn { border-top: 3px solid var(--warn); }
.stat-card-accent-danger { border-top: 3px solid var(--danger); }
.stat-card-accent-indigo { border-top: 3px solid var(--indigo); }

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-3) !important;
  margin: 0;
}
.stat-value {
  font-family: 'DM Mono', monospace;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text) !important;
  line-height: 1.1;
  margin: 0.15rem 0 0;
}
.stat-sub {
  font-size: 0.78rem;
  color: var(--text-4) !important;
  margin: 0;
}

/* Info Card — general content cards */
.info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
  box-shadow: var(--shadow-sm);
      min-height: 160px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
}
.info-card--drilldown {
            min-height: 132px;
            justify-content: flex-start;
            gap: 1.05rem;
            padding-bottom: 0.9rem;
}
.info-card-body {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-2) !important;
    line-height: 1.5;
}
.info-card--drilldown .info-card-body {
    margin-top: 1.15rem;
    flex: 1;
    display: flex;
    align-items: center;
}
.info-card h4 {
  margin: 0 0 0.4rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-2) !important;
  letter-spacing: 0.01em;
}


/* Callout blocks */
.callout {
  border-radius: var(--radius);
  padding: 0.9rem 1.1rem;
  margin: 0.75rem 0;
  font-size: 0.88rem;
  line-height: 1.55;
  display: flex;
  gap: 0.7rem;
  align-items: flex-start;
}
.callout-icon {
  font-size: 1rem;
  flex-shrink: 0;
  margin-top: 0.05rem;
}
.callout-body { flex: 1; }
.callout b { font-weight: 600; }

.callout-info   { background: var(--primary-bg); border-left: 4px solid var(--primary); }
.callout-info * { color: #134e4a !important; }

.callout-gov    { background: #f8fafc; border-left: 4px solid var(--indigo); }
.callout-gov *  { color: #1e1b4b !important; }

.callout-warn   { background: #fffbeb; border-left: 4px solid var(--warn); }
.callout-warn * { color: #78350f !important; }

/* Section headers inside tabs */
.section-header {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border);
}
.section-header h3 {
    margin: 0;
    font-size: 1.35rem;
    line-height: 1.15;
    font-weight: 800;
    color: var(--text) !important;
}
.section-header span {
  font-size: 0.8rem;
  color: var(--text-4) !important;
}

/* ── Signal Progress Cards ── */
.signal-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.15rem 1rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
    min-height: 160px;
    position: relative;
  transition: box-shadow .2s;
}
.signal-card:hover { box-shadow: var(--shadow); }

.signal-card-header{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:.5rem;
}

.signal-card-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-2) !important;
  line-height: 1.35;
  padding-right: 0;
}

.signal-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 999px;
  padding: 0.18rem 0.6rem;
  width: fit-content;
  letter-spacing: 0.02em;
}
.signal-badge-high   { background: var(--success-lt); color: #065f46 !important; }
.signal-badge-medium { background: var(--warn-lt);    color: #78350f !important; }
.signal-badge-low    { background: var(--danger-lt);  color: #7f1d1d !important; }
.signal-badge-na     { background: var(--surface-2);  color: var(--text-4) !important;
                        border: 1px solid var(--border); }

/* Main team profile badge (used in Manager view) */
.team-profile-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--indigo);
    color: #ffffff !important;
    border-radius: 999px;
    padding: 0.45rem 0.9rem;
    font-weight: 800;
    font-size: 0.95rem;
    margin-bottom: 0.8rem;
}

/* Danger variant for high-risk / low-data badges */
.team-profile-badge--danger {
    background: linear-gradient(90deg, #faa2a2, #dc2626);
    color: #fff !important;
}

.signal-track {
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: var(--bg);
  overflow: hidden;
  border: 1px solid var(--border);
}
.signal-fill {
  height: 100%;
  border-radius: 999px;
  transition: width .5s cubic-bezier(.4,0,.2,1);
}
.signal-fill-high   { background: linear-gradient(90deg, #34d399, #059669); }
.signal-fill-medium { background: linear-gradient(90deg, #fbbf24, #d97706); }
.signal-fill-low    { background: linear-gradient(90deg, #f87171, #dc2626); }

.signal-foot {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-3) !important;
  font-weight: 500;
  font-family: 'DM Mono', monospace;
}

/* Explorer summary cards */
.explorer-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.05rem 0.95rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    min-height: 168px;
}
.explorer-card:hover { box-shadow: var(--shadow); }
.explorer-card--selected {
    align-items: center;
    justify-content: center;
    text-align: center;
}
.explorer-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
}
.explorer-card-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-2) !important;
    line-height: 1.35;
}
.explorer-card-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text) !important;
    line-height: 1.05;
}
.explorer-card-value--selected {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 8.5rem;
    padding: 0.55rem 1.2rem;
    border-radius: 999px;
    background: #dbeafe;
    border: 1px solid #93c5fd;
    color: #1d4ed8 !important;
    font-size: 2rem;
    line-height: 1.1;
    letter-spacing: 0.01em;
}
.explorer-card-foot {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: var(--text-3) !important;
    font-weight: 500;
    font-family: 'DM Mono', monospace;
}
.explorer-card-track {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: var(--bg);
    overflow: hidden;
    border: 1px solid var(--border);
}
.explorer-card-fill {
    height: 100%;
    border-radius: 999px;
    transition: width .4s cubic-bezier(.4,0,.2,1);
}
.explorer-card-fill-high { background: linear-gradient(90deg, #34d399, #059669); }
.explorer-card-fill-medium { background: linear-gradient(90deg, #fbbf24, #d97706); }
.explorer-card-fill-low { background: linear-gradient(90deg, #f87171, #dc2626); }

.explorer-card-spacer { margin-bottom: 1.35rem; }

.data-docs-low-card {
    align-items: center;
    justify-content: center;
    text-align: center;
}
.data-docs-low-card-value {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 9rem;
    padding: 0.6rem 1.15rem;
    border-radius: 999px;
    background: #fee2e2;
    border: 2px solid #ef4444;
    color: #b91c1c !important;
    font-family: 'DM Mono', monospace;
    font-size: 2.05rem;
    font-weight: 800;
    line-height: 1.05;
}

/* ── Info icon popover (click to open) ── */
.info-btn-wrap{
  position: relative;
  align-self: flex-start;
}
.info-btn-wrap > details > summary {
  list-style: none;
  marker: none;
  appearance: none;
  -webkit-appearance: none;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #e2e8f0;
  border: 1.5px solid #cbd5e1;
  color: #475569 !important;
  font-weight: 700;
  font-size: 0.82rem;
  line-height: 1;
  user-select: none;
  transition: all 0.2s ease;
  outline: none;
  padding: 0;
}
.info-btn-wrap > details > summary:hover {
  background: #cbd5e1;
  border-color: #94a3b8;
}
.info-btn-wrap > details > summary::-webkit-details-marker { display: none !important; }
.info-btn-wrap > details > summary::marker { display: none !important; }
.info-btn-wrap > details[open] > summary { background: var(--primary-lt); border-color: var(--primary); }
.info-popover-bubble {
  position: absolute;
  top: 1.8rem;
  left: 0;
  right: auto;
  width: min(20rem, calc(100vw - 4rem));
  background: var(--surface);
  border: 1px solid var(--border-2);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  padding: 0.8rem 0.9rem;
  color: var(--text-2) !important;
  font-size: 0.83rem;
  line-height: 1.45;
  z-index: 10;
}
.info-popover-bubble * { color: var(--text-2) !important; }
.info-popover-bubble::before{
  content:"";
  position:absolute;
  top:-6px;
  left:10px;
  width:12px;
  height:12px;
  transform:rotate(45deg);
  background: var(--surface);
  border-left: 1px solid var(--border-2);
  border-top: 1px solid var(--border-2);
}

/* ── "What it means" blue cards ── */
.meaning-card {
  background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%);
  border: 1px solid #a5f3fc;
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
    min-height: 160px;
}
.meaning-card h4 {
  margin: 0;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--primary-dk) !important;
}
.meaning-card p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-2) !important;
  line-height: 1.5;
}

/* ── Score explanation table ── */
.score-table-wrap { width: 100%; overflow-x: auto; }
.score-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  font-size: 0.86rem;
}
.score-table th {
  background: var(--surface-2);
  font-weight: 600;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.7rem 0.9rem;
  border-bottom: 2px solid var(--border);
  text-align: left;
  color: var(--text-2) !important;
    /* allow header text to wrap so columns can size to content */
    white-space: normal;
    word-break: break-word;
}
.score-table td {
  padding: 0.7rem 0.9rem;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  color: var(--text) !important;
  line-height: 1.45;
}
.score-table tr:last-child td { border-bottom: none; }
.score-table tr:hover td { background: var(--surface-2); }

/* Compact table variant for dense layouts (smaller padding, tighter line-height) */
.score-table--compact th { padding: 0.18rem 0.28rem; }
.score-table--compact td { padding: 0.16rem 0.28rem; line-height: 1.02; }
.score-table--explorer th:nth-child(1),
.score-table--explorer td:nth-child(1) { min-width: 9.5rem; }
.score-table--explorer th:nth-child(2),
.score-table--explorer td:nth-child(2) { min-width: 9rem; }
.score-table--explorer th:nth-child(3),
.score-table--explorer td:nth-child(3) { min-width: 12rem; }
.score-table--explorer th:nth-child(4),
.score-table--explorer td:nth-child(4) { min-width: 7rem; }
.score-table--explorer th:nth-child(5),
.score-table--explorer td:nth-child(5) { min-width: 14rem; }
.score-table--explorer th:nth-child(n+6),
.score-table--explorer td:nth-child(n+6) { min-width: 6.5rem; }
.score-table--explorer th:nth-child(12),
.score-table--explorer td:nth-child(12) {
    min-width: 8.5rem;
}
.score-table--explorer th:nth-child(13),
.score-table--explorer td:nth-child(13) {
    min-width: 28rem;
    white-space: normal;
    word-break: normal;
    overflow-wrap: normal;
}
.score-table--explorer td {
    white-space: normal;
    word-break: break-word;
    overflow-wrap: anywhere;
}
.score-table-wrap--explorer {
    max-height: 620px;
    height: 620px;
    overflow-y: auto;
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
}
.score-table-wrap--explorer table {
    width: 100%;
}
.score-table-wrap--drilldown-summary .score-table--explorer th,
.score-table-wrap--drilldown-summary .score-table--explorer td {
    padding: 0.12rem 0.24rem;
    line-height: 1.0;
}
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(1),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(1) { min-width: 8.5rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(2),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(2) { min-width: 8.5rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(3),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(3) { min-width: 11rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(4),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(4) { min-width: 7.5rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(5),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(5) { min-width: 26rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(6),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(6) { min-width: 7rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(7),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(7) { min-width: 7rem; }
.score-table-wrap--drilldown-summary .score-table--explorer th:nth-child(8),
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(8) { min-width: 7rem; }
.score-table-wrap--drilldown-summary .score-table--explorer td:nth-child(5) {
    white-space: normal;
    word-break: normal;
    overflow-wrap: normal;
}
.score-table-wrap--drilldown-summary {
    max-height: 92px;
    height: 92px;
    overflow-y: auto;
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
}
.score-table-wrap--drilldown-summary .score-table--explorer th,
.score-table-wrap--drilldown-summary .score-table--explorer td {
    padding-top: 0.08rem;
    padding-bottom: 0.08rem;
}

/* Valuation explanation table tuning */
.score-table--valuation th {
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    white-space: normal;
    line-height: 1.15;
    word-break: normal;
    overflow-wrap: normal;
    hyphens: none;
}
.score-table--valuation td {
    font-size: 0.82rem;
    line-height: 1.2;
    vertical-align: middle;
}
.score-table--valuation tr td:first-child { min-width: 9rem; }
.score-table--valuation tr td:nth-child(2) { min-width: 10rem; }
.score-table--valuation tr td:nth-child(3) { min-width: 14rem; }
.score-table--valuation tr td:nth-child(4) { min-width: 16rem; }
.score-table--valuation tr th:nth-child(n+5),
.score-table--valuation tr td:nth-child(n+5) {
    min-width: 8.5rem;
}
.score-table--valuation tr td:last-child { min-width: 10rem; }
.score-table-wrap--valuation { max-width: 100%; }

.archetype-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.24rem 0.72rem;
    border-radius: 999px;
    border: 2px solid currentColor;
    font-weight: 700;
    font-size: 0.78rem;
    line-height: 1.1;
    white-space: normal;
    text-align: center;
}

/* ── Page title ── */
.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}
.page-title h1 {
  margin: 0;
  font-size: 1.65rem;
  font-weight: 700;
  color: var(--text) !important;
  letter-spacing: -0.02em;
}

/* Streamlit-generated markdown headings (ensure consistent heading scale) */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text) !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    margin: 0 0 0.35rem 0;
}
.stMarkdown h1 { font-size: 1.65rem !important; }
.stMarkdown h2 { font-size: 1.2rem !important; }
.stMarkdown h3 { font-size: 1.05rem !important; }
.page-badge {
  background: var(--primary-lt);
  color: var(--primary-dk) !important;
  border: 1px solid var(--primary);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

/* ── Role header ── */
.role-header {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.1rem 1.4rem;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
}
.role-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--primary-lt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.role-header-text { flex: 1; }
.role-header-text h3 { margin: 0 0 0.1rem; font-size: 1rem; font-weight: 700; }
.role-header-text p  { margin: 0; font-size: 0.84rem; color: var(--text-3) !important; line-height: 1.45; }

/* ── Login screen ── */
.login-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow-sm);
    min-height: 160px;
    transition: box-shadow .2s, border-color .2s;
}
.login-card:hover { box-shadow: var(--shadow); border-color: var(--primary); }
.login-card h4 {
  margin: 0 0 0.4rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text) !important;
}
.login-card p { margin: 0; font-size: 0.87rem; color: var(--text-3) !important; line-height: 1.5; }

/* ── Priority badge ── */
.priority-high   { color: var(--danger) !important; font-weight: 600; }
.priority-medium { color: var(--warn) !important;   font-weight: 600; }
.priority-low    { color: var(--success) !important; font-weight: 600; }

/* Rounded priority badges used in manager tables */
.priority-badge {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
}
.priority-badge-high {
    background: #fee2e2;
    color: #7f1d1d !important;
    border: 1px solid #fca5a5;
}
.priority-badge-medium {
    background: #fffbeb;
    color: #78350f !important;
    border: 1px solid #fcd34d;
}
.priority-badge-low {
    background: #ecfdf5;
    color: #065f46 !important;
    border: 1px solid #86efac;
}

/* Ring-style priority badges used in coaching questions */
.priority-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.22rem 0.75rem;
    border-radius: 999px;
    border: 2px solid transparent;
    font-weight: 700;
    font-size: 0.85rem;
    background: #ffffff;
    line-height: 1.2;
}
.priority-ring-high {
    border-color: #ef4444;
    color: #991b1b !important;
    background: #fef2f2;
}
.priority-ring-medium {
    border-color: #f59e0b;
    color: #92400e !important;
    background: #fffbeb;
}
.priority-ring-low {
    border-color: #22c55e;
    color: #166534 !important;
    background: #f0fdf4;
}

/* Segment name badges for coaching table */
.segment-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    line-height: 1;
}
.segment-badge--yellow { background: #fffbeb; color: #78350f !important; border: 1px solid #fcd34d; }
.segment-badge--red    { background: #fee2e2; color: #7f1d1d !important; border: 1px solid #fca5a5; }
.segment-badge--blue   { background: #dbeafe; color: #1e3a8a !important; border: 1px solid #93c5fd; }
.segment-badge--purple { background: #ede9fe; color: #5b21b6 !important; border: 1px solid #c4b5fd; }
.segment-badge--green  { background: #dcfce7; color: #166534 !important; border: 1px solid #86efac; }
.segment-badge--neutral { background: #f1f5f9; color: #334155 !important; border: 1px solid #cbd5e1; }

/* Controls above compact tables */
.score-table-controls { margin-bottom: 0.35rem; display:flex; gap:0.5rem; align-items:center; }
.score-table-controls .table-filter-input { padding: 0.35rem 0.5rem; border-radius: 6px; border:1px solid var(--border); font-size:0.9rem; }

/* Employee profile summary ovals */
.profile-oval-badge {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    font-weight: 700;
    font-size: 0.9rem;
    line-height: 1.25;
}
.profile-oval-badge--blue {
    background: #dbeafe;
    color: #1e3a8a !important;
    border: 1px solid #93c5fd;
}
.profile-oval-badge--yellow {
    background: #fef9c3;
    color: #713f12 !important;
    border: 1px solid #fde68a;
}
.profile-oval-badge--red {
    background: #fee2e2;
    color: #7f1d1d !important;
    border: 1px solid #fca5a5;
}

/* Compact variant for profile snapshot badges (avoid full-width stretch) */
.profile-oval-badge--compact {
    display: inline-flex;
    max-width: none;
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
    font-size: 1.05rem;
    padding: 0.5rem 1rem;
}

/* Increase badge size when used inside mid-aligned stat cards in HR view */
.stat-card--mid .profile-oval-badge {
    font-size: 1.35rem;
    padding: 0.6rem 1rem;
}

/* Profile snapshot card: stack at top so we can position the badge mid-card */
.info-card--profile-snapshot {
    justify-content: flex-start;
}
.info-card--profile-snapshot h4 {
    margin-bottom: 1rem;
}
.info-card--profile-snapshot .profile-oval-wrapper {
    margin-top: 0.9rem;
    display: flex;
    align-items: center;
}

/* Team size badge styling */
.team-size-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #dbeafe;
    color: #1e40af !important;
    border: 2px solid #60a5fa !important;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 1.2rem;
}

/* Level pills in score explanation table */
.level-pill {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.8rem;
    font-weight: 700;
    line-height: 1.2;
}
.level-pill-high {
    background: #fee2e2;
    color: #7f1d1d !important;
    border: 1px solid #fca5a5;
}
.level-pill-medium {
    background: #fffbeb;
    color: #78350f !important;
    border: 1px solid #fcd34d;
}
.level-pill-low {
    background: #ecfdf5;
    color: #065f46 !important;
    border: 1px solid #86efac;
}

/* ── Sidebar branding ── */
.sidebar-brand {
  font-size: 1.3rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #f8fafc !important;
}
.sidebar-tagline {
  font-size: 0.78rem;
  color: #64748b !important;
  line-height: 1.5;
  margin-top: 0.2rem;
}
.sidebar-principle {
  font-size: 0.8rem;
  color: #94a3b8 !important;
  line-height: 1.6;
  padding: 0.1rem 0;
}
.sidebar-principle b { color: #e2e8f0 !important; font-weight: 600; }
.sidebar-credit {
    font-size: 0.68rem;
    font-style: italic;
  color: #475569 !important;
  line-height: 1.5;
}

/* Material icon ligatures used by Streamlit controls */
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Outlined' !important;
    font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24 !important;
    font-size: 1.25rem !important;
    line-height: 1 !important;
    color: #e2e8f0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-variant-ligatures: normal !important;
    font-feature-settings: 'liga' 1, 'calt' 1 !important;
    text-rendering: optimizeLegibility !important;
}

/* Sidebar control needs a slightly larger arrow */
[data-testid="stSidebar"] [data-testid="stIconMaterial"],
[data-testid="stBaseButton-headerNoPadding"] [data-testid="stIconMaterial"] {
    font-size: 1.35rem !important;
}

/* Keep ordinary text rendering normal without affecting icons */
body, button, summary, [role="button"], input, select, textarea, div, span, p {
    font-variant-ligatures: none;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[2]
    outputs_dir = project_root / "outputs"
    doc_dir = project_root / "data" / "document_intelligence"

    hr_kpi       = pd.read_csv(outputs_dir / "hr_kpi_table.csv")
    absence_kpi  = pd.read_csv(outputs_dir / "absence_kpi_table.csv")
    training_kpi = pd.read_csv(outputs_dir / "training_kpi_table.csv")
    employee_value = pd.read_csv(outputs_dir / "employee_value_table_v2.csv")

    def _safe_csv(path: Path) -> pd.DataFrame:
        return pd.read_csv(path) if path.exists() else pd.DataFrame()

    return (
        hr_kpi, absence_kpi, training_kpi, employee_value,
        _safe_csv(outputs_dir / "department_value_summary_v2.csv"),
        _safe_csv(outputs_dir / "ai_segment_summary_v2.csv"),
        _safe_csv(doc_dir / "document_theme_summary.csv"),
        _safe_csv(doc_dir / "document_inventory.csv"),
        _safe_csv(outputs_dir / "recommendation_table.csv")
            if (outputs_dir / "recommendation_table.csv").exists()
            and (outputs_dir / "recommendation_table.csv").stat().st_size > 0
            else pd.DataFrame(),
        _safe_csv(outputs_dir / "onevalue_ai_insights.csv")
            if (outputs_dir / "onevalue_ai_insights.csv").exists()
            and (outputs_dir / "onevalue_ai_insights.csv").stat().st_size > 0
            else pd.DataFrame(),
    )


(
    hr_kpi, absence_kpi, training_kpi, employee_value,
    department_summary, segment_summary,
    doc_theme, doc_inventory,
    recommendation_df, onevalue_ai_df,
) = load_data()

# ──────────────────────────────────────────────────────────────────────────────
# BASIC CLEANUP
# ──────────────────────────────────────────────────────────────────────────────
if "segment_name" not in employee_value.columns:
    if "ai_segment_label" in employee_value.columns:
        employee_value["segment_name"] = employee_value["ai_segment_label"]
    elif "ai_segment" in employee_value.columns:
        employee_value["segment_name"] = "AI Segment " + employee_value["ai_segment"].astype(str)
    else:
        employee_value["segment_name"] = "Unclassified"

employee_value["segment_name"] = employee_value["segment_name"].replace({
    "Low Information": "Low Visibility Employees",
    "Engaged but At Risk": "High Engagement / High Risk",
})

DEPT_CANDIDATES = [
    "libelle_organisation_niveau_07", "department", "organisation", "entity"
]
department_col = next(
    (c for c in DEPT_CANDIDATES if c in employee_value.columns), None
)

# Privacy-safe display IDs
employee_value = employee_value.reset_index(drop=True)
employee_value["display_employee"] = [f"Employee P-{i+1:03d}" for i in range(len(employee_value))]


# ──────────────────────────────────────────────────────────────────────────────
# BLUE-LINE VALUATION SIGNALS
# ──────────────────────────────────────────────────────────────────────────────
def _norm(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return pd.Series(0.5, index=s.index)
    lo, hi = s.min(), s.max()
    if pd.isna(lo) or pd.isna(hi) or lo == hi:
        return pd.Series(0.5, index=s.index)
    return ((s - lo) / (hi - lo)).fillna(0.5)


def _col(name: str, fallback: str | None = None) -> pd.Series:
    if name in employee_value.columns:
        return employee_value[name]
    if fallback and fallback in employee_value.columns:
        return employee_value[fallback]
    return pd.Series(0.5, index=employee_value.index)


for dest, src, fb in [
    ("contribution_signal",          "performance_score",          None),
    ("learning_future_value_signal", "learning_intensity_score",   None),
    ("progression_signal",           "talent_progression_proxy",   None),
    ("interpretation_confidence",    "kpi_reliability_score",      None),
]:
    if dest not in employee_value.columns:
        employee_value[dest] = _norm(_col(src, fb))

if "sustainability_signal" not in employee_value.columns:
    employee_value["sustainability_signal"] = 1 - _norm(_col("absenteeism_risk_score"))

if "sustainable_value_potential" not in employee_value.columns:
    employee_value["sustainable_value_potential"] = (
        0.35 * employee_value["contribution_signal"]
      + 0.30 * employee_value["learning_future_value_signal"]
      + 0.20 * employee_value["sustainability_signal"]
      + 0.15 * employee_value["progression_signal"]
    )

if "reliability_adjusted_value_potential" not in employee_value.columns:
    employee_value["reliability_adjusted_value_potential"] = (
        employee_value["sustainable_value_potential"] * employee_value["interpretation_confidence"]
    )

if "interpretation_risk" not in employee_value.columns:
    employee_value["interpretation_risk"] = (
        employee_value["sustainable_value_potential"] * (1 - employee_value["interpretation_confidence"])
    )

if "valuation_archetype" not in employee_value.columns:
    def _archetype(row):
        ic = row.get("interpretation_confidence", 0.5)
        cs = row.get("contribution_signal", 0.5)
        ss = row.get("sustainability_signal", 0.5)
        ls = row.get("learning_future_value_signal", 0.5)
        vp = row.get("sustainable_value_potential", 0.5)
        if ic < 0.4:
            return "Under-Observed Profile"
        if cs >= 0.65 and ss < 0.45:
            return "Value Under Pressure"
        if cs >= 0.65 and ls < 0.4:
            return "Strong Contributor / Low Development"
        if ls >= 0.65 and cs < 0.55:
            return "Future Value Builder"
        if vp >= 0.65 and ss >= 0.55 and ls >= 0.55:
            return "Sustainable Value Builder"
        if ls < 0.4 and cs < 0.55:
            return "Low Learning Visibility"
        return "Stable / Monitor"
    employee_value["valuation_archetype"] = employee_value.apply(_archetype, axis=1)

ARCHETYPE_QUESTIONS = {
    "Under-Observed Profile":                "Do we have enough reliable data to interpret this profile safely?",
    "Value Under Pressure":                  "Is current contribution being created in a sustainable way?",
    "Strong Contributor / Low Development":  "Are strong contributors receiving enough future-oriented development?",
    "Future Value Builder":                  "How can learning investment be converted into measurable contribution?",
    "Sustainable Value Builder":             "What conditions are enabling sustainable value creation here?",
    "Low Learning Visibility":               "Is low learning due to limited access, motivation, or missing data?",
    "Stable / Monitor":                      "What should be monitored to sustain contribution and development over time?",
}
if "blue_line_question" not in employee_value.columns:
    employee_value["blue_line_question"] = (
        employee_value["valuation_archetype"]
        .map(ARCHETYPE_QUESTIONS)
        .fillna("What context should be validated before acting on this signal?")
    )

# Backward-compat aliases
employee_value["human_capital_value_proxy"]    = employee_value.get("human_capital_value_proxy",    employee_value["sustainable_value_potential"])
employee_value["reliability_adjusted_value_proxy"] = employee_value.get("reliability_adjusted_value_proxy", employee_value["reliability_adjusted_value_potential"])

if {"learning_intensity_score", "absenteeism_risk_score"}.issubset(employee_value.columns):
    employee_value["sustainability_balance"] = (
        employee_value["learning_intensity_score"] - employee_value["absenteeism_risk_score"]
    )

if {"human_capital_value_proxy", "kpi_reliability_score"}.issubset(employee_value.columns):
    employee_value["confidence_gap"] = (
        employee_value["human_capital_value_proxy"] * (1 - employee_value["kpi_reliability_score"])
    )

if "absenteeism_risk_score" in employee_value.columns:
    q75 = employee_value["absenteeism_risk_score"].quantile(0.75)
    q40 = employee_value["absenteeism_risk_score"].quantile(0.40)
    employee_value["risk_prediction_label"] = employee_value["absenteeism_risk_score"].apply(
        lambda x: "High" if x >= q75 else ("Medium" if x >= q40 else "Low")
    )
else:
    employee_value["risk_prediction_label"] = "Not available"


def _rec_from_row(row: pd.Series) -> str:
    seg  = row.get("segment_name", "")
    risk = row.get("risk_prediction_label", "")
    low  = bool(row.get("low_data_flag", False))
    bal  = row.get("sustainability_balance", None)
    if low or seg == "Low Visibility Employees":
        return "Improve data completeness before interpreting this profile."
    if risk == "High" or seg == "High Engagement / High Risk":
        return "Review workload, recovery balance, and possible wellbeing support."
    if seg == "High Performers / Low Development":
        return "Protect current contribution while offering targeted development opportunities."
    if bal is not None and pd.notna(bal) and bal < 0:
        return "Investigate whether effort is sustainable and discuss recovery or support needs."
    return "Maintain monitoring and discuss development goals in regular check-ins."

employee_value["recommended_action"] = employee_value.apply(_rec_from_row, axis=1)


# ──────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION TABLE
# ──────────────────────────────────────────────────────────────────────────────
def _build_rec_table(source_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in source_df.iterrows():
        seg  = str(row.get("segment_name", "Unclassified"))
        risk = str(row.get("risk_prediction_label", "Unknown"))
        low  = bool(row.get("low_data_flag", False))
        ab   = row.get("absenteeism_risk_score", None)
        lr   = row.get("learning_intensity_score", None)
        rel  = row.get("kpi_reliability_score", None)
        sus  = (lr - ab) if (pd.notna(lr) and pd.notna(ab)) else None

        if low or seg == "Low Visibility Employees":
            key, rec, pri, tgt, hq = (
                "Low data visibility",
                "Improve data completeness before interpreting this profile.",
                "Medium", "HR / Data AI",
                "Are we missing data, or is this employee outside tracked systems?",
            )
        elif risk == "High" or seg == "High Engagement / High Risk":
            key, rec, pri, tgt, hq = (
                "High continuity risk",
                "Review workload, recovery balance, and wellbeing support.",
                "High", "Manager / HR",
                "Is this a motivated employee or team under unsustainable pressure?",
            )
        elif seg == "High Performers / Low Development":
            key, rec, pri, tgt, hq = (
                "Strong contribution but limited development signal",
                "Offer targeted development opportunities and protect long-term capability.",
                "Medium", "Manager",
                "Are strong performers being stretched without enough future skill investment?",
            )
        elif sus is not None and pd.notna(sus) and sus < 0:
            key, rec, pri, tgt, hq = (
                "Negative sustainability balance",
                "Discuss recovery, workload, and whether current effort is sustainable.",
                "High", "Manager",
                "Is value being created in a way that may not be sustainable over time?",
            )
        elif pd.notna(rel) and rel < 0.5:
            key, rec, pri, tgt, hq = (
                "Low KPI reliability",
                "Validate data sources before using this profile for decisions.",
                "Medium", "HR / Data AI",
                "Can this signal be trusted enough to guide action?",
            )
        elif pd.notna(lr) and lr < 0.3:
            key, rec, pri, tgt, hq = (
                "Low learning intensity",
                "Explore relevant training, mobility, or upskilling opportunities.",
                "Low", "Employee / Manager",
                "What future capability should be developed next?",
            )
        else:
            key, rec, pri, tgt, hq = (
                "Stable profile",
                "Maintain regular development check-ins and continue monitoring signals.",
                "Low", "Employee / Manager",
                "How can current contribution and learning be sustained?",
            )

        rows.append({
            "display_employee":            row.get("display_employee", ""),
            "segment_name":                seg,
            "risk_prediction_label":       risk,
            "absenteeism_risk_score":      ab,
            "learning_intensity_score":    lr,
            "performance_score":           row.get("performance_score", None),
            "kpi_reliability_score":       rel,
            "human_capital_value_proxy":   row.get("human_capital_value_proxy", None),
            "reliability_adjusted_value_proxy": row.get("reliability_adjusted_value_proxy", None),
            "key_signal":                  key,
            "recommendation":              rec,
            "priority_level":              pri,
            "role_target":                 tgt,
            "human_question":              hq,
        })
    return pd.DataFrame(rows)


if recommendation_df.empty:
    recommendation_df = _build_rec_table(employee_value)
else:
    if "display_employee" not in recommendation_df.columns:
        recommendation_df = recommendation_df.reset_index(drop=True)
        recommendation_df["display_employee"] = [
            f"Employee P-{i+1:03d}" for i in range(len(recommendation_df))
        ]
    merge_cols = [
        c for c in ["display_employee", department_col, "segment_name",
                    "risk_prediction_label", "recommended_action"]
        if c and c in employee_value.columns
    ]
    if "display_employee" in merge_cols:
        recommendation_df = recommendation_df.merge(
            employee_value[merge_cols].drop_duplicates("display_employee"),
            on="display_employee", how="left", suffixes=("", "_ev"),
        )
    if "recommendation" not in recommendation_df.columns and "recommended_action" in recommendation_df.columns:
        recommendation_df["recommendation"] = recommendation_df["recommended_action"]
    for col, default in {
        "priority_level": "Low",
        "role_target": "Employee / Manager",
        "key_signal": "Generated recommendation",
        "human_question": "What action would make this signal useful for learning or support?",
        "recommended_experiment":   "Maintain regular check-ins and monitor signal evolution.",
        "expected_signal_change":   "Stable or improved signals over the next review cycle.",
        "review_period":            "1 quarter",
        "decision_owner":           "Employee / Manager",
        "governance_guardrail":     "Use indicators as learning prompts, not rankings.",
    }.items():
        if col not in recommendation_df.columns:
            recommendation_df[col] = default


# ──────────────────────────────────────────────────────────────────────────────
# HELPER UTILITIES
# ──────────────────────────────────────────────────────────────────────────────
def _get(row: pd.Series, *cols, default=None):
    """Return the first non-null value from a list of column names."""
    for c in cols:
        if c in row.index:
            v = row[c]
            if not (isinstance(v, float) and pd.isna(v)):
                return v
    return default


def safe_mean(df: pd.DataFrame, col: str, decimals: int = 3):
    if col in df.columns and len(df) > 0:
        return round(df[col].mean(), decimals)
    return "N/A"


def fmt_score(val) -> str:
    try:
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return "N/A"
        num = float(val)
        pct = round(num * 100.0, 1) if abs(num) <= 1.0 else round(num, 1)
        return f"{pct}%"
    except Exception:
        return str(val)


def score_band(value) -> str:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if pd.isna(v):
        return "N/A"
    if v >= 0.70:
        return "High"
    if v >= 0.40:
        return "Medium"
    return "Low"


VALUATION_ARCHETYPE_COLORS = {
    "Under-Observed Profile": "#fca5a5",
    "Stable / Monitor": "#facc15",
    "Value Under Pressure": "#c4b5fd",
    "Strong Contributor / Low Development": "#99f6e4",
    "Low Learning Visibility": "#fdba74",
    "Sustainable Value Builder": "#22c55e",
    "Future Value Builder": "#3b82f6",
}


def valuation_archetype_fill(color: str) -> str:
    base = color.lstrip("#")
    if len(base) != 6:
        return "#f1f5f9"
    red = int(base[0:2], 16)
    green = int(base[2:4], 16)
    blue = int(base[4:6], 16)
    mix = lambda channel: int(round(channel + (255 - channel) * 0.82))
    return f"#{mix(red):02x}{mix(green):02x}{mix(blue):02x}"


def segment_visual_style(segment_name: str | None) -> tuple[str, str]:
    seg = str(segment_name or "").strip().lower()
    if not seg or seg == "nan":
        return "segment-badge--neutral", "#64748b"
    if any(token in seg for token in ["stable", "baseline"]):
        return "segment-badge--yellow", "#facc15"
    if any(token in seg for token in ["high engagement", "high risk", "risk", "continuity", "pressure", "at risk"]):
        return "segment-badge--red", "#ef4444"
    if any(token in seg for token in ["low visibility", "low information", "under-observed", "visibility"]):
        return "segment-badge--blue", "#3b82f6"
    if any(token in seg for token in ["high performers", "development", "future value", "builder"]):
        return "segment-badge--purple", "#8b5cf6"
    if "sustainable" in seg:
        return "segment-badge--green", "#22c55e"
    return "segment-badge--neutral", "#64748b"


def segment_color_map(values: pd.Series | list) -> dict[str, str]:
    unique_values = pd.Index(values).dropna().astype(str).unique().tolist()
    return {value: segment_visual_style(value)[1] for value in unique_values}


# ──────────────────────────────────────────────────────────────────────────────
# COMPONENT BUILDERS
# ──────────────────────────────────────────────────────────────────────────────

def stat_card(label: str, value, sub: str = "", accent: str = "primary", card_class: str = "", value_html: str | None = None):
    css = {
        "primary": "stat-card-accent",
        "warn":    "stat-card-accent-warn",
        "danger":  "stat-card-accent-danger",
        "indigo":  "stat-card-accent-indigo",
    }.get(accent, "stat-card-accent")
    class_attr = f"stat-card {css}" + (f" {card_class}" if card_class else "")
    value_markup = value_html if value_html is not None else html.escape(str(value))
    st.markdown(f"""
    <div class="{class_attr}">
      <p class="stat-label">{html.escape(str(label))}</p>
      <p class="stat-value">{value_markup}</p>
      {"" if not sub else f'<p class="stat-sub">{html.escape(str(sub))}</p>'}
    </div>""", unsafe_allow_html=True)


def info_card(title: str, body: str, card_class: str = "", body_html: str | None = None):
        class_attr = "info-card" + (f" {card_class}" if card_class else "")
        body_markup = body_html if body_html is not None else html.escape(str(body))
        st.markdown(f"""
        <div class="{class_attr}">
            <h4>{html.escape(str(title))}</h4>
            <div class="info-card-body">{body_markup}</div>
        </div>""", unsafe_allow_html=True)


def profile_snapshot_card(title: str, body: str, color_class: str = "profile-oval-badge--yellow"):
        st.markdown(f"""
        <div class="info-card info-card--profile-snapshot">
            <h4>{html.escape(str(title))}</h4>
            <div class="profile-oval-wrapper">
                <div class="profile-oval-badge {color_class} profile-oval-badge--compact">{html.escape(str(body))}</div>
            </div>
        </div>""", unsafe_allow_html=True)


def callout(body: str, kind: str = "info"):
    icons = {"info": "ℹ️", "gov": "⚖️", "warn": "⚠️"}
    css   = {"info": "callout-info", "gov": "callout-gov", "warn": "callout-warn"}
    st.markdown(f"""
    <div class="callout {css.get(kind,'callout-info')}">
      <span class="callout-icon">{icons.get(kind,'ℹ️')}</span>
      <div class="callout-body">{body}</div>
    </div>""", unsafe_allow_html=True)


def section_header(title: str, sub: str = ""):
    sub_html = f'<span>{html.escape(sub)}</span>' if sub else ""
    st.markdown(f"""
    <div class="section-header">
      <h3>{html.escape(title)}</h3>
      {sub_html}
    </div>""", unsafe_allow_html=True)


def meaning_card(number: str, title: str, body: str):
    st.markdown(f"""
    <div class="meaning-card">
      <h4>{html.escape(number)} · {html.escape(title)}</h4>
      <p>{html.escape(str(body))}</p>
    </div>""", unsafe_allow_html=True)


def _norm_signal(value) -> float | None:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(v):
        return None
    return max(0.0, min(1.0, v))


def signal_progress_card(
    title: str,
    value,
    info_text: str,
    badge_labels: tuple[str, str, str] | None = None,
):
    n = _norm_signal(value)
    pct = 0.0 if n is None else round(n * 100, 1)
    low_label, medium_label, high_label = badge_labels or ("Behind", "Almost There", "On Track")
    if n is None:
        status, css = "No data", "na"
    elif n >= 0.70:
        status, css = high_label, "high"
    elif n >= 0.40:
        status, css = medium_label, "medium"
    else:
        status, css = low_label, "low"

    st.markdown(f"""
    <div class="signal-card">
      <div class="signal-card-header">
        <div class="info-btn-wrap">
          <details>
            <summary aria-label="More info">i</summary>
            <div class="info-popover-bubble">{html.escape(str(info_text))}</div>
          </details>
        </div>
        <span class="signal-badge signal-badge-{css}">{status}</span>
      </div>
      <p class="signal-card-title">{html.escape(str(title))}</p>
      <div class="signal-track">
        <div class="signal-fill signal-fill-{css}" style="width:{pct}%"></div>
      </div>
      <div class="signal-foot">
        <span>{pct}%</span>
        <span>Target 100%</span>
      </div>
    </div>""", unsafe_allow_html=True)


def explorer_progress_card(
        title: str,
        value,
        info_text: str,
        badge_labels: tuple[str, str, str] | None = None,
):
        n = _norm_signal(value)
        pct = 0.0 if n is None else round(n * 100, 1)
        low_label, medium_label, high_label = badge_labels or ("Low", "Medium", "High")
        if n is None:
                status, css = "No data", "low"
                pct = 0.0
        elif n >= 0.70:
                status, css = high_label, "high"
        elif n >= 0.40:
                status, css = medium_label, "medium"
        else:
                status, css = low_label, "low"

        st.markdown(f"""
        <div class="explorer-card">
            <div class="explorer-card-header">
                <div class="info-btn-wrap">
                    <details>
                        <summary aria-label="More info">i</summary>
                        <div class="info-popover-bubble">{html.escape(str(info_text))}</div>
                    </details>
                </div>
                <span class="signal-badge signal-badge-{css}">{status}</span>
            </div>
            <div class="explorer-card-title">{html.escape(str(title))}</div>
            <div class="explorer-card-track">
                <div class="explorer-card-fill explorer-card-fill-{css}" style="width:{pct}%"></div>
            </div>
            <div class="explorer-card-foot">
                <span>{pct}%</span>
                <span>Target 100%</span>
            </div>
        </div>""", unsafe_allow_html=True)


def selected_employees_card(count: int):
        st.markdown(f"""
        <div class="explorer-card explorer-card--selected">
            <div class="explorer-card-title">Selected employees</div>
            <div class="explorer-card-value explorer-card-value--selected">{count:,}</div>
            <div class="explorer-card-foot" style="width:100%; justify-content:center;">
                <span>Filtered in the current view</span>
            </div>
        </div>""", unsafe_allow_html=True)


def low_data_records_card(count: int):
        st.markdown(f"""
        <div class="explorer-card data-docs-low-card">
            <div class="explorer-card-title">Low-data records</div>
            <div class="data-docs-low-card-value">{count:,}</div>
            <div class="explorer-card-foot" style="width:100%; justify-content:center;">
                <span>Records flagged as low visibility</span>
            </div>
        </div>""", unsafe_allow_html=True)


def wrapped_table(df: pd.DataFrame):
    st.markdown(
        '<div class="score-table-wrap">'
        + df.to_html(index=False, escape=True, classes="score-table", border=0)
        + "</div>",
        unsafe_allow_html=True,
    )


def wrapped_table_with_level_pills(df: pd.DataFrame, level_col: str = "Level"):
    if df.empty:
        wrapped_table(df)
        return

    headers = list(df.columns)
    rows_html = []

    for _, row in df.iterrows():
        cells = []
        for h in headers:
            value = row.get(h, "")
            if h == level_col:
                label = str(value)
                css = "level-pill-low"
                if label.lower().startswith("high"):
                    css = "level-pill-high"
                elif label.lower().startswith("medium"):
                    css = "level-pill-medium"
                cells.append(f'<td><span class="level-pill {css}">{html.escape(label)}</span></td>')
            else:
                cells.append(f"<td>{html.escape(str(value))}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table_html = (
        '<div class="score-table-wrap"><table class="score-table">'
        + "<thead><tr>"
        + "".join(f"<th>{html.escape(h)}</th>" for h in headers)
        + "</tr></thead><tbody>"
        + "".join(rows_html)
        + "</tbody></table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def clean_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#0f172a", family="DM Sans, system-ui, sans-serif"),
        title_font=dict(color="#0f172a", size=14, family="DM Sans, system-ui, sans-serif"),
        legend=dict(font=dict(color="#334155")),
        margin=dict(l=40, r=30, t=50, b=40),
    )
    fig.update_xaxes(color="#334155", gridcolor="#f1f5f9", zerolinecolor="#e2e8f0",
                     tickfont=dict(size=11))
    fig.update_yaxes(color="#334155", gridcolor="#f1f5f9", zerolinecolor="#e2e8f0",
                     tickfont=dict(size=11))
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# CONTEXT LOGGING HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def _outputs_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "outputs"


def _classify_theme(text: str) -> str:
    t = str(text).lower()
    if any(w in t for w in ["workload","busy","pressure","stress","overload","capacity"]):
        return "Workload / sustainability"
    if any(w in t for w in ["training","learn","skill","course","upskill","development"]):
        return "Learning / development"
    if any(w in t for w in ["client","report","deadline","quality","error","risk","control"]):
        return "Operational value / risk prevention"
    if any(w in t for w in ["team","help","collabor","manager","colleague"]):
        return "Collaboration / team support"
    if any(w in t for w in ["data","missing","wrong","incorrect","record"]):
        return "Data quality correction"
    return "General context"


def append_log(file_name: str, row: dict):
    d = _outputs_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / file_name
    new_row = pd.DataFrame([row])
    if path.exists() and path.stat().st_size > 0:
        updated = pd.concat([pd.read_csv(path), new_row], ignore_index=True)
    else:
        updated = new_row
    updated.to_csv(path, index=False)
    st.cache_data.clear()


def load_log(file_name: str) -> pd.DataFrame:
    path = _outputs_dir() / file_name
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path)
    return pd.DataFrame()


def show_context_summary(employee_log: pd.DataFrame, manager_log: pd.DataFrame):
    section_header("How human input feeds the value tool")
    callout(
        "<b>Important:</b> comments are converted into themes that help interpret KPI signals with "
        "human context. They are not used to score or punish employees.",
        "gov",
    )
    combined = []
    for df, src in [(employee_log, "Employee input"), (manager_log, "Manager note")]:
        if not df.empty:
            tmp = df.copy(); tmp["source"] = src
            combined.append(tmp)
    if not combined:
        st.info("No human input has been saved yet in this demo session.")
        return
    ctx = pd.concat(combined, ignore_index=True)
    if "theme" in ctx.columns:
        summary = (
            ctx.groupby(["source","theme"], as_index=False)
            .size().rename(columns={"size":"entries"})
            .sort_values("entries", ascending=False)
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
# ANALYTICS HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def derive_value_lens(row: pd.Series) -> str:
    arch = str(row.get("valuation_archetype",""))
    ab   = row.get("absenteeism_risk_score", 0)
    lr   = row.get("learning_future_value_signal", row.get("learning_intensity_score", 0))
    rel  = row.get("interpretation_confidence",    row.get("kpi_reliability_score", 0))
    cs   = row.get("contribution_signal",          row.get("performance_score", 0))
    if pd.notna(rel) and rel < 0.4:
        return "Data reliability / auditability"
    if "Pressure" in arch or (pd.notna(ab) and ab >= 0.7):
        return "Operational continuity and workload sustainability"
    if pd.notna(lr) and lr < 0.35:
        return "Future capability and reskilling"
    if pd.notna(cs) and cs >= 0.65:
        return "Current contribution and knowledge retention"
    return "Standard workforce monitoring"


def show_caceis_value_lens(df: pd.DataFrame, title: str = "CACEIS Value Lens", team_label: str | None = None):
    section_header(title)
    if team_label:
        st.markdown(
            f"<div class='team-profile-badge'>Current team: <strong>{html.escape(str(team_label))}</strong></div>",
            unsafe_allow_html=True,
        )
    if df.empty:
        st.info("No data available.")
        return
    work = df.copy()
    if "caceis_value_lens" not in work.columns:
        work["caceis_value_lens"] = work.apply(derive_value_lens, axis=1)
    lens = (
        work["caceis_value_lens"]
        .value_counts().rename_axis("CACEIS question").reset_index(name="Profiles")
    )
    
    # Sort by Profiles descending for better visual hierarchy
    lens = lens.sort_values("Profiles", ascending=False).reset_index(drop=True)
    total = lens["Profiles"].sum()
    
    # Build HTML for horizontal progress bars
    html_rows = []
    for idx, row in lens.iterrows():
        question = html.escape(str(row["CACEIS question"]))
        count = int(row["Profiles"])
        pct = int(round(100 * count / total)) if total > 0 else 0
        
        bar = f'<div style="margin-bottom: 1.8rem;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;"><div style="font-size: 0.95rem; font-weight: 500; color: var(--text);">{question}</div><div style="font-size: 0.95rem; font-weight: 600; color: var(--text); white-space: nowrap; margin-left: 1rem;">{count} <span style="color: var(--text-3); font-weight: 400;">{pct}%</span></div></div><div style="width: 100%; height: 12px; background: var(--surface-2); border-radius: 999px; overflow: hidden; border: 1px solid var(--border);"><div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #1d4ed8); border-radius: 999px;"></div></div></div>'
        html_rows.append(bar)
    
    html_content = "".join(html_rows)
    html_content += f'<div style="margin-top: 2rem; padding-top: 1rem; border-top: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center;"><div style="font-size: 0.95rem; font-weight: 600; color: var(--text);">Total profiles</div><div style="font-size: 1.1rem; font-weight: 700; color: var(--text);">{total}</div></div>'
    
    st.markdown(html_content, unsafe_allow_html=True)


def show_summary_lens(summary_df: pd.DataFrame, label_col: str, count_col: str, total_label: str = "Total profiles"):
    """Render the same horizontal-lens visual style from a pre-aggregated summary table."""
    if summary_df.empty or label_col not in summary_df.columns or count_col not in summary_df.columns:
        st.info("No data available.")
        return

    lens = summary_df[[label_col, count_col]].copy()
    lens[count_col] = pd.to_numeric(lens[count_col], errors="coerce").fillna(0)
    lens = lens.sort_values(count_col, ascending=False).reset_index(drop=True)
    total = int(lens[count_col].sum())

    html_rows = []
    for _, row in lens.iterrows():
        label = html.escape(str(row[label_col]))
        count = int(row[count_col])
        pct = int(round(100 * count / total)) if total > 0 else 0
        bar = (
            '<div style="margin-bottom: 1.8rem;">'
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">'
            f'<div style="font-size: 0.95rem; font-weight: 500; color: var(--text);">{label}</div>'
            f'<div style="font-size: 0.95rem; font-weight: 600; color: var(--text); white-space: nowrap; margin-left: 1rem;">{count} <span style="color: var(--text-3); font-weight: 400;">{pct}%</span></div>'
            '</div>'
            '<div style="width: 100%; height: 12px; background: var(--surface-2); border-radius: 999px; overflow: hidden; border: 1px solid var(--border);">'
            f'<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #1d4ed8); border-radius: 999px;"></div>'
            '</div>'
            '</div>'
        )
        html_rows.append(bar)

    html_content = "".join(html_rows)
    html_content += (
        '<div style="margin-top: 2rem; padding-top: 1rem; border-top: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center;">'
        f'<div style="font-size: 0.95rem; font-weight: 600; color: var(--text);">{html.escape(total_label)}</div>'
        f'<div style="font-size: 1.1rem; font-weight: 700; color: var(--text);">{total}</div>'
        '</div>'
    )
    st.markdown(html_content, unsafe_allow_html=True)


def usefulness_answer(role: str) -> pd.DataFrame:
    rows = {
        "Employee": [
            ("What does the data say about me?",    "Shows contribution, learning, sustainability, and data-visibility signals."),
            ("What should I discuss with my manager?", "Turns signals into questions about development, workload, and invisible contribution."),
            ("Can I correct missing context?",      "Lets me add context, decisions, expected outcomes, and data-correction notes."),
        ],
        "Manager": [
            ("Who may need support first?",         "Highlights profiles with pressure, low learning visibility, or low data confidence."),
            ("What should I do next?",              "Suggests experiments: workload review, targeted training, or data validation."),
            ("Am I improving team conditions?",     "Tracks sustainability, learning, reliability, and archetype distribution over time."),
        ],
        "HR": [
            ("Where are workforce risks concentrated?", "Aggregates continuity, learning, sustainability, and data quality signals by entity."),
            ("Can we trust the model output?",      "Separates value potential from interpretation confidence; flags weak evidence."),
            ("What policy action is needed?",       "Identifies whether the issue is capability, workload, data quality, or governance."),
        ],
        "Product Owner": [
            ("Is the product ready to deploy?",     "Checks output readiness, model maturity, missing data, and governance controls."),
            ("Is the valuation model responsible?", "Monitors proxy logic, interpretation risk, archetype balance, and limitations."),
            ("What should be built next?",          "Maps gaps to future data sources, validation, and production roadmap."),
        ],
    }
    return pd.DataFrame(rows.get(role, []), columns=["Question", "Dashboard answer"])


# ──────────────────────────────────────────────────────────────────────────────
# EMPLOYEE-SPECIFIC HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def employee_signal_explanation(emp: pd.Series) -> pd.DataFrame:
    def _f(col1, col2=None):
        v = emp.get(col1, emp.get(col2) if col2 else None)
        return fmt_score(v), score_band(v)

    rows = [
        ("Development signal",
         *_f("learning_future_value_signal","learning_intensity_score"),
         "Visible training and development activity. Low can mean informal learning is not recorded — not low talent.",
         "What skill or learning opportunity should I prioritize next?"),
        ("Contribution signal",
         *_f("contribution_signal","performance_score"),
         "A proxy based on available review/performance data. Discuss with concrete examples — reviews can be incomplete or biased.",
         "Which parts of my work create the most value for my team?"),
        ("Sustainability signal",
         *_f("sustainability_signal",),
         "A continuity signal from absence/PTO-risk patterns. Higher = lower observed continuity pressure. Not a wellbeing diagnosis.",
         "Is my current workload sustainable?"),
        ("Absence / continuity risk",
         *_f("absenteeism_risk_score",),
         "Higher means more observed absence/continuity pressure. Needs human context before any interpretation.",
         "Is there context missing behind my absence/PTO pattern?"),
        ("Data visibility",
         *_f("interpretation_confidence","kpi_reliability_score"),
         "How complete the available data is. Low visibility means the dashboard should not be trusted strongly yet.",
         "Are my review, training, or HR records complete?"),
    ]
    return pd.DataFrame(rows, columns=["Signal","Your score","Level","What it means","Good next question"])


def employee_plain_language_summary(emp: pd.Series) -> dict:
    lr   = _get(emp, "learning_future_value_signal", "learning_intensity_score")
    cs   = _get(emp, "contribution_signal", "performance_score")
    ss   = _get(emp, "sustainability_signal")
    rel  = _get(emp, "interpretation_confidence", "kpi_reliability_score")
    ab   = _get(emp, "absenteeism_risk_score")

    lb, cb, sb, rb, abb = (
        score_band(lr), score_band(cs), score_band(ss), score_band(rel), score_band(ab)
    )

    if rb == "Low":
        return {
            "situation": "The dashboard does not have enough reliable data to say much yet.",
            "worry":     "Do not over-interpret these results. The main issue is data completeness, not performance.",
            "next_step": "Check whether training, review, absence/PTO, or HR records are missing or outdated.",
        }
    if abb == "High" or sb == "Low":
        return {
            "situation": "The data suggests possible workload, recovery, or continuity pressure.",
            "worry":     "This is not a judgment. It is worth discussing context before pressure grows into a bigger issue.",
            "next_step": "Prepare a conversation about workload, recovery, priorities, or support needs.",
        }
    if lb == "Low" and cb in ("Medium","High"):
        return {
            "situation": "Visible contribution appears, but recorded development activity is low.",
            "worry":     "Not a problem by itself — the next useful conversation is about future growth.",
            "next_step": "Identify one training, mentoring, mobility, or upskilling opportunity to discuss with your manager.",
        }
    if cb == "Low" and lb in ("Medium","High"):
        return {
            "situation": "Learning activity is visible, but it may not yet appear as contribution in the data.",
            "worry":     "No immediate conclusion should be drawn. The key is connecting learning to concrete work outcomes.",
            "next_step": "Ask how your recent learning can be applied to a project, process, or client deliverable.",
        }
    return {
        "situation": "Your signals look broadly stable based on the available data.",
        "worry":     "No major red flag appears from the current dashboard view.",
        "next_step": "Use your next check-in to confirm priorities, development goals, and any missing context.",
    }


def employee_manager_questions(emp: pd.Series) -> pd.DataFrame:
    lr   = _get(emp, "learning_future_value_signal", "learning_intensity_score")
    cs   = _get(emp, "contribution_signal", "performance_score")
    ss   = _get(emp, "sustainability_signal")
    rel  = _get(emp, "interpretation_confidence", "kpi_reliability_score")
    ab   = _get(emp, "absenteeism_risk_score")
    bal  = _get(emp, "sustainability_balance")
    arch = str(_get(emp, "valuation_archetype", "segment_name", default=""))

    rows = []
    def add(priority, theme, question, why):
        rows.append({"Priority": priority, "Theme": theme,
                     "Question to ask": question, "Why this question appears": why})

    if rel is not None and rel < 0.5:
        add("High","Data quality",
            "Are my review, training, absence/PTO, or HR records complete and up to date?",
            "Your data visibility is low — the dashboard should not be strongly interpreted yet.")
    if lr is not None and lr < 0.3:
        add("High","Development",
            "Which skill, training, mentoring, or mobility opportunity should I prioritize next?",
            "Your visible learning/development signal is low compared with the available scale.")
        add("Medium","Missing context",
            "Is any informal learning, project-based learning, or on-the-job development missing from the data?",
            "Low learning can mean missing records, not low effort or potential.")
    if cs is not None and cs < 0.4:
        add("High","Contribution clarity",
            "What concrete outcomes or responsibilities should I focus on to increase my visible contribution?",
            "Your contribution signal is currently low or unclear in the data.")
    elif cs is not None and cs >= 0.65:
        add("Medium","Contribution leverage",
            "Which parts of my work create the most value for the team, and how can I protect or grow them?",
            "Your contribution signal is strong — the useful question is how to sustain and develop it.")
    if (ab is not None and ab >= 0.6) or (ss is not None and ss < 0.45) or (bal is not None and bal < 0):
        add("High","Workload / sustainability",
            "Is my current workload, recovery rhythm, or prioritisation sustainable for the next review cycle?",
            "Your sustainability or absence/continuity signal suggests this deserves context and discussion.")
    if "Under-Observed" in arch or "Low Visibility" in arch:
        add("High","Visibility",
            "What important work, training, or contribution is not visible in the current dashboard?",
            "Your profile appears under-observed — improving visibility is the first useful step.")
    if "Future Value Builder" in arch:
        add("Medium","Applying learning",
            "How can I apply my learning to a concrete project, process improvement, or client deliverable?",
            "Your learning signal is stronger than your contribution signal — conversion into applied impact is the key topic.")
    if not rows:
        add("Medium","Next growth step",
            "What should be my main development or contribution priority before the next review?",
            "No strong alert appears — the best use is regular development planning.")
        add("Low","Context check",
            "Is there anything important about my work that the dashboard does not capture?",
            "Even stable signals can miss informal work, collaboration, or context.")

    order = {"High":0,"Medium":1,"Low":2}
    return (
        pd.DataFrame(rows)
        .drop_duplicates("Question to ask")
        .sort_values("Priority", key=lambda s: s.map(order).fillna(9))
    )


def build_employee_focus(emp: pd.Series | None) -> str:
    """Safe employee focus text — works whether emp is None or populated."""
    if emp is None:
        return "No profile found. Please check the demo user mapping."
    seg = str(emp.get("segment_name",""))
    risk = str(emp.get("risk_prediction_label",""))
    lr  = emp.get("learning_intensity_score", None)
    rel = emp.get("kpi_reliability_score", None)

    if seg == "High Performers / Low Development":
        return ("You show a strong contribution signal, but visible development activity is limited. "
                "A useful next step is to discuss targeted training, mobility, or upskilling opportunities.")
    if seg == "High Engagement / High Risk" or risk == "High":
        return ("Your profile suggests strong activity combined with possible pressure. "
                "A useful next step is to discuss workload, recovery balance, and support needs with your manager.")
    if seg == "Low Visibility Employees":
        return ("Some parts of your profile are not fully visible in the available data. "
                "A useful next step is to check whether your training, contribution, or recent work is being captured correctly.")
    if pd.notna(lr) and lr < 0.3:
        return ("Your learning signal is currently low. "
                "A useful next step is to identify one relevant training or development opportunity for the next review cycle.")
    if pd.notna(rel) and rel < 0.5:
        return ("Some insights are based on incomplete information. "
                "A useful next step is to review whether your HR, training, and review records are up to date.")
    return ("Your current signals appear stable. "
            "A useful next step is to maintain regular development conversations and define your next growth objective.")


def show_employee_score_dictionary():
    section_header("Score dictionary")
    wrapped_table(pd.DataFrame([
        {"Score": "Development signal",        "Meaning": "Visible training and learning activity.",                          "Important caution": "Low can mean missing or informal learning, not low ability."},
        {"Score": "Contribution signal",       "Meaning": "Available review/performance-related signal.",                    "Important caution": "Reviews can be incomplete or biased; use examples and manager context."},
        {"Score": "Sustainability signal",     "Meaning": "Continuity signal based on absence/PTO-risk patterns.",           "Important caution": "This is not a health, burnout, or wellbeing diagnosis."},
        {"Score": "Learning vs pressure bal.", "Meaning": "Learning intensity minus absenteeism risk.",                       "Important caution": "Positive = learning stronger than risk. Negative = risk stronger than learning."},
        {"Score": "Data visibility",           "Meaning": "How complete the available records are.",                          "Important caution": "Low visibility means do not make strong conclusions."},
    ]))


# ──────────────────────────────────────────────────────────────────────────────
# MANAGER-SPECIFIC HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def manager_team_plain_language_summary(team_df: pd.DataFrame) -> dict:
    if team_df.empty:
        return {
            "situation": "No team data is available.",
            "risk":      "No interpretation is possible.",
            "next_step": "Check the manager-to-department mapping and available data files.",
        }
    def _tmean(col1, col2=None):
        s = team_df.get(col1, team_df.get(col2) if col2 else pd.Series(dtype=float))
        return pd.to_numeric(s, errors="coerce").mean()

    avg_lr   = _tmean("learning_future_value_signal","learning_intensity_score")
    avg_cs   = _tmean("contribution_signal","performance_score")
    avg_ss   = _tmean("sustainability_signal")
    avg_conf = _tmean("interpretation_confidence","kpi_reliability_score")
    high_risk_share = (team_df.get("risk_prediction_label", pd.Series(dtype=str))
                       .astype(str).eq("High").mean()
                       if "risk_prediction_label" in team_df.columns else 0)
    low_data_share  = (pd.to_numeric(team_df.get("low_data_flag",
                       pd.Series(False, index=team_df.index)), errors="coerce")
                       .fillna(0).astype(bool).mean()
                       if "low_data_flag" in team_df.columns else 0)

    if pd.notna(avg_conf) and avg_conf < 0.5:
        return {
            "situation": "Your first management issue is data quality. Team signals are not reliable enough for strong interpretation.",
            "risk":      "Risk of misreading the team because some records are missing or incomplete.",
            "next_step": "Validate HR, training, review, and absence records before drawing conclusions.",
        }
    if high_risk_share >= 0.25 or (pd.notna(avg_ss) and avg_ss < 0.45):
        return {
            "situation": "The team may be delivering under pressure. The main topic is sustainability and continuity.",
            "risk":      "If ignored, this can become absence, disengagement, or loss of knowledge.",
            "next_step": "Review workload distribution, deadlines, recovery capacity, and support needs.",
        }
    if pd.notna(avg_lr) and avg_lr < 0.35 and pd.notna(avg_cs) and avg_cs >= 0.5:
        return {
            "situation": "The team appears to contribute, but visible learning/development activity is low.",
            "risk":      "Future capability could weaken if skills are not refreshed.",
            "next_step": "Identify one training, mentoring, or upskilling priority for the team.",
        }
    if pd.notna(avg_lr) and avg_lr >= 0.6 and pd.notna(avg_cs) and avg_cs < 0.5:
        return {
            "situation": "The team shows learning activity, but it may not yet be converting into visible contribution.",
            "risk":      "Training investment may not translate into operational value unless applied to real work.",
            "next_step": "Connect learning to concrete projects, process improvements, or client deliverables.",
        }
    if low_data_share >= 0.25:
        return {
            "situation": "A significant part of the team is under-observed in the available data.",
            "risk":      "Important work, informal learning, or context may be invisible.",
            "next_step": "Use manager notes and employee context inputs to fill the interpretation gap.",
        }
    return {
        "situation": "Team signals look broadly stable based on the available data.",
        "risk":      "No single major alert dominates the dashboard.",
        "next_step": "Use the dashboard to prepare regular check-ins and monitor changes over time.",
    }


def manager_dynamic_questions(team_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    def add(priority, theme, question, why):
        rows.append({"Priority":priority,"Theme":theme,"Manager question":question,"Why this appears":why})

    if team_df.empty:
        add("High","Data availability","Why is no team data mapped to this manager?","No employee rows found.")
        return pd.DataFrame(rows)

    def _tm(c1,c2=None):
        s = team_df.get(c1, team_df.get(c2) if c2 else pd.Series(dtype=float))
        return pd.to_numeric(s, errors="coerce").mean()

    avg_lr   = _tm("learning_future_value_signal","learning_intensity_score")
    avg_cs   = _tm("contribution_signal","performance_score")
    avg_ss   = _tm("sustainability_signal")
    avg_conf = _tm("interpretation_confidence","kpi_reliability_score")
    avg_bal  = _tm("sustainability_balance")
    high_n   = int(team_df.get("risk_prediction_label",pd.Series(dtype=str)).astype(str).eq("High").sum()) \
               if "risk_prediction_label" in team_df.columns else 0
    low_n    = int(pd.to_numeric(team_df.get("low_data_flag",
                  pd.Series(False,index=team_df.index)),errors="coerce").fillna(0).astype(bool).sum()) \
               if "low_data_flag" in team_df.columns else 0

    if pd.notna(avg_conf) and avg_conf < 0.5:
        add("High","Data reliability","Which team records are missing or unreliable before I act on these signals?","Average interpretation confidence is low.")
    if low_n > 0:
        add("High","Visibility","Which employees or activities are under-observed in the current data?",f"{low_n} team profile(s) have low-data flags.")
    if high_n > 0:
        add("High","Continuity / workload","Which workload, deadline, or recovery factors could explain the high-risk profiles?",f"{high_n} profile(s) show high continuity-risk labels.")
    if pd.notna(avg_ss) and avg_ss < 0.45:
        add("High","Sustainability","Is the team creating value in a way that can be sustained next quarter?","Average sustainability signal is low.")
    if pd.notna(avg_bal) and avg_bal < 0:
        add("High","Learning vs pressure","Is pressure stronger than development investment for this team?","Average learning-vs-pressure balance is negative.")
    if pd.notna(avg_lr) and avg_lr < 0.35:
        add("Medium","Development","Does the team have enough access to training, mentoring, or stretch assignments?","Average future value/development signal is low.")
    if pd.notna(avg_cs) and avg_cs < 0.45:
        add("Medium","Contribution clarity","Are team priorities and expected outcomes clear enough?","Average contribution signal is low or unclear.")
    if pd.notna(avg_lr) and avg_lr >= 0.6 and pd.notna(avg_cs) and avg_cs < 0.5:
        add("Medium","Learning conversion","How can recent learning be converted into concrete process or delivery improvements?","Learning signal is stronger than contribution signal.")
    if "valuation_archetype" in team_df.columns:
        archs = set(team_df["valuation_archetype"].dropna().astype(str))
        if any("Value Under Pressure" in a for a in archs):
            add("High","Value under pressure","Who may be contributing strongly but under unsustainable pressure?","At least one member is classified as Value Under Pressure.")
        if any("Strong Contributor / Low Development" in a for a in archs):
            add("Medium","Future capability","Which strong contributors need targeted development to protect future value?","At least one member has strong contribution but low development signal.")
        if any("Under-Observed" in a for a in archs):
            add("High","Data/context","What context should I add before HR interprets these profiles?","At least one profile is under-observed.")
    if not rows:
        add("Medium","Regular management","What is the team's main development or delivery priority before the next review?","No major alert — use the tool for proactive check-ins.")
        add("Low","Context","What important team work is not captured by the current structured data?","Dashboards can miss informal work, collaboration, and client support.")

    order = {"High":0,"Medium":1,"Low":2}
    return (
        pd.DataFrame(rows).drop_duplicates("Manager question")
        .sort_values("Priority", key=lambda s: s.map(order).fillna(9))
    )


def render_questions_table_with_badges(df: pd.DataFrame, priority_col: str = "Priority", compact: bool = False) -> str:
    if df.empty:
        return "<div class='info-card'><p>No rows.</p></div>"
    headers = list(df.columns)
    rows_html = []
    for _, r in df.iterrows():
        cells = []
        for h in headers:
            v = r.get(h, "")
            if h == priority_col:
                p = str(v)
                cls = "priority-badge-low"
                if p.lower().startswith("high"):
                    cls = "priority-badge-high"
                elif p.lower().startswith("medium"):
                    cls = "priority-badge-medium"
                # escape the label
                cells.append(f"<td><span class=\"priority-badge {cls}\">{html.escape(p)}</span></td>")
            else:
                cells.append(f"<td>{html.escape(str(v))}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table_class = "score-table"
    if compact:
        table_class += " score-table--compact"
    table_html = (
        f"<div class=\"score-table-wrap\"><table class=\"{table_class}\">"
        + "<thead><tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in headers) + "</tr></thead>"
        + "<tbody>" + "".join(rows_html) + "</tbody></table></div>"
    )
    return table_html


def render_coaching_questions_table(
    df: pd.DataFrame,
    priority_col: str = "Priority",
    compact: bool = False,
    percent_cols: list | None = None,
    uppercase_headers: bool = False,
    segment_col: str | None = "segment_name",
    controls: bool = True,
    wrap_class_override: str | None = None,
    wrap_style_override: str | None = None,
) -> str:
    if df.empty:
        return "<div class='info-card'><p>No rows.</p></div>"

    if percent_cols is None:
        percent_cols = [
            "learning_intensity_score",
            "absenteeism_risk_score",
            "sustainability_balance",
            "kpi_reliability_score",
        ]

    headers = list(df.columns)
    rows_html = []

    for _, r in df.iterrows():
        cells = []
        for h in headers:
            v = r.get(h, "")
            # Priority column as ring badge
            if h == priority_col:
                p = str(v)
                cls = "priority-ring-low"
                if p.lower().startswith("high"):
                    cls = "priority-ring-high"
                elif p.lower().startswith("medium"):
                    cls = "priority-ring-medium"
                cells.append(f"<td><span class=\"priority-ring {cls}\">{html.escape(p)}</span></td>")
            else:
                # Segment name -> colored badge
                if segment_col and h == segment_col:
                    seg = str(v) if pd.notna(v) else ""
                    cls, color = segment_visual_style(seg)
                    cells.append(
                        f'<td><span class="segment-badge {cls}" style="color:{color} !important;">{html.escape(seg)}</span></td>'
                    )
                # Format percentage columns
                elif h in percent_cols:
                    try:
                        num = float(v)
                        # scale to percent and show one decimal
                        pct = f"{num*100:.1f} %"
                    except Exception:
                        pct = html.escape(str(v))
                    cells.append(f"<td>{pct}</td>")
                else:
                    cells.append(f"<td>{html.escape(str(v))}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table_class = "score-table"
    if compact:
        table_class += " score-table--compact"
        if not controls:
            table_class += " score-table--explorer"

    # Header labels: replace underscores with spaces to be friendlier
    if uppercase_headers:
        header_html = "".join(f"<th>{html.escape(h.replace('_', ' ').upper())}</th>" for h in headers)
    else:
        header_html = "".join(f"<th>{html.escape(h.replace('_', ' '))}</th>" for h in headers)

    controls_html = ""
    wrap_class = "score-table-wrap"
    if compact and controls:
        controls_html = '<div class="score-table-controls"><input class="table-filter-input" placeholder="Filter rows..." /></div>'
        wrap_class = "score-table-wrap sortable"
    elif compact:
        wrap_class = "score-table-wrap score-table-wrap--explorer"

    if wrap_class_override:
        wrap_class = wrap_class_override

    wrap_style = f' style="{wrap_style_override}"' if wrap_style_override else ""

    table_html = (
        controls_html
        + f"<div class=\"{wrap_class}\"{wrap_style}><table class=\"{table_class}\">"
        + "<thead><tr>" + header_html + "</tr></thead>"
        + "<tbody>" + "".join(rows_html) + "</tbody></table></div>"
    )

    # client-side sorting + filtering for compact tables
    if compact and controls:
        script = r'''
<script>
(function(){
    const wraps = document.querySelectorAll('.score-table-wrap.sortable');
    wraps.forEach(wrap=>{
        const table = wrap.querySelector('table');
        if(!table) return;
        const tbody = table.querySelector('tbody');
        const ths = table.querySelectorAll('th');
        ths.forEach((th, idx)=>{
            th.style.cursor = 'pointer';
            th.addEventListener('click', ()=>{
                const asc = th.dataset.sortOrder !== 'asc';
                th.dataset.sortOrder = asc ? 'asc' : 'desc';
                const rows = Array.from(tbody.querySelectorAll('tr'));
                rows.sort((a,b)=>{
                    const aText = a.children[idx].innerText.trim();
                    const bText = b.children[idx].innerText.trim();
                    const aNum = parseFloat(aText.replace('%',''));
                    const bNum = parseFloat(bText.replace('%',''));
                    if(!isNaN(aNum) && !isNaN(bNum)) return asc ? aNum - bNum : bNum - aNum;
                    return asc ? aText.localeCompare(bText) : bText.localeCompare(aText);
                });
                rows.forEach(r=>tbody.appendChild(r));
            });
        });
        const input = wrap.parentElement.querySelector('.table-filter-input');
        if(input){
            input.addEventListener('input', ()=>{
                const q = input.value.trim().toLowerCase();
                Array.from(tbody.querySelectorAll('tr')).forEach(row=>{
                    const text = row.innerText.toLowerCase();
                    row.style.display = text.includes(q) ? '' : 'none';
                });
            });
        }
    });
})();
</script>
'''
        table_html += script

    return table_html


def render_valuation_explanation_table(
    df: pd.DataFrame,
    archetype_col: str = "valuation_archetype",
    percent_cols: list | None = None,
) -> None:
    if df.empty:
        components.html(
            "<div style='font-family:DM Sans,system-ui,sans-serif;padding:0.75rem;color:#0f172a;'>No rows.</div>",
            height=90,
            scrolling=False,
        )
        return

    if percent_cols is None:
        percent_cols = [
            "contribution_signal",
            "learning_future_value_signal",
            "sustainability_signal",
            "progression_signal",
            "sustainable_value_potential",
            "interpretation_confidence",
            "reliability_adjusted_value_potential",
            "interpretation_risk",
        ]

    headers = list(df.columns)
    header_html = "".join(
        f"<th>{html.escape(h.replace('_', ' ').upper())}</th>" for h in headers
    )
    rows_html = []

    for _, row in df.iterrows():
        cells = []
        for h in headers:
            value = row.get(h, "")
            if h == archetype_col:
                label = str(value) if pd.notna(value) else ""
                color = VALUATION_ARCHETYPE_COLORS.get(label, "#64748b")
                fill = valuation_archetype_fill(color)
                cells.append(
                    f'<td><span class="archetype-pill" style="border-color:{color}; background-color:{fill}; color:{color};">{html.escape(label)}</span></td>'
                )
            elif h in percent_cols:
                try:
                    num = float(value)
                    if pd.isna(num):
                        display = "N/A"
                    else:
                        display = f"{num * 100:.1f} %"
                except Exception:
                    display = html.escape(str(value))
                cells.append(f"<td>{display}</td>")
            else:
                cells.append(f"<td>{html.escape(str(value))}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    frame_height = 760
    html_doc = f"""
    <html>
    <head>
        <style>
            html, body {{ margin: 0; padding: 0; background: transparent; }}
            body {{ font-family: 'DM Sans', system-ui, sans-serif; color: #0f172a; }}
            .frame {{
                height: 640px;
                max-height: 640px;
                overflow-y: auto;
                overflow-x: auto;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                background: #ffffff;
                box-sizing: border-box;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.76rem;
                min-width: 1180px;
                table-layout: fixed;
            }}
            thead th {{
                position: sticky;
                top: 0;
                z-index: 2;
                background: #f8fafc;
                font-size: 0.72rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                padding: 0.5rem 0.55rem;
                border-bottom: 2px solid #e2e8f0;
                text-align: left;
                color: #334155;
                white-space: normal;
                word-break: normal;
                overflow-wrap: normal;
                hyphens: none;
            }}
            tbody td {{
                padding: 0.42rem 0.55rem;
                border-bottom: 1px solid #e2e8f0;
                vertical-align: top;
                line-height: 1.08;
                word-break: break-word;
                overflow-wrap: anywhere;
            }}
            tbody tr:last-child td {{ border-bottom: none; }}
            tbody tr:hover td {{ background: #f8fafc; }}
            thead th:nth-child(1), tbody td:nth-child(1) {{ width: 9.5rem; }}
            thead th:nth-child(2), tbody td:nth-child(2) {{ width: 8.5rem; }}
            thead th:nth-child(3), tbody td:nth-child(3) {{ width: 10.5rem; }}
            thead th:nth-child(4), tbody td:nth-child(4) {{ width: 18rem; }}
            thead th:nth-child(5), tbody td:nth-child(5),
            thead th:nth-child(6), tbody td:nth-child(6),
            thead th:nth-child(7), tbody td:nth-child(7),
            thead th:nth-child(8), tbody td:nth-child(8),
            thead th:nth-child(9), tbody td:nth-child(9),
            thead th:nth-child(10), tbody td:nth-child(10),
            thead th:nth-child(11), tbody td:nth-child(11),
            thead th:nth-child(12), tbody td:nth-child(12) {{ width: 6.9rem; }}
            .archetype-pill {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.18rem 0.55rem;
                border-radius: 999px;
                border: 2px solid currentColor;
                font-weight: 700;
                font-size: 0.72rem;
                line-height: 1.1;
                white-space: normal;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="frame">
            <table>
                <thead><tr>{header_html}</tr></thead>
                <tbody>{''.join(rows_html)}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
    components.html(html_doc, height=frame_height, scrolling=False)
    return


def manager_employee_coaching_questions(emp: pd.Series) -> pd.DataFrame:
    q = employee_manager_questions(emp).copy()
    if q.empty:
        return q
    q = q.rename(columns={"Question to ask":"Coaching question","Why this question appears":"Why this appears"})
    replacements = {
        "Are my":       "Are this employee's",
        "What skill should I":          "What skill should this employee",
        "Which part of my work":        "Which part of this employee's work",
        "Is my":        "Is this employee's",
        "How can I":    "How can this employee",
        "What concrete outcomes or responsibilities should I":
            "What concrete outcomes or responsibilities should this employee",
    }
    for old, new in replacements.items():
        q["Coaching question"] = q["Coaching question"].str.replace(old, new, regex=False)
    return q


def show_manager_score_dictionary():
    section_header("Manager score dictionary")
    wrapped_table(pd.DataFrame([
        {"Score / box":"Team size","What it tells a manager":"How many employees are visible in this manager workspace.","How to use it":"Context only — small teams make averages unstable."},
        {"Score / box":"Avg sustainable value potential","What it tells a manager":"Combined team signal from contribution, learning, sustainability, and progression.","How to use it":"Identify team-level patterns, not individual rankings."},
        {"Score / box":"Avg future value signal","What it tells a manager":"Average visible learning and development activity across the team.","How to use it":"Low values should trigger questions about training access and development planning."},
        {"Score / box":"Avg interpretation confidence","What it tells a manager":"How complete/reliable the available team data is.","How to use it":"If low, validate data before acting on the signals."},
        {"Score / box":"High continuity-risk profiles","What it tells a manager":"Number of team members with elevated absence/continuity risk labels.","How to use it":"Start workload, recovery, or context conversations. Not a blame tool."},
        {"Score / box":"Learning vs pressure balance","What it tells a manager":"Learning intensity minus absenteeism risk.","How to use it":"Negative values suggest pressure/risk is stronger than visible development."},
    ]))


# ──────────────────────────────────────────────────────────────────────────────
# DOCUMENT INTELLIGENCE  (shared between HR and Product Owner views)
# ──────────────────────────────────────────────────────────────────────────────
def show_document_intelligence():
    section_header("Document Intelligence",
                   "Unstructured documents → structured context signals")
    callout(
        "<b>How to read this:</b> document themes are contextual evidence, not direct measures. "
        "They help interpret why certain structured signals may appear — e.g. wellbeing language "
        "supporting an absenteeism-risk interpretation.",
        "info",
    )
    st.markdown(
        "Qualitative material (engagement, governance, social, inclusion reports) is "
        "connected to the quantitative KPI system through theme extraction."
    )
    if doc_inventory.empty and doc_theme.empty:
        st.warning("Document intelligence outputs not found. "
                   "Run `python src/document_theme_extraction.py` first.")
        return

    if not doc_inventory.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Documents processed", f"{len(doc_inventory):,}")
        c2.metric("File types",    f"{doc_inventory['file_type'].nunique():,}" if "file_type" in doc_inventory.columns else "N/A")
        c3.metric("Source folders",f"{doc_inventory['folder'].nunique():,}"    if "folder"    in doc_inventory.columns else "N/A")

    if not doc_theme.empty:
        section_header("Top organisational themes")
        top = (
            doc_theme.groupby("theme", as_index=False)["keyword_count"]
            .sum().sort_values("keyword_count", ascending=False)
        )
        fig = px.bar(top, x="theme", y="keyword_count",
                     title="Theme intensity across unstructured documents",
                     labels={"theme":"Theme","keyword_count":"Keyword mentions"})
        fig.update_xaxes(tickfont=dict(weight="bold"))
        fig.update_traces(textposition="outside", texttemplate="%{y}")
        st.plotly_chart(clean_chart(fig), use_container_width=True)
        
        section_header("Detected themes by document")
        doc_theme_display = doc_theme.copy()
        doc_theme_display.columns = [col.replace('_', ' ').upper() for col in doc_theme_display.columns]
        st.dataframe(doc_theme_display, use_container_width=True)
    
    if not doc_inventory.empty:
        with st.expander("📂 Document inventory"):
            st.dataframe(doc_inventory, use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-brand">🧭 ONEValue</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-tagline">Human capital intelligence platform for CACEIS — '
        'connecting people signals to sustainable value creation.</p>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("**Platform principles**")
    for principle in [
        "1. Start with signals, not conclusions",
        "2. Interpret value through context, not scores",
        "3. Focus on decisions and behaviours",
        "4. Use AI to find patterns, not judge people",
        "5. Always validate signals before acting",
    ]:
        st.markdown(f'<p class="sidebar-principle">{principle}</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**Access**")


# ──────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">
  <h1>ONEValue</h1>
  <span class="page-badge">CACEIS · Prototype</span>
</div>""", unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subcaption">A human capital intelligence platform inspired by the ONE CACEIS culture: Care, Growth, Responsibility, and Learning.</p>',
    unsafe_allow_html=True,
)

st.caption(
        "Built by Anna Mika, Nolwenn Montillot, Emma Lou Villaret &amp; Hannah Zilesch · CACEIS × Albert School Alberthon"
    )

_emp_demos = (
    employee_value.sort_values(
        by=["data_coverage_score","kpi_reliability_score"], ascending=False
    ).head(2)["display_employee"].tolist()
    if {"data_coverage_score","kpi_reliability_score","display_employee"}.issubset(employee_value.columns)
    else employee_value["display_employee"].head(2).tolist()
)
_mgr_depts = (
    employee_value.groupby(department_col).size()
    .sort_values(ascending=False).head(2).index.tolist()
    if department_col else []
)

USERS = {
    "emp_001":   {"role":"Employee",      "id":   _emp_demos[0] if _emp_demos else "Employee P-001"},
    "emp_002":   {"role":"Employee",      "id":   _emp_demos[1] if len(_emp_demos)>1 else "Employee P-002"},
    "mgr_001":   {"role":"Manager",       "department": _mgr_depts[0] if _mgr_depts else None},
    "mgr_002":   {"role":"Manager",       "department": _mgr_depts[1] if len(_mgr_depts)>1 else None},
    "hr_001":    {"role":"HR"},
    "admin_001": {"role":"Product Owner"},
}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user:
    current_login = st.session_state.logged_in_user
    current_user  = USERS[current_login]
    st.sidebar.success(f"Signed in · {current_login} ({current_user['role']})")
    if st.sidebar.button("Sign out"):
        st.session_state.logged_in_user = None
        st.rerun()
    user = USERS[st.session_state.logged_in_user]
    role = user["role"]

    # Role header banner
    avatars = {"Employee":"👤","Manager":"🧑‍💼","HR":"🏢","Product Owner":"🔧"}
    role_descriptions = {
        "Employee":     "Track your development, review signals, training visibility, and value contribution.",
        "Manager":      "Support your team, identify coaching needs, and understand value creation patterns.",
        "HR":           "Monitor workforce patterns, data quality, AI segments, and strategic recommendations.",
        "Product Owner":"Oversee pipeline health, model behaviour, recommendation quality, and deployment readiness.",
    }
    st.markdown(f"""
    <div class="role-header">
      <div class="role-avatar">{avatars.get(role,'👤')}</div>
      <div class="role-header-text">
        <h3>Hello, {user.get('id', user.get('department', role))} &nbsp;·&nbsp; {role}</h3>
        <p>{role_descriptions.get(role,'Welcome.')}</p>
      </div>
    </div>""", unsafe_allow_html=True)


else:
    # ── Login page ────────────────────────────────────────────────────────────
    login_input = st.sidebar.text_input("Enter demo login ID", key="login_input")
    if login_input in USERS:
        st.session_state.logged_in_user = login_input
        st.rerun()

    callout(
        "<b>Welcome.</b> The platform adapts to your role: employees track development, "
        "managers act on team signals, HR analyses workforce patterns, and product owners "
        "oversee system performance.",
        "info",
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        meaning_card("1", "From behaviour to value",
                     "Captures employee actions, learning, and signals to understand how value is created over time.")
    with col_b:
        meaning_card("2", "Signals, not scores",
                     "KPIs are indicators, not truth. They identify patterns, risks, and opportunities — not rank individuals.")
    with col_c:
        meaning_card("3", "Decision support system",
                     "AI highlights segments, risks, and recommendations so managers and HR can act earlier and more effectively.")

    st.markdown("")
    section_header("Demo login IDs")
    c1, c2, c3, _ = st.columns([1,1,1,3])
    with c1:
        st.markdown("**Employees**\n\n`emp_001`\n\n`emp_002`")
    with c2:
        st.markdown("**Managers**\n\n`mgr_001`\n\n`mgr_002`")
    with c3:
        st.markdown("**Other roles**\n\n`hr_001`\n\n`admin_001`")

    callout(
        "<b>Access control:</b> users only see data required for their role. "
        "Production systems would enforce this through secure authentication.",
        "gov",
    )
    st.stop()


# ════════════════════════════════════════════════════════════════════════════════
# EMPLOYEE VIEW
# ════════════════════════════════════════════════════════════════════════════════
if role == "Employee":
    selected_employee = user["id"]
    _match = employee_value[employee_value["display_employee"] == selected_employee]
    emp = _match.iloc[0] if not _match.empty else None

    # BUG FIX: build focus text once, before any tabs reference it
    employee_focus = build_employee_focus(emp)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["My Situation", "My Next Steps", "Add Context", "Help & FAQ"]
    )

    # ── TAB 1 : My Situation ─────────────────────────────────────────────────
    with tab1:
        section_header("My Situation",
            "Scores are conversation prompts, not judgments.")

        if emp is None:
            st.warning(f"No profile found for {selected_employee}. Check the demo user mapping.")
        else:
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                signal_progress_card(
                    "My development signal",
                    _get(emp,"learning_future_value_signal","learning_intensity_score"),
                    "Visible training and development activity in the data. Low can mean formal "
                    "training is low, informal learning is not recorded, or data is incomplete — "
                    "not a measure of talent.",
                )
            with c2:
                signal_progress_card(
                    "My contribution signal",
                    _get(emp,"contribution_signal","performance_score"),
                    "A proxy based mainly on available annual review/performance information. "
                    "Discuss with concrete examples — reviews can be subjective, incomplete, or biased.",
                )
            with c3:
                signal_progress_card(
                    "My sustainability signal",
                    _get(emp,"sustainability_signal"),
                    "A continuity signal based on absence/PTO-risk patterns. Higher = lower observed "
                    "continuity pressure. Not a health, burnout, or wellbeing diagnosis.",
                )
            with c4:
                signal_progress_card(
                    "My data visibility",
                    _get(emp,"interpretation_confidence","kpi_reliability_score"),
                    "How complete and reliable your available records are. If low, the dashboard "
                    "should not be used to make strong conclusions about you.",
                )

            st.markdown("<br>", unsafe_allow_html=True)
            summary = employee_plain_language_summary(emp)
            section_header("What this means")
            m1,m2,m3 = st.columns(3)
            with m1: meaning_card("1","Current situation", summary["situation"])
            with m2: meaning_card("2","Should I worry?",   summary["worry"])
            with m3: meaning_card("3","Recommended next step", summary["next_step"])

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📖 See exactly what each score means", expanded=True):
                wrapped_table_with_level_pills(employee_signal_explanation(emp), level_col="Level")

            section_header("My profile summary")
            p1,p2,p3 = st.columns(3)
            with p1:
                                team_label = str(emp.get(department_col,"Not available")) if department_col else "Not available"
                                st.markdown(f"""
                                <div class="info-card info-card--profile-snapshot">
                                    <h4>My team / entity</h4>
                                    <div class="profile-oval-wrapper"><div class="profile-oval-badge profile-oval-badge--blue profile-oval-badge--compact">{html.escape(team_label)}</div></div>
                                </div>
                                """, unsafe_allow_html=True)
            with p2:
                                current_label = str(emp.get("valuation_archetype","N/A"))
                                st.markdown(f"""
                                <div class="info-card info-card--profile-snapshot">
                                    <h4>Current situation label</h4>
                                    <div class="profile-oval-wrapper"><div class="profile-oval-badge profile-oval-badge--yellow profile-oval-badge--compact">{html.escape(current_label)}</div></div>
                                </div>
                                """, unsafe_allow_html=True)
            with p3:
                info_card("Question to discuss",
                    str(emp.get("blue_line_question","N/A")))

            section_header("Value signals overview")
            v1,v2,v3 = st.columns(3)
            with v1:
                signal_progress_card(
                    "Overall signal",
                    _get(emp,"sustainable_value_potential"),
                    "Combined contribution, learning, sustainability, and progression signals.",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )
            with v2:
                signal_progress_card(
                    "Confidence-adjusted signal",
                    _get(emp,"reliability_adjusted_value_potential"),
                    "Overall signal adjusted downward when data visibility is incomplete.",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )
            with v3:
                bal = _get(emp,"sustainability_balance")
                bal_norm = None if bal is None else max(0.0, min(1.0, (bal + 1) / 2))
                signal_progress_card(
                    "Learning vs pressure balance",
                    bal_norm,
                    "Scaled view of learning intensity minus absenteeism risk. Positive balance indicates learning is stronger than pressure.",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )

            st.info(employee_focus)

            callout(
                "<b>Your data rights:</b> this workspace uses your personal HR, training, review, and "
                "absence/PTO data to provide development-oriented insights. These insights are provided "
                "for transparency and development support. They are not used for automatic evaluation, "
                "ranking, or disciplinary decisions. See the employee data policy below.",
                "gov",
            )
            with st.expander("📋 View employee data policy and consent framework"):
                st.markdown("""
**1. Purpose of data use**
This workspace uses HR, training, annual review, and absence/PTO data to support employee development, workforce planning, and organisational learning.

**2. Employee transparency**
Employees can view the signals derived from their own data. These signals are designed to support understanding, not to define individual worth.

**3. Responsible use**
Data and AI outputs must not be used for automatic performance evaluation, employee ranking, or disciplinary action without human review.

**4. Data reliability and limitations**
Indicators depend on data completeness and quality. Missing, outdated, or biased data may affect interpretation.

**5. Consent and governance**
In a production system, employees would be informed of data usage policies, consent mechanisms, and internal HR governance rules. Processing follows GDPR principles and company data policies.

**6. Human-in-the-loop principle**
Managers and HR remain responsible for all decisions. AI-generated signals are decision-support prompts, not final judgments.

---
*Prototype policy notice for demonstration purposes.*
""")

    # ── TAB 2 : My Next Steps ────────────────────────────────────────────────
    with tab2:
        section_header("My Next Steps",
            "Employee-specific scores + a reusable action plan")

        if emp is not None:
            with st.expander("ℹ️ Which parts are employee-specific?", expanded=False):
                st.markdown(
                    "**Employee-specific:** numeric scores, current situation, recommended next step, data visibility, and saved context.  \n"
                    "**General guidance:** the checklist and example questions are reusable prompts for a review conversation."
                )

            d1,d2,d3 = st.columns(3)
            with d1:
                signal_progress_card(
                    "Development signal",
                    _get(emp,"learning_intensity_score"),
                    "Visible formal learning and training activity. Lower values can indicate missing records or low development opportunity.",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )
            with d2:
                signal_progress_card(
                    "Annual review signal",
                    _get(emp,"performance_score"),
                    "Proxy from review/performance records. Use examples in conversations to contextualize.",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )
            with d3:
                bal = _get(emp,"sustainability_balance")
                bal_norm = None if bal is None else max(0.0, min(1.0, (bal + 1) / 2))
                signal_progress_card(
                    "Learning vs pressure balance",
                    bal_norm,
                    "Negative = continuity pressure stronger than visible learning",
                    badge_labels=("Low performance", "Stable", "Great performance"),
                )

            callout(
                "<b>Sustainability balance formula:</b> learning intensity score − absenteeism risk score. "
                "A negative value means observed pressure is higher than visible learning activity. "
                "Not a health diagnosis — always discuss with context.",
                "gov",
            )

            section_header("Recommended next step")
            st.info(employee_focus)

            section_header("Suggested action plan")
            wrapped_table(pd.DataFrame([
                {"Step":"1. Validate my data",         "Why it matters":"Make sure training, annual review, and absence/PTO records reflect reality.",      "Suggested action":"Check whether anything important is missing or outdated."},
                {"Step":"2. Prepare my review",         "Why it matters":"Annual review signals need context, examples, and discussion.",                   "Suggested action":"List concrete achievements, skills developed, and contribution examples."},
                {"Step":"3. Choose one development priority","Why it matters":"Value grows through learning, not only current performance.",                "Suggested action":"Select one training, mentoring, mobility, or upskilling opportunity."},
                {"Step":"4. Discuss sustainability",   "Why it matters":"Sustained value depends on workload, recovery, and long-term engagement.",         "Suggested action":"Raise workload or support needs if the current pace is difficult to maintain."},
            ]))

            section_header("Questions for my manager",
                "Generated from this employee's actual signals")
            qdf = employee_manager_questions(emp)
            wrapped_table_with_level_pills(qdf, level_col="Priority")

            callout(
                "<b>Your development drives value:</b> value is not only performance — it comes from "
                "learning, contribution, and sustainability over time. Use this view to shape your next step.",
                "gov",
            )
        else:
            st.warning("No employee profile found.")

    # ── TAB 3 : Add Context ──────────────────────────────────────────────────
    with tab3:
        section_header("Add Context to My Profile",
            "Missing information, workload notes, data corrections, and questions for HR/manager")

        if emp is None:
            st.warning("No employee profile found — inputs cannot be linked safely.")
        else:
            with st.form("employee_context_form"):
                input_type = st.selectbox("What type of input is this?", [
                    "Question for manager/HR",
                    "Workload or capacity context",
                    "Decision or action I took",
                    "Learning or development need",
                    "Process improvement idea",
                    "Data correction",
                    "Recognition / invisible contribution",
                ])
                employee_comment = st.text_area(
                    "What do you want to add?",
                    placeholder="Example: I supported an urgent client reporting task while two colleagues were absent.",
                )
                decision_taken = st.text_area(
                    "Optional: what decision/action did you take?",
                    placeholder="Example: I prioritised client reporting before internal admin tasks.",
                )
                expected_outcome = st.text_area(
                    "Optional: what did you expect would happen?",
                    placeholder="Example: The report would be delivered on time with fewer client escalations.",
                )
                actual_outcome = st.text_area(
                    "Optional: what actually happened?",
                    placeholder="Example: The report was delivered on time, but my workload increased.",
                )
                submitted = st.form_submit_button("💾 Save my input")

            if submitted:
                full_text = " ".join([employee_comment, decision_taken, expected_outcome, actual_outcome])
                if not full_text.strip():
                    st.warning("Please write at least one comment before saving.")
                else:
                    append_log("employee_context_log.csv", {
                        "date":             pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "display_employee": selected_employee,
                        "department":       str(emp.get(department_col,"Not available")) if department_col else "Not available",
                        "input_type":       input_type,
                        "employee_comment": employee_comment,
                        "decision_taken":   decision_taken,
                        "expected_outcome": expected_outcome,
                        "actual_outcome":   actual_outcome,
                        "theme":            _classify_theme(full_text),
                        "status":           "Submitted",
                    })
                    st.success("✅ Input saved. In V4, this becomes contextual evidence for learning and support.")

            emp_log  = load_log("employee_context_log.csv")
            my_log   = (emp_log[emp_log["display_employee"] == selected_employee]
                        if not emp_log.empty and "display_employee" in emp_log.columns
                        else pd.DataFrame())

            section_header("My saved inputs")
            if my_log.empty:
                st.info("No saved inputs yet for this employee.")
            else:
                st.dataframe(my_log.sort_values("date", ascending=False),
                             use_container_width=True, hide_index=True)
            show_context_summary(my_log, pd.DataFrame())

    # ── TAB 4 : Help & FAQ ───────────────────────────────────────────────────
    with tab4:
        section_header("Help & FAQ",
            "A short guide for using the employee dashboard without over-reading the numbers.")

        faq_items = [
            ("What is the point of this tool for me?",
             "It helps you prepare better conversations: what development to ask for, whether your data is complete, what context is missing, and whether workload or recovery should be discussed."),
            ("Are these scores my evaluation?",
             "No. They are prototype signals from available HR, training, review, and absence/PTO data. They should start a conversation, not replace one."),
            ("What should I look at first?",
             "Start with the plain-language boxes under 'What this means'. Then check data visibility. Only then look at individual scores."),
            ("What does a low development signal mean?",
             "It means little formal learning is visible in the available data. It could also mean informal learning is missing from records, so you should add context or ask about training options."),
            ("What does sustainability mean here?",
             "It is a continuity/workload proxy, not a health diagnosis. The balance shown is learning intensity minus absence/continuity risk."),
            ("When should I use Add Context?",
             "Use it when the dashboard misses something important: invisible work, informal training, workload pressure, data errors, or a question for HR/manager."),
        ]
        for question, answer in faq_items:
            with st.expander(f"ℹ️ {question}"):
                st.markdown(answer)

        show_employee_score_dictionary()
        callout(
            "<b>Best use:</b> treat this as a preparation tool for a check-in — "
            "what is accurate, what is missing, and what should I develop next?",
            "gov",
        )


# ════════════════════════════════════════════════════════════════════════════════
# MANAGER VIEW
# ════════════════════════════════════════════════════════════════════════════════
elif role == "Manager":
    if not department_col:
        st.error("No department column detected. Manager access cannot be safely simulated.")
        st.stop()

    selected_department = user["department"]
    team = employee_value[employee_value[department_col] == selected_department].copy()

    if team.empty:
        st.warning(
            f"No employees found for department: **{selected_department}**. "
            "Check the demo user mapping or department names in the data."
        )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Team Dashboard",
        "Employee Drill-Down",
        "Team Signals",
        "Manager Notes",
        "Action Plan",
        "Help & FAQ",
    ])

    # ── TAB 1 ─────────────────────────────────────────────────────────────────
    with tab1:
        callout(
            "<b>How to use this view:</b> read team signals as prompts for support and development. "
            "They are not a ranking of employees or a substitute for manager judgment.",
            "gov",
        )
        with st.expander("What does this help me answer ?", expanded=False):
            st.dataframe(usefulness_answer("Manager"), use_container_width=True, hide_index=True)

        team_summary = manager_team_plain_language_summary(team)
        section_header("Manager interpretation")
        if selected_department:
            st.markdown(
                f"<div class='team-profile-badge'>Current team: <strong>{html.escape(str(selected_department))}</strong></div>",
                unsafe_allow_html=True,
            )
        m1,m2,m3 = st.columns(3)
        with m1:
            meaning_card("1","What the dashboard sees", team_summary["situation"])
        with m2:
            meaning_card("2","Main management risk",    team_summary["risk"])
        with m3:
            meaning_card("3","Recommended next step",  team_summary["next_step"])

        show_caceis_value_lens(team, "Team CACEIS value lens")

        section_header("Team-level questions to investigate")
        dq = manager_dynamic_questions(team)
        st.markdown(render_questions_table_with_badges(dq, priority_col="Priority"), unsafe_allow_html=True)

        section_header("Key team metrics")
        st.markdown(f"<div class='team-size-badge'>Team size: <strong>{len(team):,}</strong></div>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            signal_progress_card(
                "Avg contribution signal",
                safe_mean(team, "contribution_signal"),
                "Average observable contribution signal across the team. This is a proxy from available performance information, not a ranking or performance score.",
                badge_labels=("Low performance", "Stable", "Great performance"),
            )
        with c2:
            signal_progress_card(
                "Avg future value signal",
                safe_mean(team, "learning_future_value_signal"),
                "Average visible learning and development activity across the team. Low values can reflect missing records, limited access, or lower observed activity.",
                badge_labels=("Low performance", "Stable", "Great performance"),
            )
        with c3:
            signal_progress_card(
                "Avg sustainability signal",
                safe_mean(team, "sustainability_signal"),
                "Average continuity and workload balance signal for the team. Higher values indicate lower observed pressure, not a wellbeing diagnosis.",
                badge_labels=("Low performance", "Stable", "Great performance"),
            )
        with c4:
            signal_progress_card(
                "Avg interpretation confidence",
                safe_mean(team, "interpretation_confidence"),
                "Average data completeness and reliability for the team's records. If this is low, treat the signals as tentative and validate the underlying data first.",
                badge_labels=("Low performance", "Stable", "Great performance"),
            )
        st.markdown("<br style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)

        section_header("Team profile snapshot")
        main_seg = (
            team["segment_name"].mode().iloc[0]
            if "segment_name" in team.columns and not team["segment_name"].mode().empty
            else "N/A"
        )
        high_risk = (
            int((team["risk_prediction_label"] == "High").sum())
            if "risk_prediction_label" in team.columns
            else "N/A"
        )
        low_data = (
            int(team["low_data_flag"].sum()) if "low_data_flag" in team.columns else "N/A"
        )

        snap1, snap2, snap3 = st.columns(3)
        with snap1:
            st.markdown(
                f"""
            <div class="info-card info-card--profile-snapshot">
              <h4>Main team profile</h4>
              <div class="profile-oval-wrapper"><div class="profile-oval-badge profile-oval-badge--yellow profile-oval-badge--compact">{html.escape(str(main_seg))}</div></div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with snap2:
            st.markdown(
                f"""
            <div class="info-card info-card--profile-snapshot">
              <h4>High continuity-risk profiles</h4>
              <div class="profile-oval-wrapper"><div class="profile-oval-badge profile-oval-badge--red profile-oval-badge--compact">{html.escape(str(high_risk))}</div></div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with snap3:
            st.markdown(
                f"""
            <div class="info-card info-card--profile-snapshot">
              <h4>Low-data profiles</h4>
              <div class="profile-oval-wrapper"><div class="profile-oval-badge profile-oval-badge--red profile-oval-badge--compact">{html.escape(str(low_data))}</div></div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        chart_col_1, chart_col_2 = st.columns(2)

        if "segment_name" in team.columns:
            with chart_col_1:
                section_header("Team segment distribution")
                seg_counts = (team["segment_name"].value_counts()
                             .rename_axis("Team profile").reset_index(name="Employees"))
                fig = px.pie(
                    seg_counts,
                    names="Team profile",
                    values="Employees",
                    title="Team distribution across AI-generated profiles",
                    hole=0.35,
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "valuation_archetype" in team.columns:
            with chart_col_2:
                section_header("Blue-Line valuation archetypes")
                arch_counts = (team["valuation_archetype"].value_counts()
                              .rename_axis("Valuation archetype").reset_index(name="Employees"))
                fig = px.pie(
                    arch_counts,
                    names="Valuation archetype",
                    values="Employees",
                    title="Team Blue-Line valuation archetypes",
                    hole=0.35,
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)

    # ── TAB 2 ─────────────────────────────────────────────────────────────────
    with tab2:
        callout(
            "<b>How to read this:</b> the drill-down combines quantitative signals with human context. "
            "It should support a coaching conversation, not produce an automatic judgment.",
            "gov",
        )
        section_header("Employee Drill-Down",
            "Select one employee to see a granular profile for coaching conversations.")
        if team.empty:
            st.warning("No team data available.")
        else:
            sel_emp = st.selectbox("Select an employee",
                                   sorted(team["display_employee"].dropna().unique()))
            ed = team[team["display_employee"] == sel_emp].iloc[0]

            c1,c2,c3,c4 = st.columns(4)
            with c1:
                signal_progress_card(
                    "Contribution signal",
                    _get(ed,"contribution_signal","performance_score"),
                    "Observable contribution signal from available performance information. "
                    "Use this as a discussion input, not as a final judgment.",
                    badge_labels=("Low", "Medium", "High"),
                )
            with c2:
                signal_progress_card(
                    "Development signal",
                    _get(ed,"learning_future_value_signal","learning_intensity_score"),
                    "Visible learning and development activity for this employee. "
                    "Lower values can also reflect missing or incomplete records.",
                    badge_labels=("Low", "Medium", "High"),
                )
            with c3:
                signal_progress_card(
                    "Continuity risk",
                    _get(ed,"absenteeism_risk_score"),
                    "Continuity pressure signal derived from absence-related patterns. "
                    "Treat as an early prompt for context-checking, not a diagnosis.",
                    badge_labels=("Low", "Medium", "High"),
                )
            with c4:
                signal_progress_card(
                    "Data confidence",
                    _get(ed,"interpretation_confidence","kpi_reliability_score"),
                    "Confidence in data completeness and reliability for interpretation. "
                    "If low, validate context and data quality before acting.",
                    badge_labels=("Low", "Medium", "High"),
                )

            section_header("Profile interpretation")
            p1,p2,p3 = st.columns(3)
            current_situation = str(_get(ed,"valuation_archetype","segment_name",default="N/A"))
            continuity_label = str(ed.get("risk_prediction_label","N/A"))
            recommended_experiment = str(ed.get("recommended_action","N/A"))
            with p1: profile_snapshot_card("Current situation", current_situation)
            with p2: profile_snapshot_card("Continuity label", continuity_label)
            with p3: info_card("Recommended experiment", recommended_experiment, card_class="info-card--profile-snapshot")

            section_header("Coaching questions generated from this employee's data")
            st.markdown(render_coaching_questions_table(manager_employee_coaching_questions(ed), priority_col="Priority"), unsafe_allow_html=True)

            # Context logs
            emp_log = load_log("employee_context_log.csv")
            mgr_log = load_log("manager_context_log.csv")
            emp_inputs = (emp_log[emp_log["display_employee"]==sel_emp]
                          if not emp_log.empty and "display_employee" in emp_log.columns
                          else pd.DataFrame())
            mgr_notes  = (mgr_log[mgr_log["display_employee"]==sel_emp]
                          if not mgr_log.empty and "display_employee" in mgr_log.columns
                          else pd.DataFrame())

            section_header("Employee context inputs")
            if emp_inputs.empty:
                st.info("No employee context inputs saved for this employee yet.")
            else:
                st.dataframe(emp_inputs.sort_values("date",ascending=False), use_container_width=True, hide_index=True)

            section_header("Manager notes for this employee")
            if mgr_notes.empty:
                st.info("No manager notes saved for this employee yet.")
            else:
                st.dataframe(mgr_notes.sort_values("date",ascending=False), use_container_width=True, hide_index=True)

            # callout moved to top of tab

    # ── TAB 3 ─────────────────────────────────────────────────────────────────
    with tab3:
        callout(
            "<b>How to interpret these signals:</b> these are aggregated indicators to guide prioritisation. "
            "Use them as conversation starters rather than absolute measures.",
            "gov",
        )
        section_header("Team Signals",
            "Identify where the team may need support: workload, learning access, or data quality.")

        sc1,sc2 = st.columns(2)
        with sc1:
            if "risk_prediction_label" in team.columns:
                risk_counts = (team["risk_prediction_label"].value_counts()
                              .rename_axis("Continuity label").reset_index(name="Employees"))
                fig = px.pie(
                    risk_counts,
                    names="Continuity label",
                    values="Employees",
                    title="Continuity-risk distribution",
                    hole=0.45,
                    color="Continuity label",
                    color_discrete_map={"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"},
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)
        with sc2:
            if "sustainability_balance" in team.columns:
                fig = px.histogram(
                    team,
                    x="sustainability_balance",
                    nbins=25,
                    color="segment_name" if "segment_name" in team.columns else None,
                    color_discrete_map=segment_color_map(team["segment_name"]) if "segment_name" in team.columns else None,
                    title="Sustainability balance distribution",
                    labels={"sustainability_balance":"Learning vs pressure balance"},
                )
                st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Coaching attention list",
            "Employees with High/Medium continuity risk, sorted by lowest sustainability balance")
        priority = team.copy()
        if "risk_prediction_label" in priority.columns:
            priority = priority[priority["risk_prediction_label"].isin(["High","Medium"])]
        if "sustainability_balance" in priority.columns:
            priority = priority.sort_values("sustainability_balance", ascending=True)

        coaching_cols = [c for c in [
            "display_employee","segment_name","risk_prediction_label",
            "learning_intensity_score","absenteeism_risk_score",
            "sustainability_balance","kpi_reliability_score","recommended_action",
        ] if c in priority.columns]

        if priority.empty:
            st.success("No high-priority coaching alerts detected for this team.")
        else:
            st.markdown(
                render_coaching_questions_table(
                    priority[coaching_cols].head(15),
                    priority_col="risk_prediction_label",
                    compact=True,
                ),
                unsafe_allow_html=True,
            )

        # callout moved to top of tab

    # ── TAB 4 ─────────────────────────────────────────────────────────────────
    with tab4:
        section_header("Manager Notes",
            "Add structured context when data alone is incomplete.")
        if team.empty:
            st.warning("No team data available.")
        else:
            with st.form("manager_note_form"):
                note_employee = st.selectbox("Employee concerned",
                    sorted(team["display_employee"].dropna().unique()), key="mgr_note_emp")
                note_type = st.selectbox("Type of note", [
                    "Coaching","Workload / capacity","Training need",
                    "Data correction","Recognition / invisible work",
                    "Risk or context","Follow-up with HR",
                ])
                manager_note = st.text_area("Manager comment",
                    placeholder="Example: This employee absorbed extra reporting work during a peak period; "
                                "absence signal should be interpreted with context.")
                follow_up = st.selectbox("Follow-up needed?", ["No","Yes"])
                submitted_note = st.form_submit_button("💾 Save manager note")

            if submitted_note:
                if not manager_note.strip():
                    st.warning("Please write a note before saving.")
                else:
                    append_log("manager_context_log.csv", {
                        "date":                pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "manager_department":  selected_department,
                        "display_employee":    note_employee,
                        "note_type":           note_type,
                        "manager_note":        manager_note,
                        "theme":               _classify_theme(manager_note),
                        "follow_up_needed":    follow_up,
                        "status":              "Submitted",
                    })
                    st.success("✅ Manager note saved — visible to HR as context, not as a score.")

            mgr_log   = load_log("manager_context_log.csv")
            team_notes = (mgr_log[mgr_log["display_employee"].isin(team["display_employee"])]
                          if not mgr_log.empty and "display_employee" in mgr_log.columns
                          else pd.DataFrame())
            section_header("Saved notes for my team")
            if team_notes.empty:
                st.info("No manager notes saved for this team yet.")
            else:
                st.dataframe(team_notes.sort_values("date",ascending=False),
                             use_container_width=True, hide_index=True)

            emp_log = load_log("employee_context_log.csv")
            team_emp_inputs = (emp_log[emp_log["display_employee"].isin(team["display_employee"])]
                               if not emp_log.empty and "display_employee" in emp_log.columns
                               else pd.DataFrame())
            show_context_summary(team_emp_inputs, team_notes)

    # ── TAB 5 ─────────────────────────────────────────────────────────────────
    with tab5:
        callout(
            "<b>How to use this plan:</b> convert signals into small, testable management experiments. "
            "Track actions, owners, and short-term checks rather than assuming immediate outcomes.",
            "gov",
        )
        section_header("Team Action Plan",
            "Team signals → practical management actions")
        with st.expander("How is this action plan generated ?", expanded=False):
            st.markdown(
                "The first table is generated from your team’s actual signals. The second table summarizes recommendation outputs when available. Actions should be treated as experiments: try a support action, observe whether signals improve, and add context."
            )

        section_header("Dynamic management questions & experiments")
        action_plan = manager_dynamic_questions(team).rename(columns={
            "Manager question":"Management question / experiment",
            "Why this appears":"Signal behind it",
        })
        st.markdown(
            render_questions_table_with_badges(action_plan, priority_col="Priority", compact=True),
            unsafe_allow_html=True,
        )

        section_header("Team-level recommendation summary")
        team_recs = (
            recommendation_df[recommendation_df["display_employee"].isin(team["display_employee"])].copy()
            if "display_employee" in recommendation_df.columns else pd.DataFrame()
        )
        if not team_recs.empty and "recommendation" in team_recs.columns:
            action_summary = (team_recs["recommendation"].value_counts()
                             .rename_axis("Recommended action").reset_index(name="Employees"))
            st.dataframe(action_summary, use_container_width=True, hide_index=True)
        elif "recommended_action" in team.columns:
            action_summary = (team["recommended_action"].value_counts()
                             .rename_axis("Recommended action").reset_index(name="Employees"))
            st.dataframe(action_summary, use_container_width=True, hide_index=True)

        section_header("Practical coaching loop")
        lp1,lp2,lp3,lp4 = st.columns(4)
        with lp1: meaning_card("1", "Check reliability",   "Confirm whether the data is complete enough to interpret.")
        with lp2: meaning_card("2", "Identify pattern",    "Look for workload, learning, or development gaps.")
        with lp3: meaning_card("3", "Discuss context",     "Use the signal as a starting point with employees.")
        with lp4: meaning_card("4", "Act and reassess",    "Adjust support, training, or workload — then monitor evolution.")

        # callout moved to top of tab

    # ── TAB 6 ─────────────────────────────────────────────────────────────────
    with tab6:
        callout(
            "<b>Manager principle:</b> the dashboard should help managers improve the work system "
            "around people — not mechanically evaluate people.",
            "gov",
        )
        section_header("Manager Help & FAQ")
        manager_faq = [
            ("What is the manager supposed to understand first?",
             "Start with the plain-language Manager interpretation on the Team Dashboard. It tells you whether the main topic is data quality, workload sustainability, development, learning conversion, or regular monitoring."),
            ("Are employees being ranked?",
             "No. The manager view should not be used as a ranking tool. It shows coaching and context signals to help managers support the team."),
            ("What should I do with a high continuity-risk profile?",
             "Treat it as a prompt to ask about workload, recovery, staffing, deadlines, role constraints, or missing context. Do not treat it as employee fault."),
            ("What should I do with a low development signal?",
             "Check whether the employee had access to training, mentoring, mobility, or project-based learning. Also check whether informal learning is missing from records."),
            ("What does interpretation confidence mean?",
             "It tells you whether the available records are complete enough to interpret. Low confidence means validate the data before making decisions."),
            ("How should manager notes be used?",
             "Use notes to add context that structured data misses: invisible work, peak workload, data errors, training needs, support needs, or recognition."),
        ]
        for q, a in manager_faq:
            with st.expander(f"ℹ️ {q}"):
                st.markdown(a)

        show_manager_score_dictionary()

        section_header("Manager workflow")
        wrapped_table(pd.DataFrame([
            {"Step":"1. Read the interpretation",  "Manager action":"Identify whether the main issue is data quality, workload, development, or monitoring."},
            {"Step":"2. Check confidence",         "Manager action":"If data confidence is low, validate records before interpreting."},
            {"Step":"3. Review team questions",    "Manager action":"Use generated questions to prepare team or individual check-ins."},
            {"Step":"4. Add context",              "Manager action":"Use Manager Notes when structured data misses important information."},
            {"Step":"5. Run a small experiment",   "Manager action":"Try a workload, training, mentoring, or data-quality action and monitor changes."},
        ]))
        


# ════════════════════════════════════════════════════════════════════════════════
# HR VIEW
# ════════════════════════════════════════════════════════════════════════════════
elif role == "HR":

    # Build HR priority table once
    hr_priority = employee_value.copy()
    if "sustainability_balance" not in hr_priority.columns and \
       {"learning_intensity_score","absenteeism_risk_score"}.issubset(hr_priority.columns):
        hr_priority["sustainability_balance"] = (
            hr_priority["learning_intensity_score"] - hr_priority["absenteeism_risk_score"]
        )

    _high_risk   = hr_priority["absenteeism_risk_score"] >= hr_priority["absenteeism_risk_score"].quantile(0.75) \
                   if "absenteeism_risk_score" in hr_priority.columns else pd.Series(False, index=hr_priority.index)
    _low_rel     = hr_priority["kpi_reliability_score"] < 0.5 \
                   if "kpi_reliability_score" in hr_priority.columns else pd.Series(False, index=hr_priority.index)
    _neg_sus     = hr_priority["sustainability_balance"] < 0 \
                   if "sustainability_balance" in hr_priority.columns else pd.Series(False, index=hr_priority.index)
    _low_lr      = hr_priority["learning_intensity_score"] < 0.3 \
                   if "learning_intensity_score" in hr_priority.columns else pd.Series(False, index=hr_priority.index)

    hr_priority["priority_reason"] = "Standard monitoring"
    hr_priority.loc[_low_rel,   "priority_reason"] = "Low data reliability"
    hr_priority.loc[_low_lr,    "priority_reason"] = "Low learning investment"
    hr_priority.loc[_neg_sus,   "priority_reason"] = "Negative sustainability balance"
    hr_priority.loc[_high_risk, "priority_reason"] = "High continuity risk"

    hr_priority["priority_level"] = "Low"
    hr_priority.loc[_low_lr | _low_rel, "priority_level"] = "Medium"
    hr_priority.loc[_high_risk | _neg_sus, "priority_level"] = "High"

    sort_cols   = ["priority_level"]
    sort_asc    = [False]
    if "absenteeism_risk_score" in hr_priority.columns:
        sort_cols.append("absenteeism_risk_score"); sort_asc.append(False)
    if "sustainability_balance" in hr_priority.columns:
        sort_cols.append("sustainability_balance");  sort_asc.append(True)

    hr_priority["_pri_num"] = hr_priority["priority_level"].map({"High":3,"Medium":2,"Low":1})
    hr_priority = hr_priority.sort_values(
        by=["_pri_num"] + [c for c in sort_cols if c != "priority_level"],
        ascending=[False] + sort_asc[1:],
    ).drop(columns=["_pri_num"])

    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "Action Center",
        "Blue-Line Valuation",
        "Workforce Explorer",
        "Drill-Down",
        "AI Insights",
        "Data & Documents",
        "Principles",
    ])

    # ── Action Center ─────────────────────────────────────────────────────────
    with tab1:
        with st.expander("What questions can be asked ?", expanded=False):
            st.dataframe(usefulness_answer("HR"), use_container_width=True, hide_index=True)

        section_header("HR Action Center", "Who needs attention, why, and what to do next")

        employees_mapped = len(employee_value)
        high_priority_count = int((hr_priority["priority_level"] == "High").sum())
        high_continuity_count = int(_high_risk.sum())
        low_reliability_count = int(_low_rel.sum())

        c1,c2,c3,c4 = st.columns(4)
        with c1: stat_card(
            "Employees mapped",
            f"{employees_mapped:,}",
            accent="primary",
            card_class="stat-card--mid",
            value_html=f'<span class="profile-oval-badge profile-oval-badge--blue">{html.escape(f"{employees_mapped:,}")}</span>',
        )
        with c2: stat_card(
            "High-priority profiles",
            f"{high_priority_count:,}",
            accent="danger",
            card_class="stat-card--mid",
            value_html=f'<span class="profile-oval-badge profile-oval-badge--red">{html.escape(f"{high_priority_count:,}")}</span>',
        )
        with c3: stat_card(
            "High continuity risk",
            f"{high_continuity_count:,}",
            accent="danger",
            card_class="stat-card--mid",
            value_html=f'<span class="profile-oval-badge profile-oval-badge--red">{html.escape(f"{high_continuity_count:,}")}</span>',
        )
        with c4: stat_card(
            "Low reliability",
            f"{low_reliability_count:,}",
            accent="warn",
            card_class="stat-card--mid",
            value_html=f'<span class="profile-oval-badge profile-oval-badge--yellow">{html.escape(f"{low_reliability_count:,}")}</span>',
        )

        with st.expander("How to use this table ?", expanded=False):
            callout(
                "<b>How to use this table:</b> these are not automatic HR decisions. "
                "They are profiles that deserve context checking, manager discussion, or data validation.",
                "gov",
            )

        section_header("Top profiles requiring attention")
        priority_cols = [c for c in [
            "display_employee", department_col, "segment_name",
            "priority_level","priority_reason",
            "absenteeism_risk_score","learning_intensity_score",
            "sustainability_balance","performance_score",
            "kpi_reliability_score","recommended_action",
        ] if c and c in hr_priority.columns]
        st.markdown(
            render_coaching_questions_table(
                hr_priority[priority_cols].head(30),
                priority_col="priority_level",
                compact=True,
                uppercase_headers=True,
                segment_col="segment_name",
                controls=False,
                percent_cols=[
                    "absenteeism_risk_score",
                    "learning_intensity_score",
                    "sustainability_balance",
                    "performance_score",
                    "kpi_reliability_score",
                ],
            ),
            unsafe_allow_html=True,
        )

        section_header("Why profiles are flagged")
        reason_summary = (hr_priority["priority_reason"].value_counts()
                         .rename_axis("Priority reason").reset_index(name="Employees"))
        fig = px.bar(reason_summary, x="Priority reason", y="Employees",
                     title="Priority reason breakdown",
                     color="Priority reason")
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Recommendation summary")
        if not recommendation_df.empty and "recommendation" in recommendation_df.columns:
            rec_summary = (
                recommendation_df["recommendation"]
                .value_counts()
                .rename_axis("Recommendation")
                .reset_index(name="Profiles")
            )
            show_summary_lens(rec_summary, label_col="Recommendation", count_col="Profiles", total_label="Total profiles")
        elif "recommended_action" in recommendation_df.columns:
            rec_summary = (
                recommendation_df["recommended_action"]
                .value_counts()
                .rename_axis("Recommendation")
                .reset_index(name="Profiles")
            )
            show_summary_lens(rec_summary, label_col="Recommendation", count_col="Profiles", total_label="Total profiles")
        else:
            st.info("No recommendations available.")

    # ── Blue-Line Valuation ───────────────────────────────────────────────────
    with tab2:
        callout(
            "<b>Blue-Line principle:</b> indicators are not the objective. They are learning signals "
            "that help CACEIS understand which conditions may create, sustain, or destroy long-term value.",
            "gov",
        )
        section_header("Blue-Line Valuation",
            "Sustainable value potential estimated from observable signals — not employee worth.")

        c1,c2,c3,c4 = st.columns(4)
        with c1:
            signal_progress_card(
                "Avg contribution signal",
                safe_mean(employee_value, "contribution_signal"),
                "Average contribution-related signal across employees.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c2:
            signal_progress_card(
                "Avg future value signal",
                safe_mean(employee_value, "learning_future_value_signal"),
                "Average visible learning and development activity.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c3:
            signal_progress_card(
                "Avg sustainability signal",
                safe_mean(employee_value, "sustainability_signal"),
                "Average continuity and sustainability signal.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c4:
            signal_progress_card(
                "Avg interpretation confidence",
                safe_mean(employee_value, "interpretation_confidence"),
                "Average confidence in data completeness and interpretability.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )

        section_header("Valuation archetype distribution")
        arch_counts = (employee_value["valuation_archetype"].value_counts()
                      .rename_axis("Valuation archetype").reset_index(name="Employees"))
        def _wrap_axis_label(label: str, width: int = 16) -> str:
            words = str(label).split()
            if len(words) <= 2:
                return str(label)
            lines = []
            current = []
            current_len = 0
            for word in words:
                next_len = current_len + len(word) + (1 if current else 0)
                if current and next_len > width:
                    lines.append(" ".join(current))
                    current = [word]
                    current_len = len(word)
                else:
                    current.append(word)
                    current_len = next_len
            if current:
                lines.append(" ".join(current))
            return "<br>".join(lines)

        wrapped_tick_text = [f"<b>{_wrap_axis_label(label)}</b>" for label in arch_counts["Valuation archetype"]]
        fig = px.bar(arch_counts, x="Valuation archetype", y="Employees",
                     title="Distribution of Blue-Line valuation archetypes",
                     color="Valuation archetype",
                     color_discrete_map=VALUATION_ARCHETYPE_COLORS,
                     text="Employees")
        fig.update_traces(textposition="outside", texttemplate="%{text}", cliponaxis=False)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(tickmode="array", tickvals=arch_counts["Valuation archetype"], ticktext=wrapped_tick_text, tickangle=0)
        fig.update_xaxes(title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13), tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11))
        fig.update_yaxes(title="Employees", rangemode="tozero", title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13), tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11))
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Value potential vs interpretation confidence")
        fig = px.scatter(employee_value,
            x="sustainable_value_potential", y="interpretation_confidence",
            color="valuation_archetype",
            color_discrete_map=VALUATION_ARCHETYPE_COLORS,
            hover_data=[c for c in ["display_employee",department_col,
                                    "blue_line_question","interpretation_risk"]
                        if c and c in employee_value.columns],
            title="Sustainable value potential must be read alongside data confidence",
        )
        fig.update_xaxes(title="SUSTAINABLE VALUE POTENTIAL", tickformat=".0%")
        fig.update_yaxes(title="INTERPRETATION CONFIDENCE", tickformat=".0%")
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Valuation explanation table")
        exp_cols = [c for c in [
            "display_employee",department_col,"valuation_archetype","blue_line_question",
            "contribution_signal","learning_future_value_signal","sustainability_signal",
            "progression_signal","sustainable_value_potential","interpretation_confidence",
            "reliability_adjusted_value_potential","interpretation_risk",
        ] if c and c in employee_value.columns]
        render_valuation_explanation_table(employee_value[exp_cols], archetype_col="valuation_archetype")
        callout(
            "<b>Interpretation rule:</b> a high value potential with low confidence is not a strong "
            "conclusion. It is a prompt to improve data quality or validate context.",
            "warn",
        )

    # ── Workforce Explorer ────────────────────────────────────────────────────
    with tab3:
        section_header("Workforce Explorer",
            "Explore patterns by segment, department, reliability, learning, and value proxy.")
        filtered = employee_value.copy()

        fc1,fc2,fc3 = st.columns(3)
        with fc1:
            sel_segs = st.multiselect("Filter by AI segment",
                sorted(filtered["segment_name"].dropna().unique()),
                default=sorted(filtered["segment_name"].dropna().unique()))
            filtered = filtered[filtered["segment_name"].isin(sel_segs)]
        with fc2:
            if "low_data_flag" in filtered.columns:
                ld_choice = st.selectbox("Data visibility",
                    ["All","Only low-visibility employees","Exclude low-visibility employees"])
                if ld_choice == "Only low-visibility employees":
                    filtered = filtered[filtered["low_data_flag"]==True]
                elif ld_choice == "Exclude low-visibility employees":
                    filtered = filtered[filtered["low_data_flag"]==False]
        with fc3:
            if department_col:
                depts = sorted(filtered[department_col].dropna().unique())
                sel_depts = st.multiselect("Filter by department/entity", depts, default=depts)
                filtered = filtered[filtered[department_col].isin(sel_depts)]

        c1,c2,c3,c4 = st.columns(4)
        with c1:
            selected_employees_card(len(filtered))
        with c2:
            explorer_progress_card(
                "Avg value proxy",
                safe_mean(filtered, "human_capital_value_proxy"),
                "Average human capital value proxy for the current filtered population.",
                badge_labels=("Low", "Medium", "High"),
            )
        with c3:
            explorer_progress_card(
                "Avg learning signal",
                safe_mean(filtered, "learning_intensity_score"),
                "Average learning intensity signal for the current filtered population.",
                badge_labels=("Low", "Medium", "High"),
            )
        with c4:
            explorer_progress_card(
                "Avg continuity risk",
                safe_mean(filtered, "absenteeism_risk_score"),
                "Average continuity / absence risk for the current filtered population.",
                badge_labels=("Low", "Medium", "High"),
            )

        st.markdown('<div class="explorer-card-spacer"></div>', unsafe_allow_html=True)

        if {"learning_intensity_score","human_capital_value_proxy","segment_name"}.issubset(filtered.columns):
            fig = px.scatter(filtered,
                x="learning_intensity_score", y="human_capital_value_proxy",
                color="segment_name",
                labels={
                    "learning_intensity_score": "LEARNING INTENSITY SCORE",
                    "human_capital_value_proxy": "HUMAN CAPITAL VALUE PROXY",
                    "segment_name": "SEGMENT NAME",
                },
                hover_data=[c for c in ["display_employee","performance_score",
                                        "absenteeism_risk_score","kpi_reliability_score"]
                            if c in filtered.columns],
                title="<b>LEARNING INTENSITY VS HUMAN CAPITAL VALUE PROXY</b>",
            )
            fig.update_layout(legend_title_text="<b>SEGMENT NAME</b>")
            fig.update_xaxes(
                title="<b>LEARNING INTENSITY SCORE</b>",
                tickformat=".0%",
                showline=True,
                linecolor="#334155",
                linewidth=1.2,
                mirror=False,
                title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13),
                tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11),
            )
            fig.update_yaxes(
                title="<b>HUMAN CAPITAL VALUE PROXY</b>",
                tickformat=".0%",
                showline=True,
                linecolor="#334155",
                linewidth=1.2,
                mirror=False,
                title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13),
                tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11),
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if "sustainability_balance" in filtered.columns:
            fig = px.histogram(
                filtered,
                x="sustainability_balance",
                nbins=30,
                color="segment_name",
                color_discrete_map=segment_color_map(filtered["segment_name"]) if "segment_name" in filtered.columns else None,
                labels={
                    "sustainability_balance": "SUSTAINABILITY BALANCE",
                    "segment_name": "SEGMENT NAME",
                },
                title="<b>SUSTAINABILITY BALANCE DISTRIBUTION</b>",
            )
            fig.update_layout(legend_title_text="<b>SEGMENT NAME</b>")
            fig.update_xaxes(
                title="<b>SUSTAINABILITY BALANCE</b>",
                tickformat=".0%",
                showline=True,
                linecolor="#334155",
                linewidth=1.2,
                mirror=False,
                title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13),
                tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11),
            )
            fig.update_yaxes(
                title="<b>COUNT</b>",
                showline=True,
                linecolor="#334155",
                linewidth=1.2,
                mirror=False,
                title_font=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=13),
                tickfont=dict(color="#334155", family="DM Sans, system-ui, sans-serif", size=11),
            )
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("AI segment summary")
        metrics = [c for c in [
            "human_capital_value_proxy","reliability_adjusted_value_proxy",
            "performance_score","learning_intensity_score","absenteeism_risk_score",
            "sustainability_balance","data_coverage_score","kpi_reliability_score",
        ] if c in employee_value.columns]
        if metrics:
            summary_df = (
                employee_value.groupby("segment_name",as_index=False)[metrics].mean()
                .merge(employee_value.groupby("segment_name",as_index=False).size()
                       .rename(columns={"size":"employees"}),
                       on="segment_name", how="left")
            )
            st.markdown(
                render_coaching_questions_table(
                    summary_df,
                    priority_col="",
                    uppercase_headers=True,
                    segment_col="segment_name",
                    percent_cols=metrics,
                    controls=False,
                ),
                unsafe_allow_html=True,
            )

        section_header("Filtered employee profiles")
        filtered = filtered.merge(
            hr_priority[[c for c in ["display_employee","priority_level","priority_reason"]
                         if c in hr_priority.columns]],
            on="display_employee", how="left",
        )
        disp_cols = [c for c in [
            "display_employee",department_col,"segment_name",
            "priority_level","priority_reason",
            "human_capital_value_proxy","reliability_adjusted_value_proxy",
            "kpi_reliability_score","performance_score","learning_intensity_score",
            "absenteeism_risk_score","sustainability_balance","recommended_action",
        ] if c and c in filtered.columns]
        st.markdown(
            render_coaching_questions_table(
                filtered[disp_cols],
                priority_col="priority_level",
                uppercase_headers=True,
                segment_col="segment_name",
                compact=True,
                percent_cols=[
                    c for c in [
                        "human_capital_value_proxy",
                        "reliability_adjusted_value_proxy",
                        "kpi_reliability_score",
                        "performance_score",
                        "learning_intensity_score",
                        "absenteeism_risk_score",
                        "sustainability_balance",
                    ] if c in filtered.columns
                ],
                controls=False,
            ),
            unsafe_allow_html=True,
        )

    # ── Drill-Down ────────────────────────────────────────────────────────────
    with tab4:
        section_header("Employee / Team Drill-Down",
            "HR can inspect one department or employee while seeing all context logs.")
        drill_df = employee_value.copy()
        if department_col:
            depts = sorted(drill_df[department_col].dropna().unique())
            sel_hr_dept = st.selectbox("Select department/entity", ["All"] + depts)
            if sel_hr_dept != "All":
                drill_df = drill_df[drill_df[department_col] == sel_hr_dept]
        sel_hr_emp = st.selectbox("Select employee",
            sorted(drill_df["display_employee"].dropna().unique()))
        hr_emp_row = drill_df[drill_df["display_employee"]==sel_hr_emp].iloc[0]

        c1,c2,c3,c4 = st.columns(4)
        with c1:
            signal_progress_card(
                "Value proxy",
                _get(hr_emp_row, "human_capital_value_proxy"),
                "Current value proxy for the selected employee.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c2:
            signal_progress_card(
                "Learning",
                _get(hr_emp_row, "learning_intensity_score"),
                "Current learning intensity signal for the selected employee.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c3:
            signal_progress_card(
                "Continuity risk",
                _get(hr_emp_row, "absenteeism_risk_score"),
                "Current continuity / absence risk signal for the selected employee.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c4:
            signal_progress_card(
                "Reliability",
                _get(hr_emp_row, "kpi_reliability_score"),
                "Current data reliability for the selected employee.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )

        section_header("Individual signal summary")
        sig_cols = [c for c in [
            "display_employee",department_col,"segment_name","risk_prediction_label",
            "recommended_action","data_coverage_score","kpi_reliability_score","sustainability_balance",
        ] if c and c in employee_value.columns]
        st.markdown(
            '<div class="score-table-wrap--drilldown-summary">'
            + render_coaching_questions_table(
                pd.DataFrame([hr_emp_row[sig_cols]]),
                priority_col="risk_prediction_label",
                compact=True,
                percent_cols=[
                    c for c in [
                        "data_coverage_score",
                        "kpi_reliability_score",
                        "sustainability_balance",
                    ] if c in employee_value.columns
                ],
                uppercase_headers=True,
                segment_col="segment_name",
                controls=False,
                wrap_class_override="score-table-wrap score-table-wrap--drilldown-summary",
                wrap_style_override="",
            )
            + '</div>',
            unsafe_allow_html=True,
        )

        emp_log = load_log("employee_context_log.csv")
        mgr_log = load_log("manager_context_log.csv")
        emp_inputs = (emp_log[emp_log["display_employee"]==sel_hr_emp]
                      if not emp_log.empty and "display_employee" in emp_log.columns
                      else pd.DataFrame())
        mgr_notes  = (mgr_log[mgr_log["display_employee"]==sel_hr_emp]
                      if not mgr_log.empty and "display_employee" in mgr_log.columns
                      else pd.DataFrame())

        section_header("Employee inputs")
        if not emp_inputs.empty:
            st.dataframe(emp_inputs.sort_values("date",ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No employee inputs for this employee yet.")

        section_header("Manager notes")
        if not mgr_notes.empty:
            st.dataframe(mgr_notes.sort_values("date",ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No manager notes for this employee yet.")

        show_context_summary(emp_inputs, mgr_notes)

    # ── AI Insights ───────────────────────────────────────────────────────────
    with tab5:
        section_header("AI Insights",
            "AI segments, ONEValue signals, and value-creation experiments.")
        if onevalue_ai_df.empty:
            st.warning("ONEValue AI insights not found. Run `python src/onevalue_ai_layer.py` first.")
        else:
            c1,c2,c3 = st.columns(3)
            with c1: stat_card("AI insights",     f"{len(onevalue_ai_df):,}")
            with c2: stat_card("AI signal types", f"{onevalue_ai_df['ai_signal'].nunique():,}" if "ai_signal" in onevalue_ai_df.columns else "N/A", accent="indigo")
            with c3: stat_card("Decision owners", f"{onevalue_ai_df['decision_owner'].nunique():,}" if "decision_owner" in onevalue_ai_df.columns else "N/A")

            if "ai_signal" in onevalue_ai_df.columns:
                section_header("ONEValue AI signal distribution")
                signal_summary = (onevalue_ai_df["ai_signal"].value_counts()
                                 .rename_axis("AI signal").reset_index(name="Profiles"))
                fig = px.bar(signal_summary, x="AI signal", y="Profiles",
                             title="ONEValue AI signal distribution",
                             color="AI signal")
                st.plotly_chart(clean_chart(fig), use_container_width=True)
                st.dataframe(signal_summary, use_container_width=True, hide_index=True)

            section_header("High-priority AI experiments")
            high_sigs = [
                "High contribution under pressure",
                "Negative sustainability balance",
                "High performer with low development signal",
            ]
            ai_priority = onevalue_ai_df[onevalue_ai_df.get("ai_signal",pd.Series(dtype=str)).isin(high_sigs)].copy() \
                          if "ai_signal" in onevalue_ai_df.columns else pd.DataFrame()
            if ai_priority.empty:
                st.success("No high-priority AI experiments detected.")
            else:
                ai_cols = [c for c in [
                    "display_employee","segment_name","ai_signal","ai_interpretation",
                    "recommended_experiment","learning_question","decision_owner",
                ] if c in ai_priority.columns]
                st.dataframe(ai_priority[ai_cols].head(30), use_container_width=True, hide_index=True)

            section_header("All value-creation experiments")
            exp_cols = [c for c in [
                "display_employee","segment_name","ai_signal","ai_interpretation",
                "recommended_experiment","learning_question","value_creation_hypothesis","decision_owner",
            ] if c in onevalue_ai_df.columns]
            st.dataframe(onevalue_ai_df[exp_cols], use_container_width=True, hide_index=True)
            callout(
                "<b>Blue-line logic:</b> the goal is not to manage the indicator directly. "
                "The goal is to test which actions and working conditions improve sustainable value creation.",
                "gov",
            )

    # ── Data & Documents ──────────────────────────────────────────────────────
    with tab6:
        section_header("Data & Documents", "KPI audit, data quality checks, and document intelligence.")

        c1,c2,c3 = st.columns(3)
        with c1:
            explorer_progress_card(
                "Avg data coverage",
                safe_mean(employee_value, "data_coverage_score"),
                "Average completeness of the available data for the current population.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c2:
            explorer_progress_card(
                "Avg KPI reliability",
                safe_mean(employee_value, "kpi_reliability_score"),
                "Average reliability of the KPI signals for the current population.",
                badge_labels=("Low performance", "Stable", "High performance"),
            )
        with c3:
            low_data_records_card(
                int(employee_value['low_data_flag'].sum()) if "low_data_flag" in employee_value.columns else 0
            )

        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

        if "data_coverage_score" in employee_value.columns:
            fig = px.histogram(employee_value, x="data_coverage_score", nbins=20,
                               title="Data coverage score distribution",
                               labels={"data_coverage_score":"DATA COVERAGE SCORE"})
            fig.update_xaxes(tickformat=".0%", title_text="DATA COVERAGE SCORE", title_font=dict(weight="bold"))
            fig.update_yaxes(title_text="FREQUENCY", title_font=dict(weight="bold"))
            st.plotly_chart(clean_chart(fig), use_container_width=True)
        
        st.markdown("<br style='margin-bottom: 3.5rem;'>", unsafe_allow_html=True)

        section_header("KPI audit")
        kpi_section = st.radio("Choose KPI table",
            ["HR & Performance","Absenteeism / Continuity","Learning"], horizontal=True)
        if kpi_section == "HR & Performance":
            hr_kpi_display = hr_kpi.copy()
            hr_kpi_display.columns = [col.replace('_', ' ').upper() for col in hr_kpi_display.columns]
            percent_cols = [c for c in hr_kpi_display.columns if 'PERFORMANCE CONSISTENCY SCORE' in c or 'TALENT PROGRESSION PROXY' in c]
            for col in percent_cols:
                if col in hr_kpi_display.columns:
                    hr_kpi_display[col] = hr_kpi_display[col].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else x)
            st.dataframe(hr_kpi_display, use_container_width=True)
        elif kpi_section == "Absenteeism / Continuity":
            absence_kpi_display = absence_kpi.copy()
            absence_kpi_display.columns = [col.replace('_', ' ').upper() for col in absence_kpi_display.columns]
            percent_cols = [c for c in absence_kpi_display.columns if 'SCORE' in c]
            for col in percent_cols:
                if col in absence_kpi_display.columns:
                    absence_kpi_display[col] = absence_kpi_display[col].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else x)
            st.dataframe(absence_kpi_display, use_container_width=True)
        else:
            training_kpi_display = training_kpi.copy()
            training_kpi_display.columns = [col.replace('_', ' ').upper() for col in training_kpi_display.columns]
            percent_cols = [c for c in training_kpi_display.columns if 'SCORE' in c]
            for col in percent_cols:
                if col in training_kpi_display.columns:
                    training_kpi_display[col] = training_kpi_display[col].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else x)
            st.dataframe(training_kpi_display, use_container_width=True)

        st.divider()
        show_document_intelligence()

    # ── Usage & Principles ────────────────────────────────────────────────────
    with tab7:
        section_header("Usage & Principles")
        c_does, c_doesnt = st.columns(2)
        with c_does:
            info_card("What this tool does", (
                "Identifies workforce patterns using HR, absence, training, and performance data. "
                "Highlights profiles that may require attention. Translates signals into recommended "
                "actions and learning questions. Supports HR and managers in decision-making."
            ))
        with c_doesnt:
            info_card("What this tool does NOT do", (
                "It does not evaluate employees automatically. It does not replace HR or managerial "
                "judgment. It does not produce final decisions. It does not directly measure value "
                "creation — it uses proxy signals."
            ))

        section_header("Key principles")
        wrapped_table(pd.DataFrame([
            {"Principle":"Use pseudonymised data",         "Why it matters":"Employee privacy must be protected at all times."},
            {"Principle":"No automatic sanctions",         "Why it matters":"Outputs should start conversations, not trigger penalties."},
            {"Principle":"Check reliability first",        "Why it matters":"Acting on unreliable data causes harm."},
            {"Principle":"AI as signal, not truth",        "Why it matters":"Models have limitations; human judgment is essential."},
            {"Principle":"Keep humans in the loop",        "Why it matters":"Final decisions always require human accountability."},
        ]))
        callout(
            "<b>Important:</b> this is a decision-support tool. It helps identify where attention may "
            "be needed, but final decisions always require human judgment.",
            "gov",
        )

# ════════════════════════════════════════════════════════════════════════════════
# PRODUCT OWNER VIEW
# ════════════════════════════════════════════════════════════════════════════════
elif role == "Product Owner":
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
        "System Health",
        "Valuation Model",
        "Data Quality",
        "AI Monitoring",
        "Governance & Roadmap",
        "Document Pipeline",
    ])

    # ── System Health ─────────────────────────────────────────────────────────
    with tab1:
        section_header("System Health", "Pipeline readiness, generated outputs, deployment completeness.")
        st.dataframe(usefulness_answer("Product Owner"), use_container_width=True, hide_index=True)

        _el = load_log("employee_context_log.csv")
        _ml = load_log("manager_context_log.csv")
        output_checks = pd.DataFrame([
            {"Output":"hr_kpi_table.csv",             "Purpose":"HR and performance KPI source",                         "Rows":len(hr_kpi),            "Status":"✅ Loaded" if not hr_kpi.empty else "❌ Missing"},
            {"Output":"absence_kpi_table.csv",         "Purpose":"Absenteeism / continuity KPI source",                  "Rows":len(absence_kpi),       "Status":"✅ Loaded" if not absence_kpi.empty else "❌ Missing"},
            {"Output":"training_kpi_table.csv",        "Purpose":"Learning intensity KPI source",                         "Rows":len(training_kpi),      "Status":"✅ Loaded" if not training_kpi.empty else "❌ Missing"},
            {"Output":"employee_value_table_v2.csv",   "Purpose":"Integrated employee-level value table",                 "Rows":len(employee_value),    "Status":"✅ Loaded" if not employee_value.empty else "❌ Missing"},
            {"Output":"recommendation_table.csv",      "Purpose":"Recommended actions and human questions",               "Rows":len(recommendation_df), "Status":"✅ Loaded" if not recommendation_df.empty else "❌ Missing"},
            {"Output":"onevalue_ai_insights.csv",      "Purpose":"AI-generated signals, experiments, and learning Qs",   "Rows":len(onevalue_ai_df),    "Status":"✅ Loaded" if not onevalue_ai_df.empty else "❌ Missing"},
            {"Output":"document_theme_summary.csv",    "Purpose":"Unstructured document theme extraction",                "Rows":len(doc_theme),         "Status":"✅ Loaded" if not doc_theme.empty else "⚠️ Optional"},
            {"Output":"document_inventory.csv",        "Purpose":"Document inventory and source tracking",                "Rows":len(doc_inventory),     "Status":"✅ Loaded" if not doc_inventory.empty else "⚠️ Optional"},
            {"Output":"employee_context_log.csv",      "Purpose":"V4 employee questions, decisions, and context inputs",  "Rows":len(_el),               "Status":"✅ Loaded" if not _el.empty else "⚠️ No entries yet"},
            {"Output":"manager_context_log.csv",       "Purpose":"V4 manager comments and contextual notes",              "Rows":len(_ml),               "Status":"✅ Loaded" if not _ml.empty else "⚠️ No entries yet"},
        ])

        loaded = int((output_checks["Status"].str.startswith("✅")).sum())
        total  = len(output_checks)
        c1,c2,c3 = st.columns(3)
        with c1: stat_card("Pipeline outputs loaded",  f"{loaded}/{total}")
        with c2: stat_card("Employees mapped",          f"{len(employee_value):,}")
        with c3: stat_card("Deployment readiness",
                           "✅ Ready" if loaded == total else "⚠️ Incomplete",
                           accent="primary" if loaded==total else "warn")

        section_header("Output readiness checklist")
        st.dataframe(output_checks, use_container_width=True, hide_index=True)
        if loaded < total:
            st.warning("Some expected outputs are missing. Re-run the pipeline scripts before the final demo.")
        else:
            st.success("All expected outputs are loaded and ready.")

        section_header("Recommended run order")
        wrapped_table(pd.DataFrame([
            {"Step":1,"Command":"python src/integrated_value_ai.py",           "Expected output":"employee_value_table_v2.csv, department_value_summary_v2.csv, ai_segment_summary_v2.csv"},
            {"Step":2,"Command":"python src/risk_prediction.py",               "Expected output":"risk_prediction_table.csv"},
            {"Step":3,"Command":"python src/recommendation_engine.py",         "Expected output":"recommendation_table.csv"},
            {"Step":4,"Command":"python src/onevalue_ai_layer.py",             "Expected output":"onevalue_ai_insights.csv"},
            {"Step":5,"Command":"python src/document_theme_extraction.py",     "Expected output":"document_theme_summary.csv, document_inventory.csv"},
            {"Step":6,"Command":'python -m streamlit run "dashboard/final version/streamlit_app_v4.py"',"Expected output":"Launch dashboard"},
        ]))

    # ── Valuation Model ───────────────────────────────────────────────────────
    with tab2:
        section_header("Valuation Model Monitoring",
            "Is the Blue-Line valuation framework usable, reliable, and responsible?")

        c1,c2,c3,c4 = st.columns(4)
        with c1: stat_card("Avg value potential",      safe_mean(employee_value,"sustainable_value_potential"))
        with c2: stat_card("Avg adjusted potential",   safe_mean(employee_value,"reliability_adjusted_value_potential"), accent="indigo")
        with c3: stat_card("Avg interpretation risk",  safe_mean(employee_value,"interpretation_risk"), accent="warn")
        with c4: stat_card("Archetypes detected",
                           f"{employee_value['valuation_archetype'].nunique():,}"
                           if "valuation_archetype" in employee_value.columns else "N/A")

        section_header("Model input dimensions")
        dim_cols = [c for c in [
            "contribution_signal","learning_future_value_signal","sustainability_signal",
            "progression_signal","interpretation_confidence",
        ] if c in employee_value.columns]
        if dim_cols:
            dim_df = pd.DataFrame({
                "Dimension":     dim_cols,
                "Average score": [round(employee_value[c].mean(),3)  for c in dim_cols],
                "Minimum":       [round(employee_value[c].min(),3)   for c in dim_cols],
                "Maximum":       [round(employee_value[c].max(),3)   for c in dim_cols],
                "Missing values":[int(employee_value[c].isna().sum()) for c in dim_cols],
            })
            st.dataframe(dim_df, use_container_width=True, hide_index=True)
            fig = px.bar(dim_df, x="Dimension", y="Average score",
                         title="Average valuation model input dimensions",
                         color="Dimension")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Interpretation risk monitoring")
        fig = px.histogram(employee_value, x="interpretation_risk", nbins=25,
                           title="Distribution of interpretation risk")
        st.plotly_chart(clean_chart(fig), use_container_width=True)

        if department_col and "valuation_archetype" in employee_value.columns:
            section_header("Valuation archetype by department")
            arch_dept = (employee_value.groupby([department_col,"valuation_archetype"])
                        .size().reset_index(name="Employees"))
            fig = px.bar(arch_dept, x=department_col, y="Employees",
                         color="valuation_archetype",
                         title="Valuation archetypes by department/entity")
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(arch_dept, use_container_width=True, hide_index=True)

        section_header("Model limitations")
        wrapped_table(pd.DataFrame([
            {"Limitation":"Indicators are proxies",       "Implication":"Estimates sustainable value potential; does not directly measure financial value.","Control":"Show dimension scores and interpretation confidence."},
            {"Limitation":"Performance reviews may be biased","Implication":"Contribution signal may reflect review process bias.",                         "Control":"Monitor rating distributions by team and manager when data is available."},
            {"Limitation":"Absence data is lagging",      "Implication":"Burnout/disengagement may appear before absence increases.",                       "Control":"Add workload, engagement, and recovery indicators in future versions."},
            {"Limitation":"No supervised outcome labels", "Implication":"Risk labels are not validated predictive models.",                                  "Control":"Treat AI outputs as segmentation and hypothesis generation, not prediction."},
            {"Limitation":"Low data coverage",            "Implication":"Some profiles cannot be interpreted safely.",                                       "Control":"Use interpretation confidence and block strong conclusions below threshold."},
        ]))
        callout(
            "<b>Product Owner rule:</b> assess valuation by reliability, explainability, bias risk, "
            "and usefulness for learning — not by score production alone.",
            "gov",
        )

    # ── Data Quality ──────────────────────────────────────────────────────────
    with tab3:
        section_header("Data Quality",
            "Is the data complete and reliable enough to support interpretation?")

        c1,c2,c3,c4 = st.columns(4)
        with c1: stat_card("Avg data coverage",  safe_mean(employee_value,"data_coverage_score"))
        with c2: stat_card("Avg KPI reliability",safe_mean(employee_value,"kpi_reliability_score"), accent="warn")
        with c3: stat_card("Low-data records",
                           f"{int(employee_value['low_data_flag'].sum()):,}"
                           if "low_data_flag" in employee_value.columns else "N/A", accent="danger")
        with c4: stat_card("Training records",
                           f"{int(employee_value['has_training_record'].sum()):,}"
                           if "has_training_record" in employee_value.columns else "N/A")

        section_header("Coverage by data source")
        cov_rows = []
        for col, label in [("has_performance_record","Performance"),
                           ("has_absence_record","Absence"),
                           ("has_training_record","Training")]:
            if col in employee_value.columns:
                cov_rows.append({"Data source":label,
                                 "Records available":int(employee_value[col].sum()),
                                 "Coverage share":round(employee_value[col].mean(),3)})
        if cov_rows:
            cov_df = pd.DataFrame(cov_rows)
            st.dataframe(cov_df, use_container_width=True, hide_index=True)
            fig = px.bar(cov_df, x="Data source", y="Coverage share",
                         title="Data coverage by source", color="Data source",
                         color_discrete_sequence=["#0d9488","#6366f1","#f59e0b"])
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        section_header("Low-reliability records")
        dq_cols = [c for c in [
            "display_employee",department_col,"data_coverage_score","kpi_reliability_score",
            "low_data_flag","has_performance_record","has_absence_record","has_training_record",
        ] if c and c in employee_value.columns]
        if "kpi_reliability_score" in employee_value.columns:
            st.dataframe(
                employee_value.sort_values("kpi_reliability_score",ascending=True)[dq_cols].head(100),
                use_container_width=True, hide_index=True,
            )
        if "data_coverage_score" in employee_value.columns:
            fig = px.histogram(employee_value, x="data_coverage_score", nbins=20,
                               title="Data coverage score distribution")
            st.plotly_chart(clean_chart(fig), use_container_width=True)
        callout(
            "<b>Product implication:</b> low data reliability should block strong interpretation. "
            "The platform should surface reliability before recommending action.",
            "gov",
        )

    # ── AI Monitoring ─────────────────────────────────────────────────────────
    with tab4:
        section_header("AI Monitoring",
            "Balance, interpretability, usefulness, and responsible deployment readiness.")

        c1,c2,c3 = st.columns(3)
        with c1: stat_card("AI segments",       f"{employee_value['segment_name'].nunique():,}" if "segment_name" in employee_value.columns else "N/A")
        with c2: stat_card("AI insight rows",   f"{len(onevalue_ai_df):,}" if not onevalue_ai_df.empty else "0", accent="indigo")
        with c3: stat_card("Recommendation rows",f"{len(recommendation_df):,}" if not recommendation_df.empty else "0")

        if "segment_name" in employee_value.columns:
            section_header("AI segment distribution")
            seg_c = (employee_value["segment_name"].value_counts()
                    .rename_axis("AI segment").reset_index(name="Employees"))
            st.dataframe(seg_c, use_container_width=True, hide_index=True)
            fig = px.bar(seg_c, x="AI segment", y="Employees",
                         title="AI segment distribution", color="AI segment")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if not onevalue_ai_df.empty and "ai_signal" in onevalue_ai_df.columns:
            section_header("ONEValue AI signal distribution")
            sig_c = (onevalue_ai_df["ai_signal"].value_counts()
                    .rename_axis("AI signal").reset_index(name="Profiles"))
            st.dataframe(sig_c, use_container_width=True, hide_index=True)
            fig = px.bar(sig_c, x="AI signal", y="Profiles",
                         title="ONEValue AI signal distribution", color="AI signal")
            st.plotly_chart(clean_chart(fig), use_container_width=True)

        if not recommendation_df.empty and "priority_level" in recommendation_df.columns:
            section_header("Recommendation priority distribution")
            pri_c = (recommendation_df["priority_level"].value_counts()
                    .rename_axis("Priority level").reset_index(name="Profiles"))
            fig = px.bar(pri_c, x="Priority level", y="Profiles",
                         title="Recommendation priority distribution",
                         color="Priority level",
                         color_discrete_map={"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"})
            st.plotly_chart(clean_chart(fig), use_container_width=True)
            st.dataframe(pri_c, use_container_width=True, hide_index=True)

        section_header("Model maturity assessment")
        wrapped_table(pd.DataFrame([
            {"AI component":"KMeans segmentation",       "Status":"Implemented","Method":"Unsupervised learning",              "Limitation":"Finds patterns but does not predict future outcomes",                    "Next step":"Validate segments with HR experts and longitudinal outcomes"},
            {"AI component":"Continuity-risk label",     "Status":"Rule-based", "Method":"Quantile-based scoring",             "Limitation":"Not a trained supervised model",                                         "Next step":"Train model if future long-absence or attrition labels become available"},
            {"AI component":"Recommendation engine",     "Status":"Implemented","Method":"Business rules + signal logic",      "Limitation":"Recommendations are not yet validated against outcomes",                 "Next step":"Track accepted actions and outcome changes"},
            {"AI component":"ONEValue AI experiments",   "Status":"Implemented","Method":"Signal-to-hypothesis logic",         "Limitation":"No live manager/employee feedback loop yet",                             "Next step":"Add decision logging and experiment tracking"},
            {"AI component":"Document intelligence",     "Status":"Keyword-based","Method":"Theme detection",                  "Limitation":"Counts terms, does not yet summarise meaning deeply",                    "Next step":"Use NLP summarisation and link themes to departments"},
        ]))
        callout(
            "<b>Admin guardrail:</b> current AI outputs are pattern-detection and decision-support tools. "
            "They should not be presented as fully validated predictive models.",
            "gov",
        )

    # ── Governance & Roadmap ──────────────────────────────────────────────────
    with tab5:
        section_header("Governance & Roadmap",
            "From prototype to responsible production system.")

        g1,g2 = st.columns(2)
        with g1:
            info_card("What this system does today", (
                "Uses structured HR, performance, absence, and training data. "
                "Creates KPI signals, not final judgments. Builds a reliability-adjusted human capital "
                "value proxy. Uses AI segmentation to identify broad workforce patterns. "
                "Uses ONEValue AI to translate signals into experiments and learning questions."
            ))
        with g2:
            info_card("What this system does not do yet", (
                "Does not take live input from employees or managers yet. Does not train a supervised "
                "prediction model yet (no future outcome label is available). Does not automatically "
                "rank, sanction, or evaluate employees. Does not directly measure value creation; "
                "it estimates proxy signals."
            ))

        section_header("Implementation roadmap")
        wrapped_table(pd.DataFrame([
            {"Phase":"1. Prototype",          "Focus":"Structured KPIs, value proxy, AI segmentation",                                                             "Owner":"Student / Data team"},
            {"Phase":"2. Evolved prototype",  "Focus":"Document intelligence, recommendations, role-based views, ONEValue AI experiments",                         "Owner":"HR + Data/AI"},
            {"Phase":"3. Pilot",              "Focus":"Department-level testing, manager feedback loops, bias checks",                                               "Owner":"HR + managers"},
            {"Phase":"4. Scale",              "Focus":"Snowflake integration, governance workflows, supervised model monitoring",                                     "Owner":"Product Owner + HR"},
        ]))

        section_header("Governance principles")
        wrapped_table(pd.DataFrame([
            {"Principle":"Pseudonymised identifiers",    "Rationale":"Employee privacy must be protected at all times."},
            {"Principle":"No automatic sanctions",       "Rationale":"Outputs should start conversations, not trigger penalties."},
            {"Principle":"Display reliability first",    "Rationale":"Acting on unreliable data causes harm."},
            {"Principle":"Monitor bias",                 "Rationale":"Performance reviews and training access may be biased."},
            {"Principle":"AI as signal, not truth",      "Rationale":"Models have limitations; human judgment is essential."},
            {"Principle":"Experiments over decisions",   "Rationale":"Use signals to test which actions create sustainable value."},
        ]))

        section_header("Target architecture")
        wrapped_table(pd.DataFrame([
            {"Layer":"Data ingestion",   "Role":"Collect HR, absence, training, documents, and future operational data",                           "Future owner":"Data / IT"},
            {"Layer":"Data quality",     "Role":"Validate missingness, coverage, identifiers, and reliability",                                     "Future owner":"Data / HR governance"},
            {"Layer":"KPI engineering",  "Role":"Transform raw data into interpretable signals",                                                   "Future owner":"Data / HR analytics"},
            {"Layer":"AI layer",         "Role":"Detect segments, generate hypotheses, and support future predictions",                             "Future owner":"Data Science / AI"},
            {"Layer":"Decision layer",   "Role":"Log manager actions, employee feedback, experiments, and outcomes",                                "Future owner":"HR / Managers"},
            {"Layer":"Governance layer", "Role":"Ensure privacy, fairness, auditability, and human-in-the-loop use",                               "Future owner":"HR / Legal / Compliance"},
        ]))

    # ── Document Pipeline ─────────────────────────────────────────────────────
    with tab6:
        section_header("Document Pipeline",
            "Monitor unstructured document processing and theme extraction.")
        show_document_intelligence()