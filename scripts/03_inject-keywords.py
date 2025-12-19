#!/usr/bin/env python3
"""
Script 03: Core Keyword Injection Engine

This script performs the actual keyword injection into articles with:
- Natural language integration
- Comprehensive logging
- Guardrails and fail conditions
- Dry-run support

Usage:
    python 03_inject-keywords.py [--dry-run] [--article-ids 001,002] [--verbose]
"""

import re
import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import copy


@dataclass
class Placement:
    """Record of a single keyword placement."""
    location: Dict
    method: str
    before: str
    after: str


@dataclass
class KeywordAttempt:
    """Record of an attempt to inject a keyword."""
    keyword_id: str
    keyword_text: str
    action: str  # inserted, skipped
    occurrences_before: int
    occurrences_after: int
    placements: List[Dict] = field(default_factory=list)
    skip_reason: Optional[str] = None


@dataclass
class ArticleLog:
    """Complete injection log for a single article."""
    article_id: str
    article_title: str
    run_id: str
    timestamp: str
    metrics: Dict
    keywords_attempted: List[Dict]
    quality_flags: List[str]
    validation_status: str
    human_review_required: bool


class KeywordInjector:
    """Core injection engine with guardrails and logging."""
    
    def __init__(self, config: Dict, verbose: bool = False):
        self.config = config
        self.verbose = verbose
        self.insertion_rules = config.get("insertion_rules", {})
        self.guardrails = config.get("guardrails", {})
        
    def log(self, message: str):
        """Print verbose logging."""
        if self.verbose:
            print(f"    {message}")
    
    def count_words(self, text: str) -> int:
        """Count words in text, excluding code blocks."""
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        return len(text.split())
    
    def count_sentences(self, text: str) -> int:
        """Count sentences in text."""
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        # Split on sentence endings
        sentences = re.split(r'[.!?]+\s+', text)
        return len([s for s in sentences if s.strip()])
    
    def count_keyword_occurrences(self, text: str, keyword: str) -> int:
        """Count exact and near-match occurrences of a keyword."""
        pattern = re.escape(keyword)
        matches = re.findall(pattern, text, re.IGNORECASE)
        return len(matches)
    
    def extract_sections(self, content: str) -> List[Dict]:
        """Extract article sections with their headers and content."""
        sections = []
        
        # Remove frontmatter
        content_body = re.sub(r'^---[\s\S]*?---\n*', '', content)
        
        # Split by headers
        header_pattern = r'^(#{1,3})\s+(.+)$'
        lines = content_body.split('\n')
        
        current_section = {
            "level": 0,
            "header": "Introduction",
            "start_line": 0,
            "paragraphs": []
        }
        current_para = []
        para_start_line = 0
        
        for i, line in enumerate(lines):
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Save current paragraph
                if current_para:
                    current_section["paragraphs"].append({
                        "text": "\n".join(current_para),
                        "start_line": para_start_line,
                        "end_line": i - 1
                    })
                    current_para = []
                
                # Save current section
                if current_section["paragraphs"]:
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    "level": len(header_match.group(1)),
                    "header": header_match.group(2),
                    "start_line": i,
                    "paragraphs": []
                }
                para_start_line = i + 1
            elif line.strip():
                if not current_para:
                    para_start_line = i
                current_para.append(line)
            elif current_para:
                # Empty line = end of paragraph
                current_section["paragraphs"].append({
                    "text": "\n".join(current_para),
                    "start_line": para_start_line,
                    "end_line": i - 1
                })
                current_para = []
        
        # Don't forget last paragraph and section
        if current_para:
            current_section["paragraphs"].append({
                "text": "\n".join(current_para),
                "start_line": para_start_line,
                "end_line": len(lines) - 1
            })
        if current_section["paragraphs"]:
            sections.append(current_section)
        
        return sections
    
    def is_safe_context(self, text: str, position: int) -> bool:
        """Check if position is safe for injection (not in code, quotes, etc.)."""
        # Check if inside code block
        before_text = text[:position]
        code_block_opens = len(re.findall(r'```', before_text))
        if code_block_opens % 2 == 1:
            return False
        
        # Check if inside inline code
        inline_code_pattern = r'`[^`]*$'
        if re.search(inline_code_pattern, before_text):
            return False
        
        # Check if inside a quote (simple heuristic)
        quote_opens = before_text.count('"')
        if quote_opens % 2 == 1:
            return False
        
        return True
    
    def find_injection_candidates(
        self, 
        content: str, 
        keyword: Dict,
        existing_count: int
    ) -> List[Dict]:
        """Find potential injection points for a keyword."""
        max_per_article = self.insertion_rules.get("max_exact_match_per_keyword", 2)
        if existing_count >= max_per_article:
            return []
        
        candidates = []
        sections = self.extract_sections(content)
        keyword_text = keyword["text"]
        keyword_lower = keyword_text.lower()
        
        preferred_locations = self.insertion_rules.get("preferred_locations", [])
        
        for section_idx, section in enumerate(sections):
            section_name = section["header"]
            is_preferred = (
                (section_idx == 0 and "first_paragraph" in preferred_locations) or
                (section_idx == 1 and "second_paragraph" in preferred_locations) or
                ("conclusion" in preferred_locations and "conclusion" in section_name.lower()) or
                ("h2_subheadings" in preferred_locations and section["level"] == 2)
            )
            
            for para_idx, para in enumerate(section["paragraphs"]):
                para_text = para["text"]
                
                # Skip if paragraph is too short
                if len(para_text.split()) < 10:
                    continue
                
                # Split into sentences
                sentences = re.split(r'([.!?]+\s+)', para_text)
                
                for sent_idx in range(0, len(sentences), 2):
                    if sent_idx >= len(sentences):
                        break
                    
                    sentence = sentences[sent_idx]
                    if len(sentence.split()) < 8:
                        continue
                    
                    # Check for near-match (keyword words appear but not exact phrase)
                    keyword_words = keyword_lower.split()
                    sentence_lower = sentence.lower()
                    
                    words_present = sum(1 for w in keyword_words if w in sentence_lower)
                    partial_match = words_present >= len(keyword_words) * 0.5
                    
                    # Check for extension opportunity
                    extension_patterns = [
                        r'\b(services?|solutions?|platform|systems?)\b',
                        r'\b(helps?|enables?|provides?|offers?)\b',
                        r'\b(cloud|aws|azure|kubernetes)\b',
                    ]
                    has_extension_hook = any(
                        re.search(p, sentence_lower) for p in extension_patterns
                    )
                    
                    # Determine method
                    if partial_match:
                        method = "semantic-rewrite"
                        priority = 1
                    elif has_extension_hook:
                        method = "extend-sentence"
                        priority = 2
                    else:
                        method = "transitional"
                        priority = 3
                    
                    # Adjust priority for preferred locations
                    if is_preferred:
                        priority -= 0.5
                    
                    candidates.append({
                        "section_idx": section_idx,
                        "section_name": section_name,
                        "para_idx": para_idx,
                        "sent_idx": sent_idx // 2,
                        "sentence": sentence.strip(),
                        "method": method,
                        "priority": priority,
                        "para_start_line": para["start_line"]
                    })
        
        # Sort by priority
        candidates.sort(key=lambda x: x["priority"])
        
        return candidates[:5]  # Return top 5 candidates
    
    def inject_keyword(
        self,
        sentence: str,
        keyword: Dict,
        method: str
    ) -> Optional[str]:
        """
        Attempt to inject keyword into a sentence.
        Returns modified sentence or None if injection fails.
        """
        keyword_text = keyword["text"]
        keyword_lower = keyword_text.lower()
        max_words_to_add = self.insertion_rules.get("max_words_per_sentence_addition", 15)
        
        # Skip if keyword already present
        if keyword_lower in sentence.lower():
            return None
        
        original_word_count = len(sentence.split())
        
        if method == "semantic-rewrite":
            # Try to replace near-matches with exact keyword
            keyword_words = keyword_lower.split()
            
            # Look for similar phrases to replace
            patterns_to_try = [
                # "cloud solutions" -> "cloud consulting services"
                (r'\b(cloud\s+)(solutions?|services?)\b', f'\\1{keyword_text}'),
                # "consulting services" with variations
                (r'\b(consulting)\s+(and\s+)?(services?|solutions?)\b', keyword_text),
                # Generic service mentions
                (r'\b(professional|expert|specialized)\s+(services?|consulting)\b', keyword_text),
            ]
            
            modified = sentence
            for pattern, replacement in patterns_to_try:
                if re.search(pattern, modified, re.IGNORECASE):
                    new_sentence = re.sub(pattern, replacement, modified, count=1, flags=re.IGNORECASE)
                    if len(new_sentence.split()) - original_word_count <= max_words_to_add:
                        return new_sentence
            
            return None
            
        elif method == "extend-sentence":
            # Add keyword phrase to end of sentence
            # Find good extension points
            
            # Remove trailing punctuation
            sentence_stripped = sentence.rstrip('.!?')
            trailing = sentence[len(sentence_stripped):] if len(sentence) > len(sentence_stripped) else '.'
            
            # Extension templates
            extensions = [
                f" with {keyword_text}",
                f" through {keyword_text}",
                f" using {keyword_text}",
                f" leveraging {keyword_text}",
                f" including {keyword_text}",
            ]
            
            # Pick extension based on sentence context
            sentence_lower = sentence.lower()
            
            if any(w in sentence_lower for w in ['help', 'assist', 'enable', 'support']):
                extension = extensions[0]  # "with"
            elif any(w in sentence_lower for w in ['achiev', 'deliver', 'provid']):
                extension = extensions[1]  # "through"
            elif any(w in sentence_lower for w in ['leverag', 'utiliz', 'implement']):
                extension = extensions[2]  # "using"
            else:
                extension = extensions[0]  # default to "with"
            
            new_sentence = sentence_stripped + extension + trailing
            
            if len(new_sentence.split()) - original_word_count <= max_words_to_add:
                return new_sentence
            
            return None
            
        elif method == "transitional":
            # This requires more complex sentence restructuring
            # For safety, we'll skip these in automated injection
            return None
        
        return None
    
    def apply_injection(
        self,
        content: str,
        candidate: Dict,
        new_sentence: str
    ) -> str:
        """Apply the injection to the content."""
        old_sentence = candidate["sentence"]
        
        # Use simple string replacement
        # Be careful to only replace the first occurrence
        return content.replace(old_sentence, new_sentence, 1)
    
    def check_guardrails(
        self,
        original_content: str,
        modified_content: str,
        modifications: List[Dict]
    ) -> Tuple[bool, List[str]]:
        """Check if modifications violate guardrails."""
        flags = []
        article_guardrails = self.guardrails.get("article_level", {})
        
        # Word count check
        original_words = self.count_words(original_content)
        modified_words = self.count_words(modified_content)
        word_increase_pct = ((modified_words - original_words) / original_words * 100) if original_words > 0 else 0
        
        max_word_increase = article_guardrails.get("max_word_count_increase_pct", 5)
        if word_increase_pct > max_word_increase:
            flags.append(f"word_count_exceeded: {word_increase_pct:.1f}% > {max_word_increase}%")
        
        # Sentences modified check
        original_sentences = self.count_sentences(original_content)
        modified_count = len(modifications)
        modified_pct = (modified_count / original_sentences * 100) if original_sentences > 0 else 0
        
        max_modified = article_guardrails.get("max_sentences_modified_pct", 20)
        if modified_pct > max_modified:
            flags.append(f"sentences_modified_exceeded: {modified_pct:.1f}% > {max_modified}%")
        
        # Repeated phrase detection
        min_phrase_words = article_guardrails.get("min_repeated_phrase_words", 5)
        max_occurrences = article_guardrails.get("max_repeated_phrase_occurrences", 3)
        
        # Extract all 5+ word phrases and count
        words = modified_content.lower().split()
        phrase_counts = defaultdict(int)
        for i in range(len(words) - min_phrase_words + 1):
            phrase = " ".join(words[i:i + min_phrase_words])
            phrase_counts[phrase] += 1
        
        repeated = [p for p, c in phrase_counts.items() if c >= max_occurrences]
        if repeated:
            flags.append(f"repeated_phrases: {repeated[:3]}")
        
        # Determine pass/fail
        passed = len(flags) == 0
        return passed, flags
    
    def process_article(
        self,
        article_id: str,
        article_path: Path,
        keywords: List[Dict],
        run_id: str,
        dry_run: bool = False
    ) -> Tuple[Optional[str], ArticleLog]:
        """
        Process a single article for keyword injection.
        Returns (modified_content or None, log).
        """
        content = article_path.read_text(encoding='utf-8')
        
        # Extract frontmatter and body
        frontmatter_match = re.match(r'^(---[\s\S]*?---\n*)', content)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            body = content[len(frontmatter):]
        else:
            frontmatter = ""
            body = content
        
        # Extract title from frontmatter
        title_match = re.search(r'title:\s*"([^"]+)"', frontmatter)
        title = title_match.group(1) if title_match else article_id
        
        original_word_count = self.count_words(body)
        original_sentence_count = self.count_sentences(body)
        
        modified_body = body
        keyword_attempts = []
        all_placements = []
        
        # Limit total modifications to stay within guardrails
        max_modifications = max(1, int(original_sentence_count * 0.15))  # 15% of sentences
        
        for keyword in keywords:
            # Early exit if we've hit the modification limit
            if len(all_placements) >= max_modifications:
                self.log(f"  Reached modification limit ({max_modifications}), skipping remaining keywords")
                # Log remaining keywords as skipped
                keyword_attempts.append({
                    "keyword_id": keyword["id"],
                    "keyword_text": keyword["text"],
                    "action": "skipped",
                    "occurrences_before": self.count_keyword_occurrences(modified_body, keyword["text"]),
                    "occurrences_after": self.count_keyword_occurrences(modified_body, keyword["text"]),
                    "skip_reason": "modification_limit_reached"
                })
                continue
            kw_id = keyword["id"]
            kw_text = keyword["text"]
            
            self.log(f"Attempting keyword: {kw_text}")
            
            # Count existing occurrences
            occurrences_before = self.count_keyword_occurrences(modified_body, kw_text)
            
            # Check if already at max
            max_per_article = keyword.get("max_exact_per_article", 2)
            if occurrences_before >= max_per_article:
                self.log(f"  Skipped: already at max ({occurrences_before})")
                keyword_attempts.append({
                    "keyword_id": kw_id,
                    "keyword_text": kw_text,
                    "action": "skipped",
                    "occurrences_before": occurrences_before,
                    "occurrences_after": occurrences_before,
                    "skip_reason": f"already_at_max: {occurrences_before}/{max_per_article}"
                })
                continue
            
            # Find candidates
            candidates = self.find_injection_candidates(modified_body, keyword, occurrences_before)
            
            if not candidates:
                self.log(f"  Skipped: no suitable candidates found")
                keyword_attempts.append({
                    "keyword_id": kw_id,
                    "keyword_text": kw_text,
                    "action": "skipped",
                    "occurrences_before": occurrences_before,
                    "occurrences_after": occurrences_before,
                    "skip_reason": "no_suitable_candidates"
                })
                continue
            
            # Try candidates
            placements = []
            attempts = 0
            max_attempts = self.guardrails.get("keyword_level", {}).get("max_insertion_attempts", 3)
            # Be conservative: only insert 1 occurrence per keyword per run
            target_insertions = min(1, max_per_article - occurrences_before)
            
            for candidate in candidates:
                if len(placements) >= target_insertions:
                    break
                if attempts >= max_attempts:
                    break
                
                attempts += 1
                
                # Check if context is safe
                sentence = candidate["sentence"]
                pos = modified_body.find(sentence)
                if pos == -1 or not self.is_safe_context(modified_body, pos):
                    continue
                
                # Attempt injection
                new_sentence = self.inject_keyword(sentence, keyword, candidate["method"])
                
                if new_sentence:
                    modified_body = self.apply_injection(modified_body, candidate, new_sentence)
                    
                    placement = {
                        "location": {
                            "section": candidate["section_name"],
                            "paragraph": candidate["para_idx"],
                            "sentence": candidate["sent_idx"]
                        },
                        "method": candidate["method"],
                        "before": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                        "after": new_sentence[:100] + "..." if len(new_sentence) > 100 else new_sentence
                    }
                    placements.append(placement)
                    all_placements.append(placement)
                    
                    self.log(f"  Inserted via {candidate['method']} at {candidate['section_name']}")
            
            occurrences_after = self.count_keyword_occurrences(modified_body, kw_text)
            
            if placements:
                keyword_attempts.append({
                    "keyword_id": kw_id,
                    "keyword_text": kw_text,
                    "action": "inserted",
                    "occurrences_before": occurrences_before,
                    "occurrences_after": occurrences_after,
                    "placements": placements
                })
            else:
                keyword_attempts.append({
                    "keyword_id": kw_id,
                    "keyword_text": kw_text,
                    "action": "skipped",
                    "occurrences_before": occurrences_before,
                    "occurrences_after": occurrences_before,
                    "skip_reason": "injection_failed_after_attempts"
                })
        
        # Calculate final metrics
        final_word_count = self.count_words(modified_body)
        final_sentence_count = self.count_sentences(modified_body)
        
        metrics = {
            "word_count_before": original_word_count,
            "word_count_after": final_word_count,
            "word_count_delta": final_word_count - original_word_count,
            "word_count_delta_pct": round((final_word_count - original_word_count) / original_word_count * 100, 2) if original_word_count > 0 else 0,
            "sentences_modified": len(all_placements),
            "sentences_total": original_sentence_count,
            "sentences_modified_pct": round(len(all_placements) / original_sentence_count * 100, 2) if original_sentence_count > 0 else 0
        }
        
        # Check guardrails
        passed, quality_flags = self.check_guardrails(body, modified_body, all_placements)
        
        # Build log
        log = ArticleLog(
            article_id=article_id,
            article_title=title,
            run_id=run_id,
            timestamp=datetime.now().isoformat(),
            metrics=metrics,
            keywords_attempted=keyword_attempts,
            quality_flags=quality_flags,
            validation_status="passed" if passed else "failed",
            human_review_required=not passed
        )
        
        if passed and not dry_run:
            return frontmatter + modified_body, log
        elif dry_run:
            return frontmatter + modified_body, log
        else:
            return None, log


def load_keyword_data(manifest_path: Path, matrix_path: Path) -> Tuple[Dict, Dict]:
    """Load keyword manifest and assignment matrix."""
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    matrix = json.loads(matrix_path.read_text(encoding='utf-8'))
    
    # Build keyword lookup
    keyword_lookup = {kw["id"]: kw for kw in manifest["keywords"]}
    
    return keyword_lookup, matrix


def main():
    parser = argparse.ArgumentParser(
        description="Inject keywords into articles with logging and guardrails"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without modifying files"
    )
    parser.add_argument(
        "--article-ids",
        type=str,
        help="Comma-separated list of article IDs to process (e.g., 001,002,003)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="articles/raw",
        help="Input directory for articles"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="articles/processed",
        help="Output directory for processed articles"
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
    input_dir = script_dir / args.input_dir
    output_dir = script_dir / args.output_dir
    config_path = script_dir / args.config
    manifest_path = script_dir / "keywords" / "keyword-manifest.json"
    matrix_path = script_dir / "keywords" / "keyword-article-matrix.json"
    
    # Generate run ID
    run_id = f"run-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"
    logs_dir = script_dir / "logs" / run_id / "article-logs"
    
    print(f"Run ID: {run_id}")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Dry run: {args.dry_run}")
    print("-" * 50)
    
    # Load config
    config = json.loads(config_path.read_text(encoding='utf-8'))
    
    # Load keyword data
    keyword_lookup, matrix = load_keyword_data(manifest_path, matrix_path)
    
    # Build article-to-keywords mapping
    article_keywords = {}
    for assignment in matrix["assignments"]:
        article_id = assignment["article_id"]
        kw_ids = assignment["assigned_keywords"]
        article_keywords[article_id] = [keyword_lookup[kw_id] for kw_id in kw_ids if kw_id in keyword_lookup]
    
    # Get list of articles to process
    if args.article_ids:
        article_ids = [a.strip() for a in args.article_ids.split(",")]
    else:
        article_ids = list(article_keywords.keys())
    
    print(f"Processing {len(article_ids)} articles")
    print("-" * 50)
    
    # Ensure output directories exist
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize injector
    injector = KeywordInjector(config, verbose=args.verbose)
    
    # Process articles
    run_summary = {
        "run_id": run_id,
        "started_at": datetime.now().isoformat(),
        "config_hash": hashlib.md5(json.dumps(config).encode()).hexdigest()[:12],
        "dry_run": args.dry_run,
        "totals": {
            "articles_processed": 0,
            "articles_passed": 0,
            "articles_failed": 0,
            "keywords_inserted": 0,
            "keywords_skipped": 0,
            "total_words_added": 0
        },
        "failed_articles": [],
        "article_summaries": []
    }
    
    for article_id in article_ids:
        # Find article file
        article_files = list(input_dir.glob(f"{article_id}_*.md"))
        if not article_files:
            print(f"  Warning: Article {article_id} not found, skipping")
            continue
        
        article_path = article_files[0]
        keywords = article_keywords.get(article_id, [])
        
        if not keywords:
            print(f"  {article_id}: No keywords assigned, skipping")
            continue
        
        print(f"  {article_id}: Processing with {len(keywords)} keywords...")
        
        # Process article
        modified_content, log = injector.process_article(
            article_id,
            article_path,
            keywords,
            run_id,
            dry_run=args.dry_run
        )
        
        # Update summary
        run_summary["totals"]["articles_processed"] += 1
        
        inserted = sum(1 for k in log.keywords_attempted if k["action"] == "inserted")
        skipped = sum(1 for k in log.keywords_attempted if k["action"] == "skipped")
        
        run_summary["totals"]["keywords_inserted"] += inserted
        run_summary["totals"]["keywords_skipped"] += skipped
        run_summary["totals"]["total_words_added"] += log.metrics["word_count_delta"]
        
        if log.validation_status == "passed":
            run_summary["totals"]["articles_passed"] += 1
        else:
            run_summary["totals"]["articles_failed"] += 1
            run_summary["failed_articles"].append(article_id)
        
        run_summary["article_summaries"].append({
            "article_id": article_id,
            "status": log.validation_status,
            "keywords_inserted": inserted,
            "keywords_skipped": skipped,
            "word_delta": log.metrics["word_count_delta"]
        })
        
        # Save log
        if not args.dry_run:
            log_path = logs_dir / f"{article_id}_injection-log.json"
            log_path.write_text(
                json.dumps(asdict(log), indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        
        # Save modified content
        if modified_content and log.validation_status == "passed":
            if not args.dry_run:
                output_path = output_dir / article_path.name
                output_path.write_text(modified_content, encoding='utf-8')
            print(f"    -> {inserted} inserted, {skipped} skipped, +{log.metrics['word_count_delta']} words")
        else:
            print(f"    -> FAILED: {log.quality_flags}")
    
    # Finalize summary
    run_summary["completed_at"] = datetime.now().isoformat()
    
    # Save run summary
    if not args.dry_run:
        summary_path = script_dir / "logs" / run_id / "run-summary.json"
        summary_path.write_text(
            json.dumps(run_summary, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    # Print summary
    print("-" * 50)
    print("Run Summary:")
    print(f"  Articles processed: {run_summary['totals']['articles_processed']}")
    print(f"  Articles passed: {run_summary['totals']['articles_passed']}")
    print(f"  Articles failed: {run_summary['totals']['articles_failed']}")
    print(f"  Keywords inserted: {run_summary['totals']['keywords_inserted']}")
    print(f"  Keywords skipped: {run_summary['totals']['keywords_skipped']}")
    print(f"  Total words added: {run_summary['totals']['total_words_added']}")
    
    if run_summary["failed_articles"]:
        print(f"\nFailed articles: {', '.join(run_summary['failed_articles'])}")
    
    # Check run-level guardrails
    run_guardrails = config.get("guardrails", {}).get("run_level", {})
    max_failed_pct = run_guardrails.get("max_failed_articles_pct", 10)
    
    if run_summary["totals"]["articles_processed"] > 0:
        failed_pct = run_summary["totals"]["articles_failed"] / run_summary["totals"]["articles_processed"] * 100
        if failed_pct > max_failed_pct:
            print(f"\nWARNING: Failed articles ({failed_pct:.1f}%) exceeds threshold ({max_failed_pct}%)")
            print("    Run should be reviewed before committing.")
    
    return 0


if __name__ == "__main__":
    exit(main())

