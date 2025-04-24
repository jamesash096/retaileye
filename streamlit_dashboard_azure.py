import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient
import io
import os
import openai

st.set_page_config(page_title="RetailEye", layout="wide")
DATA_BLOB_CONTAINER = "predictions"
DATA_BLOB_FILE = "dashboard_ready.csv"

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_openai_explanation(product_row):
    prompt = (
        f"Explain in one sentence why this product — {product_row['itemname']} — is labeled as '{product_row['recommendation']}'. "
        f"It is priced at {product_row['UnitPrice']:.2f} with a rating of {product_row['Rating']}, and similar products cost about {product_row['Best_UnitPrice']:.2f}."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )

    return response.choices[0].message.content

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
if df.empty:
    st.stop()

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

# Display the table and let user select a row by item name
selected_item = st.selectbox("🔍 Choose a product to explain", filtered["itemname"].unique())

# Filter the DataFrame to get the selected row
selected_row = filtered[filtered["itemname"] == selected_item].iloc[0]

# Generate explanation on button click
if st.button("🧠 Explain Recommendation"):
    explanation = generate_openai_explanation(selected_row)
    st.markdown(f"**RetailEye's Explanation:** {explanation}")
