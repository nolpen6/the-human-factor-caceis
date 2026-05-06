# ONEValue @ CACEIS — Data Enrichment Roadmap
### What to add, why it matters, and when to pursue it

---

> **Core principle:** We are not collecting more data to rank people better.
> We are collecting better signals to understand *how* sustainable value is created — and *which conditions* support or destroy it.
> Every enrichment proposed here must answer a Blue-Line question, not just add a number.

---

## What We Have Today

| Source | Signal produced | Limitation |
|--------|----------------|------------|
| Performance reviews | Contribution signal | One review per year — retrospective, low frequency |
| Absence records | Sustainability signal (inverted) | Lagging indicator — absence appears *after* pressure builds |
| Training records | Learning signal | Captures volume, not quality or application |
| HR master data | Progression signal, data coverage | Tenure and role changes only — no behavior |

**The gap:** We can see *outcomes* (a score, an absence, a course completed). We cannot yet see *why* they happened or whether the conditions that produced them still exist.

---

## Enrichment Priorities

Enrichments are organised into three phases aligned with the project roadmap.

---

## Phase 1 — High Impact, Low Friction
*Data that likely already exists inside CACEIS systems*

---

### 1.1 Workload & Time Allocation

**Blue-Line question:** Is performance being created sustainably, or through overload?

**What to capture:**
- Hours worked vs. contracted hours (overtime patterns)
- Meeting load per week (calendar data)
- Peak workload periods by team and role
- Task backlog or queue depth

**Why it matters:**
The current sustainability signal uses absence as a proxy for pressure — but absence is a *lagging* indicator. Workload data gives a *leading* signal: we can detect pressure before it becomes absence. A manager can intervene earlier.

**Where it likely lives:** Timekeeping systems, calendar tools (Outlook/Teams), project management platforms.

**Signal it would improve:** Sustainability Signal — replacing a lagging absence proxy with a real-time workload indicator.

---

### 1.2 Training Quality & Application

**Blue-Line question:** Is learning investment translating into capability, or just completing hours?

**What to capture:**
- Post-training assessment scores (did understanding improve?)
- Time between training completion and on-the-job application
- Manager confirmation of skill applied (brief structured feedback)
- Whether training matched a stated development need

**Why it matters:**
Currently the learning signal counts training hours and course volume. A person can complete 40 hours of low-relevance e-learning and score identically to someone who completed a 40-hour certification directly linked to their role. Quality matters.

**Where it likely lives:** LMS (Learning Management System) — CACEIS almost certainly has post-training scores already captured but unused.

**Signal it would improve:** Learning / Future Value Signal — from volume proxy to applied capability indicator.

---

### 1.3 Role Complexity & Scope

**Blue-Line question:** Are we comparing people who are doing fundamentally different jobs?

**What to capture:**
- Number of funds/clients managed per person
- Process complexity rating by role (standardised or manager-assessed)
- Cross-team or cross-department responsibilities
- Regulatory complexity of the role

**Why it matters:**
A performance score of 3.8 means something different for a fund administrator managing 5 simple funds vs. one managing 20 complex multi-asset structures. Without role complexity, we are comparing apples and oranges. This enrichment does not change the score — it contextualises it.

**Where it likely lives:** HR master data, operations systems, manager assessment (lightweight form).

**Signal it would improve:** Contribution Signal — adjusting for role scope so comparisons are fair.

---

## Phase 2 — Deeper Signals, Moderate Effort
*Data that requires new collection or system integration*

---

### 2.1 Informal Contribution

**Blue-Line question:** Who creates value that the formal system never records?

**What to capture:**
- Peer recognition logs (structured, not social-media style)
- Mentoring or onboarding support given
- Crisis or peak-period voluntary contributions
- Knowledge sharing (documentation written, sessions run)

**Why it matters:**
The formal performance system captures individual output. It misses the person who keeps the team functioning — the one who onboards every new joiner, answers the questions no one else has time for, and holds the knowledge that would be lost if they left. This is often where real continuity risk lives.

**Collection approach:** A lightweight structured form (monthly, 3 questions max) — not a social feed. Employee and manager both contribute. Data feeds the context log already in the system.

**Signal it would improve:** Contribution Signal and Progression Signal — surfaces hidden value that formal KPIs miss.

---

### 2.2 Decision & Learning Loops

**Blue-Line question:** Are teams learning from what they do, or repeating the same mistakes?

**What to capture:**
- Manager-logged experiments: hypothesis → action → expected outcome → actual result
- Error reduction rate after a process change
- Whether a recommendation from the system was acted on
- Outcome of the action (did the signal improve?)

**Why it matters:**
This is the feature that would most directly operationalise the Blue-Line framework. Value is created through *decisions and behaviors*, not just through outcomes. Capturing decision loops closes the feedback cycle: we would know whether the coaching conversation actually changed anything.

**Collection approach:** A structured tab in the Manager view ("Experiments & Learning") — already partially designed in the dashboard. Manager logs: decision taken, hypothesis, action, review date, observed outcome.

**Signal it creates:** A new signal — **Decision Quality / Learning Loop Score** — which would eventually become an input to the value model.

---

### 2.3 Wellbeing & Sustainability Perception

**Blue-Line question:** Are people telling us something is wrong before it becomes a data point?

**What to capture:**
- Short periodic pulse surveys (3–5 questions, quarterly maximum)
  - "My current workload feels manageable"
  - "I feel I have opportunities to develop in my role"
  - "I feel recognised for my contribution"
- Voluntary self-reported workload flags (already partially in the "Add Context" tab)

**Why it matters:**
Absence data is a lagging signal. Survey data is a leading one. An employee who answers "strongly disagree" to workload manageability in Q1 is giving us advance notice of a Q3 absence pattern. The goal is not surveillance — it is the same as the context log: giving employees a voice before a data point appears.

**Governance note:** Survey data must be genuinely voluntary, never individually scored without consent, and always shown to the employee before shown to management. The data policy already in the system covers this — it just needs to be explicitly extended.

**Signal it would improve:** Sustainability Signal — from absence-inverted to a composite of behavioral and perceived sustainability.

---

## Phase 3 — Strategic Intelligence
*External data to contextualise internal signals*

---

### 3.1 Skills Market Alignment

**Blue-Line question:** Is our workforce developing toward where the market is going, or away from it?

**What to capture:**
- External job posting data for roles equivalent to CACEIS positions (demand signals)
- Skill taxonomy mapping (ESCO or O*NET) linking current roles to required competencies
- Certification and credential market data (what qualifications are employers requiring?)

**Why it matters:**
A low learning signal is more concerning if the employee is in a fast-changing role (e.g. fund administration with growing automation exposure) than in a stable, specialist role. Without external context, we cannot distinguish "learning gap that matters" from "learning gap in a stable role."

**How to use it:** Not to score individuals differently — but to flag *roles* where the gap between current learning investment and market skill demand is widest. This becomes a workforce planning signal for HR, not an individual risk flag.

---

### 3.2 Regulatory & Compliance Skill Demand

**Blue-Line question:** Are we building the compliance capabilities that regulators will require?

**What to capture:**
- Regulatory change calendar (AIFMD, EMIR, MiFID updates relevant to asset services)
- Compliance training completion rates by regulatory domain
- Gap between required certifications and current certifications held

**Why it matters:**
CACEIS operates in a heavily regulated environment. A skill gap that is invisible in today's data becomes a critical risk when a regulatory deadline arrives. This enrichment connects the learning signal directly to operational and regulatory risk.

---

### 3.3 Sector Benchmarking

**Blue-Line question:** How does our workforce investment compare to peer organisations?

**What to capture:**
- Industry-average training hours per employee (asset services sector)
- Absence rates benchmarked against financial services norms
- Retention and internal mobility rates vs. sector

**Why it matters:**
A sustainability signal of 0.65 is good — but is it good *for CACEIS's sector*? Benchmarks contextualise internal signals and help HR prioritise where investment is most differentiated vs. where it simply matches the market baseline.

---

## What Enrichment Does Not Mean

To be explicit about the governance position:

| This roadmap is NOT about | This roadmap IS about |
|--------------------------|----------------------|
| Scoring employees more precisely | Understanding value creation conditions better |
| Building a more powerful ranking system | Adding leading indicators before lagging ones appear |
| Collecting data for its own sake | Answering specific Blue-Line questions |
| Surveillance of work patterns | Giving employees and managers better information |

Every new data source proposed here must pass this test before collection begins:

> **"Which Blue-Line question does this answer, and would the employee understand why this data helps them?"**

If the answer to either part is no, the data should not be collected.

---

## Summary Table

| Enrichment | Phase | Blue-Line question answered | Signal improved | Effort |
|------------|-------|-----------------------------|-----------------|--------|
| Workload & time allocation | 1 | Is performance sustainable? | Sustainability | Low |
| Training quality & application | 1 | Is learning translating into capability? | Learning | Low |
| Role complexity & scope | 1 | Are we comparing fairly? | Contribution | Low |
| Informal contribution | 2 | Who is invisible in the data? | Contribution, Progression | Medium |
| Decision & learning loops | 2 | Are teams learning from actions? | New signal | Medium |
| Wellbeing pulse surveys | 2 | What are people telling us before absence? | Sustainability | Medium |
| Skills market alignment | 3 | Are we building the right capabilities? | Learning (contextualised) | High |
| Regulatory skill demand | 3 | Are we prepared for compliance changes? | Learning, Risk | High |
| Sector benchmarking | 3 | How do we compare? | All signals (contextualised) | High |

---