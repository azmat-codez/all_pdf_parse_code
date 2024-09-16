import pandas as pd
import re
import PyPDF2
import fitz
import pdfplumber
import json




# ! FLYJAC LOGISTICS PVT LTD
class  FlyjacLogisticsManifest:
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
    
    def get_origin_destination(self):
        text_list = [text for text in self.text.split('\n') if text.strip()]
        for i, line in enumerate(text_list):
            destination = text_list[i+1].split(',')[0]
            origin = text_list[i+2].split(',')[-1]
            return origin, destination
        return None
    
    def get_data(self):
        # ! Mawb Data
        mawb_data = {}
        hawb_data = {}
        hawb_all_data = []
        
        origin, destination = self.get_origin_destination()
        description = self.extract_text_from_coordinate_pdf((656.0, 192.0, 815.0, 555.0)).split('\n')[0]
        
        texts = self.extract_text_from_coordinate_pdf((0.0, 185.0, 282.0, 557.0))
        text_list = [text for text in texts.split('\n') if text.strip()]
        next_line = text_list[0].split(' ')
        
        # ! MAWB DATA
        mawb_data['mawb_number'] = next_line[1].replace('-','')
        mawb_data['origin'] = origin
        mawb_data['destination'] = destination
        mawb_data['pkgs'] = next_line[2].replace('CTN', '')
        mawb_data['gross_weight'] = next_line[3]
        mawb_data['description'] = description
        
        # ! HAWB DATA
        next_line = text_list[1].split(' ')
        hawb_data['hawb_number'] = next_line[1].replace('-','')
        hawb_data['origin'] = origin
        hawb_data['destination'] = destination
        hawb_data['pkgs'] = next_line[2].replace('CTN', '')
        hawb_data['gross_weight'] = next_line[3]
        hawb_data['description'] = description
        hawb_all_data.append(hawb_data)
        
        return mawb_data, hawb_all_data
        


if __name__ == "__main__":
    pdf_path = r"MANIFEST PDF\160-77783565MNFT.pdf"
    pdf_class = FlyjacLogisticsManifest(pdf_path)
    mawb_data, hawb_all_data = pdf_class.get_data()
    data = f"mawb_data : {mawb_data}, hawb_data : {hawb_all_data}"
    
    print(data)
    
    with open("json_data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("JSON data has been written to json_data.json")
