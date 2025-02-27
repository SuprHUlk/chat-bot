from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os
import re

class DocumentIndexer:
    def __init__(self, docs_dir: str = "data/docs"):
        self.docs_dir = docs_dir
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),  # Include bigrams and trigrams for better matching
            max_df=0.85,         # Ignore terms that appear in >85% of documents
            min_df=2             # Ignore terms that appear in <2 documents
        )
        self.documents = []
        self.tfidf_matrix = None
        
    def load_documents(self):
        """Loads all CDP documentation from local storage"""
        self.documents = []
        for filename in os.listdir(self.docs_dir):
            if filename.endswith('_docs.json'):
                with open(os.path.join(self.docs_dir, filename)) as f:
                    self.documents.extend(json.load(f))
                    
        # Preprocess documents to enhance "how-to" matching
        for doc in self.documents:
            # Add extra weight to "how to" content
            doc['processed_content'] = self._preprocess_for_how_to(doc['content'])
                    
        # Create TF-IDF matrix
        texts = [doc['processed_content'] for doc in self.documents]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        
    def _preprocess_for_how_to(self, content: str) -> str:
        """
        Preprocess content to enhance matching for "how-to" questions
        """
        # Convert to lowercase for better matching
        processed = content.lower()
        
        # Add extra weight to sections that look like instructions or steps
        # by duplicating those parts in the processed content
        
        # Look for numbered steps (e.g., "1. Do this", "Step 1:", etc.)
        step_patterns = [
            r'\d+\.\s+[A-Z]',           # Numbered steps: "1. Do this"
            r'step\s+\d+',              # "Step 1:"
            r'first,\s+[a-z]',          # "First, do this"
            r'second,\s+[a-z]',         # "Second, do this"
            r'finally,\s+[a-z]',        # "Finally, do this"
            r'to\s+[a-z]+,\s+you\s+',   # "To configure, you need to..."
        ]
        
        # Look for "how to" phrases
        how_to_patterns = [
            r'how\s+to\s+[a-z]+',       # "how to configure"
            r'guide\s+to\s+[a-z]+',     # "guide to setting up"
            r'steps\s+to\s+[a-z]+',     # "steps to create"
            r'instructions\s+for\s+',   # "instructions for configuring"
            r'setup\s+',                # "setup process"
            r'configure\s+',            # "configure your account"
            r'create\s+',               # "create a new source"
            r'integrate\s+',            # "integrate with"
            r'connect\s+',              # "connect your data"
        ]
        
        # Duplicate content that matches step patterns to give it more weight
        for pattern in step_patterns:
            matches = re.findall(pattern, processed)
            if matches:
                # Add the matches again to increase their weight
                processed += " " + " ".join(matches)
                
        # Duplicate content that matches how-to patterns to give it more weight
        for pattern in how_to_patterns:
            matches = re.findall(pattern, processed)
            if matches:
                # Add the matches again to increase their weight
                processed += " " + " ".join(matches)
                
        return processed
        
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Searches for relevant documentation based on the query
        Returns top k most relevant documents
        """
        if not self.tfidf_matrix.shape[0]:
            raise ValueError("Documents not loaded. Call load_documents() first.")
            
        # Preprocess query to enhance "how-to" matching
        processed_query = self._preprocess_query(query)
            
        # Transform query
        query_vector = self.vectorizer.transform([processed_query])
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top k results
        # Make sure we don't try to get more results than we have documents
        top_k = min(top_k, len(similarities))
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Filter out low-relevance results
        results = []
        for idx in top_indices:
            score = float(similarities[idx])  # Convert to Python float to avoid numpy comparison issues
            if score > 0.1:  # Only include results with some relevance
                results.append({
                    'document': self.documents[idx],
                    'score': score
                })
                
        return results
        
    def _preprocess_query(self, query: str) -> str:
        """
        Preprocess the query to better match "how-to" content
        """
        # Convert to lowercase
        processed = query.lower()
        
        # If query doesn't already contain "how to", add it
        if "how to" not in processed and "how do i" not in processed:
            # Check if it's likely a how-to question
            action_verbs = ["create", "set up", "configure", "integrate", "connect", "build", "use"]
            
            for verb in action_verbs:
                if verb in processed:
                    # It's likely a how-to question, so add "how to" to enhance matching
                    processed = f"how to {processed}"
                    break
                    
        return processed 