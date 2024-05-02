# PDF Underlined Text Extractor

<img width="1275" alt="image" src="https://github.com/sasha-korovkina/pdfUnderlinedExtractor/assets/127419480/7c148f05-7ca9-490b-9c06-3e0d15231b3a">

This repository provides tools to extract underlined text from any PDF document. The process automates the extraction and recognition of underlined text using a series of steps that convert PDFs into structured data for easy processing.

## How It Works

The process involves several key steps:

1. **XML Structuring**: The PDF is converted into a structured XML using `PyQuery`. This step allows for easier manipulation and querying of the document's content.
2. **Component Extraction**: Specific components that denote underlining in the XML are identified and extracted. This step focuses on retrieving only the underlined parts of the document.
3. **Image Slice**: The underlined sections of the PDF are sliced out and saved into memory as PNG images. This prepares the content for optical character recognition.
4. **Optical Character Recognition (OCR)**: `pytesseract` is used to perform OCR on the sliced images to read and convert the visual data into text.
5. **Results Compilation**: The extracted text is compiled into an array, providing a structured output of all underlined text elements from the original PDF.

## Installation and Setup

To use this repository, you will need Python and several dependencies, including `pytesseract` for OCR capabilities.

### Installing Python Dependencies

Ensure you have Python installed, then set up a virtual environment for the project (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install required Python libraries:
```bash
pip install -r requirements.txt
```

### Installing Pytesseract
For Ubuntu:
Run the following commands in your terminal to update your package list and install Tesseract OCR and its development libraries:
```
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

For Mac:
Use Homebrew to install Tesseract by running the following command:
```
brew install tesseract
```

For Windows:
1. Download the installer from Tesseract at UB Mannheim.
2. It is recommended to install Tesseract into the default directory (C:\Program Files\Tesseract-OCR) to ensure compatibility.
After installing Tesseract, you may need to specify the path to the tesseract executable in your Python script if it's not automatically recognized:
```
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

