"""
Results & Diffs Page
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json
import difflib

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
LOGS_DIR = SCRIPT_DIR / "logs"
ARTICLES_DIR = SCRIPT_DIR / "articles"
KEYWORDS_DIR = SCRIPT_DIR / "keywords"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("📊 Results & Diffs")
st.caption("Review injection results and compare changes")

# Get available runs
if not LOGS_DIR.exists():
    st.warning("No logs directory found.")
    st.stop()

runs = sorted([d for d in LOGS_DIR.iterdir() if d.is_dir() and d.name.startswith("run-")], reverse=True)

if not runs:
    st.info("No injection runs found. Run an injection first.")
    if st.button("Go to Injection"):
        st.switch_page("pages/3_injection.py")
    st.stop()

st.markdown("---")

# Run selector
col1, col2 = st.columns([3, 1])

with col1:
    selected_run = st.selectbox(
        "📁 Select Run",
        options=[r.name for r in runs],
        format_func=lambda x: f"{x} {'(latest)' if x == runs[0].name else ''}"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    auto_refresh = st.checkbox("Auto-select latest", value=True)

run_dir = LOGS_DIR / selected_run
summary = load_json(run_dir / "run-summary.json")

if not summary:
    st.error("Run summary not found!")
    st.stop()

# Run summary
st.markdown("---")
st.subheader("📈 Run Summary")

totals = summary.get("totals", {})

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Processed", totals.get("articles_processed", 0))

with col2:
    passed = totals.get("articles_passed", 0)
    st.metric("Passed", passed)

with col3:
    failed = totals.get("articles_failed", 0)
    delta_color = "inverse" if failed > 0 else "off"
    st.metric("Failed", failed)

with col4:
    st.metric("Keywords Inserted", totals.get("keywords_inserted", 0))

with col5:
    st.metric("Words Added", totals.get("total_words_added", 0))

# Status bar
processed = totals.get("articles_processed", 1)
pass_rate = (passed / processed * 100) if processed > 0 else 0
st.progress(pass_rate / 100, text=f"Pass rate: {pass_rate:.1f}%")

# Timestamps
st.caption(f"Started: {summary.get('started_at', 'N/A')} | Completed: {summary.get('completed_at', 'N/A')}")

if summary.get("dry_run"):
    st.info("🔍 This was a dry run - no files were modified")

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 Article Results", "🔍 Diff Viewer", "📝 Validation"])

with tab1:
    st.subheader("Article Results")
    
    # Load article info
    article_manifest = load_json(ARTICLES_DIR / "article-manifest.json")
    article_lookup = {a["id"]: a["title"] for a in article_manifest["articles"]} if article_manifest else {}
    
    article_summaries = summary.get("article_summaries", [])
    
    if article_summaries:
        # Build dataframe
        df = pd.DataFrame(article_summaries)
        df["title"] = df["article_id"].apply(lambda x: article_lookup.get(x, "Unknown")[:40] + "...")
        
        # Status icons
        df["status_icon"] = df["status"].apply(lambda x: "✅" if x == "passed" else "❌")
        
        st.dataframe(
            df[["status_icon", "article_id", "title", "keywords_inserted", "keywords_skipped", "word_delta"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "status_icon": st.column_config.TextColumn("", width="small"),
                "article_id": st.column_config.TextColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Title", width="large"),
                "keywords_inserted": st.column_config.NumberColumn("Inserted", width="small"),
                "keywords_skipped": st.column_config.NumberColumn("Skipped", width="small"),
                "word_delta": st.column_config.NumberColumn("Words +/-", width="small"),
            }
        )
        
        # Failed articles detail
        failed_articles = summary.get("failed_articles", [])
        if failed_articles:
            st.markdown("---")
            st.error(f"### ❌ Failed Articles ({len(failed_articles)})")
            
            for article_id in failed_articles:
                log_path = run_dir / "article-logs" / f"{article_id}_injection-log.json"
                log = load_json(log_path)
                
                if log:
                    with st.expander(f"**{article_id}** - {article_lookup.get(article_id, 'Unknown')[:50]}"):
                        st.markdown("**Quality Flags:**")
                        for flag in log.get("quality_flags", []):
                            st.warning(flag)
                        
                        st.markdown("**Metrics:**")
                        metrics = log.get("metrics", {})
                        st.json(metrics)
    else:
        st.info("No article results in this run.")

with tab2:
    st.subheader("Diff Viewer")
    
    # Get processed articles
    processed_dir = ARTICLES_DIR / "processed"
    raw_dir = ARTICLES_DIR / "raw"
    
    if not processed_dir.exists() or not raw_dir.exists():
        st.warning("Articles directories not found.")
    else:
        processed_files = list(processed_dir.glob("*.md"))
        
        if processed_files:
            # Article selector
            article_options = sorted([f.name[:3] for f in processed_files])
            
            selected_article = st.selectbox(
                "Select article to view diff",
                options=article_options,
                format_func=lambda x: f"{x} - {article_lookup.get(x, 'Unknown')[:50]}..."
            )
            
            if selected_article:
                raw_files = list(raw_dir.glob(f"{selected_article}_*.md"))
                proc_files = list(processed_dir.glob(f"{selected_article}_*.md"))
                
                if raw_files and proc_files:
                    original = raw_files[0].read_text(encoding='utf-8')
                    processed = proc_files[0].read_text(encoding='utf-8')
                    
                    # Show article log info
                    log_path = run_dir / "article-logs" / f"{selected_article}_injection-log.json"
                    log = load_json(log_path)
                    
                    if log:
                        st.markdown("#### Keywords Applied")
                        for kw in log.get("keywords_attempted", []):
                            if kw["action"] == "inserted":
                                st.success(f"✅ **{kw['keyword_text']}** - inserted ({kw['occurrences_after']} occurrences)")
                                for p in kw.get("placements", []):
                                    loc = p.get("location", {})
                                    st.caption(f"   📍 {loc.get('section', '?')} | Method: {p.get('method', '?')}")
                            else:
                                st.warning(f"⏭️ **{kw['keyword_text']}** - skipped: {kw.get('skip_reason', '?')}")
                    
                    st.markdown("---")
                    st.markdown("#### Diff Output")
                    
                    # Generate diff
                    original_lines = original.split('\n')
                    processed_lines = processed.split('\n')
                    
                    diff = list(difflib.unified_diff(
                        original_lines,
                        processed_lines,
                        fromfile='original',
                        tofile='processed',
                        lineterm=''
                    ))
                    
                    if diff:
                        # Color-coded diff display
                        diff_text = '\n'.join(diff)
                        st.code(diff_text[:10000], language='diff')
                        
                        if len(diff_text) > 10000:
                            st.caption("... diff truncated")
                    else:
                        st.info("No differences found (or files are identical)")
                else:
                    st.warning("Could not find both raw and processed versions.")
        else:
            st.info("No processed articles found.")

with tab3:
    st.subheader("Validation Results")
    
    validation_path = run_dir / "validation-results.json"
    validation = load_json(validation_path)
    
    if validation:
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Validated", validation.get("articles_validated", 0))
        with col2:
            st.metric("Passed", validation.get("articles_passed", 0))
        with col3:
            st.metric("Issues", validation.get("total_issues", 0))
        
        st.markdown("---")
        
        # Article validation details
        for result in validation.get("article_results", []):
            status_icon = "✅" if result["passed"] else "❌"
            
            with st.expander(f"{status_icon} **{result['article_id']}** - {result['filename'][:40]}..."):
                # Checks
                checks = result.get("checks", {})
                
                for check_name, check_result in checks.items():
                    passed = check_result.get("passed", True)
                    icon = "✅" if passed else "❌"
                    
                    st.markdown(f"**{icon} {check_name.replace('_', ' ').title()}**")
                    
                    if check_name == "word_count":
                        st.caption(f"Original: {check_result.get('original', 0)} → Processed: {check_result.get('processed', 0)} ({check_result.get('delta_pct', 0):.1f}%)")
                    elif check_name == "readability":
                        orig = check_result.get("original", {})
                        proc = check_result.get("processed", {})
                        st.caption(f"Reading ease: {orig.get('reading_ease', 0):.1f} → {proc.get('reading_ease', 0):.1f}")
                    elif check_name == "repeated_phrases" and not passed:
                        for phrase in check_result.get("phrases", [])[:3]:
                            st.caption(f"  - '{phrase['phrase']}' ({phrase['count']}x)")
                
                # Issues and warnings
                if result.get("issues"):
                    st.error("**Issues:**")
                    for issue in result["issues"]:
                        st.markdown(f"- {issue}")
                
                if result.get("warnings"):
                    st.warning("**Warnings:**")
                    for warning in result["warnings"]:
                        st.markdown(f"- {warning}")
    else:
        st.info("No validation results found for this run.")
        
        if st.button("🔍 Run Validation"):
            import subprocess
            import sys
            
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "scripts" / "04_validate-output.py"), "--run-id", selected_run],
                capture_output=True,
                text=True,
                cwd=str(SCRIPT_DIR)
            )
            
            st.code(result.stdout + result.stderr)
            st.rerun()

