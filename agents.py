import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# AI Chat Assistant
def chat_agent(question, data):

    question = question.lower()

    numeric_cols = data.select_dtypes(include='number').columns

    if "rows" in question:
        return f"Total rows: {len(data)}"

    elif "columns" in question:
        return f"Columns: {', '.join(data.columns)}"

    elif "total" in question or "sum" in question:

        for col in numeric_cols:
            if col.lower() in question:
                return f"Total {col}: {data[col].sum()}"

        return f"Available numeric columns: {', '.join(numeric_cols)}"

    elif "average" in question or "mean" in question:

        for col in numeric_cols:
            if col.lower() in question:
                return f"Average {col}: {data[col].mean():.2f}"

        return f"Available numeric columns: {', '.join(numeric_cols)}"

    elif "max" in question:

        for col in numeric_cols:
            if col.lower() in question:
                return f"Maximum {col}: {data[col].max()}"

        return f"Available numeric columns: {', '.join(numeric_cols)}"

    elif "min" in question:

        for col in numeric_cols:
            if col.lower() in question:
                return f"Minimum {col}: {data[col].min()}"

        return f"Available numeric columns: {', '.join(numeric_cols)}"

    elif "summary" in question:
        return str(data.describe())

    else:
        return "Ask about total, average, max, min, rows, columns, or summary."


# Generate insights
def generate_insights(data):

    insights = []

    numeric_cols = data.select_dtypes(include='number').columns

    for col in numeric_cols:

        insights.append(f"{col} Total: {data[col].sum()}")

        insights.append(f"{col} Average: {data[col].mean():.2f}")

        insights.append(f"{col} Maximum: {data[col].max()}")

        insights.append(f"{col} Minimum: {data[col].min()}")

    return insights


# Create PDF report
def create_pdf_report(data, insights, file_path):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(file_path)

    elements = []

    elements.append(Paragraph("AI Data Analysis Report", styles["Heading1"]))

    elements.append(Spacer(1,12))

    elements.append(Paragraph(f"Total Rows: {len(data)}", styles["Normal"]))

    elements.append(Paragraph(f"Total Columns: {len(data.columns)}", styles["Normal"]))

    elements.append(Spacer(1,12))

    elements.append(Paragraph("Columns:", styles["Heading2"]))

    for col in data.columns:
        elements.append(Paragraph(col, styles["Normal"]))

    elements.append(Spacer(1,12))

    elements.append(Paragraph("Insights:", styles["Heading2"]))

    for insight in insights:
        elements.append(Paragraph(insight, styles["Normal"]))

    doc.build(elements)