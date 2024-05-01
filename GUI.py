import tkinter as tk
from tkinter import ttk, PhotoImage

class CompressionInfoGUI(tk.Tk):
    def __init__(self, compression_info):
        super().__init__()
        self.compression_info = compression_info
        self.tree = None
        self.set_window_properties()
        self.set_background_image()
        self.create_treeview()
        self.insert_data_into_treeview()
        self.set_fonts()

    def set_window_properties(self):
        self.title("File Compression Info")
        self.geometry("1000x600")  # Adjust the values as needed

    def set_background_image(self):
        bg_image = PhotoImage(file=r"C:\Users\zohar\Downloads\My first design.png")
        bg_image = bg_image.subsample(3, 3)  # Adjust the factors as needed
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=100, relwidth=1, relheight=1)  # Adjust the y value as needed
        bg_label.image = bg_image  # Keep a reference to the image to prevent it from being garbage collected

    def create_treeview(self):
        self.tree = ttk.Treeview(self, columns=("Directory / File Name", "Runtime", "Compression Difference"))
        self.tree["show"] = "headings"
        self.tree.heading("#1", text="Directory / File Name")
        self.tree.heading("#2", text="Runtime (s)")
        self.tree.heading("#3", text="Compressed Size (bytes)")
        self.tree.column("#1", width=300)  # File Name
        self.tree.column("#2", width=300)  # Runtime
        self.tree.column("#3", width=300)  # Compressed Size
        for column in self.tree["columns"]:
            self.tree.column(column, anchor="center")  # Center text in rows
        self.tree.pack()

    def insert_data_into_treeview(self):
        for file_info in self.compression_info.files_compression_info:
            file_name, runtime, compressed_by = file_info
            self.tree.insert("", "end", values=(file_name, runtime, compressed_by))

    def set_fonts(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Sans-Serif", 16))
        style.configure("Treeview", font=("Sans-Serif", 13), tag=("data_row",))