#!/usr/bin/env python3
"""
Script 05: Export Consolidated Document with Change Log

This script exports all processed articles into a single markdown document
with a comprehensive log of all keyword changes made.

Usage:
    python 05_export-consolidated.py [--run-id RUN_ID] [--output PATH] [--include-raw]
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def load_json(path: Path) -> Optional[Dict]:
    """Load JSON file safely."""
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def generate_change_log(logs_dir: Path, run_id: str, keyword_manifest: Dict) -> str:
    """Generate a detailed change log from injection logs."""
    lines = []
    
    run_dir = logs_dir / run_id
    summary = load_json(run_dir / "run-summary.json")
    
    if not summary:
        return "No injection run found.\n"
    
    # Header
    lines.append("# Keyword Injection Change Log")
    lines.append("")
    lines.append(f"**Run ID:** {run_id}")
    lines.append(f"**Date:** {summary.get('started_at', 'Unknown')[:10]}")
    lines.append(f"**Completed:** {summary.get('completed_at', 'Unknown')[:19]}")
    lines.append("")
    
    # Summary statistics
    totals = summary.get("totals", {})
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Articles Processed | {totals.get('articles_processed', 0)} |")
    lines.append(f"| Articles Passed | {totals.get('articles_passed', 0)} |")
    lines.append(f"| Articles Failed | {totals.get('articles_failed', 0)} |")
    lines.append(f"| Keywords Inserted | {totals.get('keywords_inserted', 0)} |")
    lines.append(f"| Keywords Skipped | {totals.get('keywords_skipped', 0)} |")
    lines.append(f"| Total Words Added | {totals.get('total_words_added', 0)} |")
    lines.append("")
    
    # Build keyword lookup
    kw_lookup = {}
    if keyword_manifest:
        kw_lookup = {kw["id"]: kw["text"] for kw in keyword_manifest.get("keywords", [])}
    
    # Per-article changes
    lines.append("## Changes by Article")
    lines.append("")
    
    article_logs_dir = run_dir / "article-logs"
    if article_logs_dir.exists():
        log_files = sorted(article_logs_dir.glob("*_injection-log.json"))
        
        for log_file in log_files:
            log = load_json(log_file)
            if not log:
                continue
            
            article_id = log.get("article_id", "Unknown")
            article_title = log.get("article_title", "Unknown")
            status = log.get("validation_status", "unknown")
            
            status_icon = "✅" if status == "passed" else "❌"
            
            lines.append(f"### {status_icon} Article {article_id}: {article_title[:60]}")
            lines.append("")
            
            # Metrics
            metrics = log.get("metrics", {})
            lines.append(f"- **Words:** {metrics.get('word_count_before', 0)} → {metrics.get('word_count_after', 0)} (+{metrics.get('word_count_delta', 0)})")
            lines.append(f"- **Sentences Modified:** {metrics.get('sentences_modified', 0)}")
            lines.append("")
            
            # Keywords
            lines.append("**Keywords:**")
            lines.append("")
            
            for kw in log.get("keywords_attempted", []):
                kw_text = kw.get("keyword_text", "Unknown")
                action = kw.get("action", "unknown")
                
                if action == "inserted":
                    lines.append(f"- ✅ **{kw_text}** - Inserted ({kw.get('occurrences_after', 0)} occurrences)")
                    
                    for placement in kw.get("placements", []):
                        loc = placement.get("location", {})
                        method = placement.get("method", "unknown")
                        before = placement.get("before", "")[:80]
                        after = placement.get("after", "")[:80]
                        
                        lines.append(f"  - 📍 Section: {loc.get('section', 'Unknown')}")
                        lines.append(f"  - Method: {method}")
                        if before and after:
                            lines.append(f"  - Before: *\"{before}...\"*")
                            lines.append(f"  - After: *\"{after}...\"*")
                else:
                    skip_reason = kw.get("skip_reason", "unknown")
                    lines.append(f"- ⏭️ ~~{kw_text}~~ - Skipped ({skip_reason})")
            
            lines.append("")
            
            # Quality flags
            if log.get("quality_flags"):
                lines.append("**Quality Flags:**")
                for flag in log["quality_flags"]:
                    lines.append(f"- ⚠️ {flag}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)


def generate_consolidated_document(
    articles_dir: Path,
    logs_dir: Path,
    run_id: str,
    keyword_manifest: Dict,
    article_manifest: Dict,
    include_raw: bool = False
) -> str:
    """Generate the full consolidated document."""
    lines = []
    
    # Document header
    lines.append("# Consolidated Blog Articles")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Source:** Keyword Injection System")
    if run_id:
        lines.append(f"**Injection Run:** {run_id}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    
    processed_dir = articles_dir / "processed"
    raw_dir = articles_dir / "raw"
    
    # Use processed articles if available, otherwise raw
    if processed_dir.exists() and list(processed_dir.glob("*.md")):
        source_dir = processed_dir
        source_type = "Processed (with keywords)"
    else:
        source_dir = raw_dir
        source_type = "Raw (original)"
    
    lines.append(f"*Source: {source_type}*")
    lines.append("")
    
    # Build article list
    article_files = sorted(source_dir.glob("*.md"))
    
    # TOC entries
    for i, article_file in enumerate(article_files, 1):
        # Extract title from file
        content = article_file.read_text(encoding='utf-8')
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if not title_match:
            title_match = re.search(r'title:\s*"([^"]+)"', content)
        
        title = title_match.group(1) if title_match else article_file.stem
        title = title[:60] + "..." if len(title) > 60 else title
        
        article_id = article_file.name[:3]
        anchor = f"article-{article_id}"
        
        lines.append(f"{i}. [{title}](#{anchor})")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Change log section
    if run_id:
        lines.append(generate_change_log(logs_dir, run_id, keyword_manifest))
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Articles section
    lines.append("# Articles")
    lines.append("")
    
    for article_file in article_files:
        content = article_file.read_text(encoding='utf-8')
        article_id = article_file.name[:3]
        
        # Strip frontmatter for cleaner output
        clean_content = strip_frontmatter(content)
        
        # Add anchor
        lines.append(f'<a id="article-{article_id}"></a>')
        lines.append("")
        lines.append(clean_content)
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Export consolidated document with change log"
    )
    parser.add_argument(
        "--run-id",
        type=str,
        help="Injection run ID to include in change log (uses latest if not specified)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="exports/consolidated_articles.md",
        help="Output file path"
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Include raw articles if no processed versions exist"
    )
    parser.add_argument(
        "--log-only",
        action="store_true",
        help="Export only the change log, not the full articles"
    )
    
    args = parser.parse_args()
    
    # Paths
    script_dir = Path(__file__).parent.parent
    articles_dir = script_dir / "articles"
    logs_dir = script_dir / "logs"
    keywords_dir = script_dir / "keywords"
    output_path = script_dir / args.output
    
    print(f"Articles directory: {articles_dir}")
    print(f"Output path: {output_path}")
    
    # Load manifests
    keyword_manifest = load_json(keywords_dir / "keyword-manifest.json")
    article_manifest = load_json(articles_dir / "article-manifest.json")
    
    # Find run ID
    run_id = args.run_id
    if not run_id and logs_dir.exists():
        runs = sorted([d.name for d in logs_dir.iterdir() if d.is_dir() and d.name.startswith("run-")])
        if runs:
            run_id = runs[-1]
            print(f"Using latest run: {run_id}")
    
    # Generate document
    if args.log_only:
        if run_id:
            content = generate_change_log(logs_dir, run_id, keyword_manifest)
        else:
            content = "No injection run found.\n"
    else:
        content = generate_consolidated_document(
            articles_dir,
            logs_dir,
            run_id,
            keyword_manifest,
            article_manifest,
            include_raw=args.include_raw
        )
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    output_path.write_text(content, encoding='utf-8')
    
    # Stats
    word_count = len(content.split())
    line_count = len(content.split('\n'))
    
    print(f"\nExport complete!")
    print(f"   Output: {output_path}")
    print(f"   Size: {len(content):,} characters")
    print(f"   Words: {word_count:,}")
    print(f"   Lines: {line_count:,}")
    
    return 0


if __name__ == "__main__":
    exit(main())

