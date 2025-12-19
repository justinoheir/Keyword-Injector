"""
Shared UI Components for Keyword Injection GUI
"""

import streamlit as st
from pathlib import Path
import json


# Paths
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
ARTICLES_DIR = SCRIPT_DIR / "articles"
KEYWORDS_DIR = SCRIPT_DIR / "keywords"
LOGS_DIR = SCRIPT_DIR / "logs"
CONFIG_DIR = SCRIPT_DIR / "config"


def load_json(path):
    """Safely load a JSON file."""
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
            return None
    return None


def status_badge(status: str, text: str = None) -> str:
    """Generate HTML for a status badge."""
    colors = {
        "success": ("#166534", "#86efac"),
        "warning": ("#854d0e", "#fde047"),
        "error": ("#991b1b", "#fca5a5"),
        "info": ("#1e40af", "#93c5fd"),
    }
    
    bg, fg = colors.get(status, colors["info"])
    display_text = text or status.title()
    
    return f"""
    <span style="
        background-color: {bg};
        color: {fg};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    ">{display_text}</span>
    """


def metric_card(value, label: str, color: str = "#a855f7") -> str:
    """Generate HTML for a metric card."""
    return f"""
    <div style="
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3d3d5c;
        text-align: center;
    ">
        <div style="
            font-size: 2.5rem;
            font-weight: 700;
            color: {color};
        ">{value}</div>
        <div style="
            font-size: 0.9rem;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">{label}</div>
    </div>
    """


def get_article_lookup():
    """Get article ID to title lookup."""
    manifest = load_json(ARTICLES_DIR / "article-manifest.json")
    if manifest:
        return {a["id"]: a for a in manifest["articles"]}
    return {}


def get_keyword_lookup():
    """Get keyword ID to info lookup."""
    manifest = load_json(KEYWORDS_DIR / "keyword-manifest.json")
    if manifest:
        return {k["id"]: k for k in manifest["keywords"]}
    return {}


def get_runs():
    """Get list of injection runs."""
    if LOGS_DIR.exists():
        return sorted(
            [d for d in LOGS_DIR.iterdir() if d.is_dir() and d.name.startswith("run-")],
            reverse=True
        )
    return []


def display_keyword_badge(keyword_text: str, status: str = "default"):
    """Display a keyword as a styled badge."""
    colors = {
        "inserted": "#22c55e",
        "skipped": "#f59e0b",
        "default": "#6366f1"
    }
    color = colors.get(status, colors["default"])
    
    st.markdown(f"""
    <span style="
        background-color: {color}20;
        color: {color};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        margin-right: 4px;
    ">{keyword_text}</span>
    """, unsafe_allow_html=True)

