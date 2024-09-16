import fitz
import PyPDF2


# ! Class of UPS PDF PARSE
class UPSPdfParser:
    def __init__(self, pdf_path):
        try:
            self.pdf_path = pdf_path
            self.pdf_document = fitz.open(pdf_path)
            self.coordinates = [
                (148.0, 10.0, 594.0, 188.0)
                ]
            self.text = self.extract_text_from_coordinates_pdf()
        except Exception as e:
            print(e)

    def extract_text_from_coordinates_pdf(self):
        page = self.pdf_document.load_page(0)
        rect = fitz.Rect(self.coordinates[0])
        text = page.get_text("text", clip=rect)
        return text

    def extract_text_from_pdf_1(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            totalPages = len(pdf_reader.pages)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip(),totalPages

    def extract_text_from_pdf(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pages_text = []
            totalPages = len(pdf_reader.pages)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(page_text.strip())
        return pages_text, totalPages

    @staticmethod
    def remove_num(string):
        return "".join(x for x in string if x.isalpha())

    @staticmethod
    def origin_and_mawb_no(string):
        midpoint = len(string) // 2
        chunk = string[midpoint:]
        origin = ''.join([char for char in chunk if char.isalpha()])
        mawb_no = ''.join([char for char in chunk if char.isdigit()])
        return origin, mawb_no

    def get_ups_data(self, pdf_path=None):
        pdf_text_pages, total_pages = self.extract_text_from_pdf()

        mawb_data = {}
        hawb_all_data = []

        for page_text in pdf_text_pages:
            text = [text for text in page_text.split('\n') if text.strip()]
            for i, line in enumerate(text):
                if "MAWB" in line:
                    next_line = text[i+1].strip()
                    parts = next_line.split()
                    origin, mawb_no = self.origin_and_mawb_no(parts[0])
                    mawb_data["mawb_number"] = mawb_no
                    mawb_data["origin"] = origin
                    break
                
            for i, line in enumerate(text):
                if "SHIPMENTS" in line:
                    next_line = text[i].strip()
                    parts = next_line.split()

                    mawb_data["destination"] = [self.remove_num(parts[-3])]
                    if 'SHIPMENTS' in mawb_data["destination"] or len(mawb_data["destination"][0]) > 6:
                        next_line = text[i+1].strip()
                        mawb_data["destination"] = [self.remove_num(next_line.split(' ')[-3])]
                    mawb_data["airports_name"] = []
                    mawb_data["pkgs"] = int(parts[0])
                    gross_weight = parts[5]
                    if ',' in gross_weight and '.' in gross_weight:
                        if gross_weight.index(',') < gross_weight.index('.'):
                            gross_weight = gross_weight.replace(',', '')
                        elif gross_weight.index(',') > gross_weight.index('.'):
                            gross_weight = gross_weight.replace('.', '')
                            gross_weight = gross_weight.replace(',', '.') 
                    elif ',' in gross_weight and '.' not in gross_weight:
                        gross_weight = gross_weight.replace(',','.')
                    mawb_data["gross_weight"] = gross_weight
                    mawb_data["description"] = f"{parts[3]} {parts[4]}"
                    mawb_data["pdf_path"] = pdf_path
                    break
                
        for page_text in pdf_text_pages:
            text = [line for line in page_text.split('\n') if line.strip()]
            for i, line in enumerate(text):
                if line != '':
                    next_line = text[0].strip()
                    parts = next_line.split()
                    parts2 = next_line.split('.')
                    hawb_data = {}
                    hawb_data["hawb_number"] = parts[0]
                    destination_origin = parts[1]
                    destination_origin = destination_origin.split('/')
                    # hawb_data["origin"] = destination_origin[0]
                    hawb_data["origin"] = mawb_data["origin"]
                    hawb_data["destination"] = [destination_origin[1]]
                    hawb_data["airports_name"] = []
                    hawb_data["pkgs"] = int(parts[2])
                    gross_weight = parts[3]
                    if ',' in gross_weight and '.' in gross_weight:
                        if gross_weight.index(',') < gross_weight.index('.'):
                            gross_weight = gross_weight.replace(',', '')
                        elif gross_weight.index(',') > gross_weight.index('.'):
                            gross_weight = gross_weight.replace('.', '')
                            gross_weight = gross_weight.replace(',', '.') 
                    elif ',' in gross_weight and '.' not in gross_weight:
                        gross_weight = gross_weight.replace(',','.')
                    hawb_data["gross_weight"] = gross_weight
                    # print(2222222222, parts2)
                    description =  next_line.split(parts[3])
                    hawb_data["description"] = description[1].strip()
                    hawb_all_data.append(hawb_data)
                    break
                    
        for page_text in pdf_text_pages:
            text = [line for line in page_text.split('\n') if line.strip()]
            for i, line in enumerate(text):
                if 'Pick up Date and Time:' in line:
                    for offset in [1, 2, 4]:
                        next_line = text[i + offset].strip()
                        parts = next_line.split()
                        if parts[0][0].isdigit() and 5 < len(parts[0]) < 11:
                            hawb_data = {}
                            hawb_data["hawb_number"] = parts[0]
                            destination_origin = parts[1]
                            destination_origin = destination_origin.split('/')
                            # hawb_data["origin"] = destination_origin[0]
                            hawb_data["origin"] = mawb_data["origin"]
                            hawb_data["destination"] = [destination_origin[1]]
                            hawb_data["airports_name"] = []
                            hawb_data["pkgs"] = int(parts[2])
                            gross_weight = parts[3]
                            if ',' in gross_weight and '.' in gross_weight:
                                if gross_weight.index(',') < gross_weight.index('.'):
                                    gross_weight = gross_weight.replace(',', '')
                                elif gross_weight.index(',') > gross_weight.index('.'):
                                    gross_weight = gross_weight.replace('.', '')
                                    gross_weight = gross_weight.replace(',', '.') 
                            elif ',' in gross_weight and '.' not in gross_weight:
                                gross_weight = gross_weight.replace(',','.')
                            hawb_data["gross_weight"] = gross_weight
                            print(3333333333, parts)
                            description = parts[4:]
                            hawb_data["description"] = ' '.join(description)
                            hawb_all_data.append(hawb_data)
                            break
        return mawb_data, hawb_all_data




if __name__ == "__main__":
    
    manifest_file_path = [
                        r'MANIFEST PDF/235LAX35541796Courier International.pdf',
                        # r'MANIFEST PDF\603LHR50967593Courier_International.pdf'
                    ]
    
    parser = UPSPdfParser(manifest_file_path[0])
    check_pdf_text,total_pages = parser.extract_text_from_pdf_1()
    
    if 'UPS SUPPLY CHAIN SOLUTIONS' in check_pdf_text or 'UPS Supply Chain Solutions' in check_pdf_text:
        parser = UPSPdfParser(manifest_file_path[0])
        mawb_data, hawb_all_data = parser.get_ups_data(manifest_file_path[0])    
        data = {"mawb_data": mawb_data, "hawb_data": hawb_all_data}
        print(data)

