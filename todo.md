# Document Analyzer MCP Server: Implementation Plan

Track each phase with `[ ]` (incomplete) and `[x]` (complete).

---

## Phase 1: Data Preparation
- [x] Fetch/generate 15+ sample documents with metadata ([fetch_documents.py])
- [x] Save sample documents to `sample_documents.json`

## Phase 2: MCP Server Setup
- [x] Set up FastMCP server with `FastMCP("document_analyzer")`
- [x] Load documents from `sample_documents.json` at startup
- [x] Expose document storage and retrieval functions

## Phase 3: Analysis Tools
- [x] Implement `@mcp.tool()` for:
    - [x] `analyze_document(document_id)` (sentiment, keywords, readability, stats)
    - [x] `get_sentiment(text)` (positive/negative/neutral)
    - [x] `extract_keywords(text, limit)` (TF-IDF, stopwords removed)
    - [x] `add_document(document_data)` (append new doc to storage)
    - [x] `search_documents(query)` (basic search in title + content)

## Phase 4: Analysis Logic
- [x] Sentiment analysis (simple model or library)
- [x] Keyword extraction (scikit-learn TF-IDF, stopwords)
- [x] Readability scoring (Flesch-Kincaid Grade Level)
- [x] Basic stats (word count, sentence count)

## Phase 5: Testing & Completion
- [x] Test all MCP tools with sample inputs
- [x] Validate schema/type hints for all tools
- [x] Confirm server runs and tools are discoverable by AI client
- [x] Document the MCP server and its tools in `README.md`

---

Mark each `[ ]` as `[x]` upon completion.
