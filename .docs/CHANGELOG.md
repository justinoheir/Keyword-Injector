# Changelog

All notable changes to the Keyword Injection System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-12-19

### Added

- **Article Processing Pipeline**
  - `01_split-articles.py`: Splits consolidated markdown into individual files
  - Generates YAML frontmatter with id, slug, title, themes, word_count
  - Creates article manifest JSON for downstream processing

- **Keyword Management System**
  - `02_assign-keywords.py`: Parses and classifies keywords into clusters
  - Theme-based keyword-to-article matching algorithm
  - Generates keyword manifest and assignment matrix

- **Injection Engine**
  - `03_inject-keywords.py`: Core keyword injection with guardrails
  - Semantic rewrite method for natural integration
  - Sentence extension method for keyword appending
  - Comprehensive logging with before/after snippets
  - Dry-run mode for safe testing

- **Validation Suite**
  - `04_validate-output.py`: Post-injection quality checks
  - Readability analysis (Flesch-Kincaid)
  - Repeated phrase detection
  - New facts detection (URLs, statistics)
  - Generates validation reports

- **Utility Scripts**
  - `utils/diff_generator.py`: Creates diff reports for review
  - `utils/rollback.py`: Reverts injection changes via git or file copy

- **Configuration**
  - `injection-rules.json`: Thresholds and limits
  - `skip-patterns.json`: Contexts to avoid for injection

- **Documentation**
  - System specification
  - Project status tracking
  - Operational playbooks

### Guardrails Implemented

| Guardrail | Threshold |
|-----------|-----------|
| Max word count increase | 5% |
| Max sentences modified | 20% |
| Max repeated phrase occurrences | 3 |
| Max keywords per article | 5 |
| Max exact-match per keyword | 2 |

### Keyword Clusters

- Healthcare (26 keywords)
- Financial (26 keywords)
- Cloud-native (10 keywords)
- GenAI (8 keywords)
- Cloud-consulting (8 keywords)
- DevOps (5 keywords)
- Security (4 keywords)
- AWS-specific (2 keywords)
- General (5 keywords)

## [Unreleased]

### Planned
- Full injection run on all 98 articles
- Enhanced semantic matching for better placement
- Integration with CI/CD for automated processing

