"""
PDF Parser Module

This module provides functionality to parse PDF files and extract
question IDs and answer keys from them.
"""

import re
import json
import pdfplumber
from typing import Dict, List, Optional
import PyPDF2


class PDFParser:
    """
    A class to parse PDF files and extract question IDs and answer keys.
    
    The parser expects PDFs to contain question IDs and corresponding answer keys.
    It can handle various formats and patterns commonly found in answer key PDFs.
    """
    
    def __init__(self):
        """Initialize the PDFParser."""
        pass
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from the PDF
            
        Raises:
            Exception: If PDF cannot be read
        """
        text = ""
        
        try:
            # Try with pdfplumber first (better for structured data)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # If pdfplumber didn't extract text, try PyPDF2
            if not text.strip():
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            
            return text
            
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
    
    def extract_subject_info(self, filename: str) -> Dict[str, str]:
        """
        Extract subject code and name from filename.
        
        Expected format: subjectcode_subjectname.pdf
        
        Args:
            filename (str): Name of the PDF file
            
        Returns:
            Dict[str, str]: Dictionary with 'subject_code' and 'subject_name'
        """
        # Remove .pdf extension
        name = filename.replace('.pdf', '')
        
        # Try to split by underscore
        if '_' in name:
            parts = name.split('_', 1)
            return {
                'subject_code': parts[0].strip(),
                'subject_name': parts[1].strip() if len(parts) > 1 else ''
            }
        else:
            return {
                'subject_code': name.strip(),
                'subject_name': ''
            }
    
    def parse_answer_key(self, text: str) -> List[Dict[str, str]]:
        """
        Parse answer key from extracted text.
        
        This method looks for patterns like:
        - Q1: A, Q2: B, Q3: C
        - 1. A, 2. B, 3. C
        - Question 1: A, Question 2: B
        - 1) A, 2) B, 3) C
        
        Args:
            text (str): Extracted text from PDF
            
        Returns:
            List[Dict[str, str]]: List of question-answer pairs
                Each dict contains: {'question_id': str, 'answer': str}
        """
        answer_key = []
        
        # Pattern 1: Q1: A, Q2: B format
        pattern1 = r'Q(\d+)[:\s]+([A-D])'
        matches1 = re.finditer(pattern1, text, re.IGNORECASE)
        for match in matches1:
            answer_key.append({
                'question_id': match.group(1),
                'answer': match.group(2).upper()
            })
        
        # Pattern 2: 1. A, 2. B format (with period)
        if not answer_key:
            pattern2 = r'(\d+)\.\s*([A-D])\b'
            matches2 = re.finditer(pattern2, text)
            for match in matches2:
                answer_key.append({
                    'question_id': match.group(1),
                    'answer': match.group(2).upper()
                })
        
        # Pattern 3: 1) A, 2) B format (with parenthesis)
        if not answer_key:
            pattern3 = r'(\d+)\)\s*([A-D])\b'
            matches3 = re.finditer(pattern3, text)
            for match in matches3:
                answer_key.append({
                    'question_id': match.group(1),
                    'answer': match.group(2).upper()
                })
        
        # Pattern 4: Question 1: A format
        if not answer_key:
            pattern4 = r'Question\s+(\d+)[:\s]+([A-D])'
            matches4 = re.finditer(pattern4, text, re.IGNORECASE)
            for match in matches4:
                answer_key.append({
                    'question_id': match.group(1),
                    'answer': match.group(2).upper()
                })
        
        # Pattern 5: Simple number-letter pairs on separate lines
        if not answer_key:
            lines = text.split('\n')
            for line in lines:
                # Look for patterns like "1 A" or "1  A"
                pattern5 = r'^\s*(\d+)\s+([A-D])\s*$'
                match = re.search(pattern5, line)
                if match:
                    answer_key.append({
                        'question_id': match.group(1),
                        'answer': match.group(2).upper()
                    })
        
        return answer_key
    
    def parse_pdf(self, pdf_path: str, filename: str = None) -> Dict:
        """
        Parse a PDF file and extract all relevant information.
        
        Args:
            pdf_path (str): Path to the PDF file
            filename (str): Optional filename (if different from path basename)
            
        Returns:
            Dict: Dictionary containing parsed information:
                {
                    'subject_code': str,
                    'subject_name': str,
                    'answer_key': List[Dict],
                    'total_questions': int,
                    'source_file': str
                }
        """
        import os
        
        if filename is None:
            filename = os.path.basename(pdf_path)
        
        # Extract subject information from filename
        subject_info = self.extract_subject_info(filename)
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        # Parse answer key
        answer_key = self.parse_answer_key(text)
        
        return {
            'subject_code': subject_info['subject_code'],
            'subject_name': subject_info['subject_name'],
            'answer_key': answer_key,
            'total_questions': len(answer_key),
            'source_file': filename
        }
    
    def parse_multiple_pdfs(self, pdf_paths: List[str]) -> List[Dict]:
        """
        Parse multiple PDF files.
        
        Args:
            pdf_paths (List[str]): List of paths to PDF files
            
        Returns:
            List[Dict]: List of parsed results for each PDF
        """
        results = []
        
        for pdf_path in pdf_paths:
            try:
                result = self.parse_pdf(pdf_path)
                result['success'] = True
                result['error'] = None
            except Exception as e:
                result = {
                    'success': False,
                    'error': str(e),
                    'source_file': pdf_path
                }
            
            results.append(result)
        
        return results
    
    def save_to_json(self, data: 'Dict | List', output_path: str) -> None:
        """
        Save parsed data to a JSON file.
        
        Args:
            data: Data to save (dict or list)
            output_path (str): Path to output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
