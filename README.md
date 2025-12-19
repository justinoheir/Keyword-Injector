# Keyword Injection System

A scalable, auditable workflow system for SEO keyword injection across blog articles with full version control, structured logging, and quality guardrails.

## Features

- **Natural Language Integration**: Keywords are integrated semantically, not bolted on
- **Comprehensive Logging**: Every change is tracked with before/after snippets
- **Quality Guardrails**: Automatic checks prevent over-modification
- **Version Control Ready**: Git-integrated with easy rollback capabilities
- **Scalable Architecture**: Handles 100+ articles without quality loss

## Quick Start

### Option 1: GUI (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the GUI
streamlit run scripts/gui/app.py
```

Then open **http://localhost:8501** in your browser.

### Option 2: Command Line

```bash
# 1. Split consolidated articles
python scripts/01_split-articles.py

# 2. Assign keywords to articles
python scripts/02_assign-keywords.py

# 3. Preview changes (dry run)
python scripts/03_inject-keywords.py --dry-run

# 4. Execute injection
python scripts/03_inject-keywords.py

# 5. Validate output
python scripts/04_validate-output.py
```

## Project Structure

```
├── articles/
│   ├── raw/              # Original articles
│   └── processed/        # Keyword-injected versions
├── keywords/
│   ├── keywords.csv      # Master keyword list
│   ├── keyword-manifest.json
│   └── keyword-article-matrix.json
├── logs/                 # Per-run injection logs
├── config/
│   ├── injection-rules.json
│   └── skip-patterns.json
├── scripts/
│   ├── 01_split-articles.py
│   ├── 02_assign-keywords.py
│   ├── 03_inject-keywords.py
│   ├── 04_validate-output.py
│   ├── gui/              # Streamlit GUI
│   │   ├── app.py        # Main dashboard
│   │   └── pages/        # GUI pages
│   └── utils/
└── .docs/                # Documentation
```

## GUI Features

The Streamlit GUI provides:

- **Dashboard**: Overview metrics and recent runs
- **Articles Browser**: Search, filter, and preview articles
- **Keywords Manager**: View clusters and assignments
- **Injection Runner**: Execute with dry-run support
- **Results Viewer**: Diffs and validation reports
- **Rollback Interface**: Revert changes easily

## Configuration

### injection-rules.json

Controls thresholds and limits:
- Max keywords per article: 5
- Max word count increase: 5%
- Max sentences modified: 20%

### skip-patterns.json

Defines contexts to avoid:
- Code blocks
- Quoted text
- URLs and email addresses

## Guardrails

| Check | Threshold | Action |
|-------|-----------|--------|
| Word count increase | > 5% | Fail article |
| Sentences modified | > 20% | Fail article |
| Repeated phrases | > 3 occurrences | Fail article |
| Failed articles | > 10% of total | Warn on run |

## Rollback

```bash
# List available runs
python scripts/utils/rollback.py --list-runs

# Rollback specific run
python scripts/utils/rollback.py --run-id RUN_ID

# Rollback single article
python scripts/utils/rollback.py --run-id RUN_ID --article-id 001
```

## Documentation

See `.docs/` for:
- [System Specification](.docs/keyword-injection-spec.md)
- [Project Status](.docs/projectstatus.md)
- [Changelog](.docs/CHANGELOG.md)
- [Test Instructions](.docs/test-instructions.md)
- [Glossary](.docs/glossary.md)
- [Learnings](.docs/learnings.md)

## Requirements

- Python 3.8+
- Git

## License

Proprietary - OpsGuru

