#!/usr/bin/env python3
"""
Utility: Rollback Keyword Injection Changes

Provides utilities to rollback injection changes using git or file restore.

Usage:
    python utils/rollback.py --run-id RUN_ID [--article-id ARTICLE_ID] [--dry-run]
    python utils/rollback.py --list-runs
"""

import os
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def run_git_command(cmd: List[str], cwd: Path) -> tuple:
    """Run a git command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def list_runs(logs_dir: Path) -> List[Dict]:
    """List all injection runs."""
    runs = []
    
    if not logs_dir.exists():
        return runs
    
    for run_dir in logs_dir.iterdir():
        if run_dir.is_dir() and run_dir.name.startswith("run-"):
            summary_path = run_dir / "run-summary.json"
            if summary_path.exists():
                summary = json.loads(summary_path.read_text(encoding='utf-8'))
                runs.append({
                    "run_id": run_dir.name,
                    "started_at": summary.get("started_at", "unknown"),
                    "articles_processed": summary.get("totals", {}).get("articles_processed", 0),
                    "articles_passed": summary.get("totals", {}).get("articles_passed", 0),
                    "dry_run": summary.get("dry_run", False)
                })
    
    return sorted(runs, key=lambda x: x["started_at"], reverse=True)


def get_affected_articles(logs_dir: Path, run_id: str) -> List[str]:
    """Get list of articles affected by a run."""
    summary_path = logs_dir / run_id / "run-summary.json"
    if not summary_path.exists():
        return []
    
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    return [a["article_id"] for a in summary.get("article_summaries", []) 
            if a.get("status") == "passed"]


def rollback_article_git(
    script_dir: Path,
    article_id: str,
    dry_run: bool = False
) -> bool:
    """Rollback a single article using git checkout."""
    processed_dir = script_dir / "articles" / "processed"
    article_files = list(processed_dir.glob(f"{article_id}_*.md"))
    
    if not article_files:
        print(f"  No processed file found for article {article_id}")
        return False
    
    article_path = article_files[0]
    relative_path = article_path.relative_to(script_dir)
    
    if dry_run:
        print(f"  [DRY-RUN] Would rollback: {relative_path}")
        return True
    
    # Use git checkout to restore previous version
    success, output = run_git_command(
        ["git", "checkout", "HEAD~1", "--", str(relative_path)],
        script_dir
    )
    
    if success:
        print(f"  Rolled back: {relative_path}")
    else:
        print(f"  Failed to rollback {relative_path}: {output}")
    
    return success


def rollback_article_copy(
    script_dir: Path,
    article_id: str,
    dry_run: bool = False
) -> bool:
    """Rollback a single article by copying from raw directory."""
    raw_dir = script_dir / "articles" / "raw"
    processed_dir = script_dir / "articles" / "processed"
    
    raw_files = list(raw_dir.glob(f"{article_id}_*.md"))
    
    if not raw_files:
        print(f"  No raw file found for article {article_id}")
        return False
    
    raw_path = raw_files[0]
    processed_path = processed_dir / raw_path.name
    
    if dry_run:
        print(f"  [DRY-RUN] Would copy: {raw_path.name} -> processed/")
        return True
    
    shutil.copy2(raw_path, processed_path)
    print(f"  Restored from raw: {raw_path.name}")
    
    return True


def rollback_run(
    script_dir: Path,
    run_id: str,
    article_id: Optional[str] = None,
    use_git: bool = True,
    dry_run: bool = False
) -> int:
    """Rollback changes from a specific run."""
    logs_dir = script_dir / "logs"
    
    # Get affected articles
    if article_id:
        articles = [article_id]
    else:
        articles = get_affected_articles(logs_dir, run_id)
    
    if not articles:
        print(f"No articles found for run {run_id}")
        return 1
    
    print(f"Rolling back {len(articles)} articles from run {run_id}")
    print(f"Method: {'git checkout' if use_git else 'copy from raw'}")
    print(f"Dry run: {dry_run}")
    print("-" * 50)
    
    success_count = 0
    for aid in articles:
        if use_git:
            success = rollback_article_git(script_dir, aid, dry_run)
        else:
            success = rollback_article_copy(script_dir, aid, dry_run)
        
        if success:
            success_count += 1
    
    print("-" * 50)
    print(f"Rolled back {success_count}/{len(articles)} articles")
    
    return 0 if success_count == len(articles) else 1


def main():
    parser = argparse.ArgumentParser(
        description="Rollback keyword injection changes"
    )
    parser.add_argument(
        "--list-runs",
        action="store_true",
        help="List all injection runs"
    )
    parser.add_argument(
        "--run-id",
        type=str,
        help="Run ID to rollback"
    )
    parser.add_argument(
        "--article-id",
        type=str,
        help="Specific article ID to rollback (optional)"
    )
    parser.add_argument(
        "--use-raw",
        action="store_true",
        help="Copy from raw directory instead of using git"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.parent.parent
    logs_dir = script_dir / "logs"
    
    if args.list_runs:
        runs = list_runs(logs_dir)
        if not runs:
            print("No injection runs found")
            return 0
        
        print("Available runs:")
        print("-" * 80)
        print(f"{'Run ID':<35} {'Started':<25} {'Articles':<10} {'Passed':<10} {'Dry Run'}")
        print("-" * 80)
        
        for run in runs:
            print(f"{run['run_id']:<35} {run['started_at'][:19]:<25} {run['articles_processed']:<10} {run['articles_passed']:<10} {run['dry_run']}")
        
        return 0
    
    if not args.run_id:
        parser.print_help()
        return 1
    
    return rollback_run(
        script_dir,
        args.run_id,
        args.article_id,
        use_git=not args.use_raw,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    exit(main())

