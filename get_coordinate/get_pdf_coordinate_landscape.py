import tkinter as tk
from tkinter import filedialog
import pdfplumber

def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf_path.delete(0, tk.END)
        entry_pdf_path.insert(0, file_path)

def extract_text():
    pdf_path = entry_pdf_path.get()
    x1 = float(entry_x1.get())
    y1 = float(entry_y1.get())
    x2 = float(entry_x2.get())
    y2 = float(entry_y2.get())
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.crop((x1, y1, x2, y2)).extract_text()
            text_display.delete("1.0", tk.END)
            text_display.insert(tk.END, text)
    except Exception as e:
        text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, f"Error: {str(e)}")

# Initialize the Tkinter root window
root = tk.Tk()
root.title("PDF Coordinate Text Extractor")

# PDF File Selection
tk.Label(root, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=10)
entry_pdf_path = tk.Entry(root, width=50)
entry_pdf_path.grid(row=0, column=1, padx=10, pady=10)
btn_browse = tk.Button(root, text="Browse", command=select_pdf_file)
btn_browse.grid(row=0, column=2, padx=10, pady=10)

# Coordinate Inputs
tk.Label(root, text="X1:").grid(row=1, column=0, padx=10, pady=5)
entry_x1 = tk.Entry(root, width=10)
entry_x1.grid(row=1, column=1, padx=10, pady=5, sticky='W')

tk.Label(root, text="Y1:").grid(row=2, column=0, padx=10, pady=5)
entry_y1 = tk.Entry(root, width=10)
entry_y1.grid(row=2, column=1, padx=10, pady=5, sticky='W')

tk.Label(root, text="X2:").grid(row=3, column=0, padx=10, pady=5)
entry_x2 = tk.Entry(root, width=10)
entry_x2.grid(row=3, column=1, padx=10, pady=5, sticky='W')

tk.Label(root, text="Y2:").grid(row=4, column=0, padx=10, pady=5)
entry_y2 = tk.Entry(root, width=10)
entry_y2.grid(row=4, column=1, padx=10, pady=5, sticky='W')

# Extract Text Button
btn_extract = tk.Button(root, text="Extract Text", command=extract_text)
btn_extract.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Display Extracted Text
text_display = tk.Text(root, height=10, width=80)
text_display.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
