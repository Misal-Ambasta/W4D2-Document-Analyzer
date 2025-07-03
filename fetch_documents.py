#!/usr/bin/env python3
"""
Sample Document Fetcher for Document Analyzer MCP Server
Fetches diverse text samples from various free APIs and sources
"""

import requests
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Any

class DocumentFetcher:
    def __init__(self):
        self.documents = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_wikipedia_articles(self, titles: List[str]) -> List[Dict]:
        """Fetch Wikipedia article summaries"""
        documents = []
        
        for title in titles:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    doc = {
                        'id': f"wiki_{len(documents) + 1}",
                        'title': data.get('title', title),
                        'content': data.get('extract', ''),
                        'source': 'Wikipedia',
                        'category': 'Encyclopedia',
                        'date': datetime.now().isoformat(),
                        'word_count': len(data.get('extract', '').split()),
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                    }
                    
                    if doc['content']:  # Only add if content exists
                        documents.append(doc)
                        print(f"✓ Fetched: {doc['title']}")
                
                time.sleep(0.5)  # Be respectful to API
                
            except Exception as e:
                print(f"✗ Failed to fetch {title}: {e}")
        
        return documents
    
    def fetch_news_articles(self) -> List[Dict]:
        """Fetch sample news articles from NewsAPI (free tier)"""
        documents = []
        
        # Note: You'll need to get a free API key from https://newsapi.org/
        # For demo purposes, we'll use sample data
        
        sample_news = [
            {
                'title': 'Breakthrough in Renewable Energy Technology',
                'content': 'Scientists at leading universities have developed a new solar panel technology that could revolutionize renewable energy. The breakthrough promises to increase efficiency by 40% while reducing manufacturing costs. This development comes at a crucial time as governments worldwide push for cleaner energy solutions.',
                'category': 'Technology'
            },
            {
                'title': 'Local Community Garden Initiative Blooms',
                'content': 'A grassroots community garden project has transformed an abandoned lot into a thriving green space. Residents have come together to grow fresh vegetables and herbs, creating not just food but also stronger neighborhood bonds. The initiative has become a model for urban sustainability.',
                'category': 'Community'
            },
            {
                'title': 'Economic Uncertainty Affects Small Businesses',
                'content': 'Recent market fluctuations have created challenges for small business owners across the region. Many are adapting by embracing digital transformation and finding new ways to connect with customers. Economic experts suggest that flexibility and innovation will be key to weathering current uncertainties.',
                'category': 'Business'
            }
        ]
        
        for i, article in enumerate(sample_news):
            doc = {
                'id': f"news_{i + 1}",
                'title': article['title'],
                'content': article['content'],
                'source': 'News Sample',
                'category': article['category'],
                'date': datetime.now().isoformat(),
                'word_count': len(article['content'].split()),
                'url': ''
            }
            documents.append(doc)
            print(f"✓ Added news: {doc['title']}")
        
        return documents
    
    def fetch_quotes_and_short_texts(self) -> List[Dict]:
        """Fetch inspirational quotes and short texts"""
        documents = []
        
        # Sample short texts with different sentiments
        short_texts = [
            {
                'title': 'Inspirational Quote',
                'content': 'The only way to do great work is to love what you do. Success comes to those who dare to pursue their dreams with passion and persistence.',
                'category': 'Inspiration',
                'sentiment_hint': 'positive'
            },
            {
                'title': 'Technical Explanation',
                'content': 'Machine learning algorithms process vast amounts of data to identify patterns and make predictions. These systems learn from examples without being explicitly programmed for every scenario.',
                'category': 'Technical',
                'sentiment_hint': 'neutral'
            },
            {
                'title': 'Product Review - Negative',
                'content': 'Unfortunately, this product did not meet my expectations. The build quality feels cheap and the functionality is limited. I would not recommend this to others and will be returning it.',
                'category': 'Review',
                'sentiment_hint': 'negative'
            },
            {
                'title': 'Product Review - Positive',
                'content': 'Absolutely fantastic product! The quality exceeded my expectations and the customer service was outstanding. I highly recommend this to anyone considering a purchase.',
                'category': 'Review',
                'sentiment_hint': 'positive'
            },
            {
                'title': 'Creative Writing Sample',
                'content': 'The old lighthouse stood sentinel against the storm, its beam cutting through the darkness like a sword of hope. Waves crashed against the rocky shore, but the structure remained unmoved, a testament to human ingenuity and determination.',
                'category': 'Creative',
                'sentiment_hint': 'neutral'
            }
        ]
        
        for i, text in enumerate(short_texts):
            doc = {
                'id': f"short_{i + 1}",
                'title': text['title'],
                'content': text['content'],
                'source': 'Sample Collection',
                'category': text['category'],
                'date': datetime.now().isoformat(),
                'word_count': len(text['content'].split()),
                'sentiment_hint': text['sentiment_hint'],
                'url': ''
            }
            documents.append(doc)
            print(f"✓ Added short text: {doc['title']}")
        
        return documents
    
    def fetch_all_documents(self) -> List[Dict]:
        """Fetch all types of documents"""
        print("🚀 Fetching sample documents...")
        
        # Wikipedia articles on diverse topics
        wiki_titles = [
            'Python_(programming_language)',
            'Climate_change',
            'Artificial_intelligence',
            'Space_exploration',
            'Renewable_energy',
            'Music_theory',
            'Cooking'
        ]
        
        # Fetch from different sources
        wiki_docs = self.fetch_wikipedia_articles(wiki_titles)
        news_docs = self.fetch_news_articles()
        short_docs = self.fetch_quotes_and_short_texts()
        
        # Combine all documents
        all_documents = wiki_docs + news_docs + short_docs
        
        # Add some variety with different lengths
        self.add_sample_documents(all_documents)
        
        print(f"\n✅ Successfully fetched {len(all_documents)} documents")
        return all_documents
    
    def add_sample_documents(self, documents: List[Dict]):
        """Add some manually crafted samples for variety"""
        
        manual_samples = [
            {
                'id': 'manual_1',
                'title': 'Simple Recipe Instructions',
                'content': 'Heat oil in pan. Add onions. Cook until golden. Add garlic. Stir for one minute. Season with salt and pepper. Serve hot.',
                'source': 'Manual Sample',
                'category': 'Instructions',
                'date': datetime.now().isoformat(),
                'word_count': 24,
                'url': ''
            },
            {
                'id': 'manual_2',
                'title': 'Academic Abstract Sample',
                'content': 'This study examines the correlation between social media usage and academic performance among university students. Data was collected from 500 participants over a six-month period. Results indicate a moderate negative correlation between excessive social media use and GPA scores. The findings suggest that educational institutions should consider implementing digital wellness programs.',
                'source': 'Manual Sample',
                'category': 'Academic',
                'date': datetime.now().isoformat(),
                'word_count': 54,
                'url': ''
            }
        ]
        
        documents.extend(manual_samples)
        for doc in manual_samples:
            print(f"✓ Added manual sample: {doc['title']}")
    
    def save_documents(self, documents: List[Dict], filename: str = 'sample_documents.json'):
        """Save documents to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
            print(f"💾 Documents saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving documents: {e}")
    
    def load_documents(self, filename: str = 'sample_documents.json') -> List[Dict]:
        """Load documents from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            print(f"📖 Loaded {len(documents)} documents from {filename}")
            return documents
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return []
        except Exception as e:
            print(f"❌ Error loading documents: {e}")
            return []

def main():
    """Main function to fetch and save sample documents"""
    fetcher = DocumentFetcher()
    
    # Fetch all documents
    documents = fetcher.fetch_all_documents()
    
    # Save to file
    fetcher.save_documents(documents)
    
    # Display summary
    print("\n📊 Document Summary:")
    categories = {}
    for doc in documents:
        category = doc.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
    
    for category, count in categories.items():
        print(f"   {category}: {count} documents")
    
    print(f"\n🎉 Ready to use {len(documents)} sample documents for your MCP server!")

if __name__ == "__main__":
    main()