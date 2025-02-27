#!/usr/bin/env python
"""
Script to run the CDP chatbot API server.
"""

import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    # Run the FastAPI server
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main() 