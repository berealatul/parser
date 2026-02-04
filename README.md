# PDF Downloader & Parser

A modular web application for downloading PDFs from a given URL and parsing them to extract question IDs and answer keys. The application is designed specifically for answer key PDFs where files are named as `subjectcode_subjectname.pdf`.

## Features

- 🌐 **Web Interface**: User-friendly web interface to input URLs and view results
- 📥 **PDF Downloader**: Automatically discovers and downloads all PDF files from a given URL
- 📄 **PDF Parser**: Extracts question IDs and answer keys from PDF files
- 📊 **JSON Export**: Outputs parsed data as JSON for easy integration
- 🔧 **Modular Design**: Clean, maintainable code structure with separate modules

## Project Structure

```
parser/
├── app.py                  # Flask web application (main entry point)
├── pdf_downloader.py       # Module for downloading PDFs from URLs
├── pdf_parser.py           # Module for parsing PDFs and extracting data
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface template
├── downloads/             # Directory for downloaded PDFs (auto-created)
└── output/                # Directory for JSON output files (auto-created)
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/berealatul/parser.git
   cd parser
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Enter a URL** containing PDF links and click "Download & Parse PDFs"

4. **View results** in the web interface and download the JSON output

### Using Modules Programmatically

#### PDF Downloader Module

```python
from pdf_downloader import PDFDownloader

# Initialize downloader
downloader = PDFDownloader(download_dir="downloads")

# Download all PDFs from a URL
results = downloader.download_all_pdfs("https://example.com/pdfs")

# Download a specific PDF
success, filepath = downloader.download_pdf("https://example.com/file.pdf")
```

#### PDF Parser Module

```python
from pdf_parser import PDFParser

# Initialize parser
parser = PDFParser()

# Parse a single PDF
result = parser.parse_pdf("path/to/file.pdf")

# Parse multiple PDFs
results = parser.parse_multiple_pdfs(["file1.pdf", "file2.pdf"])

# Save results to JSON
parser.save_to_json(results, "output.json")
```

## PDF Format Requirements

The parser expects PDFs to follow these conventions:

1. **Filename Format**: `subjectcode_subjectname.pdf`
   - Example: `CS101_IntroToCS.pdf`, `MATH201_Calculus.pdf`

2. **Content Format**: Answer keys in one of these formats:
   - `Q1: A`, `Q2: B`, `Q3: C`
   - `1. A`, `2. B`, `3. C`
   - `1) A`, `2) B`, `3) C`
   - `Question 1: A`, `Question 2: B`
   - `1 A`, `2 B`, `3 C` (on separate lines)

## Output Format

The application generates JSON output with the following structure:

```json
[
  {
    "subject_code": "CS101",
    "subject_name": "IntroToCS",
    "answer_key": [
      {"question_id": "1", "answer": "A"},
      {"question_id": "2", "answer": "B"},
      {"question_id": "3", "answer": "C"}
    ],
    "total_questions": 3,
    "source_file": "CS101_IntroToCS.pdf",
    "success": true,
    "error": null
  }
]
```

## API Endpoints

- `GET /` - Main web interface
- `POST /process` - Process a URL and return parsed results
- `GET /download/<filename>` - Download a generated JSON file
- `GET /health` - Health check endpoint

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for downloading
- **BeautifulSoup4**: HTML parsing for finding PDF links
- **PyPDF2**: PDF text extraction
- **pdfplumber**: Advanced PDF parsing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Atul Bera