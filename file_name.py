import pandas as pd

df = pd.read_csv('MailDataAttachment-2024-08-31.csv')

df_lists = df['attachment'].tolist()

for idx, df_list in enumerate(df_lists):
    # if idx == 100:
    #     break
    # else:
    df_list = df_list.split(r'/')[-1]
    if df_list.lower().endswith('.pdf'):
        print(df_list)
            
        
# for df_list in df_lists:
#     df_list = df_list.split(r'/')[-1]
#     if df_list.lower().endswith('.pdf'):
#         print(df_list)

