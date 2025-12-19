"""
Rollback Page
"""

import streamlit as st
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="Rollback", page_icon="⏪", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
LOGS_DIR = SCRIPT_DIR / "logs"
ARTICLES_DIR = SCRIPT_DIR / "articles"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("⏪ Rollback")
st.caption("Revert keyword injection changes")

st.markdown("---")

# Get available runs
runs = []
if LOGS_DIR.exists():
    runs = sorted([d for d in LOGS_DIR.iterdir() if d.is_dir() and d.name.startswith("run-")], reverse=True)

if not runs:
    st.info("No injection runs found to rollback.")
    st.stop()

# Current status
st.subheader("📊 Current Status")

col1, col2, col3 = st.columns(3)

with col1:
    raw_count = len(list((ARTICLES_DIR / "raw").glob("*.md"))) if (ARTICLES_DIR / "raw").exists() else 0
    st.metric("Raw Articles", raw_count)

with col2:
    processed_count = len(list((ARTICLES_DIR / "processed").glob("*.md"))) if (ARTICLES_DIR / "processed").exists() else 0
    st.metric("Processed Articles", processed_count)

with col3:
    st.metric("Injection Runs", len(runs))

st.markdown("---")

# Rollback options
st.subheader("🔧 Rollback Options")

rollback_method = st.radio(
    "Rollback method",
    ["Restore from Raw (copy original files)", "Git Rollback (revert changes)"],
    help="Choose how to rollback changes"
)

use_git = "Git" in rollback_method

st.markdown("---")

# Run selection
st.subheader("📁 Select Run to Rollback")

# Build run info
run_data = []
for run_dir in runs:
    summary = load_json(run_dir / "run-summary.json")
    if summary:
        run_data.append({
            "run_id": run_dir.name,
            "started": summary.get("started_at", "N/A")[:19],
            "processed": summary.get("totals", {}).get("articles_processed", 0),
            "passed": summary.get("totals", {}).get("articles_passed", 0),
            "dry_run": summary.get("dry_run", False)
        })

if run_data:
    import pandas as pd
    df = pd.DataFrame(run_data)
    df["status"] = df.apply(lambda x: "🔍 Dry Run" if x["dry_run"] else f"✅ {x['passed']}/{x['processed']} passed", axis=1)
    
    st.dataframe(
        df[["run_id", "started", "status"]],
        use_container_width=True,
        hide_index=True
    )

selected_run = st.selectbox(
    "Select run to rollback",
    options=[r.name for r in runs],
    format_func=lambda x: f"{x} - {next((r['started'] for r in run_data if r['run_id'] == x), 'N/A')}"
)

# Load run details
run_dir = LOGS_DIR / selected_run
summary = load_json(run_dir / "run-summary.json")

if summary:
    # Show what would be affected
    st.markdown("---")
    st.subheader("📋 Affected Articles")
    
    article_summaries = summary.get("article_summaries", [])
    passed_articles = [a["article_id"] for a in article_summaries if a.get("status") == "passed"]
    
    if passed_articles:
        st.info(f"This run modified **{len(passed_articles)}** articles")
        
        # Article selector
        rollback_scope = st.radio(
            "Rollback scope",
            ["All articles from this run", "Select specific articles"],
            horizontal=True
        )
        
        selected_articles = []
        
        if rollback_scope == "All articles from this run":
            selected_articles = passed_articles
        else:
            selected_articles = st.multiselect(
                "Select articles to rollback",
                options=passed_articles
            )
        
        if selected_articles:
            with st.expander(f"Preview: {len(selected_articles)} articles to rollback"):
                for aid in selected_articles[:20]:
                    st.markdown(f"- {aid}")
                if len(selected_articles) > 20:
                    st.caption(f"... and {len(selected_articles) - 20} more")
    else:
        st.warning("No articles were modified in this run (was it a dry run?)")
        selected_articles = []

st.markdown("---")

# Execute rollback
st.subheader("⚠️ Execute Rollback")

col1, col2 = st.columns([2, 1])

with col1:
    dry_run = st.checkbox("🔍 Dry run (preview only)", value=True)

with col2:
    st.warning("This cannot be undone!")

if st.button(
    "⏪ Execute Rollback" if not dry_run else "🔍 Preview Rollback",
    type="primary" if not dry_run else "secondary",
    use_container_width=True,
    disabled=len(selected_articles) == 0 if 'selected_articles' in dir() else True
):
    if not selected_articles:
        st.error("No articles selected!")
    else:
        # Build command
        cmd = [
            sys.executable, 
            str(SCRIPT_DIR / "scripts" / "utils" / "rollback.py"),
            "--run-id", selected_run
        ]
        
        if dry_run:
            cmd.append("--dry-run")
        
        if not use_git:
            cmd.append("--use-raw")
        
        if len(selected_articles) == 1:
            cmd.extend(["--article-id", selected_articles[0]])
        
        st.markdown("---")
        st.markdown("### 📊 Rollback Output")
        
        with st.spinner("Executing rollback..."):
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(SCRIPT_DIR)
            )
        
        if result.returncode == 0:
            st.success("✅ Rollback completed!")
        else:
            st.error("❌ Rollback failed!")
        
        with st.expander("📝 Full Output", expanded=True):
            st.code(result.stdout + result.stderr)
        
        if not dry_run:
            st.info("Refresh the page to see updated status.")

# Alternative: Manual rollback instructions
st.markdown("---")
st.subheader("📖 Manual Rollback")

with st.expander("Git Commands"):
    st.markdown("""
    **View changes:**
    ```bash
    git diff articles/processed/
    ```
    
    **Rollback specific article:**
    ```bash
    git checkout HEAD~1 -- articles/processed/001_*.md
    ```
    
    **Rollback all processed articles:**
    ```bash
    git checkout HEAD~1 -- articles/processed/
    ```
    
    **Revert entire commit:**
    ```bash
    git revert <commit-hash>
    ```
    """)

with st.expander("File System Commands"):
    st.markdown("""
    **Copy original back:**
    ```powershell
    Copy-Item articles/raw/001_*.md articles/processed/
    ```
    
    **Clear all processed:**
    ```powershell
    Remove-Item articles/processed/*.md
    ```
    """)

