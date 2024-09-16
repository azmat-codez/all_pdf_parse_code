import fitz
import re
from airport import airport_codes
import json




# ! Class of PDF PARSE
class NormalPDFParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_document = fitz.open(pdf_path)
        # airport_data = Airport.objects.filter(is_active=True).values("name", "code")
        # self.airport_data_dict = {airport["code"]: airport["name"] for airport in airport_data}
        self.airport_data_dict = airport_codes

        
        self.coordinates = [
            (295.0, 0.0, 593.0, 127.0),
            (23.0, 250.0, 253.0, 370.0),
            (24.0, 393.0, 126.0, 478.0),
            (336.0, 373.0, 599.0, 497.0),
            (1.0, 2.0, 253.0, 119.0)
        ]

        self.coordinates3 = [
            (73.0, 376.0, 205.0, 554.0),
            (74.0, 342.0, 203.0, 552.0),
            (34.0, 372.0, 137.0, 459.0),
            (27.0, 396.0, 160.0, 446.0),
            (31.0, 357.0, 136.0, 396.0),
            (39.0, 429.0, 149.0, 501.0),
            (17.0, 393.0, 107.0, 467.0),
            (26.0, 525.0, 172.0, 560.0), 
            (2.0, 507.0, 113.0, 589.0),
            (27.0, 391.0, 107.0, 437.0),
            (21.0, 394.0, 109.0, 428.0),
            # (0.0, 361.0, 89.0, 405.0)
            (0.0, 358.0, 177.0, 476.0)
        ]
        
    def extract_text_from_coordinates(self, page_number, coordinates):
        page = self.pdf_document.load_page(page_number)
        rect = fitz.Rect(coordinates)
        text = page.get_text("text", clip=rect)
        return text
    
    def extract_text_from_coordinates_2(self, page_number, coordinates):
        page = self.pdf_document.load_page(page_number)
        rect = fitz.Rect(coordinates)
        text = page.get_text("text", clip=rect)
        # Todo -------Changes-------
        text = text.replace('\n', '')
        return text

    def remove_numeric_prefix(self, string):
        if string.isalnum():
            for i, char in enumerate(string):
                if not char.isdigit():
                    return string[i:]
        return string

    def filter_pkgs_and_weight(self, word):
        word = word.replace(',', '.')
        matches = re.findall(r'\d+\.\d+|\d+', word)
        numbers_string = ''.join(matches)
        return numbers_string
    
    def find_hawb_no_1(self, text):
        if text is None:
            return None
        pattern = r'HAWB No[:：\s]*([\w-]+)|HAWB[:：\s]*([\w-]+)|HBL[:：\s]*([\w-]+)|VTR/[:：\s]*([\w-]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            hawb_no = match.group(1) or match.group(2) or match.group(3) or match.group(4)
            cleaned_hawb_no = re.sub(r'(HAWB No[:：\s]*|HAWB[:：\s]*|No[:：\s]*|\n|/)', '', hawb_no)
            return cleaned_hawb_no
        return None


    def find_hawb_no_2(self, texts):
        text_list = [text for text in texts.split('\n') if text.strip()]
        for line in text_list:
            line = line.replace('/', '').replace('-', '').replace(' ', '')
            if line.isalpha():
                continue
            elif line.isalnum() and len(line) > 6 and len(line) < 20:
                if line.isalnum:
                    return self.remove_numeric_prefix(line)
                return line
        return ""
    
    def find_hawb_no_3(self):
        cleaned_path = self.pdf_path.replace('hawb', '')
        cleaned_path = cleaned_path.split('/')
        pattern = re.compile(r'\b(?!\d{11}\b)[A-Za-z0-9]{5,15}\b')
        matches = pattern.findall(cleaned_path[-1])
        for match in matches:
            if not match.isalpha():
                return match
        return None


    def find_mawb_no_1(self):
        cleaned_path = self.pdf_path.replace(' ', '').replace('-', '')
        numbers = re.findall(r'\d+', cleaned_path)
        for number in numbers:
            if len(number) == 11:
                return number
        return ""

    def find_mawb_no_2(self, texts):
        text_list = [text for text in texts.split('\n') if text.strip()]
        for line in text_list:
            line = self.filter_pkgs_and_weight(line)
            if line.isdigit() and len(line) > 6:
                return line
        return ""

    def find_pkgs_and_weight(self, texts):
        pkgs = None
        gross_weight = None
        for line in texts.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                line = line.replace(',', '.')
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

    def find_pkgs_and_weight_2(self, texts):
        pkgs_weight_list = [text.strip() for text in texts.split('\n') if text.strip()]
        if 'RCP' in pkgs_weight_list or 'Pieces Weight' in pkgs_weight_list:
            for i in range(len(pkgs_weight_list)):
                try:
                    parts = pkgs_weight_list[i].split()
                    if len(parts) == 2:
                        pkgs = self.filter_pkgs_and_weight(parts[0])
                        gross_weight = self.filter_pkgs_and_weight(parts[1])
                        if pkgs is not None and gross_weight is not None:
                            return pkgs, gross_weight
                except Exception as e:
                    print(f'Error Occurred: {e}')
            for i in range(len(pkgs_weight_list) - 1, 0, -1):
                try:
                    parts = pkgs_weight_list[i].split()
                    parts2 = pkgs_weight_list[i - 1]
                    pkgs = self.filter_pkgs_and_weight(parts2)
                    gross_weight = self.filter_pkgs_and_weight(parts[0])
                    if pkgs is not None and gross_weight is not None:
                        return pkgs, gross_weight
                except Exception as e:
                    print(f'Error Occurred: {e}')
        return None, None

# ! --------- ORIGIN / DESTINATION / AIRPORT NAME start ---------

    def find_airports(self, text):
        text = text.replace('(SFO) SAN', 'SFO')
        found_airports = []
        for airport_code in self.airport_data_dict:
            matches = [(airport_code, m.start()) for m in re.finditer(r'\b' + re.escape(airport_code) + r'\b', text)]
            found_airports.extend(matches)
        found_airports.sort(key=lambda x: x[1])
        unique_airports = []
        for airport_code, position in found_airports:
            if airport_code not in unique_airports:
                unique_airports.append(airport_code)
                if len(unique_airports) == 2:
                    break
        return unique_airports
        
    def find_origin(self, text):
        text = text.replace('NMDBL', ' ')
        replace_values = ['GOT FREIGHT','BRITANNIA IND EST', 'CO.,LTD', 'INT’L', 'CO., LTD',
            'ADD:ROOM329', 'DDI:', '.COM', 'VTR', 'ASIA PTE LTD', 'TEL:', 'FAX:', 
            'VAL VIBRATA', 'VIA LEONARDO', 'C. SRL', 'VIA A.', '/ SPA', 'VIA CARLO',
            'VIA S.', 'IMAL SRL', 'VAT:', 'AIR WAYBILL', 'ITK', '(VIET NAM)', 'GO DAU DIST,TAY',
            'CTS INTERNATIONAL', 'LIMITED', 'CORPORATION LIM', 'WEG EQUIPAMENTOS', 'DO SUL',
            'DYJ LOGISTICS', 'KYU', 'EI  KYO', 'STI CS', ')  LTD', 'AGS GROUP', 'PIF GLOBAL', 'CHINA]LTD']

        def find_origin_1(text):
            pattern = re.compile(r'\b(\d+)\s([A-Za-z]{3})\s(\d+)\b')
            match = pattern.search(text)
            print(match)
            if match:
                str_between_integers = match.group(2)
                if len(str_between_integers) == 3:
                    return str_between_integers
            return None
        
        def find_origin_2(text):
            pattern = re.compile(r'\b[A-Z]{3}\b')
            match = pattern.search(text)
            print(match)
            if match:
                return match.group()
            return None
        
        
        for value in replace_values:
            text = text.replace(value, '')
        origin = find_origin_1(text)
        if origin is None:
            origin = find_origin_2(text)
        return origin
    
    def find_airports_name(self, text):
        text = text.replace('CHENNAI-600084', '').replace('DONG', 'SHANGHAI')
        text = text.upper()
        found_airports = []
        for airport_code, airport_name in self.airport_data_dict.items():
            if airport_name.upper() in text:
                position = text.find(airport_name.upper())
                found_airports.append((airport_name, position))
        found_airports.sort(key=lambda x: x[1])
        unique_airports = []
        for airport_name, position in found_airports:
            if airport_name not in unique_airports:
                unique_airports.append(airport_name)
                if len(unique_airports) == 2:
                    break
        return unique_airports

# ! --------- ORIGIN / DESTINATION / AIRPORT NAME end ---------

    def find_description(self, texts):
        replace_values = ['AGREED', 'agreed', 'Total', 'ARRANGED', 'A G R E E D', 
        'Agreed','s  ', 'AS  ', 'Logistics Inc)', 'on and has', 'being', 'solidation has', 
        'ransited', 'nistan, Libya,', 'ARRAND', 'SHIKHARLOGISTICS.COM', 'arge', '67,14', 'Volume)', 'value)',
        'PPD COLL']
        
        for value in replace_values:
            texts = texts.replace(value, '')
        lst = [text.strip() for text in texts.split('\n') if text.strip()]
        result = None
        for i in range(len(lst)):
            if "Dimensions" in lst[i] or 'Dimentsions' in lst[i] or 'DIMENSIONS' in lst[i] or 'Invoice Number' in lst[i]:
                if i + 1 < len(lst):
                    next_item = lst[i + 1]
                    if len(next_item) >= 4 and not any(char.isdigit() for char in next_item):
                        result = next_item
                        break
                for j in range(i + 2, len(lst)):
                    if len(lst[j]) >= 4 and not any(char.isdigit() for char in lst[j]):
                        result = lst[j]
                        break
                break
            
            elif 'X-RAY' in texts:
                result = 'X-RAY'
        return result
    
    @staticmethod
    def find_description_2(texts):
        
        replace_values = ['AGREED', 'agreed', 'Total', 'ARRANGED', 'A G R E E D', 
        'Agreed','s  ', 'AS  ', 'Logistics Inc)', 'on and has', 'being', 'solidation has', 
        'ransited', 'nistan, Libya,', 'ARRAND', 'SHIKHARLOGISTICS.COM', 'arge', '67,14', 'Volume)']
        
        for value in replace_values:
            texts = texts.replace(value, '')
        lst = [text.strip() for text in texts.split('\n') if text.strip()]
        
        keywords_to_exclude = ['INVOICE', 'HS CODE', 'MANIFEST', 'NO.', 'PALLETS', 'CONTAINING:', 'DUE:', 'AWB', 'CBM']
        result = None
        for text in lst:
            if not any(keyword in text for keyword in keywords_to_exclude):
                result = text
                if not any(char.isdigit() for char in result) and len(result) > 5:
                    break
        return result if result else "No description found"
    
    def get_mawb_hawb(self):
        page_number = 0
        data = {}
        try:
            mawb_hawb_no = self.extract_text_from_coordinates(page_number, self.coordinates[0])
            if not data.get('mawb_hawb'):
                data['mawb_hawb'] = self.find_hawb_no_1(mawb_hawb_no)
            if not data.get('mawb_hawb'):
                data['mawb_hawb'] = self.find_hawb_no_2(mawb_hawb_no)
            if not data.get('mawb_hawb'):
                alternative_mawb_hawb_no = self.extract_text_from_coordinates(page_number, (299.0, 143.0, 590.0, 258.0))
                data['mawb_hawb'] = self.find_hawb_no_1(alternative_mawb_hawb_no)
            if not data.get('mawb_hawb'):
                data['mawb_hawb'] = self.find_hawb_no_3()
            if not data.get('mawb_hawb'):
                data['mawb_hawb'] = self.find_mawb_no_1()
            if not data.get('mawb_hawb'):
                data['mawb_hawb'] = self.find_mawb_no_2(mawb_hawb_no)
        except Exception as e:
            print(f"Error occurred while extracting MAWB/HAWB: {e}")
        return data


    def get_pdf_data(self, pdf_path):
        page_number = 0
        data = {}
        
        try:
            # HAWB and MAWB
            mawb_hawb_no = self.extract_text_from_coordinates(page_number, self.coordinates[0])
            data['hawb_number'] = self.find_hawb_no_1(mawb_hawb_no)
            if not data['hawb_number']:
                data['hawb_number'] = self.find_hawb_no_2(mawb_hawb_no)
            if not data['hawb_number']:
                mawb_hawb_no = self.extract_text_from_coordinates(page_number, (299.0, 143.0, 590.0, 258.0))
                data['hawb_number'] = self.find_hawb_no_1(mawb_hawb_no)
            if not data['hawb_number']:
                data['hawb_number'] = self.find_hawb_no_3()
            
            data['mawb_number'] = self.find_mawb_no_1()
            if data['mawb_number'] == "":
                data['mawb_number'] = self.find_mawb_no_2(mawb_hawb_no)
            
            # Origin
            origin = self.extract_text_from_coordinates(page_number, self.coordinates[4])
            data['origin'] = self.find_origin(origin)
            
            print(data['origin'])
                    
            # Destination
            destination = self.extract_text_from_coordinates(page_number, self.coordinates[1])
            data['destination'] = self.find_airports(destination)
            if not data['destination']:
                destination = self.extract_text_from_coordinates(page_number, (0.0, 238.0, 278.0, 322.0))
                data['destination'] = self.find_airports(destination)
            
            # Airport Name
            airports_name = self.extract_text_from_coordinates(page_number, self.coordinates[1])
            data['airports_name'] = self.find_airports_name(airports_name)
            if not data['airports_name']:
                airports_name = self.extract_text_from_coordinates(page_number, (0.0, 238.0, 278.0, 322.0))
                data['airports_name'] = self.find_airports_name(airports_name)
            if not data['airports_name']:
                airports_name = self.extract_text_from_coordinates_2(page_number, (0.0, 238.0, 278.0, 322.0))
                data['airports_name'] = self.find_airports_name(airports_name)
            
            # ? ------------------------- PKGS and Gross Weight Start -------------------------
            pkgs = gross_weight = ''
            pkgs_weight = self.extract_text_from_coordinates(page_number, self.coordinates3[11])
            matches = re.findall(r'(\d[\d,.]*)\s+([\d.,]+(?:[a-zA-Z]*))', pkgs_weight.replace("24 HOUR EMERGENCY CONTACT:+8610863",""))
            
            if not matches:
                pkgs_weight = self.extract_text_from_coordinates(page_number, self.coordinates3[10])
                # matches = re.findall(r'(\d[\d,.]*[a-zA-Z]*)\s*[\s\S]*?(\d+)', pkgs_weight)
                matches = re.findall(r'(\d[\d,.]*\s*[a-zA-Z]*)[\s\S]*?Weight[\s\S]*?(\d+)', pkgs_weight)
            try:
                if len(matches) == 2:
                    pkgs, gross_weight = matches[1]
                    if '.' not in gross_weight:
                        if ',' not in gross_weight:
                            if not gross_weight.isdigit():
                                pkgs, gross_weight = matches[0]
                            
                elif len(matches) == 3:
                    pkgs, gross_weight = matches[2]
                    if '.' not in gross_weight:
                        if ',' not in gross_weight:
                            if not gross_weight.isdigit():
                                pkgs, gross_weight = matches[0]
                else:
                    pkgs, gross_weight = matches[0]
                pkgs = re.sub(r'[a-zA-Z]', '', pkgs)
                if not pkgs.isdigit():
                    pkgs, gross_weight = gross_weight, pkgs
                gross_weight = re.sub(r'[a-zA-Z]', '', gross_weight)
                    # if ',' in gross_weight:
                    #     gross_weight = gross_weight.replace('.','')
                    
                data['pkgs'] = pkgs
                if ',' in gross_weight and '.' in gross_weight:
                    if gross_weight.index(',') < gross_weight.index('.'):
                        # 1,544.00
                        gross_weight = gross_weight.replace(',', '')
                    elif gross_weight.index(',') > gross_weight.index('.'):
                        # 2.55,00
                        gross_weight = gross_weight.replace('.', '')
                        gross_weight = gross_weight.replace(',', '.') 
                elif ',' in gross_weight and '.' not in gross_weight:
                    gross_weight = gross_weight.replace(',','.')

                gross_weight = re.sub(r'[a-zA-Z]', '', gross_weight)
                data['gross_weight'] = gross_weight.replace(" ", '')
            except Exception:
                pass
            # ? ------------------------- PKGS and Gross Weight End -------------------------
            
            # Description
            description = self.extract_text_from_coordinates(page_number, self.coordinates[3])
            data['description'] = self.find_description(description)
            if data['description'] == None:
                data['description'] = self.find_description_2(description)
            data['pdf_path'] = pdf_path            
            
        except Exception as e:
            print(e)
        return data

# password_pdf/603-51132152_001.pdf 
# password_pdf/603-51132152_2_20240906.pdf 
# password_pdf/VHF20742108.pdf


# Shipper’s Name and Address
# Shipper’s Account Number
# PIF GLOBAL LOGISTICS[CHINA]LTD.SHANGHAIBRA
# ROOM 307-309, NO. 1438 NORTH SHANXI ROAD, 
# PUTUO DISTRICT, SHANGHAI
# USCI+91310109323170469D
# 160  
# PVG 85975315


# 3214

if __name__ == '__main__':
    pdf_path = r'MAWB_HAWB\MAWB\160-85975315MAWB.pdf'
    data = NormalPDFParser(pdf_path)
    data = data.get_pdf_data(pdf_path)
    print(data)