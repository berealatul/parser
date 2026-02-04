"""
Test Script for PDF Parser

This script creates a test PDF with sample answer keys and tests the parsing functionality.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf_parser import PDFParser


def create_test_pdf(filename, subject_code, subject_name, answers):
    """
    Create a test PDF with answer keys.
    
    Args:
        filename (str): Path where the PDF will be saved
        subject_code (str): Subject code
        subject_name (str): Subject name
        answers (list): List of tuples (question_id, answer)
    """
    # Create PDF
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Add title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, f"{subject_code} - {subject_name}")
    c.drawString(100, 720, "Answer Key")
    
    # Add answers
    c.setFont("Helvetica", 12)
    y_position = 680
    
    for q_id, answer in answers:
        c.drawString(100, y_position, f"Q{q_id}: {answer}")
        y_position -= 20
        
        # Start new page if needed
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750
    
    c.save()
    print(f"Created test PDF: {filename}")


def run_tests():
    """Run tests on the PDF parser."""
    
    # Create test directory
    test_dir = "test_pdfs"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Test 1: Simple answer key
    print("\nTest 1: Creating simple answer key PDF...")
    test1_file = os.path.join(test_dir, "CS101_IntroToCS.pdf")
    answers1 = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "A")]
    create_test_pdf(test1_file, "CS101", "Intro to Computer Science", answers1)
    
    # Test 2: Math answer key
    print("\nTest 2: Creating math answer key PDF...")
    test2_file = os.path.join(test_dir, "MATH201_Calculus.pdf")
    answers2 = [(1, "B"), (2, "C"), (3, "A"), (4, "D"), (5, "B"), (6, "A")]
    create_test_pdf(test2_file, "MATH201", "Calculus", answers2)
    
    # Parse the test PDFs
    print("\n" + "="*60)
    print("Parsing Test PDFs")
    print("="*60)
    
    parser = PDFParser()
    
    # Test parsing
    test_files = [test1_file, test2_file]
    results = parser.parse_multiple_pdfs(test_files)
    
    # Display results
    for result in results:
        print(f"\nFile: {result['source_file']}")
        print(f"Subject Code: {result['subject_code']}")
        print(f"Subject Name: {result['subject_name']}")
        print(f"Total Questions: {result['total_questions']}")
        print(f"Success: {result['success']}")
        
        if result['success']:
            print("Answer Key:")
            for item in result['answer_key']:
                print(f"  Q{item['question_id']}: {item['answer']}")
        else:
            print(f"Error: {result['error']}")
    
    # Save results to JSON
    output_file = "test_results.json"
    parser.save_to_json(results, output_file)
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    # Check if reportlab is installed
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        run_tests()
    except ImportError:
        print("Error: reportlab library is required for creating test PDFs.")
        print("Install it with: pip install reportlab")
        print("\nAlternatively, you can test with existing PDF files.")
