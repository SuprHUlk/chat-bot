#!/usr/bin/env python
"""
Command-line interface for testing the CDP chatbot.
"""

import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import CDPChatbot

def main():
    print("CDP Support Chatbot")
    print("------------------")
    print("Ask me how to perform tasks in Segment, mParticle, Lytics, or Zeotap.")
    print("Type 'exit' or 'quit' to end the session.")
    print()
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            print("Chatbot: Goodbye! Have a great day!")
            break
            
        # Get response from chatbot
        try:
            response = chatbot.answer_question(user_input)
            print("\nChatbot:", response)
            print()
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different question.\n")

if __name__ == "__main__":
    main() 