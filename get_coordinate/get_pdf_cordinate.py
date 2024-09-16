import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter import Canvas

class PDFCoordinateExtractor:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Coordinate Extractor")
        self.canvas = Canvas(master, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.pdf_path = filedialog.askopenfilename(filetypes=[("Example.pdf", "*.pdf")])
        self.pdf_document = fitz.open(self.pdf_path)
        self.page = self.pdf_document.load_page(0)  # Load the first page

        self.tk_img = tk.PhotoImage(data=self.page.get_pixmap().tobytes("ppm"))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_release(self, event):
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        print(f"Coordinates: ({x0}, {y0}, {x1}, {y1})")

if __name__ == "__main__":
    root = tk.Tk() 
    app = PDFCoordinateExtractor(root)
    root.mainloop()
