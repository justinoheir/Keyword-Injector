# Keyword Injection System Specification

## Overview

This system provides a scalable, auditable workflow to inject SEO keywords across blog articles while maintaining content quality and natural language flow.

## System Architecture

```
V3/
├── articles/
│   ├── raw/              # Original articles (immutable reference)
│   └── processed/        # Keyword-injected versions
├── keywords/
│   ├── keywords.csv      # Master keyword list
│   ├── keyword-manifest.json
│   └── keyword-article-matrix.json
├── logs/
│   └── {run-id}/         # Per-run logs and reports
├── config/
│   ├── injection-rules.json
│   └── skip-patterns.json
└── scripts/
    ├── 01_split-articles.py
    ├── 02_assign-keywords.py
    ├── 03_inject-keywords.py
    ├── 04_validate-output.py
    └── utils/
```

## Processing Pipeline

### Phase 1: Article Preparation
```bash
python scripts/01_split-articles.py
```
- Splits consolidated markdown into individual article files
- Generates YAML frontmatter with metadata (id, slug, title, themes)
- Creates `articles/article-manifest.json`

### Phase 2: Keyword Assignment
```bash
python scripts/02_assign-keywords.py
```
- Parses keywords and classifies into thematic clusters
- Matches keywords to articles based on theme alignment
- Creates `keywords/keyword-manifest.json` and `keyword-article-matrix.json`

### Phase 3: Keyword Injection
```bash
python scripts/03_inject-keywords.py [--dry-run] [--article-ids IDS] [--verbose]
```
- Injects assigned keywords into articles
- Applies guardrails and quality checks
- Generates detailed per-article logs

### Phase 4: Validation
```bash
python scripts/04_validate-output.py [--run-id ID] [--strict]
```
- Validates processed articles against quality standards
- Checks word count, readability, repeated phrases
- Generates validation report

## Keyword Clusters

| Cluster | Keywords | Target Themes |
|---------|----------|---------------|
| healthcare | HIPAA, medical, clinical, patient | security, compliance |
| financial | banking, fintech, SOX, PCI | security, compliance |
| cloud-native | kubernetes, serverless, containers | kubernetes, devops |
| devops | CI/CD, automation, pipeline | devops, tutorial |
| genai | AI, bedrock, LLM, semantic | genai, aws |

## Insertion Rules

| Rule | Value | Rationale |
|------|-------|-----------|
| Max keywords per article | 5 | Prevents stuffing |
| Max exact-match per keyword | 2 | Avoids repetition |
| Max sentences modified | 15% | Limits disruption |
| Max words added | 5% | Prevents bloat |

## Guardrails

### Article-Level (abort if exceeded)
- Word count increase > 5%
- Sentences modified > 20%
- Repeated 5-word phrase > 3 times
- New factual claims detected

### Run-Level (warning if exceeded)
- Failed articles > 10%
- Average word count increase > 4%

## Rollback Procedures

### Rollback single article
```bash
git checkout HEAD~1 -- articles/processed/001_*.md
```

### Rollback entire run
```bash
python scripts/utils/rollback.py --run-id RUN_ID
```

### List available runs
```bash
python scripts/utils/rollback.py --list-runs
```

## Logging

Each injection run produces:
- `run-summary.json`: Aggregate statistics
- `article-logs/*.json`: Per-article detailed logs
- `validation-results.json`: Quality check results

### Log Schema
```json
{
  "article_id": "001",
  "keywords_attempted": [
    {
      "keyword_id": "kw-001",
      "keyword_text": "cloud consulting services",
      "action": "inserted|skipped",
      "placements": [...],
      "skip_reason": "..."
    }
  ],
  "metrics": {
    "word_count_before": 500,
    "word_count_after": 515,
    "sentences_modified": 3
  }
}
```

## Usage Examples

### Full Pipeline (Recommended)
```bash
# 1. Split articles
python scripts/01_split-articles.py

# 2. Assign keywords
python scripts/02_assign-keywords.py

# 3. Dry run first
python scripts/03_inject-keywords.py --dry-run

# 4. Execute injection
python scripts/03_inject-keywords.py

# 5. Validate output
python scripts/04_validate-output.py

# 6. Review and commit
git add articles/processed/ logs/
git commit -m "[keyword-inject] Batch injection with validation"
```

### Selective Processing
```bash
# Process specific articles
python scripts/03_inject-keywords.py --article-ids "001,002,003"

# Verbose output
python scripts/03_inject-keywords.py --verbose

# Strict validation
python scripts/04_validate-output.py --strict
```

## Configuration

### injection-rules.json
Controls all thresholds and limits for the injection process.

### skip-patterns.json
Defines contexts where injection should be avoided (code blocks, quotes, etc.).

## Version Control Strategy

1. Work on `feature/keyword-injection-system` branch
2. Each injection run creates a commit with detailed message
3. Review diffs before merging to main
4. Use git revert for rollback if needed

