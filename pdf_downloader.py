"""
PDF Downloader Module

This module provides functionality to download PDF files from a given URL.
It scrapes the webpage for PDF links and downloads them to a specified directory.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Tuple


class PDFDownloader:
    """
    A class to handle downloading PDF files from a given URL.
    
    Attributes:
        download_dir (str): Directory where PDFs will be saved
        timeout (int): Timeout for HTTP requests in seconds
    """
    
    def __init__(self, download_dir: str = "downloads", timeout: int = 30):
        """
        Initialize the PDFDownloader.
        
        Args:
            download_dir (str): Directory to save downloaded PDFs
            timeout (int): Timeout for HTTP requests
        """
        self.download_dir = download_dir
        self.timeout = timeout
        self._ensure_download_directory()
    
    def _ensure_download_directory(self) -> None:
        """Create download directory if it doesn't exist."""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def find_pdf_links(self, url: str) -> List[str]:
        """
        Find all PDF links on a given webpage.
        
        Args:
            url (str): URL of the webpage to scrape
            
        Returns:
            List[str]: List of absolute URLs to PDF files
            
        Raises:
            requests.RequestException: If the webpage cannot be accessed
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_links = []
            
            # Find all anchor tags
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Check if the link points to a PDF
                if href.lower().endswith('.pdf') or '.pdf' in href.lower():
                    absolute_url = urljoin(url, href)
                    pdf_links.append(absolute_url)
            
            return pdf_links
            
        except requests.RequestException as e:
            raise Exception(f"Error accessing URL {url}: {str(e)}")
    
    def download_pdf(self, pdf_url: str, filename: str = None) -> Tuple[bool, str]:
        """
        Download a single PDF file.
        
        Args:
            pdf_url (str): URL of the PDF to download
            filename (str): Optional custom filename for the PDF
            
        Returns:
            Tuple[bool, str]: (Success status, filepath or error message)
        """
        try:
            # Determine filename
            if not filename:
                # Extract filename from URL
                parsed_url = urlparse(pdf_url)
                filename = os.path.basename(parsed_url.path)
                
                # If no filename in URL, generate one
                if not filename or not filename.endswith('.pdf'):
                    filename = f"document_{hash(pdf_url)}.pdf"
            
            # Ensure .pdf extension
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            filepath = os.path.join(self.download_dir, filename)
            
            # Download the PDF
            response = requests.get(pdf_url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True, filepath
            
        except Exception as e:
            return False, f"Error downloading {pdf_url}: {str(e)}"
    
    def download_all_pdfs(self, url: str) -> List[dict]:
        """
        Find and download all PDFs from a given URL.
        
        Args:
            url (str): URL of the webpage containing PDF links
            
        Returns:
            List[dict]: List of dictionaries with download results
                Each dict contains: {
                    'url': str,
                    'success': bool,
                    'filepath': str or None,
                    'error': str or None
                }
        """
        results = []
        
        try:
            # Find all PDF links
            pdf_links = self.find_pdf_links(url)
            
            if not pdf_links:
                return [{
                    'url': url,
                    'success': False,
                    'filepath': None,
                    'error': 'No PDF links found on the page'
                }]
            
            # Download each PDF
            for pdf_url in pdf_links:
                success, result = self.download_pdf(pdf_url)
                
                results.append({
                    'url': pdf_url,
                    'success': success,
                    'filepath': result if success else None,
                    'error': None if success else result
                })
        
        except Exception as e:
            results.append({
                'url': url,
                'success': False,
                'filepath': None,
                'error': str(e)
            })
        
        return results
