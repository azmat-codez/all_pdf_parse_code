import re

def mawb_len(pdf_path):
    cleaned_path = pdf_path.replace(' ', '').replace('-', '')
    numbers = re.findall(r'\d+', cleaned_path)
    for number in numbers:
        if len(number) == 11:
            return number
    return None

path = [
    "password_pdf/603-51132152_001.pdf",
    "password_pdf/603-51132152_2_20240906.pdf",
    "password_pdf/VHF20742108.pdf",
]

pathh = [r"password_pdf/603-51132152_001.pdf"]

tt = mawb_len(pathh)
print(tt)

# for t in path:
#     tx = mawb_len(t)
#     print(tx)



exit()
import pdfplumber

# def extract_text_from_pdf(pdf_path, x1, y1, x2, y2):
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             # Assuming extraction from the first page
#             first_page = pdf.pages[0]
#             # Crop to the specified rectangle and extract text
#             cropped_page = first_page.within_bbox((x1, y1, x2, y2))
#             extracted_text = cropped_page.extract_text()
#             return extracted_text if extracted_text else "No text found in the specified coordinates."
#     except Exception as e:
#         return f"Error: {str(e)}"


# def extract_text_from_pdf(pdf_path, x1, y1, x2, y2):
#     extracted_texts = {}
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page_num, page in enumerate(pdf.pages, start=1):
#                 # Crop to the specified rectangle and extract text
#                 cropped_page = page.within_bbox((x1, y1, x2, y2))
#                 extracted_text = cropped_page.extract_text()
#                 extracted_texts[page_num] = extracted_text if extracted_text else "No text found in the specified coordinates."
#     except Exception as e:
#         return {"Error": str(e)}
#     return extracted_texts


def extract_text_from_pdf(pdf_path, coordinates):
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                cropped_page = page.within_bbox(coordinates)
                extracted_text = cropped_page.extract_text()
                if extracted_text:
                    all_text.append(extracted_text)
    except Exception as e:
        return f"Error: {str(e)}"
    return "\n".join(all_text)


if __name__ == "__main__":
    pdf_file_path = "AIRFREIGHT MANIFEST.pdf"
    text = extract_text_from_pdf(pdf_file_path, (0.0, 200.0, 440.0, 460.0))
    print(text)
