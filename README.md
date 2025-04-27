# 🛍️ RetailEye: AI-Driven Product Pricing Intelligence

<p><b>Team</b>: Team 5</p>
<p><b>Members</b>: Aashi Patni, Aditya Ravikrishnan, Dipak Bhujpal, James Ashwin Rodriguez, Yixuan (Rita) Wang</p> 

## 📖 Project Summary

**RetailEye** is an end-to-end AI-powered product pricing intelligence solution that helps retailers optimize their prices by analyzing competitor listings across marketplaces like Amazon, Walmart, and Etsy.  
It flags underpriced or overpriced products, recommends actions, and generates natural language explanations to justify each recommendation — making AI insights actionable and understandable.

---

## ⚙️ Technology Stack

| Category | Technology Used |
|----------|-----------------|
| **Cloud Platform** | Microsoft Azure |
| **Data Storage** | Azure Blob Storage |
| **Data Engineering** | Azure Data Factory, PySpark |
| **Machine Learning** | XGBoost, scikit-learn |
| **LLM Explanations** | Azure OpenAI (GPT-3.5 / GPT-4) |
| **App Hosting** | Azure App Service (Linux) |
| **Dashboard UI** | Streamlit |
| **CI/CD** | GitHub Actions |

---

## 🔥 End-to-End Pipeline Overview

1. **Data Ingestion**
   - Upload raw retail transaction data and competitor listing data into **Azure Blob Storage** under `/raw/`.

2. **ETL & Feature Engineering**
   - Use **Azure Data Factory** or **PySpark notebooks** to:
     - Clean product descriptions
     - Extract structured attributes (e.g., brand, unit price)
     - Compute derived features like `rating_score`

3. **Machine Learning**
   - Train an **XGBoost classifier** to predict whether a product should:
     - Raise Price
     - Drop Price
     - Retain Price
   - Features used: `UnitPrice`, `Quantity`, `Rating`, `rating_score`

4. **Model Deployment**
   - Upload the trained model (`price_classifier.pkl`) to Azure Blob Storage
   - Save price predictions (`price_predictions.parquet`) in Blob Storage for dashboard consumption

5. **Front-End Dashboard**
   - Build a **Streamlit** application to:
     - Allow users to filter by store, product, and recommendation
     - Display KPIs (e.g., overpriced count)
     - Visualize recommendations in charts and tables

6. **LLM Integration for Explainability**
   - Integrate **Azure OpenAI Service** to:
     - Generate short explanations for why a product's price recommendation was made
     - Dynamically create natural language output for selected products in the dashboard

7. **Deployment**
   - Host the dashboard on **Azure App Service**
   - Secure API keys and blob connection strings through Azure App Settings
   - Automate deployments via **GitHub Actions**

---

## 🧠 Key Features

- 📊 Price optimization insights in real-time
- 💬 AI-powered explanations for pricing decisions
- ☁️ Scalable, cloud-native architecture
- 🔒 Secure and enterprise-compliant with Microsoft Azure

---
