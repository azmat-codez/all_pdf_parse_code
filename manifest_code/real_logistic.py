import re
import PyPDF2
import fitz
import pdfplumber
import json

class  RealogisticsManifest:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_document = fitz.open(pdf_path)
        self.text = self.extract_text_from_pdf()
    
    def extract_text_from_pdf(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text.strip()
    
    def extract_text_from_coordinate_pdf(self, coordinates):
        all_text = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    cropped_page = page.within_bbox(coordinates)
                    extracted_text = cropped_page.extract_text()
                    if extracted_text:
                        all_text.append(extracted_text)
        except Exception as e:
            return f"Error: {str(e)}"
        return "\n".join(all_text)
    
    # Todo ----------- MAWB CODE START -----------
    def get_mawb_no(self):
        text_list = [text for text in self.text.split('\n') if text.strip()]
        for i, line in enumerate(text_list):
            if 'MASTER AWB NO.' in line:
                next_line = text_list[i+2].strip().replace(' ', '')
                return next_line
        return None

    def get_origin(self):
        text_list = [text for text in self.text.split('\n') if text.strip()]
        for i, line in enumerate(text_list):
            if 'PORT OF DEPARTURE' in line:
                next_line = text_list[i+1].replace('TG', '').strip()
                return next_line
        return None
    
    def get_destination(self):
        text_list = [text for text in self.text.split('\n') if text.strip()]
        for i, line in enumerate(text_list):
            if 'Port of Discharge' in line:
                next_line = text_list[i+1].strip()
                next_line = next_line.split(' ')
                return next_line[0]
        return None
    
    def get_pkgs_weight(self):
        text_list = [text for text in self.text.split('\n') if text.strip()]
        for i, line in enumerate(text_list):
            if 'END OF REPORT' in line:
                pkgs = text_list[i+1].strip()
                pkgs = pkgs.split(' ')
                pkgs = pkgs[-1]
                weight = line.strip().split(' ')
                weight = weight[-1][1:]
                return pkgs, weight
        return None, None
    # Todo ----------- MAWB CODE END -----------
    
    def get_hawb_data(self):
        text = self.extract_text_from_coordinate_pdf((0.0, 200.0, 440.0, 460.0))
        text = text.replace('WEIGHT(KGS)', '')
        text_list = [text for text in text.split('\n') if text.strip()]
        hawb_data = {}
        hawb_all_data = []
        for i, line in enumerate(text_list):
            if 'HAWB NO.' in line:
                next_line = text_list[i+1].strip().split(' ')
                if len(next_line) >= 3:
                    hawb_data = {
                        'hawb_number': next_line[0],
                        'origin': self.get_origin(),
                        'destination': next_line[-1],
                        'pkgs': next_line[1],
                        'gross_weight': next_line[2],
                        'description': ' '.join(next_line[3:-1]),
                    }
                    hawb_all_data.append(hawb_data)
                    
                next_line = text_list[i+2].strip().split(' ')
                if len(next_line) > 4:
                    hawb_data = {
                        'hawb_number': next_line[0],
                        'origin': self.get_origin(),
                        'destination': next_line[-1],
                        'pkgs': next_line[1],
                        'gross_weight': next_line[2],
                        'description': ' '.join(next_line[3:-1]),
                    }
                    hawb_all_data.append(hawb_data)
        return hawb_all_data

    def get_data(self):
        # ! Mawb Data
        mawb_data = {}
        mawb_data = {}
        mawb_data['mawb_number'] = self.get_mawb_no()
        mawb_data['origin'] = self.get_origin()
        mawb_data['destination'] = self.get_destination()
        mawb_data['pkgs'], mawb_data['gross_weight'] = self.get_pkgs_weight()
        
        hawb_all_data = self.get_hawb_data()
        return mawb_data, hawb_all_data
        
        
        
        
        
        
        
if __name__ == "__main__":
    pdf_path = r"MANIFEST PDF\AIRFREIGHT MANIFEST.pdf"
    # pdf_path = r"AIRFREIGHT MANIFEST.pdf"
    pdf_class = RealogisticsManifest(pdf_path)
    mawb_data, hawb_all_data = pdf_class.get_data()
    data = f"mawb_data : {mawb_data}, hawb_data : {hawb_all_data}"
    print(data)
    
    # with open("json_data.json", "w") as file:
    #     json.dump(data, file, indent=4)
    # print("JSON data has been written to json_data.json")