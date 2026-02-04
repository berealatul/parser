"""
Example Script: Using PDF Downloader and Parser Programmatically

This script demonstrates how to use the pdf_downloader and pdf_parser
modules independently, without the web interface.
"""

from pdf_downloader import PDFDownloader
from pdf_parser import PDFParser
import json
import sys


def main():
    """
    Main function demonstrating programmatic usage of the modules.
    """
    # Check if URL is provided
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <URL>")
        print("Example: python example_usage.py https://example.com/pdfs")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"Processing URL: {url}\n")
    
    # Step 1: Initialize the downloader
    print("Step 1: Initializing PDF Downloader...")
    downloader = PDFDownloader(download_dir="downloads", timeout=30)
    
    # Step 2: Download all PDFs
    print(f"Step 2: Downloading PDFs from {url}...")
    download_results = downloader.download_all_pdfs(url)
    
    # Display download results
    print(f"\nDownload Results:")
    print(f"{'='*60}")
    for result in download_results:
        if result['success']:
            print(f"✓ Successfully downloaded: {result['filepath']}")
        else:
            print(f"✗ Failed: {result['error']}")
    
    # Get list of successfully downloaded files
    downloaded_files = [
        result['filepath'] 
        for result in download_results 
        if result['success']
    ]
    
    if not downloaded_files:
        print("\nNo PDFs were successfully downloaded. Exiting.")
        sys.exit(1)
    
    # Step 3: Initialize the parser
    print(f"\nStep 3: Initializing PDF Parser...")
    parser = PDFParser()
    
    # Step 4: Parse all downloaded PDFs
    print(f"Step 4: Parsing {len(downloaded_files)} PDF(s)...")
    parsed_results = parser.parse_multiple_pdfs(downloaded_files)
    
    # Display parsing results
    print(f"\nParsing Results:")
    print(f"{'='*60}")
    
    total_questions = 0
    for result in parsed_results:
        if result.get('success', False):
            print(f"\n📄 {result['source_file']}")
            print(f"   Subject Code: {result['subject_code']}")
            print(f"   Subject Name: {result['subject_name']}")
            print(f"   Total Questions: {result['total_questions']}")
            total_questions += result['total_questions']
            
            # Show first 5 answers as preview
            print(f"   Answer Key Preview:")
            for i, answer in enumerate(result['answer_key'][:5]):
                print(f"      Q{answer['question_id']}: {answer['answer']}")
            
            if len(result['answer_key']) > 5:
                print(f"      ... and {len(result['answer_key']) - 5} more")
        else:
            print(f"\n✗ Error parsing {result['source_file']}: {result.get('error', 'Unknown error')}")
    
    # Step 5: Save results to JSON
    output_file = "parsed_results.json"
    print(f"\nStep 5: Saving results to {output_file}...")
    parser.save_to_json(parsed_results, output_file)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  - PDFs Downloaded: {len(downloaded_files)}")
    print(f"  - PDFs Parsed Successfully: {sum(1 for r in parsed_results if r.get('success', False))}")
    print(f"  - Total Questions Extracted: {total_questions}")
    print(f"  - Output saved to: {output_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
