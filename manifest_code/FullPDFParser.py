import re
import fitz
import pytesseract
from PIL import Image, ImageEnhance
import io
from airport import airport_codes


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# ! Class of FULL PDF PARSE
class FullPDFParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_document = fitz.open(pdf_path)
        self.airport_data_dict = airport_codes
    
    def filter_pkgs_and_weight(self, word):
        matches = re.findall(r'\d+\.\d+|\d+', word)
        numbers_string = ''.join(matches)
        return numbers_string
    
    def remove_numeric_prefix(self, string):
        if string.isalnum():
            for i, char in enumerate(string):
                if not char.isdigit():
                    return string[i:]
        return string
    
    def filter_description(self, word):
        return word.replace(' // INV NO', '')
    
    def find_hawb_no(self, text):
        pattern = r'HAWB NO\.[:\s]*([\w-]+)|HAWB[:\s]*([\w-]+)|VTR/[:\s]*([\w-]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            hawb_no = match.group(1) or match.group(2) or match.group(3)
            cleaned_hawb_no = re.sub(r'(HAWB NO\.[:\s]*|HAWB[:\s]*|VTR/[:\s]*|\n|/)', '', hawb_no)
            return cleaned_hawb_no
        return ""
    
    def find_hawb_no_2(self, texts):
        text_list = [text for text in texts.split('\n') if text.strip()]
        for line in text_list:
            line = line.replace('/', '').replace('-', '').replace(' ', '').replace('BNo:', '')
            if line.isalpha():
                continue
            elif line.isalnum() and len(line) >= 6 and len(line) < 20:
                if line.isalnum:
                    translation_table = str.maketrans('', '', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                    int_line = line.translate(translation_table)
                    if len(int_line) == 11:
                        return int_line
                    else:
                        return line
                return line
        return ""
    
    def find_origin(self, text):
        pattern = re.compile(r'\b\d+\s([A-Za-z]{3})\s\d+\b')
        match = pattern.search(text)
        if match:
            return match.group(1)
        return None
    
    def find_origin_2(self, texts):
        text = texts.split()
        for airport in text:
            if airport in self.airport_code_tuple:
                return airport
            elif any(code in airport for code in self.airport_code_tuple):
                for code in self.airport_code_tuple:
                    if code in airport:
                        return code
        return None
    
    def find_airports(self, text):
        pattern = r'\b(' + '|'.join(self.airport_code_tuple) + r')\b'
        found_airports = []
        for match in re.finditer(pattern, text):
            airport = match.group(0)
            position = match.start()
            found_airports.append((airport, position))
        found_airports.sort(key=lambda x: x[1])
        unique_airports = []
        for airport, position in found_airports:
            if airport not in unique_airports:
                unique_airports.append(airport)
                if len(unique_airports) >= 3:
                    break
        return unique_airports
    
    def find_airports_name(self, text):
        text = text.upper()
        found_airports = []
        for airport in self.airport_name_tuple:
            position = text.find(airport)
            if position != -1:
                found_airports.append((airport, position))
        found_airports.sort(key=lambda x: x[1])
        unique_airports = []
        for airport, position in found_airports:
            if airport not in unique_airports:
                unique_airports.append(airport)
                if len(unique_airports) == 2:
                    break
        return unique_airports
    
    def find_pkgs_and_weight(self, texts):
        if '.' in texts:
            texts = texts.replace(',', '')
        else:
            texts = texts.replace(',','.')
        pkgs_weight_list = [text.strip() for text in texts.split('\n') if text.strip()]
        for i, line in enumerate(pkgs_weight_list):
            if 'RCP' in line or 'Pieces Weight' in line:
                if i + 1 < len(pkgs_weight_list):
                    next_line = pkgs_weight_list[i + 1].strip()
                    parts = next_line.split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        pkgs = parts[0]
                        gross_weight = self.filter_pkgs_and_weight(parts[1])
                        return pkgs, gross_weight
        return None, None
    
    def find_pkgs_and_weight_2(self, texts):
        if '.' in texts:
            texts = texts.replace(',', '')
        else:
            texts = texts.replace(',','.')
        pkgs = None
        gross_weight = None
        for line in texts.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                number = float(line)
                if '.' not in line and number.is_integer():
                    pkgs = int(number)
                    pkgs = str(pkgs)
                else:
                    gross_weight = number
                    gross_weight = str(round(gross_weight, 3))
            except ValueError:
                continue
        return pkgs, gross_weight
    
    def find_description_1(self, texts):
        texts_lst = texts.replace('AGREED', '').replace('agreed', '').replace('Total', '').replace('ARRANGED', '').replace('A G R E E D', '').replace('Agreed', '').replace('Volume)','').replace('AS AGREED', '')
        lst = [text.strip() for text in texts_lst.split('\n') if text.strip()]
        result = None
        for i in range(len(lst)):
            if "Dimensions" in lst[i] or 'Dimentsions' in lst[i] or 'DIMENSIONS' in lst[i] or 'Dimensions or Volume' in lst[i] or '(incl. Dimensions' in lst[i] or 'Dimentions' in lst[i]:
                if i + 1 < len(lst):
                    next_item = lst[i + 1]
                    if len(next_item) >= 4 and not any(char.isdigit() for char in next_item):
                        result = next_item
                        break
                for j in range(i + 2, len(lst)):
                    if len(lst[j]) >= 4 and not any (char.isdigit() for char in lst[j]):
                        result = lst[j]
                        break
                break
            else:
                result = lst[-1]
        return result

    def extract_text_from_coordinates(self, pdf_path, page_numbers=None):
        coordinates = [
            (1279.0, 4.0, 2549.0, 409.0),
            (0.0, 1000.0, 1292.0, 1601.0),
            (0.0, 1432.0, 922.0, 2000.0),
            (1537.0, 1498.0, 2602.0, 1931.0),
            (0.0, 0.0, 1286.0, 562.0),
            (1232.0, 5.0, 2477.0, 584.0)
        ]

        if page_numbers is None:
            page_numbers = range(len(self.pdf_document))

        def crop_and_extract_text(img, coord_index):
            x0, y0, x1, y1 = coordinates[coord_index]
            cropped_img = img.crop((x0, y0, x1, y1))
            return pytesseract.image_to_string(cropped_img)

        mawb_data = {}
        hawb_data = {}
        hawb_all_data = []

        for page_num in page_numbers:
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            check = crop_and_extract_text(img, 5)
            if 'Air Waybill' in check or 'HOUSE AIR WAYBILL' in check:
                mawb_hawb_no = crop_and_extract_text(img, 0)
                mawb_hawb_no = self.find_hawb_no(mawb_hawb_no) or self.find_hawb_no_2(mawb_hawb_no)

                if mawb_hawb_no.isdigit() and len(mawb_hawb_no) == 11:
                    mawb_data['mawb_number'] = mawb_hawb_no
                    
                    origin_text = crop_and_extract_text(img, 4)
                    mawb_data['origin'] = self.find_origin_2(origin_text) or self.find_origin(origin_text)
                    
                    destination_text = crop_and_extract_text(img, 1)
                    mawb_data['destination'] = self.find_airports(destination_text)
                    
                    airports_name_text = crop_and_extract_text(img, 1)
                    mawb_data['airports_name'] = self.find_airports_name(airports_name_text)
                    
                    pkgs_weight_text = crop_and_extract_text(img, 2)
                    pkgs, gross_weight = self.find_pkgs_and_weight(pkgs_weight_text)
                    if pkgs is None or gross_weight is None:
                        pkgs, gross_weight = self.find_pkgs_and_weight_2(pkgs_weight_text)
                    mawb_data['pkgs'] = pkgs
                    mawb_data['gross_weight'] = gross_weight
                    
                    description_text = crop_and_extract_text(img, 3)
                    mawb_data['description'] = self.find_description_1(description_text)
                    
                    mawb_data['pdf_path'] = pdf_path
                else:
                    hawb_data['hawb_number'] = mawb_hawb_no
                    
                    origin_text = crop_and_extract_text(img, 4)
                    hawb_data['origin'] = self.find_origin_2(origin_text) or self.find_origin(origin_text)
                    
                    destination_text = crop_and_extract_text(img, 1)
                    hawb_data['destination'] = self.find_airports(destination_text)
                    
                    airports_name_text = crop_and_extract_text(img, 1)
                    hawb_data['airports_name'] = self.find_airports_name(airports_name_text)
                    
                    pkgs_weight_text = crop_and_extract_text(img, 2)
                    pkgs, gross_weight = self.find_pkgs_and_weight(pkgs_weight_text)
                    if pkgs is None or gross_weight is None:
                        pkgs, gross_weight = self.find_pkgs_and_weight_2(pkgs_weight_text)
                    hawb_data['pkgs'] = pkgs
                    hawb_data['gross_weight'] = gross_weight
                    
                    description_text = crop_and_extract_text(img, 3)
                    hawb_data['description'] = self.find_description_1(description_text)
                    
        hawb_all_data.append(hawb_data)
        return mawb_data, hawb_all_data


if __name__ == "__main__":
    
    pdf_path = r""
    image_pdf_formate = FullPDFParser(pdf_path)
    mawb_data, hawb_all_data = image_pdf_formate.extract_text_from_coordinates(pdf_path)
    data = f"mawb_data : {mawb_data}, hawb_data : {hawb_all_data}"
    print(data)