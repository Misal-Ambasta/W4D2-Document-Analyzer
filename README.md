# Document Analyzer MCP Server

A tool-based document analysis server using the FastMCP protocol (not REST), designed for AI clients (e.g., Claude) to call structured analysis tools directly.

## Features
- Document storage and management
- Sentiment analysis (VADER)
- Keyword extraction (TF-IDF with stopwords removal)
- Readability scoring (Flesch-Kincaid Grade Level)
- Basic stats (word/sentence count)

## Setup (with uv & pyproject.toml)

1. **Create and activate a virtual environment (recommended):**
   ```sh
   uv venv .venv
   source .venv/Scripts/activate  # On Windows (bash)
   # or .venv\Scripts\activate on Windows CMD
   ```

2. **Install dependencies:**
   ```sh
   uv pip install
   ```

3. **Fetch sample documents:**
   ```sh
   python fetch_documents.py
   ```

4. **Run the server (with MCP Inspector):**
   ```sh
   mcp dev main.py
   ```
   - This will launch the MCP server and Inspector for interactive tool testing.
   

## Exposed Tools
| Tool Name              | Description                                               | Arguments                        |
|------------------------|-----------------------------------------------------------|-----------------------------------|
| `analyze_document`     | Full analysis (sentiment, keywords, readability, stats)   | `document_id: str`                |
| `get_sentiment`        | Sentiment for any text (positive/negative/neutral)        | `text: str`                       |
| `extract_keywords`     | Top keywords from text (TF-IDF, stopwords removed)        | `text: str, limit: int = 5`       |
| `add_document`         | Add new document to storage                               | `document_data: dict`             |
| `search_documents`     | Search by content/title                                   | `query: str`                      |

## Protocol
- Uses FastMCP (JSON-RPC over stdio/SSE)
- No HTTP/REST endpoints
- Decorators (`@mcp.tool()`) expose functions as callable tools
- Type hints required for schema


## Notes
- All analysis logic is self-contained (no external API calls required at runtime)
- For production, persist new documents to file/database as needed