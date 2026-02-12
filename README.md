# LinkedIn Intelligence

Turn your LinkedIn data export into an interactive browser dashboard. Analyze your connections, content, activity patterns, and network clusters — entirely offline.

## Features

**Connections** — Browse all your connections with a stackable multi-filter system. Filter by seniority level, company, connection year, or position keywords. Add multiple filters, remove any with one click.

**Network Visualization** — See your network by company, seniority, growth over time, and clusters. Identify where your network is concentrated and spot dormant relationships.

**Post Analysis** — Every post you've published with content preview, type classification (Long Text, Short Text, Media, Link Share, Repost), word count analysis, day/hour patterns, and direct links to the original.

**Activity Patterns** — Track your posting, commenting, and reaction activity over time. See which reaction types you use most.

## Quick Start

### 1. Export your LinkedIn data

Go to [linkedin.com/mypreferences/d/download-my-data](https://www.linkedin.com/mypreferences/d/download-my-data), request an archive (all data or at minimum: Connections, Shares, Comments, Reactions), and download when ready.

### 2. Install dependencies

```bash
pip install pandas openpyxl
```

### 3. Run the dashboard generator

Place your extracted LinkedIn export folder in this directory, then update the path in `build_dashboard.py`:

```python
EXPORT_DIR = "./your-linkedin-export-folder"
```

```bash
python build_dashboard.py
open dashboard.html
```

That's it. One HTML file, no server needed.

## Dashboard Overview

| Tab | What's Inside |
|---|---|
| **Overview** | Key stats + 4 summary charts |
| **Connections** | All connections with search + stackable filters |
| **Companies** | Top 20 companies in your network |
| **Seniority** | Network breakdown by seniority level |
| **Growth** | Connection growth over time |
| **Posts** | Deep post analysis with 5 charts + content feed |
| **Activity** | Posting/commenting/reaction patterns |
| **Clusters** | Companies with 5+ connections |
| **Dormant** | Connections older than 2 years |

## How the Filter System Works

On the Connections tab, click **+ Add Filter** to open the filter builder:

- **Seniority** — C-Level / Founder, VP, Director, Head of, Manager / Lead, Senior IC, IC / Specialist
- **Company** — Select from your top 100 companies
- **Connection Year** — Filter by when you connected
- **Position Contains** — Free text match (e.g., "Engineer", "Sales")

Filters stack: add as many as you need. Each shows as a removable tag. All filters must match (AND logic).

## Privacy

Your data stays local. Nothing is sent to any server.

- The script reads your LinkedIn CSV files and generates a static HTML file
- The HTML contains your data as embedded JSON — **do not publish it**
- `.gitignore` is preconfigured to exclude:
  - All LinkedIn export folders and CSVs
  - Generated `dashboard.html`
  - Any `.xlsx` files

**Before pushing to GitHub**, verify with:

```bash
git status
```

You should only see `build_dashboard.py`, `SKILL.md`, `README.md`, `.gitignore`, and `examples/` — never your personal data.

## Limitations

- **No likes/views/impressions**: LinkedIn's data export doesn't include engagement metrics (impressions, reactions received, views) on your posts. Only your content and outbound activity are exported.
- **Comment counts are partial**: Shows your own replies per post, not total comments from others.
- **Seniority detection is heuristic**: Based on keyword matching in job titles — may misclassify unusual titles.

## Tech Stack

- **Python 3.9+** with `pandas` for data processing
- **Chart.js 4.x** for interactive charts (loaded from CDN)
- Single self-contained HTML output — no build step, no framework, no server

## Project Structure

```
.
├── build_dashboard.py    # Main script — generates dashboard.html
├── SKILL.md              # Detailed skill documentation
├── README.md             # This file
├── .gitignore            # Protects personal data from git
└── examples/
    ├── sample_connections.csv
    ├── sample_posts.csv
    └── workflow_*.md
```

## License

MIT
