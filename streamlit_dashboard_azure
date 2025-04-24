import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient
import io
import os

st.set_page_config(page_title="RetailEye Dashboard", layout="wide")
DATA_BLOB_CONTAINER = "predictions"
DATA_BLOB_FILE = "dashboard_ready.csv"

# Load CSV from Azure Blob
@st.cache_data
def load_data():
    conn_str = os.getenv("AZURE_BLOB_CONN_STR")
    if not conn_str:
        st.error("❌ AZURE_BLOB_CONN_STR not found. Please configure it in Azure App Service.")
        return pd.DataFrame()
    try:
        blob_service = BlobServiceClient.from_connection_string(conn_str)
        blob = blob_service.get_blob_client(container=DATA_BLOB_CONTAINER, blob=DATA_BLOB_FILE)
        data = blob.download_blob().readall()
        return pd.read_csv(io.BytesIO(data))
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty():
    st.stop()

st.set_page_config(page_title="RetailEye Dashboard", layout="wide")
st.title("🛍️ RetailEye: Pricing Recommendation Dashboard")
st.markdown("Explore model-driven pricing suggestions across stores and categories.")

# Sidebar Filters
store = st.selectbox("🛒 Select Store", sorted(df["Store"].unique()))
filtered = df[df["Store"] == store]

# Optional bar chart recommendation filter
selected_reco = st.radio(
    "📊 Filter by Recommendation",
    options=["All"] + list(filtered["recommendation"].unique()),
    horizontal=True,
    index=0
)

if selected_reco != "All":
    filtered = filtered[filtered["recommendation"] == selected_reco]

# KPIs
col1, col2 = st.columns(2)
col1.metric("Total Products", len(filtered))
col2.metric("Overpriced", (filtered["predicted_label"] == 1).sum())

# Bar Chart
chart_data = filtered["recommendation"].value_counts().reset_index()
chart_data.columns = ["Recommendation", "Count"]
st.bar_chart(data=chart_data, x="Recommendation", y="Count")

# Compute Best Price by Item
best_price_df = (
    df.loc[df.groupby("itemname")["UnitPrice"].idxmin()][["itemname", "UnitPrice", "Store"]]
    .rename(columns={"UnitPrice": "Best_UnitPrice", "Store": "Best_Store"})
)

# Merge best price info into filtered data
filtered = filtered.merge(best_price_df, on="itemname", how="left")

# Show table
st.markdown("### 📋 Product-Level Recommendations")
st.dataframe(
    filtered[["itemname", "Store", "UnitPrice", "Rating", "recommendation", "Best_Store", "Best_UnitPrice"]],
    use_container_width=True
)
