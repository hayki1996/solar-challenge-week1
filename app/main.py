import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cache the data loading for better performance
@st.cache_data
def load_data():
    benin = pd.read_csv("data/benin-malanville.csv")
    sierra_leone = pd.read_csv("data/sierraleone-bumbuna.csv")
    togo = pd.read_csv("data/togo-dapaong_qc.csv")
    
    benin['Country'] = 'Benin'
    sierra_leone['Country'] = 'Sierra Leone'
    togo['Country'] = 'Togo'
    
    return pd.concat([benin, sierra_leone, togo], ignore_index=True)

# Load data once
df = load_data()

# Sidebar: Country selection
st.sidebar.title("Country Filter")
selected_countries = st.sidebar.multiselect(
    "Select countries:",
    options=df['Country'].unique(),
    default=list(df['Country'].unique())
)

# Sidebar: Metric selection
st.sidebar.title("Solar Metric")
metric = st.sidebar.selectbox("Select solar metric:", ['GHI', 'DNI', 'DHI'])

# Filter data based on selected countries
filtered_df = df[df['Country'].isin(selected_countries)]

# Main title
st.title("🌞 Solar Potential Dashboard")

# Boxplot of selected metric by country
st.subheader(f"{metric} Distribution by Country")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x='Country', y=metric, ax=ax, palette="Set2")
ax.set_xlabel("Country")
ax.set_ylabel(metric)
st.pyplot(fig)

# Top 5 regions by the selected metric
st.subheader(f"Top 5 Regions by {metric}")
top_regions = (
    filtered_df[['Country', 'region', metric]]
    .sort_values(by=metric, ascending=False)
    .head(5)
    .reset_index(drop=True)
)
st.table(top_regions)
  