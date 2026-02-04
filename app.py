"""
Flask Web Application for PDF Downloader and Parser

This web application allows users to:
1. Enter a URL containing PDF links
2. Download all PDFs from that URL
3. Parse the PDFs to extract question IDs and answer keys
4. View and download results as JSON
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from pdf_downloader import PDFDownloader
from pdf_parser import PDFParser

app = Flask(__name__)

# Configuration
DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "output"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_url():
    """
    Process the URL: download PDFs and parse them.
    
    Expected POST data:
        {
            'url': 'https://example.com/pdfs'
        }
    
    Returns:
        JSON response with parsed results
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'No URL provided'
            }), 400
        
        # Initialize downloader and parser
        downloader = PDFDownloader(download_dir=DOWNLOAD_DIR)
        parser = PDFParser()
        
        # Download PDFs
        download_results = downloader.download_all_pdfs(url)
        
        # Get successfully downloaded files
        downloaded_files = [
            result['filepath'] 
            for result in download_results 
            if result['success']
        ]
        
        if not downloaded_files:
            return jsonify({
                'success': False,
                'error': 'No PDFs were successfully downloaded',
                'download_results': download_results
            }), 400
        
        # Parse PDFs
        parsed_results = parser.parse_multiple_pdfs(downloaded_files)
        
        # Save results to JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'parsed_results_{timestamp}.json'
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        parser.save_to_json(parsed_results, output_path)
        
        return jsonify({
            'success': True,
            'message': f'Successfully processed {len(downloaded_files)} PDF(s)',
            'results': parsed_results,
            'download_results': download_results,
            'output_file': output_filename
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """
    Download a generated JSON file.
    
    Args:
        filename: Name of the file to download
    """
    try:
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'PDF Downloader and Parser is running'
    })


if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
