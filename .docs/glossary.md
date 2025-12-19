# Glossary

## System Terms

### Article Manifest
JSON file containing metadata for all extracted articles, including id, slug, title, themes, and word count.

### Keyword Cluster
A grouping of related keywords by theme (e.g., healthcare, financial, cloud-native) used for targeted article matching.

### Keyword Manifest
JSON file containing all keywords with their cluster assignments, priorities, and semantic variants.

### Keyword-Article Matrix
JSON file mapping which keywords should be injected into which articles, based on theme matching.

### Injection Run
A single execution of the injection script, producing a timestamped set of logs and processed articles.

### Guardrail
A threshold or limit that prevents over-modification of content (e.g., max word count increase).

### Semantic Rewrite
Injection method that modifies existing phrases to incorporate keywords naturally.

### Sentence Extension
Injection method that appends keyword phrases to the end of existing sentences.

### Dry Run
Execution mode that simulates injection without modifying files, useful for testing.

---

## SEO Terms

### Keyword Stuffing
The practice of overloading content with keywords, which degrades readability and can trigger search engine penalties.

### Exact Match
When a keyword appears in content exactly as specified, without variations.

### Semantic Variant
An alternative phrasing of a keyword that conveys the same meaning (e.g., "cloud consulting" vs "consulting for cloud").

### Keyword Density
The percentage of words in content that are keywords. Generally, 1-2% is considered optimal.

---

## Technical Terms

### Frontmatter
YAML metadata block at the beginning of markdown files, delimited by `---`.

### Flesch-Kincaid
Readability metric that indicates the U.S. school grade level required to understand text.

### YAML
"YAML Ain't Markup Language" - a human-readable data serialization format used for configuration and metadata.

---

## Acronyms

| Acronym | Meaning |
|---------|---------|
| SEO | Search Engine Optimization |
| HIPAA | Health Insurance Portability and Accountability Act |
| SOX | Sarbanes-Oxley Act |
| PCI DSS | Payment Card Industry Data Security Standard |
| CI/CD | Continuous Integration / Continuous Deployment |
| EKS | Elastic Kubernetes Service |
| AKS | Azure Kubernetes Service |
| GKE | Google Kubernetes Engine |
| IAC | Infrastructure as Code |
| LLM | Large Language Model |

