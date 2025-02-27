from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

class DocumentProcessor:
    def __init__(self, base_docs_dir: str = "data/docs"):
        self.base_docs_dir = base_docs_dir
        self.cdp_sources = {
            "segment": "https://segment.com/docs/",
            "mparticle": "https://docs.mparticle.com/",
            "lytics": "https://docs.lytics.com/",
            "zeotap": "https://docs.zeotap.com/home/en-us/"
        }
        
        # Create directory if it doesn't exist
        os.makedirs(self.base_docs_dir, exist_ok=True)
        
    def fetch_all_documentation(self):
        """Fetches documentation from all supported CDPs"""
        for cdp in self.cdp_sources:
            print(f"Fetching documentation for {cdp}...")
            self.fetch_documentation(cdp)
            
    def fetch_documentation(self, cdp: str) -> List[Dict]:
        """
        Fetches documentation from the specified CDP's website
        Returns a list of dictionaries containing processed content
        """
        if cdp not in self.cdp_sources:
            raise ValueError(f"Unsupported CDP: {cdp}")
            
        base_url = self.cdp_sources[cdp]
        docs = []
        
        try:
            # Start with the main documentation page
            pages_to_visit = [base_url]
            visited_pages = set()
            
            # Limit the number of pages to crawl to avoid excessive requests
            max_pages = 50
            count = 0
            
            while pages_to_visit and count < max_pages:
                url = pages_to_visit.pop(0)
                
                if url in visited_pages:
                    continue
                    
                visited_pages.add(url)
                count += 1
                
                print(f"Processing {url} ({count}/{max_pages})")
                
                # Fetch the page
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Failed to fetch {url}: {response.status_code}")
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content based on CDP-specific selectors
                content = self._extract_content(soup, cdp)
                
                if content:
                    # Create document
                    title = self._extract_title(soup)
                    doc = {
                        'title': title,
                        'content': content,
                        'url': url,
                        'cdp': cdp
                    }
                    docs.append(doc)
                
                # Find more links to follow
                new_links = self._extract_links(soup, base_url, url)
                for link in new_links:
                    if link not in visited_pages and link not in pages_to_visit:
                        pages_to_visit.append(link)
                
                # Be nice to the server
                time.sleep(1)
                
        except Exception as e:
            print(f"Error fetching documentation for {cdp}: {str(e)}")
            
        # Save to local file
        self._save_docs(cdp, docs)
        return docs
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the page"""
        title_tag = soup.find(['h1', 'h2'])
        if title_tag:
            return title_tag.get_text().strip()
        return soup.title.get_text().strip() if soup.title else "Untitled"
    
    def _extract_content(self, soup: BeautifulSoup, cdp: str) -> str:
        """Extract content based on CDP-specific selectors"""
        content = ""
        
        # Different CDPs have different HTML structures
        if cdp == "segment":
            main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
            if main_content:
                # Extract all paragraphs, lists, and code blocks
                for elem in main_content.find_all(['p', 'ul', 'ol', 'pre', 'code', 'h2', 'h3', 'h4']):
                    content += elem.get_text().strip() + "\n\n"
        
        elif cdp == "mparticle":
            main_content = soup.find('article') or soup.find('div', class_='content')
            if main_content:
                for elem in main_content.find_all(['p', 'ul', 'ol', 'pre', 'code', 'h2', 'h3', 'h4']):
                    content += elem.get_text().strip() + "\n\n"
        
        elif cdp == "lytics":
            main_content = soup.find('main') or soup.find('div', class_='content')
            if main_content:
                for elem in main_content.find_all(['p', 'ul', 'ol', 'pre', 'code', 'h2', 'h3', 'h4']):
                    content += elem.get_text().strip() + "\n\n"
        
        elif cdp == "zeotap":
            main_content = soup.find('article') or soup.find('div', class_='content')
            if main_content:
                for elem in main_content.find_all(['p', 'ul', 'ol', 'pre', 'code', 'h2', 'h3', 'h4']):
                    content += elem.get_text().strip() + "\n\n"
        
        # Fallback for any CDP if specific selectors don't work
        if not content:
            # Try to find any content in the page
            body = soup.find('body')
            if body:
                # Remove navigation, header, footer, etc.
                for elem in body.find_all(['nav', 'header', 'footer', 'script', 'style']):
                    elem.decompose()
                
                # Get remaining text
                content = body.get_text().strip()
                
                # Clean up whitespace
                content = re.sub(r'\s+', ' ', content).strip()
        
        return content
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str, current_url: str) -> List[str]:
        """Extract links to other documentation pages"""
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Skip empty links, anchors, and external links
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
                
            # Convert relative URLs to absolute
            if not href.startswith('http'):
                if href.startswith('/'):
                    # Absolute path relative to domain
                    domain = '/'.join(base_url.split('/')[:3])  # Get domain from base_url
                    href = domain + href
                else:
                    # Relative path
                    href = os.path.dirname(current_url) + '/' + href
            
            # Only include links from the same domain and documentation section
            if base_url in href:
                links.append(href)
                
        return links
    
    def _save_docs(self, cdp: str, docs: List[Dict]):
        """Saves processed documentation to local storage"""
        filepath = os.path.join(self.base_docs_dir, f"{cdp}_docs.json")
        with open(filepath, 'w') as f:
            json.dump(docs, f, indent=2)
            
    def process_existing_docs(self):
        """Process existing documentation files"""
        all_docs = []
        
        for cdp in self.cdp_sources:
            filepath = os.path.join(self.base_docs_dir, f"{cdp}_docs.json")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    docs = json.load(f)
                    all_docs.extend(docs)
                    
        return all_docs 