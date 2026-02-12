"""
Query LinkedIn data from the command line.
Returns JSON results for natural language processing by Claude.

Usage:
    python3 query_linkedin.py --type summary
    python3 query_linkedin.py --type connections --company "Google"
    python3 query_linkedin.py --type connections --seniority "VP" --company "Stripe"
    python3 query_linkedin.py --type posts --search "AI"
    python3 query_linkedin.py --type connections --recent 90
    python3 query_linkedin.py --type comments --search "revenue"
    python3 query_linkedin.py --type reactions
"""

import argparse
import json
import sys
import pandas as pd
from datetime import datetime, timedelta

from linkedin_data import find_export_dir, load_all, build_conversations


def build_summary(data):
    """Build compact summary statistics."""
    conn_df = data["connections"]
    reactions_df = data["reactions"]
    posts = data["posts"]

    senior_count = int(conn_df[conn_df["Seniority"].isin(
        ["C-Level / Founder", "VP", "Director", "Head of"]
    )].shape[0])

    top_companies = conn_df["Company"].value_counts().head(20)
    seniority_dist = conn_df["Seniority"].value_counts()

    return {
        "total_connections": int(len(conn_df)),
        "unique_companies": int(conn_df["Company"].nunique()),
        "total_posts": int(len(posts)),
        "total_comments": int(len(data["comments"])),
        "total_reactions": int(len(reactions_df)),
        "senior_connections": senior_count,
        "earliest_connection": conn_df["Connected On"].min().strftime("%Y-%m-%d") if conn_df["Connected On"].notna().any() else None,
        "latest_connection": conn_df["Connected On"].max().strftime("%Y-%m-%d") if conn_df["Connected On"].notna().any() else None,
        "top_companies": {k: int(v) for k, v in top_companies.items()},
        "seniority_distribution": {k: int(v) for k, v in seniority_dist.items()},
    }


def query_connections(data, args):
    """Filter and return connections."""
    df = data["connections"].copy()

    filters = {}

    if args.company:
        pattern = args.company.lower()
        df = df[df["Company"].str.lower().str.contains(pattern, na=False)]
        filters["company"] = args.company

    if args.seniority:
        df = df[df["Seniority"].isin(args.seniority)]
        filters["seniority"] = args.seniority

    if args.position:
        pattern = args.position.lower()
        df = df[df["Position"].str.lower().str.contains(pattern, na=False)]
        filters["position"] = args.position

    if args.year:
        df = df[df["Connected On"].dt.year == args.year]
        filters["year"] = args.year

    if args.recent:
        cutoff = datetime.now() - timedelta(days=args.recent)
        df = df[df["Connected On"] >= cutoff]
        filters["recent_days"] = args.recent

    if args.search:
        pattern = args.search.lower()
        mask = (
            df["Full Name"].str.lower().str.contains(pattern, na=False) |
            df["Company"].str.lower().str.contains(pattern, na=False) |
            df["Position"].str.lower().str.contains(pattern, na=False)
        )
        df = df[mask]
        filters["search"] = args.search

    df = df.sort_values("Connected On", ascending=False)
    total = len(df)

    records = []
    for _, r in df.head(args.limit).iterrows():
        records.append({
            "name": r["Full Name"],
            "company": r["Company"],
            "position": r["Position"],
            "seniority": r["Seniority"],
            "connected": r["Connected On"].strftime("%Y-%m-%d") if pd.notna(r["Connected On"]) else "",
            "url": r.get("URL", "") if pd.notna(r.get("URL", "")) else "",
        })

    return {
        "type": "connections",
        "total": total,
        "showing": len(records),
        "filters": filters,
        "results": records,
    }


def query_posts(data, args):
    """Filter and return posts."""
    posts = data["posts"]

    filters = {}

    if args.search:
        pattern = args.search.lower()
        posts = [p for p in posts if pattern in p["content"].lower()]
        filters["search"] = args.search

    if args.post_type:
        posts = [p for p in posts if p["type"] == args.post_type]
        filters["post_type"] = args.post_type

    if args.year:
        posts = [p for p in posts if p["date"].startswith(str(args.year))]
        filters["year"] = args.year

    # Sort by date descending
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    total = len(posts)

    results = []
    for p in posts[:args.limit]:
        results.append({
            "date": p["date"],
            "day": p["day"],
            "content": p["content"],
            "wordCount": p["wordCount"],
            "type": p["type"],
            "comments": p["comments"],
            "link": p["link"],
        })

    return {
        "type": "posts",
        "total": total,
        "showing": len(results),
        "filters": filters,
        "results": results,
    }


def query_comments(data, args):
    """Filter and return comments."""
    df = data["comments"].copy()

    filters = {}

    if args.search:
        pattern = args.search.lower()
        if "Message" in df.columns:
            df = df[df["Message"].fillna("").str.lower().str.contains(pattern, na=False)]
        filters["search"] = args.search

    if args.year:
        df = df[df["Date"].dt.year == args.year]
        filters["year"] = args.year

    df = df.sort_values("Date", ascending=False)
    total = len(df)

    records = []
    for _, r in df.head(args.limit).iterrows():
        records.append({
            "date": r["Date"].strftime("%Y-%m-%d") if pd.notna(r["Date"]) else "",
            "message": str(r.get("Message", "")) if pd.notna(r.get("Message")) else "",
            "link": str(r.get("Link", "")) if pd.notna(r.get("Link")) else "",
        })

    return {
        "type": "comments",
        "total": total,
        "showing": len(records),
        "filters": filters,
        "results": records,
    }


def query_reactions(data, args):
    """Filter and return reactions."""
    df = data["reactions"].copy()

    filters = {}

    if args.year:
        df = df[df["Date"].dt.year == args.year]
        filters["year"] = args.year

    type_dist = {}
    if "Type" in df.columns:
        type_dist = {k: int(v) for k, v in df["Type"].value_counts().items()}

    total = len(df)

    return {
        "type": "reactions",
        "total": total,
        "filters": filters,
        "type_distribution": type_dist,
    }


def query_messages(data, args):
    """Filter and return message conversations."""
    messages_df = data["messages"]
    if messages_df.empty:
        return {"type": "messages", "total": 0, "showing": 0, "filters": {}, "results": [],
                "error": "No messages.csv found in export"}

    filters = {}

    # Filter by recency
    if args.recent:
        cutoff = pd.Timestamp.now(tz="UTC") - timedelta(days=args.recent)
        messages_df = messages_df[messages_df["DATE"] >= cutoff]
        filters["recent_days"] = args.recent

    if args.year:
        messages_df = messages_df[messages_df["DATE"].dt.year == args.year]
        filters["year"] = args.year

    convos = build_conversations(messages_df)

    # Filter by search (matches person name or message content)
    if args.search:
        pattern = args.search.lower()
        convos = [c for c in convos if
                  pattern in c["other"].lower() or
                  pattern in c["last_content"].lower()]
        filters["search"] = args.search

    # Filter by awaiting reply only
    if args.awaiting_reply:
        convos = [c for c in convos if c["awaiting_your_reply"]]
        filters["awaiting_reply"] = True

    total = len(convos)
    results = convos[:args.limit]

    return {
        "type": "messages",
        "total": total,
        "showing": len(results),
        "filters": filters,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Query LinkedIn export data")
    parser.add_argument("--type", choices=["summary", "connections", "posts", "comments", "reactions", "messages"],
                        default="summary", help="Type of data to query")
    parser.add_argument("--company", help="Filter connections by company name (partial match)")
    parser.add_argument("--seniority", action="append",
                        help="Filter by seniority level (can specify multiple)")
    parser.add_argument("--position", help="Filter by position keyword")
    parser.add_argument("--search", help="Full-text search")
    parser.add_argument("--year", type=int, help="Filter by year")
    parser.add_argument("--recent", type=int, help="Connections from last N days")
    parser.add_argument("--post-type", help="Filter posts by type (Long Text, Short Text, Media, Link Share, Repost)")
    parser.add_argument("--awaiting-reply", action="store_true", help="Show only conversations awaiting your reply")
    parser.add_argument("--limit", type=int, default=500, help="Max results to return (default: 500)")
    parser.add_argument("--export-dir", help="Path to LinkedIn export directory (auto-detected if omitted)")

    args = parser.parse_args()

    try:
        export_dir = args.export_dir or find_export_dir()
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    data = load_all(export_dir)
    summary = build_summary(data)

    if args.type == "summary":
        result = {"type": "summary", "summary": summary}
    elif args.type == "connections":
        result = query_connections(data, args)
        result["summary"] = summary
    elif args.type == "posts":
        result = query_posts(data, args)
        result["summary"] = summary
    elif args.type == "comments":
        result = query_comments(data, args)
    elif args.type == "reactions":
        result = query_reactions(data, args)
    elif args.type == "messages":
        result = query_messages(data, args)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
