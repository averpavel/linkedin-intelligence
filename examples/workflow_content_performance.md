# Example Workflow: Content Performance Analysis

## Scenario
You want to understand which of your LinkedIn posts perform best and identify patterns.

## Step 1: Prepare Data

### Option A: LinkedIn Export
Export your post data via LinkedIn Settings → Data Privacy → Get a copy of your data → Select "Posts".

### Option B: Manual CSV
Create a CSV with these columns:
```
Date,Content,Impressions,Reactions,Comments,Shares
```

See `sample_posts.csv` for an example.

## Step 2: Run Analysis

### Ask Claude
Upload your post data and prompt:

> "Analyze my LinkedIn post performance. Create an Excel dashboard showing engagement trends, my top content, and what patterns drive the most engagement."

### Or run directly
```bash
pip install pandas openpyxl
python templates/content_analysis.py posts.csv my_content_dashboard.xlsx
```

## Step 3: Review Dashboard

The output workbook includes:
- **Dashboard** — Key metrics: total posts, impressions, avg engagement rate
- **Post Performance** — All posts ranked by engagement
- **Trends** — Monthly line charts of impressions and engagement
- **Top Content** — Top 10 posts with analysis
- **Content Patterns** — Performance breakdown by day of week

## Sample Insights from `sample_posts.csv`

| Metric | Value |
|---|---|
| Total Posts | 15 |
| Total Impressions | 124,230 |
| Highest Engagement Post | "Hiring managers: stop requiring 5 years..." (18,900 impressions) |
| Best Day | Monday posts average highest engagement |
| Top Format | "Hot takes" and "unpopular opinions" drive 3x more comments |
| Optimal Length | Posts with 2-3 key points outperform longer threads |
