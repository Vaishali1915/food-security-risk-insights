# config.py
# Central place for project settings — change values here instead of inside app.py

DATA_FILE = 'processed_food_security.csv'

PILLARS = [
    'Affordability',
    'Availability',
    'Quality and Safety',
    'Sustainability and Adaptation'
]

CLUSTER_LABELS = {
    0: "Cluster 0 — Moderate Risk",
    1: "Cluster 1 — Food Secure",
    2: "Cluster 2 — High Risk (Compounding Vulnerability)"
}

RISK_CATEGORY_BINS = 3  # number of risk tiers (Low/Medium/High)

APP_TITLE = "🌾 Food Security and Nutrition Risk Insights System"
APP_CAPTION = "Based on the Global Food Security Index (GFSI) 2022"

DISCLAIMER = (
    "⚠️ This risk score is a simplified composite index and should not replace "
    "expert humanitarian assessment. Built for the IIT Mandi HimShikhar DSAI program."
)