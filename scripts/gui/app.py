#!/usr/bin/env python3
"""
Keyword Injection System - GUI
Run with: streamlit run scripts/gui/app.py
"""

import streamlit as st
from pathlib import Path
import json
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Page config
st.set_page_config(
    page_title="Keyword Injection System",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #a855f7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3d3d5c;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #a855f7;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .success-badge {
        background-color: #166534;
        color: #86efac;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .warning-badge {
        background-color: #854d0e;
        color: #fde047;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .error-badge {
        background-color: #991b1b;
        color: #fca5a5;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .run-card {
        background: #1e1e2e;
        border: 1px solid #3d3d5c;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent
ARTICLES_DIR = SCRIPT_DIR / "articles"
KEYWORDS_DIR = SCRIPT_DIR / "keywords"
LOGS_DIR = SCRIPT_DIR / "logs"
CONFIG_DIR = SCRIPT_DIR / "config"


def load_json(path):
    """Load JSON file safely."""
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            return None
    return None


# Sidebar navigation
st.sidebar.markdown("## 🔑 Keyword Injection")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
st.sidebar.page_link("app.py", label="🏠 Dashboard", icon="🏠")
st.sidebar.page_link("pages/1_articles.py", label="📄 Articles")
st.sidebar.page_link("pages/2_keywords.py", label="🏷️ Keywords")
st.sidebar.page_link("pages/3_injection.py", label="💉 Run Injection")
st.sidebar.page_link("pages/4_results.py", label="📊 Results & Diffs")
st.sidebar.page_link("pages/5_rollback.py", label="⏪ Rollback")

st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | OpsGuru")

# Main content
st.markdown('<p class="main-header">Keyword Injection Dashboard</p>', unsafe_allow_html=True)

# Load stats
article_manifest = load_json(ARTICLES_DIR / "article-manifest.json")
keyword_manifest = load_json(KEYWORDS_DIR / "keyword-manifest.json")
matrix = load_json(KEYWORDS_DIR / "keyword-article-matrix.json")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    value = article_manifest["total_articles"] if article_manifest else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Articles</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    value = keyword_manifest["total_keywords"] if keyword_manifest else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Keywords</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    value = matrix["statistics"]["total_assignments"] if matrix else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">Assignments</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    runs = list(LOGS_DIR.glob("run-*")) if LOGS_DIR.exists() else []
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(runs)}</div>
        <div class="metric-label">Runs</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Two column layout
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📁 Recent Injection Runs")
    
    if LOGS_DIR.exists():
        runs = sorted(LOGS_DIR.glob("run-*"), reverse=True)[:5]
        
        if runs:
            for run_dir in runs:
                summary_path = run_dir / "run-summary.json"
                if summary_path.exists():
                    summary = load_json(summary_path)
                    if summary:
                        totals = summary.get("totals", {})
                        passed = totals.get("articles_passed", 0)
                        failed = totals.get("articles_failed", 0)
                        
                        status_badge = "success-badge" if failed == 0 else "warning-badge" if failed < passed else "error-badge"
                        status_text = "SUCCESS" if failed == 0 else f"{failed} FAILED"
                        
                        with st.expander(f"**{run_dir.name}**"):
                            cols = st.columns(5)
                            cols[0].metric("Processed", totals.get("articles_processed", 0))
                            cols[1].metric("Passed", passed)
                            cols[2].metric("Failed", failed)
                            cols[3].metric("Keywords", totals.get("keywords_inserted", 0))
                            cols[4].metric("Words Added", totals.get("total_words_added", 0))
                            
                            if summary.get("failed_articles"):
                                st.warning(f"Failed: {', '.join(summary['failed_articles'])}")
        else:
            st.info("No injection runs yet. Go to **Run Injection** to start.")
    else:
        st.info("Logs directory not found.")

with right_col:
    st.subheader("📊 Cluster Distribution")
    
    if keyword_manifest:
        cluster_data = keyword_manifest.get("cluster_summary", {})
        if cluster_data:
            import pandas as pd
            df = pd.DataFrame([
                {"Cluster": k, "Keywords": v} 
                for k, v in sorted(cluster_data.items(), key=lambda x: -x[1])
            ])
            st.bar_chart(df.set_index("Cluster"))
    else:
        st.info("No keyword data available.")

st.markdown("---")

# Quick actions
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Preview Changes")
    st.caption("Run a dry-run to see what would change")
    if st.button("🔍 Dry Run", use_container_width=True):
        st.switch_page("pages/3_injection.py")

with col2:
    st.markdown("#### Execute Injection")
    st.caption("Run the full injection pipeline")
    if st.button("🚀 Run Injection", use_container_width=True, type="primary"):
        st.switch_page("pages/3_injection.py")

with col3:
    st.markdown("#### View Results")
    st.caption("Review logs and diffs")
    if st.button("📊 View Results", use_container_width=True):
        st.switch_page("pages/4_results.py")

# System status
st.markdown("---")
st.subheader("🔧 System Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    raw_count = len(list((ARTICLES_DIR / "raw").glob("*.md"))) if (ARTICLES_DIR / "raw").exists() else 0
    if raw_count > 0:
        st.success(f"✅ {raw_count} raw articles ready")
    else:
        st.error("❌ No raw articles found")

with status_col2:
    if matrix:
        st.success(f"✅ Keyword matrix loaded ({matrix['statistics']['total_assignments']} assignments)")
    else:
        st.warning("⚠️ Run keyword assignment first")

with status_col3:
    processed_count = len(list((ARTICLES_DIR / "processed").glob("*.md"))) if (ARTICLES_DIR / "processed").exists() else 0
    if processed_count > 0:
        st.info(f"📝 {processed_count} articles processed")
    else:
        st.info("📝 No processed articles yet")

