#!/usr/bin/env python3
"""
Script 01: Split Consolidated Markdown into Individual Article Files

This script extracts individual articles from a consolidated markdown file
and saves them as separate files with YAML frontmatter metadata.

Usage:
    python 01_split-articles.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import re
import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def slugify(text: str, max_length: int = 50) -> str:
    """Convert text to a URL-friendly slug."""
    # Remove special characters, convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace whitespace with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Truncate to max length at word boundary
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]
    return slug


def extract_themes(content: str, title: str) -> List[str]:
    """Extract themes from article content based on keyword patterns."""
    themes = []
    content_lower = (content + " " + title).lower()
    
    theme_patterns = {
        "kubernetes": ["kubernetes", "k8s", "eks", "aks", "gke", "container orchestration"],
        "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "cloudformation"],
        "azure": ["azure", "microsoft cloud"],
        "gcp": ["google cloud", "gcp", "bigquery"],
        "devops": ["devops", "ci/cd", "pipeline", "automation", "gitops", "github actions"],
        "security": ["security", "compliance", "hipaa", "sox", "pci", "encryption", "iam"],
        "migration": ["migration", "migrate", "modernization", "legacy"],
        "data-analytics": ["data", "analytics", "opensearch", "elasticsearch", "bigquery"],
        "serverless": ["serverless", "lambda", "functions", "faas"],
        "containers": ["container", "docker", "ecs", "fargate"],
        "genai": ["genai", "generative ai", "llm", "bedrock", "machine learning", "ai"],
        "terraform": ["terraform", "infrastructure as code", "iac"],
        "company-news": ["announces", "announcement", "welcomes", "achieves", "designation"],
        "case-study": ["customer success", "case study", "the challenge", "our solution", "the result"],
        "tutorial": ["walkthrough", "how to", "step by step", "tutorial", "guide"],
        "cloud-consulting": ["consulting", "cloud transformation", "digital transformation"],
    }
    
    for theme, patterns in theme_patterns.items():
        for pattern in patterns:
            if pattern in content_lower:
                themes.append(theme)
                break
    
    return list(set(themes)) if themes else ["general"]


def count_words(text: str) -> int:
    """Count words in text, excluding code blocks and metadata."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove special characters
    text = re.sub(r'[#*_\-\[\](){}|]', ' ', text)
    # Split and count
    words = text.split()
    return len(words)


def extract_articles(content: str) -> List[Tuple[str, str]]:
    """
    Extract individual articles from consolidated markdown.
    Returns list of (title, content) tuples.
    """
    # Split on H1 headers (# Title)
    # Pattern matches lines starting with single # followed by space and title
    pattern = r'^# ([^\n]+)\n'
    
    # Find all article starts
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    
    if not matches:
        print("Warning: No H1 headers found in content")
        return []
    
    articles = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.start()
        
        # Find end (start of next article or end of file)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)
        
        article_content = content[start:end].strip()
        articles.append((title, article_content))
    
    return articles


def generate_frontmatter(
    article_id: str,
    title: str,
    content: str,
    extraction_date: str
) -> str:
    """Generate YAML frontmatter for an article."""
    slug = slugify(title)
    word_count = count_words(content)
    themes = extract_themes(content, title)
    
    # Create content hash for change detection
    content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
    
    frontmatter = f"""---
id: "{article_id}"
slug: "{slug}"
title: "{title.replace('"', '\\"')}"
word_count: {word_count}
themes: {json.dumps(themes)}
extraction_date: "{extraction_date}"
content_hash: "{content_hash}"
---

"""
    return frontmatter


def save_article(
    output_dir: Path,
    article_id: str,
    title: str,
    content: str,
    extraction_date: str,
    dry_run: bool = False
) -> Dict:
    """Save an article to a file and return metadata."""
    slug = slugify(title)
    filename = f"{article_id}_{slug}.md"
    filepath = output_dir / filename
    
    frontmatter = generate_frontmatter(article_id, title, content, extraction_date)
    full_content = frontmatter + content
    
    metadata = {
        "id": article_id,
        "slug": slug,
        "title": title,
        "filename": filename,
        "word_count": count_words(content),
        "themes": extract_themes(content, title),
        "extraction_date": extraction_date,
    }
    
    if not dry_run:
        filepath.write_text(full_content, encoding='utf-8')
        print(f"  Created: {filename} ({metadata['word_count']} words)")
    else:
        print(f"  [DRY-RUN] Would create: {filename} ({metadata['word_count']} words)")
    
    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Split consolidated markdown into individual article files"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="OpsGuru_Blog_consolidated.md",
        help="Path to consolidated markdown file"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="articles/raw",
        help="Output directory for individual articles"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files"
    )
    parser.add_argument(
        "--manifest-output",
        type=str,
        default="articles/article-manifest.json",
        help="Path to output article manifest JSON"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent.parent
    input_path = script_dir / args.input
    output_dir = script_dir / args.output_dir
    manifest_path = script_dir / args.manifest_output
    
    print(f"Input file: {input_path}")
    print(f"Output directory: {output_dir}")
    print(f"Dry run: {args.dry_run}")
    print("-" * 50)
    
    # Read consolidated file
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    content = input_path.read_text(encoding='utf-8')
    print(f"Read {len(content):,} characters from input file")
    
    # Extract articles
    articles = extract_articles(content)
    print(f"Found {len(articles)} articles")
    print("-" * 50)
    
    # Ensure output directory exists
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each article
    extraction_date = datetime.now().strftime("%Y-%m-%d")
    manifest = {
        "extraction_date": extraction_date,
        "source_file": str(args.input),
        "total_articles": len(articles),
        "articles": []
    }
    
    for i, (title, article_content) in enumerate(articles, 1):
        article_id = f"{i:03d}"
        metadata = save_article(
            output_dir,
            article_id,
            title,
            article_content,
            extraction_date,
            dry_run=args.dry_run
        )
        manifest["articles"].append(metadata)
    
    # Save manifest
    if not args.dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print("-" * 50)
        print(f"Manifest saved to: {manifest_path}")
    
    # Summary
    print("-" * 50)
    total_words = sum(a["word_count"] for a in manifest["articles"])
    print(f"Total articles: {len(manifest['articles'])}")
    print(f"Total words: {total_words:,}")
    print(f"Average words per article: {total_words // len(manifest['articles']):,}")
    
    # Theme distribution
    theme_counts = {}
    for article in manifest["articles"]:
        for theme in article["themes"]:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    print("\nTheme distribution:")
    for theme, count in sorted(theme_counts.items(), key=lambda x: -x[1]):
        print(f"  {theme}: {count}")
    
    return 0


if __name__ == "__main__":
    exit(main())

