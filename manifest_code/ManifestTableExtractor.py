import pandas as pd
import re
import PyPDF2
import pdfplumber

# ! Class of Manifest table extract
class  ManifestTableExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
    
    def extract_text_from_pdf(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def get_origin(self):
        text = self.extract_text_from_pdf()
        patterns = [
            r"PORT OF LOADING：\s*(\w+)",
            r"PORT OF DEPARTURE:\s*(\w+)",
            r"DESTNATION :\s*(\w+)",
            r"PORT OF DEPARTURE:\s*(\w+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def get_dest(self):
        text = self.extract_text_from_pdf()
        patterns = [
            r"DEST:\s*(\w+)",
            r"ORIGIN :\s*(\w+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def get_mawb_no(self):
        text = self.extract_text_from_pdf()
        text = text.replace('-','')
        patterns = [
            r"MAWB:\s*(\w+)",
            r"MAWB No.:\s*(\w+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    def clean_description(self, text):
        if text is not None:
            text = text.replace('\n', ' ')
        return text
    
    def filter_digits(self,input_str):
        filtered = ''.join(re.findall(r'\d+', input_str))
        return filtered if filtered else '0'

    def filter_digits_commas_dots(self,input_str):
        filtered = ''.join(re.findall(r'[\d,\.]+', input_str))
        return filtered if re.match(r'^\d+([.,]\d+)*$', filtered) else '0.0'
    
    def extract_tables_01(self,pdf_path):
        mawb_data = {}
        hawb_all_data = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    header_row = pd.DataFrame([table[0]], columns=df.columns)
                    df = pd.concat([header_row, df], ignore_index=True)
                    df = df[df.iloc[:, 0].str.contains('MB|HB', na=False)]
                    filtered_df = df.iloc[:, :8]
                    for _, row in filtered_df.iterrows():
                        mawb_hawb = row.iloc[1].replace('-', '').replace(' ', '')
                        origin = self.get_origin()
                        if mawb_hawb.isdigit() and len(mawb_hawb) == 11:
                            data = {
                                "mawb_number": mawb_hawb,
                                "origin": origin,
                                "destination": row.iloc[7],
                                "pkgs": row.iloc[2],
                                "gross_weight": row.iloc[3],
                                "description": self.clean_description(row.iloc[6]),
                                "pdf_path" : pdf_path
                            }
                            mawb_data = data
                        else:
                            data = {
                                "hawb_number": mawb_hawb,
                                "origin": origin,
                                "destination": row.iloc[7],
                                "pkgs": row.iloc[2],
                                "gross_weight": row.iloc[3],
                                "description": self.clean_description(row.iloc[6])
                            }
                            hawb_all_data.append(data)
        return mawb_data, hawb_all_data
    
    def extract_tables_02(self,pdf_path):
        mawb_data = {}
        hawb_all_data = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    filtered_df = df.iloc[:, :9]
                    for _, row in filtered_df.iterrows():
                        mawb_hawb = row.iloc[0].replace('-', '').replace(' ', '').replace('MAWBNO:', '').replace('\n','')
                        if mawb_hawb.isdigit() and len(mawb_hawb) == 11:
                            data = {
                                "mawb_number": mawb_hawb,
                                "origin":  row.iloc[4],
                                "destination": row.iloc[5],
                                "pkgs": self.filter_digits(row.iloc[2]),
                                "gross_weight": self.filter_digits_commas_dots(row.iloc[3]),
                                "description": self.clean_description(row.iloc[8]),
                                "pdf_path" : pdf_path
                            }
                            mawb_data = data
                        elif mawb_hawb.isalnum():
                            data = {
                                "hawb_number": mawb_hawb,
                                "origin":  row.iloc[4],
                                "destination": row.iloc[5],
                                "pkgs": self.filter_digits(row.iloc[2]),
                                "gross_weight": self.filter_digits_commas_dots(row.iloc[3]),
                                "description": self.clean_description(row.iloc[8])
                            }
                            hawb_all_data.append(data)
                        else:
                            continue
        return mawb_data, hawb_all_data
    
    def extract_tables_03(self,pdf_path):
        mawb_data = {}
        hawb_all_data = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    filtered_df = df.iloc[:, :7]
                    for _, row in filtered_df.iterrows():
                        mawb_hawb = row.iloc[0].replace('-', '').replace(' ', '')
                        mawb_number = self.get_mawb_no()
                        text = self.extract_text_from_pdf()
                        if 'AIR CARGO MANIFEST' in text:
                            if mawb_hawb.isalnum():
                                data = {
                                    "mawb_number": mawb_number,
                                    "origin":  self.get_origin(),
                                    "destination": self.get_dest(),
                                    "pkgs": row.iloc[1],
                                    "gross_weight": row.iloc[3].replace('KGS', ''),
                                    "description": self.clean_description(row.iloc[2]),
                                    "pdf_path" : pdf_path
                                }
                                mawb_data = data
                            if mawb_hawb.isalnum():
                                data = {
                                    "hawb_number": mawb_hawb,
                                    "origin":  self.get_origin(),
                                    "destination": self.get_dest(),
                                    "pkgs": row.iloc[1],
                                    "gross_weight": row.iloc[3].replace('KGS', ''),
                                    "description": self.clean_description(row.iloc[2])
                                }
                                hawb_all_data.append(data)
                        else:
                            if mawb_hawb.isalnum():
                                data = {
                                    "mawb_number": mawb_number,
                                    "origin":  '',
                                    "destination": row.iloc[3],
                                    "pkgs": row.iloc[1],
                                    "gross_weight": row.iloc[2],
                                    "description": self.clean_description(row.iloc[6]),
                                    "pdf_path" : pdf_path
                                }
                                mawb_data = data
                            elif mawb_hawb.isalnum():
                                data = {
                                    "hawb_number": mawb_hawb,
                                    "origin":  '',
                                    "destination": row.iloc[3],
                                    "pkgs": row.iloc[1],
                                    "gross_weight": row.iloc[2],
                                    "description": self.clean_description(row.iloc[6])
                                }
                                hawb_all_data.append(data)
                            
        return mawb_data, hawb_all_data
    
    def extract_tables_04(self,pdf_path):
        mawb_data = {}
        hawb_all_data = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        filtered_df = df.iloc[:, :-1]
                        for _, row in filtered_df.iterrows():
                            
                            if row.iloc[0] is None or row.iloc[1] is None or row.iloc[2] is None or row.iloc[5] is None:
                                continue
                            mawb_hawb = row.iloc[0].replace('-', '').replace(' ', '')
                            
                            if mawb_hawb.isdigit() and len(mawb_hawb) == 11:
                                pkgs = row.iloc[1].split('\n')
                                gross_weight = row.iloc[2].split('\n')
                                origin = self.get_origin()
                                destination = self.get_dest()
                                mawb_data = {
                                    "mawb_number": mawb_hawb,
                                    "origin": origin,
                                    "destination": destination,
                                    "pkgs": pkgs[0],
                                    "gross_weight": gross_weight[0],
                                    "description": self.clean_description(row.iloc[5]),
                                    "pdf_path" : pdf_path
                                }
                                
                            if mawb_hawb.isalnum():
                                data = {
                                    "hawb_number": mawb_hawb,
                                    "origin":  origin,
                                    "destination": destination,
                                    "pkgs": pkgs[1],
                                    "gross_weight": gross_weight[1],
                                    "description": self.clean_description(row.iloc[5])
                                }
                                hawb_all_data.append(data)
        except IndexError as e:
            print('ERROR: ', e)
        return mawb_data, hawb_all_data

    # Todo ------------------------ PDF Parse Function End ------------------------
    # * ------------------------ CALL Parse Function Start ------------------------
    
    def get_pdf_data(self,pdf_path):

        try:
            print("Attempting extract_tables_01")
            try:
                mawb_data, hawb_all_data = self.extract_tables_01(pdf_path)
            except Exception as e:
                pass

            if not mawb_data and not hawb_all_data:
                print("Attempting extract_tables_02")
                try:
                    mawb_data, hawb_all_data = self.extract_tables_02(pdf_path)
                except Exception as e:
                    pass

            if not mawb_data and not hawb_all_data:
                print("Attempting extract_tables_03")
                try:
                    mawb_data, hawb_all_data = self.extract_tables_03(pdf_path)
                except Exception as e:
                    pass

            if not mawb_data and not hawb_all_data:
                print("Attempting extract_tables_04")
                mawb_data, hawb_all_data = self.extract_tables_04(pdf_path)

            return mawb_data, hawb_all_data
        except Exception as e:
            print('Unexpected ERROR: ', e)
            return None, None




if __name__ == '__main__':
    
    manifest_file_path = ['PDF FILES\TABLE MANIFEST PDF\921-46033201 MF (1).PDF']
    
    cargo_manifest_check = True
    table_pdf_format = ManifestTableExtractor(manifest_file_path[0])
    mawb_data,hawb_all_data = table_pdf_format.get_pdf_data(manifest_file_path[0])
    print(mawb_data,111)
    print(hawb_all_data,222)