# LinkedIn Intelligence

A Claude skill that turns LinkedIn data exports into an interactive browser dashboard. Analyzes your connections, posts, activity patterns, and network clusters — all locally, no data leaves your machine.

## What It Does

Takes a standard LinkedIn data export (ZIP/folder) and generates a single self-contained `dashboard.html` file with:

### Connection Analysis
- Full searchable table of all connections with multi-filter system
- Filter by seniority (C-Level, VP, Director, etc.), company, year, position keywords
- Stack multiple filters, remove them individually
- Seniority auto-classification from job titles
- Names link directly to LinkedIn profiles

### Network Visualization
- Top companies and positions in your network (bar charts)
- Seniority distribution (donut chart)
- Network growth over time — monthly and cumulative (line charts)
- Yearly connection breakdown
- Network clusters: companies with 5+ connections (donut + table)
- Dormant connections: people connected 2+ years ago

### Post Analysis
- All posts with content preview, type classification, word count, and comment cross-referencing
- Post type distribution: Long Text, Short Text, Media, Link Share, Repost
- Posting patterns: day of week, hour of day
- Word count distribution
- Posts per month timeline
- Filter by type, search by content, link to original post

### Activity Patterns
- Monthly activity timeline: posts, comments, reactions
- Reaction type distribution (LIKE, PRAISE, EMPATHY, etc.)
- Reaction activity over time

## How to Use

### Step 1: Export Your Data from LinkedIn
1. Go to **linkedin.com/mypreferences/d/download-my-data**
2. Select **all available data** (or at minimum: Connections, Shares, Comments, Reactions)
3. Click **Request archive** — LinkedIn emails a download link within 24 hours
4. Download the ZIP and extract it (or leave it as a folder)

### Step 2: Place the Export
Copy the extracted folder into this project directory. The folder name typically looks like:
```
Complete_LinkedInDataExport_MM-DD-YYYY.zip/
```

### Step 3: Update the Path
Edit `build_dashboard.py` and set `EXPORT_DIR` to your folder name:
```python
EXPORT_DIR = "./Complete_LinkedInDataExport_01-20-2026.zip"
```

### Step 4: Generate the Dashboard
```bash
pip install pandas openpyxl
python build_dashboard.py
```

### Step 5: Open
```bash
open dashboard.html   # macOS
xdg-open dashboard.html  # Linux
start dashboard.html  # Windows
```

## Required Files from LinkedIn Export

| File | Used For |
|---|---|
| `Connections.csv` | Network analysis, filters, clusters, dormant detection |
| `Shares.csv` | Post content, type classification, posting patterns |
| `Comments.csv` | Comment cross-referencing per post |
| `Reactions.csv` | Reaction types and activity timeline |
| `Profile.csv` | Name and headline (for dashboard header) |

## Dashboard Tabs

| Tab | Content |
|---|---|
| **Overview** | 6 stat cards + 4 summary charts |
| **Connections** | All connections, searchable with stackable multi-filters |
| **Companies** | Top 20 companies bar chart + table |
| **Seniority** | Seniority donut + top 20 positions |
| **Growth** | Cumulative line chart, monthly bars, yearly breakdown |
| **Posts** | Deep post analysis with 5 charts + scrollable feed |
| **Activity** | Monthly posts/comments/reactions + reaction type breakdown |
| **Clusters** | Companies with 5+ connections |
| **Dormant** | Connections from 2+ years ago |

## Filter System (Connections Tab)

Click **+ Add Filter** to add any combination of:
- **Seniority**: C-Level / Founder, VP, Director, Head of, Manager / Lead, Senior IC, IC / Specialist, Junior / Associate
- **Company**: Dropdown of top 100 companies in your network
- **Connection Year**: Any year present in your data
- **Position Contains**: Free text search (e.g., "Engineer", "Sales", "Product")

Filters appear as blue tags. Click **x** on any tag to remove it. Filters stack — results must match ALL active filters.

## Technical Details

- **Output**: Single self-contained HTML file (no server required)
- **Charts**: Chart.js 4.x loaded from CDN
- **Dependencies**: Python 3.9+, `pandas`, `openpyxl` (for CSV parsing only)
- **Performance**: Handles 10k+ connections; tables cap at 500 rows with a prompt to filter
- **Seniority detection**: Rule-based keyword matching on job titles

## Data Handling & Privacy

- All processing happens locally — no data is sent anywhere
- The generated `dashboard.html` contains your connection data embedded as JSON
- **Do NOT publish `dashboard.html` or your LinkedIn export publicly**
- `.gitignore` is preconfigured to exclude all personal data
- LinkedIn CSVs often have 2-3 metadata rows before the header — the script handles this automatically
- Multiline post content in CSVs is handled with `on_bad_lines="skip"`

## Limitations

- **No likes/views counts**: LinkedIn's data export does not include impression or reaction counts on your own posts. The export only contains the content you posted and your own outbound activity (reactions/comments you gave to others).
- **Comment counts are partial**: The "comments" shown per post are your own replies cross-referenced by URL, not the total comment count from others.
- **No engagement rate**: Without impressions data, engagement rate cannot be calculated.
- **Position/title parsing**: Seniority classification is heuristic-based and may misclassify unusual titles.

## Common Issues

| Issue | Fix |
|---|---|
| `ParserError` on CSV | Script uses `on_bad_lines="skip"` — some multiline posts may be skipped |
| Dates not parsing | Uses `format="mixed"` with `dayfirst=True` for LinkedIn's format |
| Empty company/position | Filled with "Not Specified" automatically |
| Charts don't render | Open in Chrome/Firefox/Edge — Safari may lag on large datasets |
| Too many connections to display | Use filters to narrow down — table shows max 500 rows |
