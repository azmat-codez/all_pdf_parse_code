import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # ----------PDF DECRYPT----------
        if reader.is_encrypted:
            cleaned_path = pdf_path.replace(' ', '').replace('_', '')
            match = re.search(r'\d{3}-\d{7,8}', cleaned_path)
            if match:
                mawb_number = match.group(0)
                mawb_number_cleaned = re.sub(r'[^\d-]', '', mawb_number)
            reader.decrypt(mawb_number_cleaned)
        # ----------PDF DECRYPT----------
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text



# pdf_path = r"password_pdf\603-51132152_001.pdf"
pdf_path = r"password_pdf\603-51132152_2_20240906.pdf"
text = extract_text_from_pdf(pdf_path)
print(text)



exit()
def is_pdf_encrypted(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return reader.is_encrypted

pdf_file = r'password_pdf\603-51132152_2_20240906.pdf'
# pdf_file = r'password_pdf\603-51132152_001.pdf'
# pdf_file = r'password_pdf\VHF20742108.pdf'
password = '603-51132152'

# if is_pdf_encrypted(pdf_file):
#     print(f"The PDF '{pdf_file}' is encrypted.")
# else:
#     print(f"The PDF '{pdf_file}' is not encrypted.")


# extracted_text = extract_text_from_pdf(pdf_file, password)
# print(extracted_text)


# password_pdf\603-51132152_2_20240906.pdf => 603-51132152
# password_pdf\603-51132152_001.pdf => 603-51132152
# MANIFEST PDF/160-77783565MNFT.pdf => 160-77783565
# MANIFEST PDF/615-06385912_MNFT.pdf => 615-06385912
# FULL PDF/020-0193 8370.pdf => 020-01938370
# FULL PDF/098-20091260.pdf => 098-20091260
# FULL PDF/157-3748 6805.pdf => 157-37486805
# FULL PDF/936-0064 2880 P.pdf => 936-00642880


def find_mawb_no_1(pdf_path):
    cleaned_path = pdf_path.replace(' ', '')
    numbers = re.findall(r'\d+', cleaned_path)
    for number in numbers:
        if len(number) == 11:
            return number
    return ""

# num = find_mawb_no_1(pdf_file)
# print(num)



def find_mawb_no_1(pdf_path):
    cleaned_path = pdf_path.replace(' ', '').replace('_', '')
    match = re.search(r'\d{3}-\d{7,8}', cleaned_path)
    
    if match:
        mawb_number = match.group(0)
        mawb_number_cleaned = re.sub(r'[^\d-]', '', mawb_number)
        return mawb_number_cleaned
    
    return ""


pdf_file =[
    r"password_pdf\603-51132152_2_20240906.pdf => 603-51132152",
    r"password_pdf\603-51132152_001.pdf => 603-51132152",
    r"MANIFEST PDF/160-77783565MNFT.pdf => 160-77783565",
    r"MANIFEST PDF/615-06385912_MNFT.pdf => 615-06385912",
    r"FULL PDF/020-0193 8370.pdf => 020-01938370",
    r"FULL PDF/098-20091260.pdf => 098-20091260",
    r"FULL PDF/157-3748 6805.pdf => 157-37486805",
    r"FULL PDF/936-0064 2880 P.pdf => 936-00642880",
]

# Example usage
# pdf_file = 'FULL PDF/936-0064 2880 P.pdf'

for pdf in pdf_file:
    num = find_mawb_no_1(pdf)
    print(len(num))




def extract_text_from_pdf_1(self):
    with open(self.pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # ----------PDF DECRYPT----------
        if pdf_reader.is_encrypted:
            cleaned_path = self.pdf_path.replace(' ', '').replace('_', '')
            match = re.search(r'\d{3}-\d{7,8}', cleaned_path)
            if match:
                mawb_number = match.group(0)
                mawb_number_cleaned = re.sub(r'[^\d-]', '', mawb_number)
            pdf_reader.decrypt(mawb_number_cleaned)
        # ----------PDF DECRYPT----------
        text = ""
        totalPages = len(pdf_reader.pages)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text.strip(),totalPages
