# ONEValue @ CACEIS — Code Review
### Dangers, Bugs & Recommendations

---

> **How to read this document**
> Issues are grouped by severity: **High** (will cause crashes or wrong results), **Medium** (silent failures or data integrity risks), **Low** (maintainability and performance).
> Items marked ✅ have already been fixed in the codebase.

---

## HIGH SEVERITY

### ✅ 1. `display()` crashes outside Jupyter
**File:** `src/data_cleaning.py` — line 128
`display(df.head())` is a Jupyter built-in. Running the pipeline as a plain Python script raises `NameError` and the entire cleaning script crashes.
**Fix applied:** Replaced with `print(df.head().to_string())`.

---

### ✅ 2. `DataFrame.get()` does not exist
**File:** `dashboard/final version/streamlit_app_v5.py` — lines 768–769
`.get()` is a dict method, not a DataFrame method. Calling it raises `AttributeError` on startup whenever an expected column is absent from the CSV.
**Fix applied:** Replaced with explicit `if "column" not in df.columns:` guards.

---

### ✅ 3. Silent "all Low" risk labels when absence data is missing
**File:** `src/risk_prediction.py` — lines 29–41
If `absenteeism_risk_score` is all-NaN, `.quantile()` returns NaN. Any comparison `x >= NaN` is False — so every employee silently gets "Low" risk. HR sees a clean table with no high-risk profiles when data is simply absent.
**Fix applied:** Added NaN validation on quantiles; falls back to "Unknown" with a warning. Also fixed stale segment name strings left over from a previous version.

---

### ✅ 4. Silent data loss in talent progression
**File:** `src/kpi_engineering.py` — lines 188–215
`summary` is built with `.drop_duplicates()` keeping only first-occurrence indices. Assigning `summary["col"] = df["col"]` then aligns by index and silently drops all rows except the first per employee.
**Fix applied:** Replaced with `groupby(employee_col).agg("max")` so all rows per employee are considered.

---

### ✅ 5. Median imputation with no NaN validation
**File:** `src/integrated_value_ai.py` — lines 69–75
If `performance_score` is entirely missing, `.median()` returns NaN. `fillna(NaN)` does nothing — NaN values propagate silently into the value potential score.
**Fix applied:** Median is validated before use; falls back to `0.5` (neutral) with a printed warning.

---

## MEDIUM SEVERITY

### ✅ 6. Race condition in context logging
**File:** `dashboard/final version/streamlit_app_v5.py` — `append_log()`
Two simultaneous submissions both read the same old file, both append in memory, and the second write overwrites the first. One submission is silently lost.
**Fix applied:** Wrapped in `fcntl.flock` exclusive lock — one write at a time.

---

### ✅ 7. Silent document processing failures
**File:** `src/document_theme_extraction.py` — lines 34–62
Bare `except: pass` swallows every error including `MemoryError`. Failed documents produce no output and no indication anything went wrong.
**Fix applied:** Replaced with `except Exception as e: print(...)`.

---

### 8. Hard-coded column name breaks on data changes
**File:** `src/integrated_value_ai.py` — ~line 295
`libelle_organisation_niveau_07` is hard-coded. A minor rename in CACEIS's HR export causes a `KeyError` crash with no useful message.
**Recommendation:** Move all source column names into a single `COLS = {...}` dictionary at the top of the file (or a shared `config.py`). One change propagates everywhere.

---

### 9. Dashboard shows `0.5` defaults with no indication data is missing
**File:** `dashboard/final version/streamlit_app_v5.py` — `_col()` / `_norm()` helpers
When a column is absent, helpers silently return `0.5`. Signal cards render normally with placeholder values. Managers and HR have no way to know they are not looking at real data.
**Recommendation:** When a fallback is used, show the existing "No data" badge instead of a number. The badge system already exists — just use it.

---

### 10. `@st.cache_data` serves stale data after pipeline reruns
**File:** `dashboard/final version/streamlit_app_v5.py` — `load_data()`
CSVs are cached indefinitely. If the pipeline is rerun while the dashboard is open, users see old data with no warning.
**Recommendation:**
```python
@st.cache_data(ttl=3600)  # refresh every hour
def load_data(): ...
```
Or add a "Refresh data" button in the sidebar that calls `st.cache_data.clear()`.

---

### 11. Context log rewrites entire file on every submission
**File:** `dashboard/final version/streamlit_app_v5.py` — `append_log()`
Every submission reads the full CSV, concatenates one row, and writes the whole file back. At production scale this is O(n) per submission.
**Recommendation:** Use SQLite for production. For the prototype, at minimum:
```python
new_row.to_csv(path, mode="a", header=not path.exists(), index=False)
```

---

## LOW SEVERITY

### 12. Fragile string-based null handling
**File:** `src/data_cleaning.py` — lines 59–60
`replace({"nan": None, "None": None})` only catches literal strings. Real float `NaN` values pass through, leaving mixed null types in the data.
**Recommendation:** Use `df.replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})` as a global pass, then use `pd.notna()` for downstream checks.

---

### 13. Performance score std deviation undefined for single-review employees
**File:** `src/kpi_engineering.py` — ~line 124
`.std()` on a single value returns `NaN`. No fallback. Consistency score becomes NaN and propagates silently.
**Recommendation:**
```python
consistency = series.std()
if pd.isna(consistency):
    consistency = 0.0
```

---

### 14. KMeans crashes if fewer than 4 distinct profiles exist
**File:** `src/integrated_value_ai.py` — ~line 265
`KMeans(n_clusters=4)` is hard-coded. Small test datasets or all-identical feature values cause a crash or degenerate clusters.
**Recommendation:**
```python
n_clusters = min(4, len(scaled_data))
if n_clusters < 2:
    df["ai_segment"] = 0
else:
    kmeans = KMeans(n_clusters=n_clusters, ...)
```

---

### 15. Non-ASCII characters may be corrupted on import
**File:** `src/integrated_value_ai.py` — lines 26–43
`encoding="utf-8-sig"` assumes BOM-prefixed files. Standard UTF-8 files without a BOM may corrupt French accented characters.
**Recommendation:**
```python
try:
    df = pd.read_csv(path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(path, encoding="latin-1")
```

---

### 16. Theme classification has false positives from substring matching
**File:** `dashboard/final version/streamlit_app_v5.py` — ~line 1103
Keywords are matched anywhere in text — "business" matches "busy", "discussion" matches partial patterns. Context entries may be miscategorised.
**Recommendation:** Match on whole words:
```python
import re
def has_keyword(text, keyword):
    return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
```

---

### 17. Duplicate archetype logic in two files
**Files:** `src/recommendation_engine.py` and `src/onevalue_ai_layer.py`
Both files independently implement archetype-to-signal mapping. A change to one must be manually mirrored in the other.
**Recommendation:** Extract into a shared `src/archetypes.py` module that both files import.

---

## PRODUCTION READINESS CHECKLIST

| Item | Status | Priority |
|------|--------|----------|
| Replace CSV storage with a database | Not done | High |
| GDPR-compliant data handling (consent, right to deletion) | Not done | High |
| Replace demo login with real authentication | Not done | High |
| Column name configuration instead of hard-coded strings | Not done | Medium |
| Add supervised outcome labels to improve AI beyond clustering | Not done | Medium |
| Model monitoring (detect signal drift over time) | Not done | Medium |
| Validate expected columns exist on pipeline startup | Not done | Medium |
| Add `ttl` to cache or expose a manual refresh button | Not done | Low |
| Whole-word regex for theme classification | Not done | Low |
| Consolidate archetype logic into a shared module | Not done | Low |

---