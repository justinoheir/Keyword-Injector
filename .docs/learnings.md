# Learnings

## Keyword Injection System Development

### Problem: PowerShell Argument Parsing
**Date:** 2025-12-19

**Issue:** When passing comma-separated article IDs like `001,002,003` to Python scripts via PowerShell, the leading zeros were being stripped.

**Solution:** Wrap the argument in quotes: `--article-ids "001,002,003"`

**Tip:** Always quote string arguments in PowerShell when they contain special characters or leading zeros.

---

### Problem: Unicode Encoding in Windows Console
**Date:** 2025-12-19

**Issue:** Emoji characters (like warning symbols) caused `UnicodeEncodeError` when printing to Windows console using cp1252 encoding.

**Solution:** Replace emoji with plain text alternatives in console output:
```python
# Before (fails on Windows)
print("⚠️ WARNING: ...")

# After (works everywhere)
print("WARNING: ...")
```

**Tip:** Avoid emoji in CLI output for cross-platform compatibility.

---

### Problem: JSON File Encoding
**Date:** 2025-12-19

**Issue:** Reading JSON files without specifying encoding caused `UnicodeDecodeError` on Windows.

**Solution:** Always specify UTF-8 encoding:
```python
json.load(open('file.json', encoding='utf-8'))
```

---

### Problem: Aggressive Keyword Injection
**Date:** 2025-12-19

**Issue:** Initial injection logic was too aggressive, inserting 2 occurrences of each keyword and modifying too many sentences, causing guardrail failures.

**Solution:** 
1. Limit to 1 insertion per keyword per run
2. Track total modifications and stop early when approaching limits
3. Calculate max modifications as percentage of total sentences

**Tip:** Be conservative with automated content modification. Multiple passes are better than over-modification.

---

### Problem: Repeated Phrase Detection False Positives
**Date:** 2025-12-19

**Issue:** Articles with technical code blocks or repeated structural phrases (like "which will be executed on") were failing the repeated phrase check.

**Solution:** The current implementation correctly identifies these as potential issues. However, filtering out code blocks before detection helps reduce false positives.

**Tip:** Consider context when detecting repeated phrases - some repetition is natural in technical content.

---

### Problem: Theme-Based Keyword Assignment Gaps
**Date:** 2025-12-19

**Issue:** Healthcare and financial keywords had limited assignment opportunities because most blog articles are about general cloud/DevOps topics.

**Solution:** The system correctly identifies this mismatch. Options:
1. Accept lower coverage for niche keywords
2. Create topic-specific articles to target these keywords
3. Broaden theme matching criteria (with care)

**Tip:** Keyword strategy should align with content themes. Don't force irrelevant keywords.

