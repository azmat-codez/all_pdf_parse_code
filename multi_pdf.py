import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_into_single_pages(pdf_path):

    temp_dir = tempfile.TemporaryDirectory()
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    single_page_pdfs = []

    for i in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        single_pdf_path = os.path.join(temp_dir.name, f"page_{i+1}.pdf")

        with open(single_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        single_page_pdfs.append(single_pdf_path)
    
    return single_page_pdfs


# C:\Users\A100156\AppData\Local\Temp\tmp36kj8zvx

pdf_path = r"FULL PDF\020-0193 8370.pdf"
single_page_pdfs = split_pdf_into_single_pages(pdf_path)
print(single_page_pdfs)

# for pdf in single_page_pdfs:
#     print(pdf)

















Full Stack Developer | Python | Django | Flask | Pandas


1. Full Stack Developer 🧑‍💻 | Python/Django/Flask 💻 | Data Analysis with Pandas 🌟 | Passionate about Building Innovative Web Solutions 🚀
2. Seeking Opportunities to Blend Creativity and Data in Full Stack Development | Let's Build Something Awesome Together! 💻🌟


"""
how to get reach and follower on linkdin
how to do linkden marketing
how to post diffrent type of post on linkden
how to write Attractive post on linkden
how to customize linkden profile for software engineer

"""

i am full stack developer with experties in python, django, flask, pandas


Experienced Full Stack Developer | Expertise in Python, Django, Flask & Pandas | Passionate about Creating Efficient Solutions

1. Full Stack Developer | Python, Django, Flask Expert | Specializing in Data Analysis with Pandas | Passionate about Creating Efficient Solutions 🐍💻
2. Innovative Full Stack Developer | Python, Django, Flask | Data Analysis Pro with Pandas | Ready to Elevate Your Tech Team to New Heights 🚀