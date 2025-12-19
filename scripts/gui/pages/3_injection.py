"""
Keyword Injection Page
"""

import streamlit as st
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="Injection", page_icon="💉", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
KEYWORDS_DIR = SCRIPT_DIR / "keywords"
ARTICLES_DIR = SCRIPT_DIR / "articles"
CONFIG_DIR = SCRIPT_DIR / "config"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("💉 Keyword Injection")
st.caption("Run keyword injection on articles")

# Load data
matrix = load_json(KEYWORDS_DIR / "keyword-article-matrix.json")
config = load_json(CONFIG_DIR / "injection-rules.json")
article_manifest = load_json(ARTICLES_DIR / "article-manifest.json")

if not matrix:
    st.error("Keyword assignment matrix not found!")
    st.markdown("Run the assignment script first:")
    st.code("python scripts/02_assign-keywords.py")
    
    if st.button("🔧 Run Assignment Script"):
        with st.spinner("Running keyword assignment..."):
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "scripts" / "02_assign-keywords.py")],
                capture_output=True,
                text=True,
                cwd=str(SCRIPT_DIR)
            )
            if result.returncode == 0:
                st.success("Assignment complete! Refresh the page.")
            else:
                st.error("Assignment failed!")
            st.code(result.stdout + result.stderr)
    st.stop()

st.markdown("---")

# Configuration section
st.subheader("⚙️ Injection Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Run Mode")
    dry_run = st.toggle("🔍 Dry Run (preview only)", value=True, help="Preview changes without modifying files")
    verbose = st.toggle("📝 Verbose Output", value=False, help="Show detailed logging")

with col2:
    st.markdown("##### Current Limits")
    if config:
        guardrails = config.get("guardrails", {}).get("article_level", {})
        st.caption(f"Max word increase: {guardrails.get('max_word_count_increase_pct', 5)}%")
        st.caption(f"Max sentences modified: {guardrails.get('max_sentences_modified_pct', 20)}%")
        st.caption(f"Max repeated phrases: {guardrails.get('max_repeated_phrase_occurrences', 3)}")

st.markdown("---")

# Article selection
st.subheader("📄 Select Articles")

all_assignments = matrix.get("assignments", [])
all_article_ids = [a["article_id"] for a in all_assignments]

# Build article info lookup
article_info = {}
if article_manifest:
    for a in article_manifest["articles"]:
        article_info[a["id"]] = a

# Selection method
selection_method = st.radio(
    "Selection method",
    ["All Articles", "Select Specific", "By Theme", "Quick Sample"],
    horizontal=True
)

selected_articles = []

if selection_method == "All Articles":
    selected_articles = all_article_ids
    st.info(f"Will process all **{len(selected_articles)}** articles")

elif selection_method == "Select Specific":
    # Multiselect with article titles
    options = []
    for aid in all_article_ids:
        info = article_info.get(aid, {})
        title = info.get("title", "Unknown")[:40]
        kw_count = next((a["assignment_count"] for a in all_assignments if a["article_id"] == aid), 0)
        options.append(f"{aid} - {title}... ({kw_count} kw)")
    
    selected_options = st.multiselect(
        "Select articles",
        options=options,
        help="Select articles to process"
    )
    
    selected_articles = [opt.split(" - ")[0] for opt in selected_options]
    st.caption(f"Selected: {len(selected_articles)} articles")

elif selection_method == "By Theme":
    # Get all themes
    all_themes = set()
    for a in article_manifest.get("articles", []) if article_manifest else []:
        all_themes.update(a.get("themes", []))
    
    selected_themes = st.multiselect(
        "Select themes",
        options=sorted(all_themes)
    )
    
    if selected_themes:
        for aid in all_article_ids:
            info = article_info.get(aid, {})
            if any(t in info.get("themes", []) for t in selected_themes):
                selected_articles.append(aid)
    
    st.caption(f"Matched: {len(selected_articles)} articles")

elif selection_method == "Quick Sample":
    sample_size = st.slider("Sample size", min_value=1, max_value=20, value=5)
    selected_articles = all_article_ids[:sample_size]
    st.caption(f"Will process first {sample_size} articles")

# Preview selected articles
if selected_articles and len(selected_articles) <= 20:
    with st.expander("📋 Preview Selected Articles", expanded=False):
        for aid in selected_articles:
            assignment = next((a for a in all_assignments if a["article_id"] == aid), None)
            info = article_info.get(aid, {})
            
            kw_count = assignment["assignment_count"] if assignment else 0
            title = info.get("title", "Unknown")[:50]
            
            st.markdown(f"- **{aid}**: {title}... ({kw_count} keywords)")

st.markdown("---")

# Run injection
st.subheader("🚀 Execute")

col1, col2 = st.columns([2, 1])

with col1:
    if dry_run:
        button_text = "🔍 Run Dry Run (Preview)"
        button_type = "secondary"
    else:
        button_text = "🚀 Run Injection"
        button_type = "primary"
    
    run_button = st.button(
        button_text,
        type=button_type,
        use_container_width=True,
        disabled=len(selected_articles) == 0
    )

with col2:
    if not dry_run:
        st.warning("⚠️ This will modify files!")

if run_button:
    if not selected_articles:
        st.error("No articles selected!")
    else:
        # Build command
        cmd = [sys.executable, str(SCRIPT_DIR / "scripts" / "03_inject-keywords.py")]
        
        if dry_run:
            cmd.append("--dry-run")
        if verbose:
            cmd.append("--verbose")
        if selected_articles and len(selected_articles) < len(all_article_ids):
            cmd.extend(["--article-ids", ",".join(selected_articles)])
        
        st.markdown("---")
        st.markdown("### 📊 Execution Output")
        
        # Progress placeholder
        progress_placeholder = st.empty()
        output_placeholder = st.empty()
        
        with st.spinner(f"Processing {len(selected_articles)} articles..."):
            start_time = datetime.now()
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(SCRIPT_DIR)
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
        
        # Show results
        if result.returncode == 0:
            st.success(f"✅ Injection completed in {elapsed:.1f}s")
        else:
            st.error(f"❌ Injection failed (exit code: {result.returncode})")
        
        # Parse output for summary
        output = result.stdout + result.stderr
        
        # Display output
        with st.expander("📝 Full Output", expanded=True):
            st.code(output)
        
        # Quick stats from output
        if "Run Summary:" in output:
            st.markdown("### 📈 Quick Stats")
            
            lines = output.split("\n")
            for line in lines:
                if "Articles processed:" in line:
                    st.metric("Processed", line.split(":")[-1].strip())
                elif "Articles passed:" in line:
                    st.metric("Passed", line.split(":")[-1].strip())
                elif "Keywords inserted:" in line:
                    st.metric("Keywords Inserted", line.split(":")[-1].strip())
        
        # Next steps
        st.markdown("---")
        st.markdown("### Next Steps")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 View Results", use_container_width=True):
                st.switch_page("pages/4_results.py")
        with col2:
            if st.button("⏪ Rollback", use_container_width=True):
                st.switch_page("pages/5_rollback.py")

