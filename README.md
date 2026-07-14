# Food Security and Nutrition Risk Insights System

**Track:** DSAI — IIT Mandi HimShikhar Program (AAI)
**Author:** Vaishali Gupta
🔗 **Live Demo:** https://food-security-risk-insights-y6spbmchssxvya62jgkuzn.streamlit.app
## Problem Statement

Food insecurity affects countries differently depending on how affordable,
available, safe, and sustainable their food systems are. This project analyzes
the Global Food Security Index (GFSI) 2022 to build a composite risk score,
categorize countries into risk tiers, and cluster them by food security
profile — helping policymakers, NGOs, and researchers identify which regions
need intervention first, and why.

## Users / Stakeholders

- Government food policy analysts
- NGOs and humanitarian aid organizations
- Researchers studying global food security trends

## Dataset

**Source:** Global Food Security Index (GFSI) 2022
**Records:** 113 countries, 5 usable indicators (Overall score + 4 pillar
scores: Affordability, Availability, Quality and Safety, Sustainability and
Adaptation)
**Note:** The dataset required minimal cleaning — no missing values or
duplicates were found. The main cleaning steps were dropping a redundant index
column and converting the `Rank` field from text (e.g. "1st", "=108th") into a
clean integer.

## Tools Used

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn (KMeans,
RandomForestRegressor), Google Colab

## Project Workflow

1. Load and inspect the dataset
2. Clean (drop index column, fix `Rank` formatting, strip whitespace)
3. Exploratory Data Analysis — score distributions and pillar correlations
4. Build a composite **risk score** (inverted Overall score) and classify into
   Low / Medium / High risk categories
5. **K-Means clustering** — group countries by food security profile
6. **Random Forest feature importance** — identify which pillar drives risk
   most
7. Save processed data for use in an interactive dashboard

## AI/ML Components

This project uses two complementary machine learning techniques:

**1. K-Means Clustering (Unsupervised)**
Groups the 113 countries into 3 clusters based on similarity across the four
pillar scores — revealing structural similarity between countries that a
single ranking can't show. Two countries with the same risk score can struggle
for very different reasons; clustering exposes that difference.

**2. Random Forest Feature Importance (Supervised)**
Trained to predict `risk_score` from the four pillars, not for future
prediction (the score is derived directly from these pillars), but purely as
an interpretability tool — to rank which pillar matters most in driving
overall risk.

Together: clustering answers **"who is at risk, and in what way,"** while
feature importance answers **"what's driving that risk in general."**

## How to Run


**Option 1 — Try it live (recommended):**
🔗 https://food-security-risk-insights-y6spbmchssxvya62jgkuzn.streamlit.app

**Option 2 — Run locally:**
1. Clone this repository:

## Results and Insights

**Highest-risk countries:** Syria, Haiti, Yemen, Sierra Leone, and Madagascar
scored highest on the composite risk score, consistent with real-world food
security assessments — validating the scoring approach.

**Cluster profiles:**
- **Cluster 1** (Overall ≈ 75.1): Strongest across all four pillars — likely
  wealthier, more food-secure nations.
- **Cluster 0** (Overall ≈ 60.75): Mid-range across all pillars, with
  Sustainability and Adaptation as the relative weak point.
- **Cluster 2** (Overall ≈ 45.6): Weakest across *every* pillar
  simultaneously — broad, compounding vulnerability rather than a single point
  of failure. All four highest-risk countries (Syria, Haiti, Yemen, Sierra
  Leone) fall into this cluster, confirming agreement between the risk score
  and clustering methods.

**Cluster validation:** Silhouette score of 0.327 — a moderate, reasonable
separation given the gradual, real-world nature of country-level food
security data.

**Top risk driver:** Random Forest feature importance identified **Quality and
Safety** (0.49) and **Affordability** (0.37) as the two dominant drivers of
overall risk, together accounting for over 86% of predictive weight —
substantially more than Availability (0.10) or Sustainability and Adaptation
(0.04). This suggests interventions targeting food quality/safety standards
and affordability are likely to have the greatest impact on a country's
overall food security standing.

## Limitations

- The GFSI composite score simplifies complex, multi-dimensional food systems
  into a single number and may not capture rapid shocks (e.g. conflict,
  sudden price spikes) occurring after the data was published.
- Risk categorization by quantiles is relative to this dataset's 113
  countries, not an absolute global threshold.
- Random Forest feature importance is used for interpretability only, not
  prediction — the target variable is derived directly from the same
  features used to train it.
- This tool is intended to support, not replace, expert humanitarian
  assessment.

## Future Improvements

- Incorporate multi-year time-series data to detect trends and forecast risk
- Break down each pillar into its sub-indicators for finer-grained analysis
- Expand the Streamlit dashboard with regional comparison and filtering
- Explore alternative clustering algorithms (e.g. hierarchical clustering) to
  cross-validate the K-Means groupings

## Team

Vaishali Gupta
