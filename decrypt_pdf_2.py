import PyPDF2

def remove_pdf_encryption(input_pdf_path, output_pdf_path, password):

    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)

        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PyPDF2.PdfWriter()
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"Decrypted PDF saved as '{output_pdf_path}'.")

input_pdf = r'password_pdf/603-51132152_2_20240906.pdf'
output_pdf = '603-51132152_2_20240906_decrypted.pdf'
password = '603-51132152'

# Remove encryption and save the decrypted PDF
remove_pdf_encryption(input_pdf, output_pdf, password)
