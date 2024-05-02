from pdfquery import PDFQuery
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
import fitz
import pytesseract
from PIL import Image
import io

# File path definitions
xml_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\outXML.xml"
pdf_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsum.pdf"
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sasha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

underline_text = []
words = []

def get_coordinates(pdf_path):
    pdf = PDFQuery(pdf_path)
    pdf.load()
    pdf.tree.write(xml_path, pretty_print=True)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    pdf_reader = PdfReader(pdf_path)

    for page in root.findall('.//LTPage'):
        page_num = int(page.get('page_index'))
        pdf_page = pdf_reader.pages[page_num]
        page_height = float(pdf_page.mediabox[3])

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(pdf_page.mediabox[2], page_height))
        can.setPageSize((pdf_page.mediabox[2], page_height))

        for elem in page.findall('.//*[@bbox]'):
            bbox = eval(elem.get('bbox'))
            x0, y0, x1, y1 = map(float, bbox)
            # can.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)
            text = elem.text.strip() if elem.text else ""
            text_x = x0
            text_y = y0
            can.drawString(text_x, text_y, text)

        for elem in page.findall('.//LTRect[@bbox]'):
            bbox = eval(elem.get('bbox'))
            x0, y0, x1, y1 = map(float, bbox)
            underline_text.append([x0, y0, x1, y1])

    return underline_text

def extract_region_from_pdf(pdf_path, page_number, record):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)  # page numbering starts from 0
    page_rect = page.rect
    y1_coordinate = page_rect.y1

    y0 = y1_coordinate - record[3] - 10
    y1 = y1_coordinate - record[3]
    x0 = record[0]
    x1 = record[2]

    coordinates = [x0, y0, x1, y1]

    # Create a rectangle for the specific area to be extracted
    clip_rect = fitz.Rect(coordinates)

    pix = page.get_pixmap(clip=clip_rect)

    # Convert the pixmap to an in-memory image
    img_bytes = io.BytesIO(pix.tobytes("png"))  # Save image to a bytes buffer
    img = Image.open(img_bytes)

    # Use pytesseract to perform OCR on the image
    text = pytesseract.image_to_string(img)

    doc.close()
    return text

page_number = 0

underline_text = get_coordinates(pdf_path)

page_number = int(input('Please enter the page number you need (starting at 0): '))

for record in underline_text:
    extracted_text = extract_region_from_pdf(pdf_path, page_number, record)
    cleaned_text = extracted_text.replace('\n', '')
    words.append(cleaned_text)

print(words)
