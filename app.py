import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from agents import chat_agent, generate_insights, create_pdf_report


# Page config
st.set_page_config(
    page_title="AI Intelligent Data Assistant",
    page_icon="🤖",
    layout="wide"
)


# Create upload folder
os.makedirs("uploaded_files", exist_ok=True)


# Title
st.title("Oracle-Level AI Intelligent Data Assistant")

st.write("Developed by Shridhar Kumar")

st.write("Upload any CSV file to analyze, visualize, and generate AI report.")


# Upload file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


data = None


# If file uploaded
if uploaded_file is not None:

    file_path = os.path.join("uploaded_files", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    data = pd.read_csv(file_path)


    # Preview
    st.subheader("Dataset Preview")

    st.dataframe(data)


    # Dataset Info
    st.subheader("Dataset Information")

    st.write("Columns:", list(data.columns))

    st.write("Data Types:")
    st.write(data.dtypes)


    # Download dataset
    csv = data.to_csv(index=False)

    st.download_button(
        "Download Dataset",
        csv,
        "dataset.csv",
        "text/csv"
    )


    # Dashboard Metrics
    col1, col2 = st.columns(2)

    col1.metric("Total Rows", len(data))

    col2.metric("Total Columns", len(data.columns))


    # Chart Visualization
    numeric_cols = data.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:

        st.subheader("Chart Visualization")

        selected_col = st.selectbox("Select column", numeric_cols)

        fig, ax = plt.subplots()

        data[selected_col].plot(kind="bar", ax=ax)

        st.pyplot(fig)


    # AI Insights
    st.subheader("AI Insights")

    insights = generate_insights(data)

    for insight in insights:
        st.write(insight)


    # PDF Report
    pdf_path = os.path.join("uploaded_files", "AI_Report.pdf")

    create_pdf_report(data, insights, pdf_path)

    with open(pdf_path, "rb") as f:

        st.download_button(
            label="Download PDF Report",
            data=f,
            file_name="AI_Data_Report.pdf",
            mime="application/pdf"
        )


# AI Assistant
st.subheader("AI Assistant")

question = st.text_input("Ask question about dataset")

if st.button("Ask AI"):

    if data is not None:

        answer = chat_agent(question, data)

        st.success(answer)

    else:

        st.error("Please upload dataset first.")