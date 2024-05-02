import fitz

def extract_region_from_pdf(pdf_path, page_number, rect, output_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)  # page numbering starts from 0
    page_rect = page.rect
    print("Page dimensions:", page_rect)
    clip_rect = fitz.Rect(rect)
    pix = page.get_pixmap(clip=clip_rect)
    pix.save(output_path)
    doc.close()

pdf_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsum.pdf"
output_image_path = r"C:\Users\sasha\projects\pdfUnderlinedExtractor\loremIpsumImgTest.png"

# found box: [107.57, 757.9, 139.97, 758.14]
# found box: [180.31, 724.06, 215.854, 724.3]
# found box: [410.33, 689.95, 523.42, 690.19]
# found box: [181.75, 622.97, 224.734, 623.21]
# found box: [281.88, 589.13, 333.984, 589.37]
# found box: [252.82, 538.22, 282.604, 538.46]
# found box: [349.58, 538.22, 387.044, 538.46]
# found box: [361.1, 521.18, 403.364, 521.42]

record = [281.88, 589.13, 333.984, 589.37]

y0 = 841.9199829101562 - record[3] - 10
y1 = 841.9199829101562 - record[3]
x0 = record[0]
x1 = record[2]

coordinates = [x0, y0, x1, y1]
print(coordinates)
#coordinates = [107.57, 757.9, 139.97, 758.14]  # [x0, y0, x1, y1]
page_number = 0  # change as per your PDF

# Call the function with the specified parameters
extract_region_from_pdf(pdf_path, page_number, coordinates, output_image_path)

print("Image saved at:", output_image_path)