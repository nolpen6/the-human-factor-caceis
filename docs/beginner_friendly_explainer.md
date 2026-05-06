# ONEValue @ CACEIS — Beginner-Friendly Explainer
### What we built, why we built it, and how it works

---

> **Who this is for:** Anyone curious about the thinking behind ONEValue — no technical background required. If you've used the demo, this document explains what was happening under the hood.

---

## Part 1 — The Big Idea: What's Wrong With Traditional HR Dashboards?

Imagine your company tracks three things for every employee: their annual performance review score, how many days they were absent, and how many training courses they completed. At the end of the year, you add those numbers up into a single "score" and use it to decide who gets promoted, who gets flagged, and who gets let go.

Sounds logical. But there's a serious problem with this approach — and it's the problem that ONEValue was built to solve.

**The problem: numbers are not the same thing as value.**

A high performance score tells you something happened. It does not tell you *why* it happened, whether it was sustainable, whether the person had great conditions or terrible ones, or whether it will happen again next year. A low absence count might mean someone is healthy and motivated — or it might mean someone is afraid to take sick days. A high training count might mean genuine learning — or it might mean a manager who ticks boxes.

When you treat a number as if it *is* the truth, you make bad decisions. You reward the wrong things. You miss the real risks. And you can cause serious harm to the people being measured.

This is not a new observation. It is the central argument of a landmark piece of research from INSEAD.

---

## Part 2 — The INSEAD Paper: Indicators Are Not Value

**INSEAD** is one of the world's leading business schools, based in France. Their researchers — working on what they call the **"Blue-Line framework"** — made a deceptively simple argument:

> *Observable KPIs (Key Performance Indicators) are not value. They are signals — noisy, incomplete traces of the conditions and behaviors that may create, sustain, or destroy value over time.*

Think of it this way. A thermometer reading of 38.5°C is not the same thing as a fever. The temperature is a signal. The fever is what's actually happening. A good doctor looks at the temperature alongside other signals, asks the patient questions, considers the context — and then forms a judgment. They do not say: "Your temperature is 38.5°C, therefore you are sick and will miss work for 3 days." That would be absurd. Yet that is essentially what most HR KPI dashboards do.

The INSEAD framework proposes two contrasting approaches:

| | The Red-Line Approach ❌ | The Blue-Line Approach ✅ |
|--|--|--|
| **What it does** | Measures KPIs and treats them as value | Treats KPIs as signals and asks what they reveal |
| **Time horizon** | Looks backwards (what happened?) | Looks forwards (what conditions are in place?) |
| **Focus** | Individual metrics | System conditions and behaviors |
| **Risk** | Rewards visible output, misses hidden pressure | Asks whether value creation is sustainable |
| **Conclusion** | "Your score is 3.8 out of 5" | "This pattern suggests a conversation is needed" |

The Blue-Line framework asks three questions that a Red-Line dashboard never asks:
1. Is this contribution being created **sustainably** — or is the person burning out to produce it?
2. Is this person **investing in future capability** — or only delivering on current tasks?
3. Do we have **enough reliable data** to draw any conclusion at all?

These three questions became the foundation of ONEValue.

---

## Part 3 — The Brainstorming: From Paper to Prototype

### Stage 1: What data does CACEIS already have?

The first question was simple: what signals do we actually have access to, without building anything new?

CACEIS already maintained four sources of HR data:
- **HR Master Data** — who works here, in what role, for how long, in which department
- **Performance Reviews** — annual scores (on a 0–5 scale)
- **Absence Records** — how many absence events, how many total days absent
- **Training Records** — how many training courses, how many hours of training

The insight was that by combining them through the lens of the Blue-Line framework, they could become something far more useful than four separate numbers.

### Stage 2: What questions should the system answer?

Rather than asking "how do we score employees?", the design question became: **what decisions do managers and HR need to make, and what would actually help them?**

Four different perspectives emerged:
- **The employee** wants to understand their own situation and know what to do next — not be judged by a number.
- **The manager** wants to know who on their team needs a conversation and what to say — not a ranking.
- **HR** wants to see workforce-level patterns and flag risks early — not make individual decisions automatically.
- **The product owner** wants to know whether the system is trustworthy and what its limitations are.

### Stage 3: What should we refuse to do?

The most important brainstorming question was: **what must this system never do?**

- Never automatically rank employees against each other
- Never trigger an HR decision without human review
- Never show a strong conclusion when the underlying data is weak
- Never present an indicator as if it were a judgment of someone's worth

This is where the concept of **interpretation confidence** came from. If the data on a particular person is incomplete, the system says so explicitly and reduces its own confidence level.

### Stage 4: How do we make it honest about uncertainty?

The final design insight was the **reliability-adjusted score**. Instead of just computing a value potential score and displaying it, the system multiplies that score by a confidence factor. If the data is strong and complete, the confidence is high. If the data is patchy, the adjusted score drops — forcing humility into every conclusion.

---

## Part 4 — The Calculations: How It Actually Works

### Step 1: Gather the raw data

For each of CACEIS's ~3,765 employees, the system collects performance scores, absence records, training records, and career progression data.

### Step 2: Turn raw numbers into signals (0 to 1)

Every raw number is converted into a **percentile score** between 0 and 1, showing where this person sits relative to the whole organisation. This makes every signal comparable across departments and roles.

### Step 3: Build the four core signals

**Contribution Signal** — built from performance review scores. Higher = more visible current output.

**Learning / Future Value Signal** — built equally from training course count and training hours:
```
Learning Signal = 50% × (training count percentile)
               + 50% × (training hours percentile)
```

**Sustainability Signal** — built from absence data, inverted:
```
Absenteeism Risk = 40% × (absence events percentile)
                 + 60% × (absence days percentile)

Sustainability Signal = 1 − Absenteeism Risk
```
*Absence days are weighted more (60%) than events (40%) because a single long absence carries different implications than several short ones.*

**Progression Signal** — built from promotions, role changes, and tenure progression.

### Step 4: Compute Interpretation Confidence

The system checks how much data exists for each person:
```
Data Coverage = average of:
    - Has performance record? (yes = 1, no = 0)
    - Has absence record?     (yes = 1, no = 0)
    - Has training record?    (yes = 1, no = 0)
```
If data is flagged as incomplete, coverage is halved as an additional penalty. This becomes the **Interpretation Confidence** (0 to 1).

### Step 5: Compute the Value Potential Score

```
Value Potential = 35% × Contribution Signal
               + 30% × Learning Signal
               + 20% × Sustainability Signal
               + 15% × Progression Signal
```

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Contribution | 35% | Most directly observable signal |
| Learning | 30% | Second most strategically important |
| Sustainability | 20% | Durability matters — but is a lagging indicator |
| Progression | 15% | Important but least complete data source |

### Step 6: Apply the reliability adjustment

```
Reliability-Adjusted Value = Value Potential × Interpretation Confidence
Interpretation Risk         = Value Potential × (1 − Interpretation Confidence)
```

**Example:** An employee has a Value Potential of 0.80 but Interpretation Confidence of only 0.45 (missing training records).

> Reliability-Adjusted Value = 0.80 × 0.45 = **0.36**
> The system displays: "High potential signal — but low confidence. Do not act on this without better data."

### Step 7: Assign a Valuation Archetype

Each employee is classified into one of seven readable patterns:

| Archetype | What it means |
|-----------|---------------|
| **Sustainable Value Builder** | High contribution + high learning + sustainable pace |
| **Value Under Pressure** | High contribution + low sustainability (fragile pattern) |
| **Strong Contributor / Low Development** | Delivering today, not visibly investing in tomorrow |
| **Future Value Builder** | High learning, contribution may not be fully visible yet |
| **Low Learning Visibility** | Low signals across learning and contribution |
| **Under-Observed Profile** | Not enough reliable data to say anything safely |
| **Stable / Monitor** | No strong positive or negative signal |

Each archetype comes with a **Blue-Line question** — a prompt for a human conversation, not a verdict.

### Step 8: Run AI Segmentation

The system uses **KMeans clustering** to find natural groupings across the whole workforce — like finding clusters of dots on a map. Four clusters are identified and labelled:

- Operational continuity risk
- Learning-intensive profile
- High sustainable value potential
- Stable baseline profile

These are patterns for discovery, not rankings.

### Step 9: Generate Recommendations

Each profile gets a recommended action, a priority level, and a governance guardrail — all designed as prompts for a human decision, never automatic actions.

---

## Part 5 — The Five Principles

1. **Start with signals, not conclusions.**
2. **Interpret value through context, not scores.**
3. **Focus on decisions and behaviors.**
4. **Use AI to find patterns, not judge people.**
5. **Always validate signals before acting.**

---