#!/usr/bin/env python3
"""
Utility: Generate Diff Reports for Keyword Injection

Creates human-readable diff reports comparing original and injected articles.

Usage:
    python utils/diff_generator.py --run-id RUN_ID [--output-format html|md]
"""

import os
import json
import difflib
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def load_run_summary(logs_dir: Path, run_id: str) -> Dict:
    """Load run summary for a specific run."""
    summary_path = logs_dir / run_id / "run-summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"Run summary not found: {summary_path}")
    return json.loads(summary_path.read_text(encoding='utf-8'))


def load_article_log(logs_dir: Path, run_id: str, article_id: str) -> Dict:
    """Load injection log for a specific article."""
    log_path = logs_dir / run_id / "article-logs" / f"{article_id}_injection-log.json"
    if not log_path.exists():
        return None
    return json.loads(log_path.read_text(encoding='utf-8'))


def generate_unified_diff(original: str, modified: str, filename: str) -> List[str]:
    """Generate unified diff between original and modified content."""
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    
    diff = list(difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm=""
    ))
    
    return diff


def format_diff_html(diff_lines: List[str], article_log: Dict) -> str:
    """Format diff as HTML with syntax highlighting."""
    html_lines = []
    
    for line in diff_lines:
        if line.startswith('+++') or line.startswith('---'):
            html_lines.append(f'<div class="diff-header">{escape_html(line)}</div>')
        elif line.startswith('@@'):
            html_lines.append(f'<div class="diff-hunk">{escape_html(line)}</div>')
        elif line.startswith('+'):
            html_lines.append(f'<div class="diff-add">{escape_html(line)}</div>')
        elif line.startswith('-'):
            html_lines.append(f'<div class="diff-remove">{escape_html(line)}</div>')
        else:
            html_lines.append(f'<div class="diff-context">{escape_html(line)}</div>')
    
    return '\n'.join(html_lines)


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;'))


def generate_markdown_report(
    article_id: str,
    article_log: Dict,
    diff_lines: List[str]
) -> str:
    """Generate markdown report for an article."""
    lines = [
        f"## Article {article_id}: {article_log.get('article_title', 'Unknown')}",
        "",
        f"**Status:** {article_log.get('validation_status', 'unknown')}",
        f"**Run ID:** {article_log.get('run_id', 'unknown')}",
        f"**Timestamp:** {article_log.get('timestamp', 'unknown')}",
        "",
        "### Metrics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
    ]
    
    metrics = article_log.get('metrics', {})
    for key, value in metrics.items():
        lines.append(f"| {key.replace('_', ' ').title()} | {value} |")
    
    lines.extend([
        "",
        "### Keywords Attempted",
        "",
    ])
    
    for kw in article_log.get('keywords_attempted', []):
        action = kw.get('action', 'unknown')
        icon = "✅" if action == "inserted" else "⏭️"
        lines.append(f"- {icon} **{kw.get('keyword_text', 'unknown')}**: {action}")
        
        if kw.get('skip_reason'):
            lines.append(f"  - Skip reason: {kw['skip_reason']}")
        
        for placement in kw.get('placements', []):
            loc = placement.get('location', {})
            lines.append(f"  - Location: {loc.get('section', '?')}, para {loc.get('paragraph', '?')}, sent {loc.get('sentence', '?')}")
            lines.append(f"  - Method: {placement.get('method', '?')}")
    
    if article_log.get('quality_flags'):
        lines.extend([
            "",
            "### Quality Flags",
            "",
        ])
        for flag in article_log['quality_flags']:
            lines.append(f"- ⚠️ {flag}")
    
    if diff_lines:
        lines.extend([
            "",
            "### Diff",
            "",
            "```diff",
        ])
        lines.extend(diff_lines[:100])  # Limit to first 100 lines
        if len(diff_lines) > 100:
            lines.append(f"... ({len(diff_lines) - 100} more lines)")
        lines.append("```")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    return '\n'.join(lines)


def generate_full_report(
    run_id: str,
    script_dir: Path,
    output_format: str = "md"
) -> str:
    """Generate full report for a run."""
    logs_dir = script_dir / "logs"
    raw_dir = script_dir / "articles" / "raw"
    processed_dir = script_dir / "articles" / "processed"
    
    summary = load_run_summary(logs_dir, run_id)
    
    report_lines = [
        f"# Keyword Injection Report: {run_id}",
        "",
        f"**Started:** {summary.get('started_at', 'unknown')}",
        f"**Completed:** {summary.get('completed_at', 'unknown')}",
        f"**Dry Run:** {summary.get('dry_run', False)}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    
    totals = summary.get('totals', {})
    for key, value in totals.items():
        report_lines.append(f"| {key.replace('_', ' ').title()} | {value} |")
    
    report_lines.extend([
        "",
        "## Article Details",
        "",
    ])
    
    for article_summary in summary.get('article_summaries', []):
        article_id = article_summary['article_id']
        article_log = load_article_log(logs_dir, run_id, article_id)
        
        if not article_log:
            continue
        
        # Load original and processed files
        original_files = list(raw_dir.glob(f"{article_id}_*.md"))
        processed_files = list(processed_dir.glob(f"{article_id}_*.md"))
        
        diff_lines = []
        if original_files and processed_files:
            original = original_files[0].read_text(encoding='utf-8')
            processed = processed_files[0].read_text(encoding='utf-8')
            diff_lines = generate_unified_diff(original, processed, original_files[0].name)
        
        report_lines.append(generate_markdown_report(article_id, article_log, diff_lines))
    
    return '\n'.join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate diff reports for keyword injection runs"
    )
    parser.add_argument(
        "--run-id",
        type=str,
        required=True,
        help="Run ID to generate report for"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["md", "html"],
        default="md",
        help="Output format"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (defaults to logs/{run-id}/report.{format})"
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.parent.parent
    
    report = generate_full_report(args.run_id, script_dir, args.output_format)
    
    if args.output:
        output_path = Path(args.output)
    else:
        ext = "md" if args.output_format == "md" else "html"
        output_path = script_dir / "logs" / args.run_id / f"report.{ext}"
    
    output_path.write_text(report, encoding='utf-8')
    print(f"Report saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())

