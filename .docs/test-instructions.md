# Test Instructions

## Keyword Injection System Testing Guide

### Prerequisites

- Python 3.8+
- Git initialized repository
- All scripts in `scripts/` directory
- Configuration files in `config/` directory

---

## Test Cases

### TC-001: Article Splitting
**Purpose:** Verify consolidated markdown splits correctly into individual files

**Setup:**
- Place consolidated markdown file at project root

**Steps:**
1. Run: `python scripts/01_split-articles.py --dry-run`
2. Verify output shows correct article count
3. Run: `python scripts/01_split-articles.py`
4. Check `articles/raw/` for individual files

**Expected Results:**
- Correct number of articles extracted (98)
- Each file has YAML frontmatter
- Article manifest created at `articles/article-manifest.json`

---

### TC-002: Keyword Assignment
**Purpose:** Verify keywords are correctly classified and assigned

**Setup:**
- Articles must be split first (TC-001)
- Keywords CSV in `keywords/` directory

**Steps:**
1. Run: `python scripts/02_assign-keywords.py`
2. Review `keywords/keyword-manifest.json`
3. Review `keywords/keyword-article-matrix.json`

**Expected Results:**
- All keywords have cluster assignments
- Matrix shows keyword-to-article mappings
- Statistics printed to console

---

### TC-003: Injection Dry Run
**Purpose:** Verify injection logic without modifying files

**Steps:**
1. Run: `python scripts/03_inject-keywords.py --dry-run --article-ids "001,002,003"`
2. Review console output

**Expected Results:**
- No files modified
- Shows which keywords would be inserted/skipped
- Reports word count changes

---

### TC-004: Injection Execution
**Purpose:** Verify actual keyword injection

**Steps:**
1. Run: `python scripts/03_inject-keywords.py --article-ids "001,002,003"`
2. Check `articles/processed/` for output
3. Check `logs/` for run logs

**Expected Results:**
- Processed files created
- Run summary JSON created
- Per-article logs created

---

### TC-005: Guardrail Enforcement
**Purpose:** Verify guardrails prevent over-modification

**Steps:**
1. Temporarily lower word count threshold in config
2. Run injection on a small article
3. Verify article fails validation

**Expected Results:**
- Article marked as failed
- Quality flags list the exceeded threshold
- File not written to processed directory

---

### TC-006: Validation Suite
**Purpose:** Verify post-injection validation

**Setup:**
- Complete TC-004 first

**Steps:**
1. Run: `python scripts/04_validate-output.py`
2. Review validation results

**Expected Results:**
- All checks run (word count, readability, phrases)
- Results saved to logs directory
- Console shows pass/fail summary

---

### TC-007: Rollback
**Purpose:** Verify rollback functionality

**Setup:**
- Complete TC-004 first
- Commit processed files

**Steps:**
1. Run: `python scripts/utils/rollback.py --list-runs`
2. Run: `python scripts/utils/rollback.py --run-id RUN_ID --dry-run`
3. Run: `python scripts/utils/rollback.py --run-id RUN_ID`

**Expected Results:**
- Lists available runs
- Dry run shows files to restore
- Files restored to pre-injection state

---

## Regression Testing

After any code changes, run:

```bash
# Full pipeline test
python scripts/01_split-articles.py
python scripts/02_assign-keywords.py
python scripts/03_inject-keywords.py --dry-run
python scripts/04_validate-output.py
```

All commands should complete without errors.

---

## Performance Benchmarks

| Operation | Expected Time |
|-----------|---------------|
| Split 98 articles | < 5 seconds |
| Assign keywords | < 2 seconds |
| Inject 10 articles | < 10 seconds |
| Validate 10 articles | < 5 seconds |

