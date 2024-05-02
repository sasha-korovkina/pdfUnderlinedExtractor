import fitz
import pytesseract
from PIL import Image
import io

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
    print(text)
    return text

pdf_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsum.pdf"
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sasha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

record = [281.88, 589.13, 333.984, 589.37]
page_number = 0
extract_region_from_pdf(pdf_path, page_number, record)
