import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import config

st.set_page_config(page_title="Food Security Risk Insights", page_icon="🌾", layout="wide")

st.title(config.APP_TITLE)
st.caption(config.APP_CAPTION)

# --- Load data (cached + with error handling) ---
@st.cache_data
def load_data():
    return pd.read_csv(config.DATA_FILE)

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'processed_food_security.csv' is in the same folder as this app.")
    st.stop()

pillars = config.PILLARS
cluster_labels = config.CLUSTER_LABELS
df['cluster_label'] = df['cluster'].map(cluster_labels)

# --- Continent mapping ---
continent_map = {
    'Afghanistan': 'Asia', 'Albania': 'Europe', 'Algeria': 'Africa', 'Angola': 'Africa',
    'Argentina': 'South America', 'Armenia': 'Asia', 'Australia': 'Oceania', 'Austria': 'Europe',
    'Azerbaijan': 'Asia', 'Bahrain': 'Asia', 'Bangladesh': 'Asia', 'Belarus': 'Europe',
    'Belgium': 'Europe', 'Benin': 'Africa', 'Bolivia': 'South America', 'Botswana': 'Africa',
    'Brazil': 'South America', 'Bulgaria': 'Europe', 'Burkina Faso': 'Africa', 'Burundi': 'Africa',
    'Cambodia': 'Asia', 'Cameroon': 'Africa', 'Canada': 'North America', 'Chad': 'Africa',
    'Chile': 'South America', 'China': 'Asia', 'Colombia': 'South America', 'Costa Rica': 'North America',
    'Croatia': 'Europe', "Cote d'Ivoire": 'Africa', "Côte d'Ivoire": 'Africa', 'Cuba': 'North America', 'Czech Republic': 'Europe',
    'Democratic Republic of Congo': 'Africa', 'Denmark': 'Europe', 'Dominican Republic': 'North America',
    'Ecuador': 'South America', 'Egypt': 'Africa', 'El Salvador': 'North America', 'Eritrea': 'Africa',
    'Estonia': 'Europe', 'Ethiopia': 'Africa', 'Finland': 'Europe', 'France': 'Europe', 'Gabon': 'Africa',
    'Georgia': 'Asia', 'Germany': 'Europe', 'Ghana': 'Africa', 'Greece': 'Europe', 'Guatemala': 'North America',
    'Guinea': 'Africa', 'Haiti': 'North America', 'Honduras': 'North America', 'Hungary': 'Europe',
    'India': 'Asia', 'Indonesia': 'Asia', 'Iran': 'Asia', 'Iraq': 'Asia', 'Ireland': 'Europe',
    'Israel': 'Asia', 'Italy': 'Europe', 'Jamaica': 'North America', 'Japan': 'Asia', 'Jordan': 'Asia',
    'Kazakhstan': 'Asia', 'Kenya': 'Africa', 'Kuwait': 'Asia', 'Laos': 'Asia', 'Latvia': 'Europe',
    'Lebanon': 'Asia', 'Liberia': 'Africa', 'Libya': 'Africa', 'Lithuania': 'Europe', 'Madagascar': 'Africa',
    'Malawi': 'Africa', 'Malaysia': 'Asia', 'Mali': 'Africa', 'Mauritania': 'Africa', 'Mexico': 'North America',
    'Moldova': 'Europe', 'Mongolia': 'Asia', 'Morocco': 'Africa', 'Mozambique': 'Africa', 'Myanmar': 'Asia',
    'Namibia': 'Africa', 'Nepal': 'Asia', 'Netherlands': 'Europe', 'New Zealand': 'Oceania',
    'Nicaragua': 'North America', 'Niger': 'Africa', 'Nigeria': 'Africa', 'North Korea': 'Asia',
    'Norway': 'Europe', 'Oman': 'Asia', 'Pakistan': 'Asia', 'Panama': 'North America',
    'Papua New Guinea': 'Oceania', 'Paraguay': 'South America', 'Peru': 'South America',
    'Philippines': 'Asia', 'Poland': 'Europe', 'Portugal': 'Europe', 'Qatar': 'Asia', 'Romania': 'Europe',
    'Russia': 'Europe', 'Rwanda': 'Africa', 'Saudi Arabia': 'Asia', 'Senegal': 'Africa', 'Serbia': 'Europe',
    'Sierra Leone': 'Africa', 'Singapore': 'Asia', 'Slovakia': 'Europe', 'Slovenia': 'Europe',
    'Somalia': 'Africa', 'South Africa': 'Africa', 'South Korea': 'Asia', 'South Sudan': 'Africa',
    'Spain': 'Europe', 'Sri Lanka': 'Asia', 'Sudan': 'Africa', 'Sweden': 'Europe', 'Switzerland': 'Europe',
    'Syria': 'Asia', 'Taiwan': 'Asia', 'Tajikistan': 'Asia', 'Tanzania': 'Africa', 'Thailand': 'Asia',
    'Togo': 'Africa', 'Tunisia': 'Africa', 'Turkey': 'Asia', 'Uganda': 'Africa', 'Ukraine': 'Europe',
    'United Arab Emirates': 'Asia', 'United Kingdom': 'Europe', 'United States': 'North America',
    'Uruguay': 'South America', 'Uzbekistan': 'Asia', 'Venezuela': 'South America', 'Vietnam': 'Asia',
    'Yemen': 'Asia', 'Zambia': 'Africa', 'Zimbabwe': 'Africa'
}
df['continent'] = df['Country'].map(continent_map)
df['continent'] = df['continent'].fillna('Other')

# --- Intro text ---
st.markdown("""
This dashboard analyzes food security risk across 113 countries using the
**Global Food Security Index (GFSI) 2022**. It combines a composite risk score,
K-Means clustering, and Random Forest feature importance to help identify
which countries face the highest risk — and why.

📌 **Data snapshot:** GFSI 2022. This is not updated in real time.
""")

# --- At a Glance summary panel ---
st.divider()
st.subheader("📌 At a Glance")

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Total Countries", len(df))
col_b.metric("High Risk", (df['risk_category'] == 'High').sum())
col_b.write(f"{round((df['risk_category']=='High').sum() / len(df) * 100)}% of countries")
col_c.metric("Medium Risk", (df['risk_category'] == 'Medium').sum())
col_c.write(f"{round((df['risk_category']=='Medium').sum() / len(df) * 100)}% of countries")
col_d.metric("Low Risk", (df['risk_category'] == 'Low').sum())
col_d.write(f"{round((df['risk_category']=='Low').sum() / len(df) * 100)}% of countries")

st.metric("Global Average Risk Score", f"{df['risk_score'].mean():.1f}")

st.divider()

# --- Sidebar filters ---
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Filter by Risk Category",
    options=df['risk_category'].unique(),
    default=list(df['risk_category'].unique())
)

score_range = st.sidebar.slider(
    "Filter by Risk Score Range",
    min_value=float(df['risk_score'].min()),
    max_value=float(df['risk_score'].max()),
    value=(float(df['risk_score'].min()), float(df['risk_score'].max()))
)

continent_filter = st.sidebar.multiselect(
    "Filter by Continent",
    options=sorted(df['continent'].unique()),
    default=sorted(df['continent'].unique())
)

filtered_df = df[
    (df['risk_category'].isin(risk_filter)) &
    (df['risk_score'] >= score_range[0]) &
    (df['risk_score'] <= score_range[1]) &
    (df['continent'].isin(continent_filter))
]

# --- Country lookup ---
st.subheader("🔍 Look up a country")
country = st.selectbox("Select a country", sorted(df['Country'].unique()))
row = df[df['Country'] == country].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Risk Score", f"{row['risk_score']:.1f}")
col2.metric("Risk Category", row['risk_category'])
col3.write("**Cluster Group**")
col3.write(f"### {row['cluster_label']}")

st.write("**Pillar breakdown:**")
pillar_cols = st.columns(4)
for i, p in enumerate(pillars):
    pillar_cols[i].metric(p, f"{row[p]:.1f}")

# --- Radar chart for selected country ---
radar_values = [row[p] for p in pillars] + [row[pillars[0]]]
radar_labels = pillars + [pillars[0]]

fig_radar = px.line_polar(
    r=radar_values,
    theta=radar_labels,
    line_close=True,
    title=f"{country} — Pillar Profile"
)
fig_radar.update_traces(fill='toself')
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")

st.divider()

# --- Country Comparison ---

# --- Country Comparison ---
st.subheader("⚖️ Compare Two Countries")
compare_col1, compare_col2 = st.columns(2)
country_a = compare_col1.selectbox("Country A", sorted(df['Country'].unique()), index=0, key="country_a")
country_b = compare_col2.selectbox("Country B", sorted(df['Country'].unique()), index=1, key="country_b")

row_a = df[df['Country'] == country_a].iloc[0]
row_b = df[df['Country'] == country_b].iloc[0]

comparison_data = {
    'Metric': ['Risk Score', 'Risk Category', 'Cluster'] + pillars,
    country_a: [f"{row_a['risk_score']:.1f}", row_a['risk_category'], row_a['cluster_label']] + [f"{row_a[p]:.1f}" for p in pillars],
    country_b: [f"{row_b['risk_score']:.1f}", row_b['risk_category'], row_b['cluster_label']] + [f"{row_b[p]:.1f}" for p in pillars]
}
comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

fig_compare = px.bar(
    x=pillars,
    y=[row_a[p] for p in pillars],
    title=f"{country_a} vs {country_b} — Pillar Comparison"
)
fig_compare.add_bar(x=pillars, y=[row_b[p] for p in pillars], name=country_b)
fig_compare.data[0].name = country_a
fig_compare.update_layout(barmode='group', showlegend=True)
st.plotly_chart(fig_compare, use_container_width=True, key="compare_chart")

st.divider()

# --- World map ---
st.subheader("🗺️ Global Risk Map")
fig_map = px.choropleth(
    df,
    locations='Country',
    locationmode='country names',
    color='risk_score',
    color_continuous_scale='Reds',
    title='Food Security Risk Score by Country',
    hover_data={'risk_category': True, 'Overall score': True}
)
st.plotly_chart(fig_map, use_container_width=True, key="map_chart")

st.divider()

# --- Search all countries ---
st.subheader("🔎 Search All Countries")
search_term = st.text_input("Type a country name to search", "")

if search_term:
    search_results = filtered_df[filtered_df['Country'].str.contains(search_term, case=False, na=False)]
    st.write(f"Found {len(search_results)} matching countries:")
    st.dataframe(
        search_results[['Country', 'risk_score', 'risk_category', 'cluster_label']].sort_values('risk_score', ascending=False),
        use_container_width=True
    )

st.divider()

# --- Top risk countries ---
st.subheader("⚠️ Top 15 Highest-Risk Countries")
top_risk = filtered_df.sort_values('risk_score', ascending=False).head(15)
st.dataframe(
    top_risk[['Country', 'risk_score', 'risk_category', 'cluster_label']],
    use_container_width=True
)

st.download_button(
    "⬇️ Download filtered data as CSV",
    filtered_df.to_csv(index=False),
    "filtered_food_security_data.csv",
    "text/csv"
)

st.divider()

# --- Cluster comparison ---
st.subheader("📊 Cluster Profile Comparison")
cluster_avg = df.groupby('cluster')[pillars + ['Overall score']].mean().round(1)
st.dataframe(cluster_avg, use_container_width=True)

fig_cluster = px.scatter(
    df, x='Affordability', y='Quality and Safety',
    color=df['cluster_label'],
    hover_name='Country',
    title='Countries by Affordability vs Quality and Safety, colored by Cluster'
)
st.plotly_chart(fig_cluster, use_container_width=True, key="cluster_scatter")
st.caption("Red = High Risk cluster · Light blue = Moderate Risk · Dark blue = Food Secure")

st.divider()

# --- Feature Importance (from Random Forest) ---
st.subheader("🌲 What Drives Food Security Risk Most?")
st.write(
    "Using a Random Forest model trained on the four pillars, we identified "
    "which factors most strongly predict overall risk:"
)

with st.spinner("Calculating feature importance..."):
    X = df[pillars]
    y = df['risk_score']
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X, y)

    importance_df = pd.DataFrame({
        'Pillar': pillars,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=True)

fig_importance = px.bar(
    importance_df, x='Importance', y='Pillar', orientation='h',
    title='Feature Importance: Which Pillar Drives Risk Most?'
)
st.plotly_chart(fig_importance, use_container_width=True, key="importance_chart")

top_driver = importance_df.iloc[-1]['Pillar']
st.info(f"📊 **{top_driver}** is the strongest driver of overall food security risk based on this analysis.")

st.divider()

# --- About / Methodology ---
with st.expander("ℹ️ About This Dashboard"):
    st.markdown("""
    **Methodology:**
    - **Risk Score:** Calculated by inverting the GFSI Overall score (higher = more risk)
    - **Risk Categories:** Countries split into Low/Medium/High using quantile-based bins
    - **Clustering:** K-Means (unsupervised ML) groups countries by similar food security profiles
    - **Feature Importance:** Random Forest (supervised ML) identifies which pillar drives risk most

    **Data Source:** [Global Food Security Index 2022 on Kaggle](https://www.kaggle.com/datasets/kanchana1990/global-food-security-intelligence)

    """)

st.divider()
st.caption(config.DISCLAIMER)

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85em;'>"
    "IIT Mandi HimShikhar DSAI Program · "
    "Data: <a href='https://www.kaggle.com/datasets/kanchana1990/global-food-security-intelligence' target='_blank'>GFSI 2022 (Kaggle)</a>"
    "</div>",
    unsafe_allow_html=True
)