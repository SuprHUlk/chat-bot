#!/usr/bin/env python
"""
Script to fetch and process documentation from all supported CDPs.
This script should be run to populate the data/docs directory with documentation.
"""

import os
import sys
import argparse

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_processor import DocumentProcessor

def main():
    parser = argparse.ArgumentParser(description='Fetch CDP documentation')
    parser.add_argument('--cdp', choices=['segment', 'mparticle', 'lytics', 'zeotap', 'all'],
                        default='all', help='Which CDP to fetch documentation for')
    args = parser.parse_args()
    
    processor = DocumentProcessor()
    
    if args.cdp == 'all':
        print("Fetching documentation for all CDPs...")
        processor.fetch_all_documentation()
    else:
        print(f"Fetching documentation for {args.cdp}...")
        processor.fetch_documentation(args.cdp)
        
    print("Documentation fetching complete!")

if __name__ == "__main__":
    main() 