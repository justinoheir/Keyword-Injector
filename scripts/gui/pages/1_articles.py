"""
Articles Browser Page
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.set_page_config(page_title="Articles", page_icon="📄", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
ARTICLES_DIR = SCRIPT_DIR / "articles"
KEYWORDS_DIR = SCRIPT_DIR / "keywords"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("📄 Articles Browser")
st.caption("Browse, search, and preview articles")

# Load manifest
manifest_path = ARTICLES_DIR / "article-manifest.json"
matrix = load_json(KEYWORDS_DIR / "keyword-article-matrix.json")

if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    articles = manifest["articles"]
    
    # Build keyword lookup for articles
    article_keywords = {}
    if matrix:
        for assignment in matrix.get("assignments", []):
            article_keywords[assignment["article_id"]] = assignment["assigned_keywords"]
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        all_themes = sorted(set(t for a in articles for t in a.get("themes", [])))
        theme_filter = st.multiselect(
            "🏷️ Filter by Theme",
            options=all_themes
        )
    
    with col2:
        search = st.text_input("🔍 Search titles", placeholder="Type to search...")
    
    with col3:
        show_processed = st.checkbox("Show processed only", value=False)
    
    # Filter articles
    filtered = articles
    
    if theme_filter:
        filtered = [a for a in filtered if any(t in a.get("themes", []) for t in theme_filter)]
    
    if search:
        filtered = [a for a in filtered if search.lower() in a["title"].lower()]
    
    if show_processed:
        processed_dir = ARTICLES_DIR / "processed"
        if processed_dir.exists():
            processed_ids = set(f.name[:3] for f in processed_dir.glob("*.md"))
            filtered = [a for a in filtered if a["id"] in processed_ids]
    
    st.markdown(f"**Showing {len(filtered)} of {len(articles)} articles**")
    
    # Display as table
    if filtered:
        df = pd.DataFrame(filtered)
        df["themes"] = df["themes"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        df["keywords"] = df["id"].apply(lambda x: len(article_keywords.get(x, [])))
        
        # Check processed status
        processed_dir = ARTICLES_DIR / "processed"
        if processed_dir.exists():
            processed_ids = set(f.name[:3] for f in processed_dir.glob("*.md"))
            df["status"] = df["id"].apply(lambda x: "✅ Processed" if x in processed_ids else "⏳ Pending")
        else:
            df["status"] = "⏳ Pending"
        
        st.dataframe(
            df[["id", "title", "word_count", "keywords", "status", "themes"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Title", width="large"),
                "word_count": st.column_config.NumberColumn("Words", width="small"),
                "keywords": st.column_config.NumberColumn("Keywords", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "themes": st.column_config.TextColumn("Themes", width="medium"),
            }
        )
        
        # Article detail view
        st.markdown("---")
        st.subheader("📖 Article Preview")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_id = st.selectbox(
                "Select article to preview",
                options=[a["id"] for a in filtered],
                format_func=lambda x: f"{x} - {next(a['title'] for a in filtered if a['id'] == x)[:60]}..."
            )
        
        with col2:
            view_mode = st.radio("View", ["Original", "Processed", "Diff"], horizontal=True)
        
        if selected_id:
            article_files = list((ARTICLES_DIR / "raw").glob(f"{selected_id}_*.md"))
            processed_files = list((ARTICLES_DIR / "processed").glob(f"{selected_id}_*.md"))
            
            # Show assigned keywords
            if selected_id in article_keywords:
                keyword_manifest = load_json(KEYWORDS_DIR / "keyword-manifest.json")
                if keyword_manifest:
                    kw_lookup = {kw["id"]: kw["text"] for kw in keyword_manifest["keywords"]}
                    assigned = [kw_lookup.get(k, k) for k in article_keywords[selected_id]]
                    st.info(f"**Assigned Keywords:** {', '.join(assigned)}")
            
            if article_files:
                original_content = article_files[0].read_text(encoding='utf-8')
                
                # Remove frontmatter for display
                if original_content.startswith("---"):
                    parts = original_content.split("---", 2)
                    if len(parts) >= 3:
                        original_display = parts[2].strip()
                    else:
                        original_display = original_content
                else:
                    original_display = original_content
                
                if view_mode == "Original":
                    st.markdown(original_display[:5000] + ("..." if len(original_display) > 5000 else ""))
                
                elif view_mode == "Processed":
                    if processed_files:
                        processed_content = processed_files[0].read_text(encoding='utf-8')
                        if processed_content.startswith("---"):
                            parts = processed_content.split("---", 2)
                            if len(parts) >= 3:
                                processed_display = parts[2].strip()
                            else:
                                processed_display = processed_content
                        else:
                            processed_display = processed_content
                        st.markdown(processed_display[:5000] + ("..." if len(processed_display) > 5000 else ""))
                    else:
                        st.warning("No processed version available yet.")
                
                elif view_mode == "Diff":
                    if processed_files:
                        import difflib
                        processed_content = processed_files[0].read_text(encoding='utf-8')
                        
                        # Simple line diff
                        original_lines = original_content.split('\n')
                        processed_lines = processed_content.split('\n')
                        
                        diff = list(difflib.unified_diff(
                            original_lines,
                            processed_lines,
                            fromfile='original',
                            tofile='processed',
                            lineterm=''
                        ))
                        
                        if diff:
                            st.code('\n'.join(diff[:200]), language='diff')
                            if len(diff) > 200:
                                st.caption(f"... {len(diff) - 200} more lines")
                        else:
                            st.info("No differences found.")
                    else:
                        st.warning("No processed version available for diff.")
    else:
        st.info("No articles match your filters.")
else:
    st.error("Article manifest not found. Please run the split script first:")
    st.code("python scripts/01_split-articles.py")

