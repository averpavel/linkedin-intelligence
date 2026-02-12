# Example Workflow: Connection Analysis

## Scenario
You have exported your LinkedIn connections and want a comprehensive network analysis.

## Step 1: Export from LinkedIn
1. Go to LinkedIn → Settings → Data Privacy → Get a copy of your data
2. Select "Connections" → Request archive
3. Download the ZIP and extract `Connections.csv`

## Step 2: Run Analysis

### Option A: Ask Claude
Upload your `Connections.csv` and prompt:

> "Analyze my LinkedIn connections. Create an Excel report showing my network by company, position, and connection growth over time. Identify dormant connections and network clusters."

Claude will use the `connection_analysis.py` template to generate a full workbook.

### Option B: Run the template directly
```bash
pip install pandas openpyxl
python templates/connection_analysis.py Connections.csv my_network_report.xlsx
```

## Step 3: Review Output
Open `my_network_report.xlsx` in Excel or LibreOffice. You'll find:

- **Overview** — Total connections, date range, top company/position
- **By Company** — Bar chart of top 20 companies
- **By Position** — Bar chart of top 20 job titles
- **Growth Timeline** — Line chart showing monthly connection growth
- **Dormant Connections** — Connections older than 12 months
- **Clusters** — Companies with 3+ connections and pie chart

## Sample Output Insights
With the sample data (`sample_connections.csv`):
- **30 connections** across 8 companies
- **Top company:** Google (6 connections)
- **Network clusters:** Google, Meta, Amazon, Microsoft
- **Dormant connections:** Xavier Hall (Stripe CTO, connected Feb 2021)
