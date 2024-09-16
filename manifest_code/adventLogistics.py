import pandas as pd
import pdfplumber


def extract_tables_05(pdf_path):
    mawb_data = {}
    hawb_all_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if tables:
                    for table_number, table in enumerate(tables, start=1):
                        df = pd.DataFrame(table[1:], columns=table[0])
                        if table_number == 2:
                            for _, row in df.iterrows():
                                data = {
                                    "mawb_number": (row.iloc[0]).replace('-', ''),
                                    "origin":  row.iloc[2],
                                    "destination": row.iloc[3],
                                    "pkgs": row.iloc[4],
                                    "gross_weight": row.iloc[5],
                                    "description": row.iloc[6],
                                    # "pdf_path" : pdf_path
                                }
                                mawb_data = data
                        elif table_number == 3:
                            for _, row in df.iterrows():
                                if not row.iloc[0] or row.iloc[0] == 'TOTAL':
                                    continue
                                else:
                                    data = {
                                        "hawb_number": (row.iloc[0]).replace('-', ''),
                                        "origin":  row.iloc[2],
                                        "destination": row.iloc[3],
                                        "pkgs": row.iloc[4],
                                        "gross_weight": row.iloc[5],
                                        "description": row.iloc[6]
                                    }
                                    hawb_all_data.append(data)
                        else:
                            continue
                else:
                    print(f"No tables found on Page {page_number}")
                    
        return mawb_data, hawb_all_data
    except Exception as e:
        print('ERROR: ', e)


pdf_path = r'MANIFEST PDF\615-06385912_MNFT.pdf'
mawb_data, hawb_all_data = extract_tables_05(pdf_path)
print(mawb_data, hawb_all_data)