import re
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Sugar Trap Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("nutrient_matrix_data.csv")
    return df

df = load_data()

st.title("Sugar Trap: Market Gap Analysis")
st.caption("Finding the Blue Ocean in the healthy snacking aisle")

# Sidebar filters
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select snack categories",
    options=sorted(df["primary_category"].dropna().unique()),
    default=sorted(df["primary_category"].dropna().unique())
)

filtered_df = df[df["primary_category"].isin(categories)].copy()

# Thresholds
LOW_SUGAR_THRESHOLD = 5
HIGH_PROTEIN_THRESHOLD = 10

target_df = filtered_df[
    (filtered_df["sugars_100g"] <= LOW_SUGAR_THRESHOLD) &
    (filtered_df["proteins_100g"] >= HIGH_PROTEIN_THRESHOLD)
]

snack_bar_target_count = target_df[
    target_df["primary_category"] == "Snack Bars"
].shape[0]

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Products analyzed", f"{len(filtered_df):,}")
col2.metric("High protein threshold", "≥ 10g")
col3.metric("Low sugar threshold", "≤ 5g")
col4.metric("Snack bars in target zone", snack_bar_target_count)

st.divider()

# Key Insight
st.subheader("Key Insight")
st.info(
    "The High Protein + Low Sugar zone is not empty, but it is dominated by Nuts & Seeds. "
    "Snack Bars are underrepresented in this zone, suggesting an opportunity to build convenient, "
    "low-sugar, high-protein snack bars."
)

# Scatter plot
st.subheader("Nutrient Matrix: Sugar vs Protein")

fig = px.scatter(
    filtered_df,
    x="sugars_100g",
    y="proteins_100g",
    color="primary_category",
    hover_data=["product_name", "primary_category", "sugars_100g", "proteins_100g"],
    opacity=0.65,
    title="Sugar vs Protein by Snack Category"
)

fig.add_vline(
    x=LOW_SUGAR_THRESHOLD,
    line_dash="dash",
    annotation_text="Low Sugar Threshold"
)

fig.add_hline(
    y=HIGH_PROTEIN_THRESHOLD,
    line_dash="dash",
    annotation_text="High Protein Threshold"
)

fig.update_layout(
    xaxis_title="Sugar per 100g",
    yaxis_title="Protein per 100g",
    legend_title="Primary Category"
)

st.plotly_chart(fig, use_container_width=True)

# Category averages
st.subheader("Average Sugar and Protein by Category")

category_summary = (
    filtered_df.groupby("primary_category")[["sugars_100g", "proteins_100g"]]
    .mean()
    .round(2)
    .reset_index()
)

fig_bar = px.bar(
    category_summary,
    x="primary_category",
    y=["sugars_100g", "proteins_100g"],
    barmode="group",
    title="Average Sugar and Protein by Category"
)

fig_bar.update_layout(
    xaxis_title="Category",
    yaxis_title="Grams per 100g",
    legend_title="Metric"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Target quadrant count
st.subheader("Products in the High Protein + Low Sugar Zone")

target_counts = (
    target_df["primary_category"]
    .value_counts()
    .reset_index()
)

target_counts.columns = ["primary_category", "count"]

fig_target = px.bar(
    target_counts,
    x="primary_category",
    y="count",
    title="High Protein + Low Sugar Products by Category"
)

fig_target.update_layout(
    xaxis_title="Category",
    yaxis_title="Number of Products"
)

st.plotly_chart(fig_target, use_container_width=True)

# Hidden Gem ingredient analysis
st.subheader("Hidden Gem: Common Protein Sources")

protein_keywords = [
    "whey", "soy", "peanut", "almond", "milk", "casein",
    "pea protein", "nuts", "seed", "oat", "egg"
]

ingredients = target_df["ingredients_text"].dropna().str.lower()

protein_source_counts = Counter()

for text in ingredients:
    for keyword in protein_keywords:
        if keyword in text:
            protein_source_counts[keyword] += 1

top_sources = pd.DataFrame(
    protein_source_counts.most_common(3),
    columns=["Protein Source", "Count"]
)

if len(top_sources) > 0:
    st.table(top_sources)
else:
    st.write("No common protein sources found in the ingredient text.")

# Candidate's Choice
st.subheader("Candidate's Choice: Health Opportunity Score")

filtered_df["health_opportunity_score"] = (
    filtered_df["proteins_100g"]
    + filtered_df["fiber_100g"].fillna(0)
    - filtered_df["sugars_100g"]
    - (0.3 * filtered_df["fat_100g"].fillna(0))
)

score_summary = (
    filtered_df.groupby("primary_category")["health_opportunity_score"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
    .reset_index()
)

fig_score = px.bar(
    score_summary,
    x="primary_category",
    y="health_opportunity_score",
    title="Average Health Opportunity Score by Category"
)

fig_score.update_layout(
    xaxis_title="Category",
    yaxis_title="Health Opportunity Score"
)

st.plotly_chart(fig_score, use_container_width=True)

st.caption(
    "Candidate's Choice: I added a Health Opportunity Score to rank categories by rewarding protein "
    "and fiber while penalizing sugar and fat. This gives the client a simple business-friendly metric "
    "for identifying healthier product opportunities."
)

# Recommendation
st.subheader("Recommendation")
st.success(
    "Based on the data, the biggest market opportunity is in Snack Bars, specifically targeting "
    "products with at least 10g of protein and less than 5g of sugar per 100g."
)