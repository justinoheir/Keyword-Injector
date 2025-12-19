"""
Export Page - Generate consolidated documents with change logs
"""

import streamlit as st
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="Export", page_icon="📦", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
ARTICLES_DIR = SCRIPT_DIR / "articles"
LOGS_DIR = SCRIPT_DIR / "logs"
EXPORTS_DIR = SCRIPT_DIR / "exports"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("📦 Export")
st.caption("Generate consolidated documents with change logs")

st.markdown("---")

# Current status
st.subheader("📊 Available Content")

col1, col2, col3 = st.columns(3)

with col1:
    raw_count = len(list((ARTICLES_DIR / "raw").glob("*.md"))) if (ARTICLES_DIR / "raw").exists() else 0
    st.metric("Raw Articles", raw_count)

with col2:
    processed_count = len(list((ARTICLES_DIR / "processed").glob("*.md"))) if (ARTICLES_DIR / "processed").exists() else 0
    st.metric("Processed Articles", processed_count)

with col3:
    runs = sorted([d for d in LOGS_DIR.iterdir() if d.is_dir() and d.name.startswith("run-")], reverse=True) if LOGS_DIR.exists() else []
    st.metric("Injection Runs", len(runs))

st.markdown("---")

# Export options
st.subheader("⚙️ Export Options")

col1, col2 = st.columns(2)

with col1:
    export_type = st.radio(
        "Export Type",
        ["Full Document (Articles + Change Log)", "Change Log Only", "Articles Only"],
        help="Choose what to include in the export"
    )

with col2:
    # Run selector
    if runs:
        run_options = ["Latest"] + [r.name for r in runs]
        selected_run = st.selectbox(
            "Include changes from run",
            options=run_options,
            help="Select which injection run to include in the change log"
        )
        
        if selected_run == "Latest":
            run_id = runs[0].name if runs else None
        else:
            run_id = selected_run
    else:
        st.info("No injection runs available")
        run_id = None

# Output format
st.markdown("---")
st.subheader("📄 Output Settings")

col1, col2 = st.columns(2)

with col1:
    output_filename = st.text_input(
        "Output filename",
        value=f"consolidated_articles_{datetime.now().strftime('%Y%m%d')}.md",
        help="Name for the exported file"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    include_toc = st.checkbox("Include Table of Contents", value=True)

st.markdown("---")

# Preview section
if run_id:
    with st.expander("📋 Preview Change Log Summary"):
        summary = load_json(LOGS_DIR / run_id / "run-summary.json")
        if summary:
            totals = summary.get("totals", {})
            
            st.markdown(f"**Run:** {run_id}")
            st.markdown(f"**Date:** {summary.get('started_at', 'Unknown')[:10]}")
            
            cols = st.columns(4)
            cols[0].metric("Processed", totals.get("articles_processed", 0))
            cols[1].metric("Passed", totals.get("articles_passed", 0))
            cols[2].metric("Keywords Added", totals.get("keywords_inserted", 0))
            cols[3].metric("Words Added", totals.get("total_words_added", 0))

# Export button
st.markdown("---")

if st.button("📦 Generate Export", type="primary", use_container_width=True):
    with st.spinner("Generating export..."):
        # Build command
        cmd = [
            sys.executable,
            str(SCRIPT_DIR / "scripts" / "05_export-consolidated.py"),
            "--output", f"exports/{output_filename}"
        ]
        
        if run_id:
            cmd.extend(["--run-id", run_id])
        
        if export_type == "Change Log Only":
            cmd.append("--log-only")
        
        # Run export
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR)
        )
    
    if result.returncode == 0:
        st.success("✅ Export generated successfully!")
        
        # Show output path
        output_path = EXPORTS_DIR / output_filename
        
        if output_path.exists():
            content = output_path.read_text(encoding='utf-8')
            
            # Stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Size", f"{len(content):,} chars")
            col2.metric("Words", f"{len(content.split()):,}")
            col3.metric("Lines", f"{len(content.splitlines()):,}")
            
            # Download button
            st.download_button(
                label="⬇️ Download Export",
                data=content,
                file_name=output_filename,
                mime="text/markdown",
                use_container_width=True
            )
            
            # Preview
            with st.expander("📄 Preview (first 5000 characters)"):
                st.markdown(content[:5000])
                if len(content) > 5000:
                    st.caption(f"... and {len(content) - 5000:,} more characters")
    else:
        st.error("❌ Export failed!")
        with st.expander("Error details"):
            st.code(result.stdout + result.stderr)

# Previous exports
st.markdown("---")
st.subheader("📁 Previous Exports")

if EXPORTS_DIR.exists():
    export_files = sorted(EXPORTS_DIR.glob("*.md"), reverse=True)
    
    if export_files:
        for export_file in export_files[:10]:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{export_file.name}**")
                st.caption(f"Modified: {datetime.fromtimestamp(export_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                size_kb = export_file.stat().st_size / 1024
                st.caption(f"{size_kb:.1f} KB")
            
            with col3:
                content = export_file.read_text(encoding='utf-8')
                st.download_button(
                    label="⬇️",
                    data=content,
                    file_name=export_file.name,
                    mime="text/markdown",
                    key=f"download_{export_file.name}"
                )
    else:
        st.info("No exports yet. Generate one above!")
else:
    st.info("No exports directory found.")

