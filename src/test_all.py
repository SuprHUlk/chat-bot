#!/usr/bin/env python
"""
Consolidated test script for the CDP chatbot.
This script provides a menu-driven interface to test all aspects of the chatbot.
"""

import os
import sys
import time
import argparse
import json

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import CDPChatbot

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60 + "\n")

def print_divider():
    """Print a divider line"""
    print("\n" + "-" * 60 + "\n")

def save_to_file(content, filename):
    """Save content to a file"""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Results saved to {filename}")

def test_basic_questions():
    """Test the four basic CDP questions"""
    print_header("Testing Basic CDP Questions")
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    # Test questions
    test_questions = [
        "How do I set up a new source in Segment?",
        "How can I create a user profile in mParticle?",
        "How do I build an audience segment in Lytics?",
        "How can I integrate my data with Zeotap?"
    ]
    
    results = []
    
    # Run tests
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        print("-" * 60)
        
        # Get response from chatbot
        start_time = time.time()
        response = chatbot.answer_question(question)
        end_time = time.time()
        
        # Print response and timing
        print(f"Response (took {end_time - start_time:.2f}s):")
        print(response)
        print_divider()
        
        # Store results
        results.append({
            "question": question,
            "response": response,
            "time_taken": end_time - start_time
        })
    
    # Ask if user wants to save results
    save = input("Do you want to save the results to a file? (y/n): ")
    if save.lower() == 'y':
        filename = input("Enter filename (default: basic_questions_results.json): ") or "basic_questions_results.json"
        save_to_file(json.dumps(results, indent=2), filename)
    
    print("\nBasic questions testing complete!")

def test_comparison_questions():
    """Test comparison questions between CDPs"""
    print_header("Testing CDP Comparison Questions")
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    # Test comparison questions
    test_questions = [
        "Which CDP is better for identity resolution?",
        "How does Segment's audience creation compare to Lytics?",
        "What are the differences between mParticle and Zeotap?",
        "Segment vs mParticle for data collection"
    ]
    
    results = []
    
    # Run tests
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        print("-" * 60)
        
        # Check if it's identified as a comparison question
        is_comparison = chatbot._is_comparison_question(question)
        print(f"Identified as comparison question: {is_comparison}")
        
        # Get response from chatbot
        start_time = time.time()
        response = chatbot.answer_question(question)
        end_time = time.time()
        
        # Print response and timing
        print(f"Response (took {end_time - start_time:.2f}s):")
        print(response)
        print_divider()
        
        # Store results
        results.append({
            "question": question,
            "is_comparison": is_comparison,
            "response": response,
            "time_taken": end_time - start_time
        })
    
    # Ask if user wants to save results
    save = input("Do you want to save the results to a file? (y/n): ")
    if save.lower() == 'y':
        filename = input("Enter filename (default: comparison_questions_results.json): ") or "comparison_questions_results.json"
        save_to_file(json.dumps(results, indent=2), filename)
    
    print("\nComparison questions testing complete!")

def test_debug_lytics():
    """Debug the Lytics question issue"""
    print_header("Debugging Lytics Question")
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    # The question
    question = "How do I build an audience segment in Lytics?"
    print(f"Question: {question}")
    print("-" * 60)
    
    # Check if it's identified as a comparison question
    is_comparison = chatbot._is_comparison_question(question)
    print(f"Is identified as comparison question: {is_comparison}")
    
    # Identify which CDP the question is about
    cdp = chatbot._identify_cdp(question)
    print(f"Identified CDP: {cdp}")
    
    # Get response from chatbot
    start_time = time.time()
    response = chatbot.answer_question(question)
    end_time = time.time()
    
    # Print response and timing
    print(f"\nResponse (took {end_time - start_time:.2f}s):")
    print(response)
    
    print("\nLytics question debugging complete!")

def test_custom_question():
    """Test a custom user-provided question"""
    print_header("Testing Custom Question")
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    # Get question from user
    question = input("Enter your question: ")
    print("-" * 60)
    
    # Check if it's identified as a comparison question
    is_comparison = chatbot._is_comparison_question(question)
    print(f"Is identified as comparison question: {is_comparison}")
    
    # Identify which CDP the question is about
    cdp = chatbot._identify_cdp(question)
    print(f"Identified CDP: {cdp}")
    
    # Get response from chatbot
    start_time = time.time()
    response = chatbot.answer_question(question)
    end_time = time.time()
    
    # Print response and timing
    print(f"\nResponse (took {end_time - start_time:.2f}s):")
    print(response)
    
    print("\nCustom question testing complete!")

def test_single_question():
    """Test a single predefined question"""
    print_header("Testing Single Question")
    
    # Initialize the chatbot
    chatbot = CDPChatbot()
    
    # Define test questions
    questions = [
        "How do I set up a new source in Segment?",
        "How can I create a user profile in mParticle?",
        "How do I build an audience segment in Lytics?",
        "How can I integrate my data with Zeotap?"
    ]
    
    # Display question options
    print("Available questions:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    # Get question selection from user
    while True:
        try:
            selection = int(input("\nSelect a question number (1-4): "))
            if 1 <= selection <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    question = questions[selection - 1]
    print(f"\nTesting question: {question}")
    print("-" * 60)
    
    # Get response from chatbot
    start_time = time.time()
    response = chatbot.answer_question(question)
    end_time = time.time()
    
    # Print response and timing
    print(f"Response (took {end_time - start_time:.2f}s):")
    print(response)
    
    print("\nSingle question testing complete!")

def main():
    """Main function to run the test script"""
    parser = argparse.ArgumentParser(description='Test the CDP chatbot')
    parser.add_argument('--mode', choices=['all', 'basic', 'comparison', 'lytics', 'custom', 'single'],
                        help='Test mode to run (default: interactive menu)')
    args = parser.parse_args()
    
    if args.mode:
        # Run in specified mode
        if args.mode == 'all':
            test_basic_questions()
            test_comparison_questions()
            test_debug_lytics()
        elif args.mode == 'basic':
            test_basic_questions()
        elif args.mode == 'comparison':
            test_comparison_questions()
        elif args.mode == 'lytics':
            test_debug_lytics()
        elif args.mode == 'custom':
            test_custom_question()
        elif args.mode == 'single':
            test_single_question()
    else:
        # Interactive menu
        while True:
            clear_screen()
            print_header("CDP Support Chatbot Test Suite")
            print("1. Test Basic CDP Questions")
            print("2. Test Comparison Questions")
            print("3. Debug Lytics Question")
            print("4. Test Custom Question")
            print("5. Test Single Predefined Question")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                clear_screen()
                test_basic_questions()
            elif choice == '2':
                clear_screen()
                test_comparison_questions()
            elif choice == '3':
                clear_screen()
                test_debug_lytics()
            elif choice == '4':
                clear_screen()
                test_custom_question()
            elif choice == '5':
                clear_screen()
                test_single_question()
            elif choice == '6':
                print("\nExiting test suite. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 