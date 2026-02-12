# Example Workflow: Prospecting Support

## Scenario
You want to identify VPs and Directors in your network at tech companies and generate outreach messages.

## Step 1: Define Criteria
Decide what you're looking for:
- **Title keywords:** VP, Director, Head of, C-level
- **Target companies:** Google, Meta, Amazon, etc.
- **Location:** (optional) San Francisco, New York, etc.

## Step 2: Run Prospecting

### Ask Claude
Upload your `Connections.csv` and prompt:

> "From my connections, find everyone with 'VP', 'Director', or 'Head of' in their title at tech companies. Generate personalized outreach messages and export to Excel."

### Or run directly
```bash
pip install pandas openpyxl
python templates/prospecting.py Connections.csv prospects.xlsx \
    --titles "VP,Director,Head of,CTO" \
    --companies "Google,Meta,Amazon,Stripe"
```

## Step 3: Review Prospect Workbook

The output includes:
- **Prospects** — Filtered list with name, company, position, email, connection date
- **Outreach Templates** — 3 personalized message templates per prospect:
  1. **Reconnection** — Casual catch-up message
  2. **Value-First** — Lead with something useful
  3. **Intro Request** — Ask about mutual connections
- **Prospect Summary** — Count of prospects by company

## Sample Results from `sample_connections.csv`

Filtering for VPs, Directors, Heads, and CTOs:

| Name | Company | Position |
|---|---|---|
| Eve Davis | Microsoft | VP of Engineering |
| Grace Wilson | Stripe | Head of Product |
| Henry Moore | Meta | Director of Engineering |
| Quinn Martinez | Shopify | VP of Sales |
| Tina Rodriguez | Salesforce | Director of Sales |
| Victor Lee | Google | Engineering Director |
| Xavier Hall | Stripe | CTO |

**7 prospects** across 5 companies, each with 3 personalized outreach templates.
