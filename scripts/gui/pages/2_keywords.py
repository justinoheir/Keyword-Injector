"""
Keywords Management Page
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.set_page_config(page_title="Keywords", page_icon="🏷️", layout="wide")

# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
KEYWORDS_DIR = SCRIPT_DIR / "keywords"
ARTICLES_DIR = SCRIPT_DIR / "articles"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


st.title("🏷️ Keywords Management")
st.caption("View keywords, clusters, and assignments")

# Load data
manifest = load_json(KEYWORDS_DIR / "keyword-manifest.json")
matrix = load_json(KEYWORDS_DIR / "keyword-article-matrix.json")

if manifest:
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Keywords", manifest["total_keywords"])
    
    with col2:
        st.metric("Clusters", len(manifest.get("clusters", {})))
    
    with col3:
        if matrix:
            st.metric("Assigned", matrix["statistics"]["assigned_keywords"])
        else:
            st.metric("Assigned", 0)
    
    with col4:
        if matrix:
            st.metric("Unassigned", matrix["statistics"]["unassigned_keywords"])
        else:
            st.metric("Unassigned", manifest["total_keywords"])
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All Keywords", "📊 By Cluster", "🔗 Assignments"])
    
    with tab1:
        st.subheader("All Keywords")
        
        # Filter
        col1, col2 = st.columns([2, 2])
        with col1:
            cluster_filter = st.multiselect(
                "Filter by Cluster",
                options=sorted(manifest.get("cluster_summary", {}).keys())
            )
        with col2:
            search = st.text_input("Search keywords", placeholder="Type to search...")
        
        # Build dataframe
        keywords = manifest.get("keywords", [])
        
        if cluster_filter:
            keywords = [k for k in keywords if k.get("cluster") in cluster_filter]
        
        if search:
            keywords = [k for k in keywords if search.lower() in k["text"].lower()]
        
        if keywords:
            # Build assignment counts
            assignment_counts = {}
            if matrix:
                for detail in matrix.get("assignment_details", []):
                    kw_id = detail["keyword_id"]
                    assignment_counts[kw_id] = assignment_counts.get(kw_id, 0) + 1
            
            df = pd.DataFrame([
                {
                    "ID": k["id"],
                    "Keyword": k["text"],
                    "Cluster": k.get("cluster", "general"),
                    "Priority": k.get("priority", 4),
                    "Articles": assignment_counts.get(k["id"], 0),
                    "Variants": len(k.get("variants", []))
                }
                for k in keywords
            ])
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Keyword": st.column_config.TextColumn("Keyword", width="large"),
                    "Cluster": st.column_config.TextColumn("Cluster", width="small"),
                    "Priority": st.column_config.NumberColumn("Priority", width="small"),
                    "Articles": st.column_config.NumberColumn("Articles", width="small"),
                    "Variants": st.column_config.NumberColumn("Variants", width="small"),
                }
            )
            
            st.caption(f"Showing {len(keywords)} keywords")
        else:
            st.info("No keywords match your filters.")
    
    with tab2:
        st.subheader("Keywords by Cluster")
        
        cluster_summary = manifest.get("cluster_summary", {})
        clusters = manifest.get("clusters", {})
        
        # Bar chart
        if cluster_summary:
            df = pd.DataFrame([
                {"Cluster": k, "Count": v}
                for k, v in sorted(cluster_summary.items(), key=lambda x: -x[1])
            ])
            st.bar_chart(df.set_index("Cluster"), color="#a855f7")
        
        st.markdown("---")
        
        # Cluster details
        for cluster_name, count in sorted(cluster_summary.items(), key=lambda x: -x[1]):
            cluster_info = clusters.get(cluster_name, {})
            
            with st.expander(f"**{cluster_name.title()}** ({count} keywords)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Target Themes:**")
                    themes = cluster_info.get("target_themes", [])
                    st.write(", ".join(themes) if themes else "None specified")
                
                with col2:
                    st.markdown("**Priority:**")
                    st.write(cluster_info.get("priority", "N/A"))
                
                # List keywords in this cluster
                cluster_keywords = [k for k in manifest["keywords"] if k.get("cluster") == cluster_name]
                if cluster_keywords:
                    st.markdown("**Keywords:**")
                    for kw in cluster_keywords[:20]:
                        st.markdown(f"- {kw['text']}")
                    if len(cluster_keywords) > 20:
                        st.caption(f"... and {len(cluster_keywords) - 20} more")
    
    with tab3:
        st.subheader("Keyword Assignments")
        
        if matrix:
            # Assignment statistics
            stats = matrix.get("statistics", {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Assignments", stats.get("total_assignments", 0))
            with col2:
                st.metric("Articles with Keywords", stats.get("articles_with_keywords", 0))
            with col3:
                st.metric("Avg Keywords/Article", stats.get("avg_keywords_per_article", 0))
            
            st.markdown("---")
            
            # Unassigned keywords
            unassigned = matrix.get("unassigned_keywords", [])
            if unassigned:
                with st.expander(f"⚠️ Unassigned Keywords ({len(unassigned)})", expanded=False):
                    for uk in unassigned:
                        st.markdown(f"- **{uk['keyword_text']}** - {uk.get('reason', 'unknown')}")
            
            # Assignment details
            st.markdown("### Assignment Details")
            
            # Build article lookup
            article_manifest = load_json(ARTICLES_DIR / "article-manifest.json")
            article_lookup = {}
            if article_manifest:
                article_lookup = {a["id"]: a["title"] for a in article_manifest["articles"]}
            
            # Group by article
            assignments = matrix.get("assignments", [])
            
            if assignments:
                for assignment in assignments[:50]:
                    article_id = assignment["article_id"]
                    kw_ids = assignment["assigned_keywords"]
                    article_title = article_lookup.get(article_id, "Unknown")[:50]
                    
                    with st.expander(f"**{article_id}** - {article_title}... ({len(kw_ids)} keywords)"):
                        # Get keyword texts
                        kw_lookup = {k["id"]: k for k in manifest["keywords"]}
                        for kw_id in kw_ids:
                            kw = kw_lookup.get(kw_id, {})
                            st.markdown(f"- {kw.get('text', kw_id)} `[{kw.get('cluster', '?')}]`")
                
                if len(assignments) > 50:
                    st.caption(f"Showing 50 of {len(assignments)} articles")
        else:
            st.warning("Keyword assignment matrix not found. Run the assignment script first:")
            st.code("python scripts/02_assign-keywords.py")
else:
    st.error("Keyword manifest not found. Please run the keyword scripts first:")
    st.code("python scripts/02_assign-keywords.py")

