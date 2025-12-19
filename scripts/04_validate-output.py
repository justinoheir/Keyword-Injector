#!/usr/bin/env python3
"""
Script 04: Validate Keyword Injection Output

This script performs comprehensive quality checks on injected articles:
- Word count and sentence modification limits
- Readability analysis
- Repeated phrase detection
- Factual claim detection
- Style consistency checks

Usage:
    python 04_validate-output.py [--run-id RUN_ID] [--article-ids IDS] [--strict]
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter, defaultdict
import math


class ArticleValidator:
    """Validates injected articles against quality standards."""
    
    def __init__(self, config: Dict, strict: bool = False):
        self.config = config
        self.strict = strict
        self.guardrails = config.get("guardrails", {})
        self.quality_config = config.get("quality_flags", {})
    
    def count_words(self, text: str) -> int:
        """Count words in text, excluding code blocks."""
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        return len(text.split())
    
    def count_sentences(self, text: str) -> int:
        """Count sentences in text."""
        text = re.sub(r'```[\s\S]*?```', '', text)
        sentences = re.split(r'[.!?]+\s+', text)
        return len([s for s in sentences if s.strip()])
    
    def calculate_readability(self, text: str) -> Dict:
        """
        Calculate readability metrics.
        Returns Flesch-Kincaid grade level and reading ease.
        """
        # Clean text
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        words = text.split()
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {"grade_level": 0, "reading_ease": 100}
        
        # Count syllables (simplified)
        def count_syllables(word):
            word = word.lower()
            if len(word) <= 3:
                return 1
            # Remove common endings that don't add syllables
            word = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', word)
            word = re.sub(r'^y', '', word)
            vowels = re.findall(r'[aeiouy]+', word)
            return max(1, len(vowels))
        
        total_syllables = sum(count_syllables(w) for w in words)
        
        avg_words_per_sentence = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        
        # Flesch Reading Ease
        reading_ease = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        # Flesch-Kincaid Grade Level
        grade_level = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59
        
        return {
            "grade_level": round(max(0, grade_level), 1),
            "reading_ease": round(max(0, min(100, reading_ease)), 1),
            "avg_words_per_sentence": round(avg_words_per_sentence, 1),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2)
        }
    
    def detect_repeated_phrases(self, text: str, min_words: int = 5, max_occurrences: int = 2) -> List[Dict]:
        """Detect repeated phrases in text."""
        # Clean text
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        words = text.lower().split()
        phrase_counts = Counter()
        
        for i in range(len(words) - min_words + 1):
            phrase = " ".join(words[i:i + min_words])
            phrase_counts[phrase] += 1
        
        repeated = []
        for phrase, count in phrase_counts.items():
            if count > max_occurrences:
                repeated.append({
                    "phrase": phrase,
                    "count": count,
                    "severity": "high" if count > max_occurrences + 2 else "medium"
                })
        
        return sorted(repeated, key=lambda x: -x["count"])
    
    def detect_awkward_patterns(self, text: str) -> List[Dict]:
        """Detect awkward constructions and patterns."""
        issues = []
        
        patterns = self.quality_config.get("awkward_construction_patterns", [])
        
        for pattern in patterns:
            try:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                for match in matches:
                    issues.append({
                        "pattern": pattern,
                        "match": match.group(),
                        "position": match.start(),
                        "context": text[max(0, match.start()-30):match.end()+30]
                    })
            except re.error:
                pass
        
        return issues
    
    def detect_new_facts(self, original: str, modified: str) -> List[Dict]:
        """Detect potential new facts added (URLs, statistics, proper nouns)."""
        issues = []
        
        # URLs
        original_urls = set(re.findall(r'https?://[^\s]+', original))
        modified_urls = set(re.findall(r'https?://[^\s]+', modified))
        new_urls = modified_urls - original_urls
        for url in new_urls:
            issues.append({
                "type": "new_url",
                "value": url,
                "severity": "high"
            })
        
        # Statistics/numbers with context
        original_stats = set(re.findall(r'\d+(?:\.\d+)?%', original))
        modified_stats = set(re.findall(r'\d+(?:\.\d+)?%', modified))
        new_stats = modified_stats - original_stats
        for stat in new_stats:
            issues.append({
                "type": "new_statistic",
                "value": stat,
                "severity": "high"
            })
        
        return issues
    
    def validate_article(
        self,
        original_path: Path,
        processed_path: Path
    ) -> Dict:
        """Validate a single article."""
        original = original_path.read_text(encoding='utf-8')
        processed = processed_path.read_text(encoding='utf-8')
        
        # Remove frontmatter for analysis
        original_body = re.sub(r'^---[\s\S]*?---\n*', '', original)
        processed_body = re.sub(r'^---[\s\S]*?---\n*', '', processed)
        
        article_id = original_path.name[:3]
        
        result = {
            "article_id": article_id,
            "filename": original_path.name,
            "validation_time": datetime.now().isoformat(),
            "passed": True,
            "checks": {},
            "issues": [],
            "warnings": []
        }
        
        # Word count check
        original_words = self.count_words(original_body)
        processed_words = self.count_words(processed_body)
        word_delta_pct = ((processed_words - original_words) / original_words * 100) if original_words > 0 else 0
        
        max_word_increase = self.guardrails.get("article_level", {}).get("max_word_count_increase_pct", 5)
        
        result["checks"]["word_count"] = {
            "original": original_words,
            "processed": processed_words,
            "delta": processed_words - original_words,
            "delta_pct": round(word_delta_pct, 2),
            "threshold": max_word_increase,
            "passed": word_delta_pct <= max_word_increase
        }
        
        if not result["checks"]["word_count"]["passed"]:
            result["passed"] = False
            result["issues"].append(f"Word count increase ({word_delta_pct:.1f}%) exceeds threshold ({max_word_increase}%)")
        
        # Readability check
        original_readability = self.calculate_readability(original_body)
        processed_readability = self.calculate_readability(processed_body)
        
        readability_drop = original_readability["reading_ease"] - processed_readability["reading_ease"]
        max_drop = self.guardrails.get("article_level", {}).get("max_readability_score_drop", 5)
        
        result["checks"]["readability"] = {
            "original": original_readability,
            "processed": processed_readability,
            "reading_ease_drop": round(readability_drop, 1),
            "threshold": max_drop,
            "passed": readability_drop <= max_drop
        }
        
        if not result["checks"]["readability"]["passed"]:
            if self.strict:
                result["passed"] = False
                result["issues"].append(f"Readability drop ({readability_drop:.1f}) exceeds threshold ({max_drop})")
            else:
                result["warnings"].append(f"Readability drop ({readability_drop:.1f}) exceeds threshold ({max_drop})")
        
        # Repeated phrases check
        max_occurrences = self.guardrails.get("article_level", {}).get("max_repeated_phrase_occurrences", 3)
        min_phrase_words = self.guardrails.get("article_level", {}).get("min_repeated_phrase_words", 5)
        
        repeated = self.detect_repeated_phrases(processed_body, min_phrase_words, max_occurrences)
        
        result["checks"]["repeated_phrases"] = {
            "count": len(repeated),
            "phrases": repeated[:5],
            "passed": len(repeated) == 0
        }
        
        if not result["checks"]["repeated_phrases"]["passed"]:
            result["passed"] = False
            result["issues"].append(f"Found {len(repeated)} repeated phrases")
        
        # Awkward patterns check
        awkward = self.detect_awkward_patterns(processed_body)
        
        result["checks"]["awkward_patterns"] = {
            "count": len(awkward),
            "patterns": awkward[:5],
            "passed": len(awkward) == 0
        }
        
        if not result["checks"]["awkward_patterns"]["passed"]:
            result["warnings"].append(f"Found {len(awkward)} potentially awkward constructions")
        
        # New facts check
        new_facts = self.detect_new_facts(original_body, processed_body)
        
        result["checks"]["new_facts"] = {
            "count": len(new_facts),
            "facts": new_facts,
            "passed": len(new_facts) == 0
        }
        
        if not result["checks"]["new_facts"]["passed"]:
            result["passed"] = False
            result["issues"].append(f"Found {len(new_facts)} potential new facts added")
        
        return result
    
    def validate_run(
        self,
        script_dir: Path,
        run_id: str,
        article_ids: Optional[List[str]] = None
    ) -> Dict:
        """Validate all articles from a run."""
        logs_dir = script_dir / "logs" / run_id
        raw_dir = script_dir / "articles" / "raw"
        processed_dir = script_dir / "articles" / "processed"
        
        # Load run summary
        summary_path = logs_dir / "run-summary.json"
        if not summary_path.exists():
            return {"error": f"Run summary not found: {summary_path}"}
        
        run_summary = json.loads(summary_path.read_text(encoding='utf-8'))
        
        # Get articles to validate
        if article_ids:
            articles_to_check = article_ids
        else:
            articles_to_check = [
                a["article_id"] for a in run_summary.get("article_summaries", [])
                if a.get("status") == "passed"
            ]
        
        validation_results = {
            "run_id": run_id,
            "validation_time": datetime.now().isoformat(),
            "strict_mode": self.strict,
            "articles_validated": 0,
            "articles_passed": 0,
            "articles_failed": 0,
            "total_issues": 0,
            "total_warnings": 0,
            "article_results": []
        }
        
        for article_id in articles_to_check:
            raw_files = list(raw_dir.glob(f"{article_id}_*.md"))
            processed_files = list(processed_dir.glob(f"{article_id}_*.md"))
            
            if not raw_files or not processed_files:
                continue
            
            result = self.validate_article(raw_files[0], processed_files[0])
            validation_results["article_results"].append(result)
            validation_results["articles_validated"] += 1
            
            if result["passed"]:
                validation_results["articles_passed"] += 1
            else:
                validation_results["articles_failed"] += 1
            
            validation_results["total_issues"] += len(result["issues"])
            validation_results["total_warnings"] += len(result["warnings"])
        
        return validation_results


def main():
    parser = argparse.ArgumentParser(
        description="Validate keyword injection output"
    )
    parser.add_argument(
        "--run-id",
        type=str,
        help="Run ID to validate (validates most recent if not specified)"
    )
    parser.add_argument(
        "--article-ids",
        type=str,
        help="Comma-separated list of article IDs to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode (warnings become failures)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/injection-rules.json",
        help="Path to injection rules config"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for validation report JSON"
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / args.config
    logs_dir = script_dir / "logs"
    
    # Load config
    config = json.loads(config_path.read_text(encoding='utf-8'))
    
    # Find run ID if not specified
    if args.run_id:
        run_id = args.run_id
    else:
        # Find most recent run
        runs = sorted([d.name for d in logs_dir.iterdir() if d.is_dir() and d.name.startswith("run-")])
        if not runs:
            print("No injection runs found")
            return 1
        run_id = runs[-1]
        print(f"Using most recent run: {run_id}")
    
    # Parse article IDs
    article_ids = None
    if args.article_ids:
        article_ids = [a.strip() for a in args.article_ids.split(",")]
    
    # Run validation
    validator = ArticleValidator(config, strict=args.strict)
    results = validator.validate_run(script_dir, run_id, article_ids)
    
    # Print results
    print(f"\nValidation Results for {run_id}")
    print("=" * 60)
    print(f"Articles validated: {results['articles_validated']}")
    print(f"Articles passed: {results['articles_passed']}")
    print(f"Articles failed: {results['articles_failed']}")
    print(f"Total issues: {results['total_issues']}")
    print(f"Total warnings: {results['total_warnings']}")
    
    if results["articles_failed"] > 0:
        print("\nFailed Articles:")
        print("-" * 60)
        for article in results["article_results"]:
            if not article["passed"]:
                print(f"\n  {article['article_id']}: {article['filename']}")
                for issue in article["issues"]:
                    print(f"    - {issue}")
    
    if results["total_warnings"] > 0:
        print("\nWarnings:")
        print("-" * 60)
        for article in results["article_results"]:
            if article["warnings"]:
                print(f"\n  {article['article_id']}:")
                for warning in article["warnings"]:
                    print(f"    - {warning}")
    
    # Save results
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = logs_dir / run_id / "validation-results.json"
    
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\nResults saved to: {output_path}")
    
    return 0 if results["articles_failed"] == 0 else 1


if __name__ == "__main__":
    exit(main())

