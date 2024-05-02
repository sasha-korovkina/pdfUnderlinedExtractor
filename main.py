from pdfquery import PDFQuery
import xml.etree.ElementTree as ET
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.colors import pink, blue
from reportlab.pdfgen import canvas
import io

# Your file path goes here
file_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsum.pdf"
xml_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\outXML.xml"
output_pdf_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsumOut.pdf"

pdf = PDFQuery(file_path)
pdf.load()
pdf.tree.write(xml_path, pretty_print=True)

tree = ET.parse(xml_path)
root = tree.getroot()

pdf_reader = PdfReader(file_path)
pdf_writer = PdfWriter()

all_text = []
underline_text = []

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
        if text:
            all_text.append([text_x, text_y, x1, y1, text])

    for elem in page.findall('.//LTRect[@bbox]'):
        bbox = eval(elem.get('bbox'))
        x0, y0, x1, y1 = map(float, bbox)
        can.setStrokeColor(blue)
        can.setLineWidth(1)
        can.rect(x0, y0, x1 - x0, y1 - y0)
        text = elem.text.strip() if elem.text else ""
        print('found box: ' + str([x0, y0, x1, y1]))
        underline_text.append([x0, y0, x1, y1])

    for elem in page.findall('.//LTLine[@bbox]'):  # Adjust this XPath if necessary
        bbox = eval(elem.get('bbox'))  # Safely parse 'bbox' attribute to get coordinates
        x0, y0, x1, y1 = map(float, bbox)  # Convert all coordinates to floats

        can.setStrokeColor(pink)
        can.setLineWidth(1)  # Set line width, adjust as needed
        can.line(x0, y0, x1, y1)  # Draw a line from start to end point

    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]
    pdf_writer.add_page(new_page)

matched_records = []
collections = []

for row in underline_text:
    print(row)
    for record in all_text:
        if round(row[0]) == round(record[0]) and round(row[2]) == round(record[2]):
            matched_records.append(record)  # Store matched records

flat_list = [sublist2 for sublist1 in collections for sublist2 in sublist1]
print(str(flat_list))
# print(f'Collections are: {flat_list}')

# dataframe_text(all_text, flat_list, results_bene, results_pos, results_isin, results_date, results_owner)

with open(output_pdf_path, 'wb') as output_pdf:
    pdf_writer.write(output_pdf)