import tkinter as tk
from tkinter import filedialog, Canvas, Scrollbar
from PIL import Image, ImageTk

class ImageCoordinateExtractor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Coordinate Extractor")
        
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        self.canvas = Canvas(self.frame, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.scroll_x = Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.scroll_y = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.tk_img = ImageTk.PhotoImage(self.image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
            
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_click(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_release(self, event):
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        print(f"Coordinates: ({x0}, {y0}, {x1}, {y1})")

if __name__ == "__main__":
    root = tk.Tk() 
    app = ImageCoordinateExtractor(root)
    root.mainloop()
