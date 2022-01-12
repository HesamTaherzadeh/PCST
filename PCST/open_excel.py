from tkinter.ttk import Treeview
from tkinter import filedialog
from tkinter.ttk import Treeview
import pandas as pd
from tkinter import *
import numpy as np


class Open():
    def __init__(self, root):
        self.root = root
        self.filename = None

    def extract(self):
        self._open_file()
        return self.df

    def _open_file(self):
        filename = filedialog.askopenfilename(title="Open a File", filetype=(("xlxs files", ".*xlsx"),
        ("All Files", "*.")))
        a = Toplevel(self.root)
        new = Frame(a)
        new.pack()
        self.tree1 = Treeview(new)
        if filename:
          try:
             self.filename = r"{}".format(filename)
             self.df = pd.read_excel(self.filename)
          except ValueError:
             error1 = Label("File could not be opened")
             error1.pack()
          except FileNotFoundError:
             error2 = Label("File Not Found")
             error2.pack()

        # Clear all the previous data in tree
        self.clear_treeview()

        # Add new data in Treeview widget
        self.tree1["column"] = list(self.df.columns)
        self.tree1["show"] = "headings"

        # For Headings iterate over the columns
        for col in self.tree1["column"]:
          self.tree1.heading(col, text=col)

        # Put Data in Rows
        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
          self.tree1.insert("", "end", values=row)
        self.tree1.pack()
        btn = Button(a,text="proceed", padx=22, bg="powder blue", command=a.destroy)
        btn.pack(side = RIGHT)
        btn2 = Button(a,text="Choose again", padx=22, bg="powder blue", command=lambda :Open(self.root))
        btn2.pack(side = LEFT)


    def clear_treeview(self):
        self.tree1.delete(*self.tree1.get_children())