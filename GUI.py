import tkinter as tk
from tkinter import ttk, PhotoImage

class CompressionInfoGUI(tk.Tk):
    def __init__(self, compression_info):
        super().__init__()
        self.title("File Compression Info")


        # Set the default window size (width x height)
        self.geometry("1000x600")  # Adjust the values as needed

        # Load the image file
        bg_image = PhotoImage(file=r"C:\Users\zohar\Downloads\My first design.png")
        bg_image = bg_image.subsample(3, 3)  # Adjust the factors as needed

        # Create a label and set the image as the label's image
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=100, relwidth=1, relheight=1)  # Adjust the y
        # value as needed

        # Keep a reference to the image to prevent it from being garbage collected
        bg_label.image = bg_image

        # Keep a reference to the image to prevent it from being garbage collected
        bg_label.image = bg_image


        # Create a treeview widget with three additional columns
        self.tree = ttk.Treeview(self, columns=("Directory / File Name",
                                                "Runtime",
                                                "Compression Difference"))

        # Hide the identifier column (empty heading)
        self.tree["show"] = "headings"

        # Set column headings
        self.tree.heading("#1", text="Directory / File Name")
        self.tree.heading("#2", text="Runtime (s)")
        self.tree.heading("#3", text="Compressed Size (bytes)")

        # Set column widths (adjust as needed)
        self.tree.column("#1", width=300)  # File Name
        self.tree.column("#2", width=300)  # Runtime
        self.tree.column("#3", width=300)  # Compressed Size

        # Center the values in rows
        for column in self.tree["columns"]:
            self.tree.column(column, anchor="center")  # Center text in rows

        # Insert data into the treeview
        for file_info in compression_info.files_compression_info:
            file_name, runtime, compressed_by = file_info
            self.tree.insert("", "end", values=(file_name, runtime, compressed_by))

        # Set the font for column headings
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Sans-Serif", 16))

        # Set the font for data rows
        style.configure("Treeview", font=("Sans-Serif", 13), tag=("data_row",))

        # Pack the treeview
        self.tree.pack()

