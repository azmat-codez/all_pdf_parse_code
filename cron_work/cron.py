from apps.models import MailData, MailDataAttachment
from apps.pdf_parse_script import pdf_process_zip_file

def get_file():
    all_data = MailData.objects.all()
    for data in all_data:
        if data.remark is None and data.processed is False:
            mail_data_attachments = MailDataAttachment.objects.filter(mail_data=data)
            
            if '59327f60-0e1e-4315-936e-bb0b5a120fe5' in str(data.uid):
            
                if len(mail_data_attachments) > 1:
                    mawb_file_paths = []
                    hawb_file_paths = []
                    for dt in mail_data_attachments:
                        if dt.attachment.name.lower().endswith('.pdf'):
                            file_name = dt.attachment.name.upper()
                            hawb_list=["HAWB","HOUSE"]
                            mawb_list=["MAWB", "MASTER"]
                            if any(hawb in file_name for hawb in hawb_list):
                                path = [dt.attachment.path, dt.attachment.path]
                                hawb_file_paths.append(path)
                            elif any(mawb in file_name for mawb in mawb_list):
                                path = [dt.attachment.path, dt.attachment.path]
                                mawb_file_paths.append(path)
                            else:
                                pass
                        try:
                            result_json = pdf_process_zip_file(mawb_file_paths, hawb_file_paths, None)
                            print(f"data : {result_json}")
                        except Exception as e:
                                print(f"An error occurred: {e}")

get_file()

            # if len(mailDdata_attachment) == 1:
            #     for dt in mailDdata_attachment:
            #         if dt.attachment.name.endswith('.pdf') or dt.attachment.name.endswith('.PDF'):
            #             file = dt.attachment
            #             manifest_file_paths = [
            #                 [f'media_cargo/{file}', f'media_cargo/{file}']
            #             ]
            #             mawb_file_paths = hawb_file_paths = None
            #             try:
            #                 result_json = pdf_process_zip_file(mawb_file_paths, hawb_file_paths, manifest_file_paths)
            #                 print(f"data : {result_json}")
            #             except Exception as e:
            #                 print(f"An error occurred: {e}")



from apps.models import MailData, MailDataAttachment
from apps.pdf_parse_script import pdf_process_zip_file

def get_file():
    all_data = MailData.objects.all()
    for data in all_data:
        if data.remark is None and data.processed is False:
            mail_data_attachments = MailDataAttachment.objects.filter(mail_data=data)
            
            if len(mail_data_attachments) > 1:
                mawb_file_paths = []
                hawb_file_paths = []
                
                for dt in mail_data_attachments:
                    if dt.attachment.name.lower().endswith('.pdf'):
                        file_name = dt.attachment.name.upper()
                        if 'HAWB' in file_name:
                            hawb_file_paths.append(dt.attachment.path)
                        elif 'MAWB' in file_name:
                            mawb_file_paths.append(dt.attachment.path)
                
                print('MAWB FILE:- ', mawb_file_paths)
                print('HAWB FILE:- ', hawb_file_paths)

get_file()
