#!/usr/bin/env python3
"""
Script 02: Build Keyword Manifest and Assign Keywords to Articles

This script:
1. Parses keywords.csv into a structured manifest with clusters and variants
2. Maps keywords to articles based on theme matching
3. Produces keyword-article-matrix.json for the injection phase

Usage:
    python 02_assign-keywords.py [--keywords PATH] [--articles PATH] [--output-dir PATH]
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict


# Keyword clustering configuration
KEYWORD_CLUSTERS = {
    "healthcare": {
        "patterns": ["hipaa", "healthcare", "medical", "clinical", "patient", "health"],
        "target_themes": ["security", "compliance", "cloud-consulting", "migration"],
        "priority": 1
    },
    "financial": {
        "patterns": ["financial", "banking", "fintech", "sox", "pci", "credit", "investment", "insurance"],
        "target_themes": ["security", "compliance", "cloud-consulting", "migration", "data-analytics"],
        "priority": 1
    },
    "cloud-native": {
        "patterns": ["cloud-native", "kubernetes", "microservices", "serverless", "container"],
        "target_themes": ["kubernetes", "containers", "serverless", "devops", "aws", "azure", "gcp"],
        "priority": 2
    },
    "devops": {
        "patterns": ["devops", "ci/cd", "automation", "pipeline", "gitops"],
        "target_themes": ["devops", "automation", "terraform", "tutorial"],
        "priority": 2
    },
    "genai": {
        "patterns": ["genai", "ai", "bedrock", "llm", "machine learning", "semantic", "embedding", "transformer"],
        "target_themes": ["genai", "aws", "data-analytics", "tutorial"],
        "priority": 2
    },
    "cloud-consulting": {
        "patterns": ["consulting", "strategy", "transformation", "modernization", "optimization"],
        "target_themes": ["cloud-consulting", "migration", "company-news"],
        "priority": 3
    },
    "aws-specific": {
        "patterns": ["aws", "amazon", "eks", "ecs", "lambda", "bedrock", "nova"],
        "target_themes": ["aws", "kubernetes", "containers", "serverless", "genai"],
        "priority": 2
    },
    "security": {
        "patterns": ["security", "compliance", "credential", "soc", "sbom", "shadow"],
        "target_themes": ["security", "devops", "cloud-consulting"],
        "priority": 2
    },
    "general": {
        "patterns": [],
        "target_themes": ["general", "tutorial", "cloud-consulting"],
        "priority": 4
    }
}


def classify_keyword(keyword: str) -> Tuple[str, int]:
    """Classify a keyword into a cluster and assign priority."""
    keyword_lower = keyword.lower()
    
    for cluster_name, config in KEYWORD_CLUSTERS.items():
        if cluster_name == "general":
            continue
        for pattern in config["patterns"]:
            if pattern in keyword_lower:
                return cluster_name, config["priority"]
    
    return "general", KEYWORD_CLUSTERS["general"]["priority"]


def generate_variants(keyword: str) -> List[str]:
    """Generate semantic variants of a keyword."""
    variants = []
    keyword_lower = keyword.lower()
    
    # Variant strategies
    # 1. Reorder compound phrases
    words = keyword.split()
    if len(words) >= 2:
        # Try swapping first and last significant word
        if len(words) == 2:
            variants.append(f"{words[1]} {words[0]}")
        elif len(words) >= 3:
            # For "A B C", try "C B A" and "B A C"
            variants.append(" ".join(reversed(words)))
    
    # 2. Add common prefixes/suffixes
    if "consulting" in keyword_lower and "services" not in keyword_lower:
        variants.append(f"{keyword} services")
    if "cloud" in keyword_lower and "solutions" not in keyword_lower:
        variants.append(keyword.replace("cloud", "cloud solutions").replace("solutions solutions", "solutions"))
    
    # 3. Hyphenation variants
    if "-" in keyword:
        variants.append(keyword.replace("-", " "))
    elif " " in keyword and any(w in keyword_lower for w in ["native", "based", "driven"]):
        # "cloud native" -> "cloud-native"
        for connector in ["native", "based", "driven"]:
            if connector in keyword_lower:
                parts = keyword_lower.split(connector)
                if len(parts) == 2 and parts[0].strip():
                    variants.append(f"{parts[0].strip()}-{connector}{parts[1]}")
    
    # Remove duplicates and the original
    variants = [v for v in set(variants) if v.lower() != keyword_lower]
    
    return variants[:2]  # Limit to 2 variants


def parse_keywords(keywords_path: Path) -> List[Dict]:
    """Parse keywords.csv and build structured keyword objects."""
    content = keywords_path.read_text(encoding='utf-8')
    lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
    
    keywords = []
    seen = set()
    
    for i, line in enumerate(lines, 1):
        # Skip header if present
        if i == 1 and line.lower() in ['keyword', 'keywords', 'term', 'terms']:
            continue
        
        keyword = line.strip()
        keyword_lower = keyword.lower()
        
        # Skip duplicates
        if keyword_lower in seen:
            continue
        seen.add(keyword_lower)
        
        cluster, priority = classify_keyword(keyword)
        variants = generate_variants(keyword)
        
        keywords.append({
            "id": f"kw-{i:03d}",
            "text": keyword,
            "text_lower": keyword_lower,
            "cluster": cluster,
            "priority": priority,
            "max_exact_per_article": 2,
            "allow_semantic_variants": True,
            "variants": variants,
            "word_count": len(keyword.split())
        })
    
    return keywords


def load_article_manifest(manifest_path: Path) -> Dict:
    """Load the article manifest generated by script 01."""
    if not manifest_path.exists():
        raise FileNotFoundError(f"Article manifest not found: {manifest_path}")
    
    return json.loads(manifest_path.read_text(encoding='utf-8'))


def calculate_theme_match_score(keyword: Dict, article: Dict) -> float:
    """
    Calculate how well a keyword matches an article based on themes.
    Returns a score from 0.0 (no match) to 1.0 (perfect match).
    """
    cluster = keyword["cluster"]
    cluster_config = KEYWORD_CLUSTERS.get(cluster, KEYWORD_CLUSTERS["general"])
    target_themes = set(cluster_config["target_themes"])
    article_themes = set(article.get("themes", []))
    
    if not target_themes or not article_themes:
        return 0.1  # Minimal base score
    
    # Calculate intersection
    matching_themes = target_themes & article_themes
    
    if not matching_themes:
        return 0.0
    
    # Score based on match ratio
    score = len(matching_themes) / len(target_themes)
    
    # Boost for priority keywords
    priority_boost = (5 - keyword["priority"]) * 0.1
    
    return min(1.0, score + priority_boost)


def assign_keywords_to_articles(
    keywords: List[Dict],
    articles: List[Dict],
    config: Dict
) -> Dict:
    """
    Assign keywords to articles using theme-based matching.
    Returns the assignment matrix.
    """
    max_keywords_per_article = config.get("max_keywords_per_article", 5)
    max_articles_per_keyword = config.get("max_articles_per_keyword", 10)
    theme_mismatch_threshold = config.get("theme_mismatch_threshold", 0.7)
    
    # Track assignments
    article_keyword_counts = defaultdict(int)
    keyword_article_counts = defaultdict(int)
    assignments = {article["id"]: [] for article in articles}
    unassigned_keywords = []
    assignment_details = []
    
    # Sort keywords by priority (lower = higher priority)
    sorted_keywords = sorted(keywords, key=lambda k: (k["priority"], k["id"]))
    
    for keyword in sorted_keywords:
        kw_id = keyword["id"]
        
        # Calculate match scores for all articles
        scored_articles = []
        for article in articles:
            score = calculate_theme_match_score(keyword, article)
            if score > 0 and score >= (1 - theme_mismatch_threshold):
                scored_articles.append((article, score))
        
        # Sort by score descending
        scored_articles.sort(key=lambda x: -x[1])
        
        # Assign to top-scoring articles within limits
        assigned_count = 0
        for article, score in scored_articles:
            article_id = article["id"]
            
            # Check limits
            if article_keyword_counts[article_id] >= max_keywords_per_article:
                continue
            if keyword_article_counts[kw_id] >= max_articles_per_keyword:
                break
            
            # Assign
            assignments[article_id].append(kw_id)
            article_keyword_counts[article_id] += 1
            keyword_article_counts[kw_id] += 1
            assigned_count += 1
            
            assignment_details.append({
                "keyword_id": kw_id,
                "keyword_text": keyword["text"],
                "article_id": article_id,
                "article_title": article["title"],
                "match_score": round(score, 3),
                "matching_themes": list(set(article.get("themes", [])) & 
                                       set(KEYWORD_CLUSTERS.get(keyword["cluster"], {}).get("target_themes", [])))
            })
        
        if assigned_count == 0:
            unassigned_keywords.append({
                "keyword_id": kw_id,
                "keyword_text": keyword["text"],
                "cluster": keyword["cluster"],
                "reason": "no_matching_articles" if not scored_articles else "all_articles_at_capacity"
            })
    
    # Build final matrix
    matrix = {
        "generated_at": None,  # Will be set by caller
        "config": config,
        "assignments": [
            {
                "article_id": article_id,
                "assigned_keywords": kw_list,
                "assignment_count": len(kw_list)
            }
            for article_id, kw_list in assignments.items()
            if kw_list  # Only include articles with assignments
        ],
        "unassigned_keywords": unassigned_keywords,
        "assignment_details": assignment_details,
        "statistics": {
            "total_keywords": len(keywords),
            "assigned_keywords": len(keywords) - len(unassigned_keywords),
            "unassigned_keywords": len(unassigned_keywords),
            "total_articles": len(articles),
            "articles_with_keywords": len([a for a in assignments.values() if a]),
            "total_assignments": sum(len(a) for a in assignments.values()),
            "avg_keywords_per_article": round(
                sum(len(a) for a in assignments.values()) / 
                max(1, len([a for a in assignments.values() if a])), 2
            )
        }
    }
    
    return matrix


def build_keyword_manifest(keywords: List[Dict]) -> Dict:
    """Build the complete keyword manifest with cluster information."""
    clusters = defaultdict(list)
    for kw in keywords:
        clusters[kw["cluster"]].append(kw["id"])
    
    manifest = {
        "version": "1.0.0",
        "generated_at": None,  # Will be set by caller
        "total_keywords": len(keywords),
        "keywords": keywords,
        "clusters": {
            name: {
                "keyword_ids": ids,
                "count": len(ids),
                "target_themes": KEYWORD_CLUSTERS.get(name, {}).get("target_themes", []),
                "priority": KEYWORD_CLUSTERS.get(name, {}).get("priority", 4)
            }
            for name, ids in clusters.items()
        },
        "cluster_summary": {
            name: len(ids) for name, ids in clusters.items()
        }
    }
    
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Build keyword manifest and assign keywords to articles"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default="keywords/keywords.csv",
        help="Path to keywords CSV file"
    )
    parser.add_argument(
        "--articles",
        type=str,
        default="articles/article-manifest.json",
        help="Path to article manifest JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="keywords",
        help="Output directory for manifest and matrix"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/injection-rules.json",
        help="Path to injection rules config"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent.parent
    keywords_path = script_dir / args.keywords
    articles_path = script_dir / args.articles
    output_dir = script_dir / args.output_dir
    config_path = script_dir / args.config
    
    print(f"Keywords file: {keywords_path}")
    print(f"Articles manifest: {articles_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    # Load config
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding='utf-8'))
        assignment_config = config.get("assignment_rules", {})
    else:
        assignment_config = {
            "max_keywords_per_article": 5,
            "max_articles_per_keyword": 10,
            "theme_mismatch_threshold": 0.7
        }
    
    # Parse keywords
    if not keywords_path.exists():
        print(f"Error: Keywords file not found: {keywords_path}")
        return 1
    
    keywords = parse_keywords(keywords_path)
    print(f"Parsed {len(keywords)} unique keywords")
    
    # Build keyword manifest
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    
    manifest = build_keyword_manifest(keywords)
    manifest["generated_at"] = timestamp
    
    manifest_path = output_dir / "keyword-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"Keyword manifest saved to: {manifest_path}")
    
    # Print cluster summary
    print("\nCluster distribution:")
    for cluster, count in sorted(manifest["cluster_summary"].items(), key=lambda x: -x[1]):
        print(f"  {cluster}: {count}")
    
    # Load articles and assign keywords
    if not articles_path.exists():
        print(f"\nWarning: Article manifest not found: {articles_path}")
        print("Run 01_split-articles.py first to generate article manifest.")
        print("Skipping keyword assignment phase.")
        return 0
    
    article_manifest = load_article_manifest(articles_path)
    articles = article_manifest.get("articles", [])
    print(f"\nLoaded {len(articles)} articles")
    
    # Perform assignment
    matrix = assign_keywords_to_articles(keywords, articles, assignment_config)
    matrix["generated_at"] = timestamp
    
    matrix_path = output_dir / "keyword-article-matrix.json"
    matrix_path.write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"Assignment matrix saved to: {matrix_path}")
    
    # Print statistics
    stats = matrix["statistics"]
    print("\nAssignment Statistics:")
    print(f"  Total keywords: {stats['total_keywords']}")
    print(f"  Assigned keywords: {stats['assigned_keywords']}")
    print(f"  Unassigned keywords: {stats['unassigned_keywords']}")
    print(f"  Articles with keywords: {stats['articles_with_keywords']}/{stats['total_articles']}")
    print(f"  Total assignments: {stats['total_assignments']}")
    print(f"  Avg keywords per article: {stats['avg_keywords_per_article']}")
    
    if matrix["unassigned_keywords"]:
        print(f"\nUnassigned keywords ({len(matrix['unassigned_keywords'])}):")
        for uk in matrix["unassigned_keywords"][:10]:
            print(f"  - {uk['keyword_text']} ({uk['reason']})")
        if len(matrix["unassigned_keywords"]) > 10:
            print(f"  ... and {len(matrix['unassigned_keywords']) - 10} more")
    
    return 0


if __name__ == "__main__":
    exit(main())

