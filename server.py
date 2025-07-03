"""
MCP Server Setup for Document Analyzer
"""
from mcp.server.fastmcp import FastMCP
import json
from typing import List, Dict, Any
import threading

# Load documents at startup
def load_documents(filename: str = 'sample_documents.json') -> List[Dict[str, Any]]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        print(f"Loaded {len(documents)} documents from {filename}")
        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

documents_lock = threading.Lock()
documents: List[Dict[str, Any]] = load_documents()

# MCP Server instance
mcp = FastMCP("document_analyzer")

# Document storage and retrieval functions (not yet tools)
def get_all_documents() -> List[Dict[str, Any]]:
    with documents_lock:
        return list(documents)

def get_document_by_id(doc_id: str) -> Dict[str, Any]:
    with documents_lock:
        for doc in documents:
            if doc.get('id') == doc_id:
                return doc
    return {}

from typing import Optional

@mcp.tool()
def analyze_document(document_id: str) -> dict:
    """Full document analysis: sentiment, keywords, readability, stats."""
    doc = get_document_by_id(document_id)
    if not doc:
        return {"error": "Document not found"}
    text = doc.get("content", "")
    return {
        "id": doc.get("id"),
        "title": doc.get("title"),
        "sentiment": get_sentiment(text),
        "keywords": extract_keywords(text, 5),
        "readability": get_readability(text),
        "stats": {
            "word_count": get_word_count(text),
            "sentence_count": get_sentence_count(text)
        }
    }

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)

@mcp.tool()
def get_sentiment(text: str) -> str:
    """Analyze sentiment of the input text (positive/negative/neutral)."""
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

@mcp.tool()
def extract_keywords(text: str, limit: int = 5) -> list:
    """Extract top keywords from text using TF-IDF and stopwords removal."""
    if not text or len(text.split()) < 3:
        return []
    
    stop_words = set(stopwords.words('english'))
    
    # Split text into sentences to give TF-IDF multiple "documents"
    sentences = text.split('. ')
    if len(sentences) < 2:
        # Fallback: simple word frequency for short texts
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top words by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:limit]]
    
    try:
        vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=limit)
        tfidf = vectorizer.fit_transform(sentences)
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
    except Exception:
        return []

@mcp.tool()
def add_document(document_data: dict) -> dict:
    """Add a new document to storage."""
    with documents_lock:
        doc_id = document_data.get("id") or f"user_{len(documents)+1}"
        document_data["id"] = doc_id
        document_data["word_count"] = get_word_count(document_data.get("content", ""))
        documents.append(document_data)
        # Optionally, persist to file (not required for MVP)
        return {"success": True, "id": doc_id}

@mcp.tool()
def search_documents(query: str) -> list:
    """Basic search in title + content. Returns list of matching documents."""
    results = []
    query_lower = query.lower()
    
    with documents_lock:
        for doc in documents:
            title = doc.get("title", "").lower()
            content = doc.get("content", "").lower()
            
            # Debug: Check if query matches
            if query_lower in title or query_lower in content:
                results.append({
                    "id": doc.get("id"), 
                    "title": doc.get("title"),
                    "snippet": doc.get("content", "")[:100] + "..."  # Add snippet
                })
    
    # If no results and query is empty, return all documents
    if not results and not query.strip():
        with documents_lock:
            for doc in documents:
                results.append({
                    "id": doc.get("id"), 
                    "title": doc.get("title")
                })
    
    return results

# --- Analysis Logic for Readability and Stats ---
import textstat
import re

def get_readability(text: str) -> float:
    """Flesch-Kincaid Grade Level readability score."""
    try:
        return textstat.flesch_kincaid_grade(text)
    except Exception:
        return -1.0

def get_word_count(text: str) -> int:
    return len(text.split())

def get_sentence_count(text: str) -> int:
    # Use textstat for robust sentence count
    try:
        return textstat.sentence_count(text)
    except Exception:
        # Fallback: simple split
        return len(re.split(r'[.!?]+', text))
