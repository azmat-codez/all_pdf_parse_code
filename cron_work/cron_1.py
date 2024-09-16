from apps.models import MailData, MailDataAttachment
from apps.pdf_parse_script import pdf_process_zip_file
import json

def get_file():
    all_data = MailData.objects.all()
    for data in all_data:
        if data.remark is None and data.processed is False:
            mailDdata_attachment = MailDataAttachment.objects.filter(mail_data = data)
            
            if len(mailDdata_attachment) == 1:
                for dt in mailDdata_attachment:
                    if dt.attachment.name.endswith('.pdf') or dt.attachment.name.endswith('.PDF'):

                        path = dt.attachment
                        
                        manifest_file_paths = [
                            [f'media_cargo/{path}', f'media_cargo/{path}']
                        ]
                        
                        mawb_file_paths = hawb_file_paths = None
                        try:
                            result_json = pdf_process_zip_file(mawb_file_paths, hawb_file_paths, manifest_file_paths)
                            print(f"data : {result_json}")
                        except Exception as e:
                            print(f"An error occurred: {e}")

get_file()





# --------------------------------------------------------------------------


import os

def print_file_paths(root_folder):
    
    mawb_file_paths = []
    hawb_file_paths = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file = file.upper()
            if 'HAWB' in file:
                file = [file, file]
                hawb_file_paths.append(file)
            elif 'MAWB' in file:
                file = [file, file]
                mawb_file_paths.append(file)
        print(hawb_file_paths)
        print(mawb_file_paths)

root_folder = r'AIR PDF\098-00297975'
print_file_paths(root_folder)

