# launcher.py
"""GUI to launch interactive Python environments"""

# -----------------------------------------------------------------------
# external dependencies
# -----------------------------------------------------------------------
# (none)
# -----------------------------------------------------------------------

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as Filedialog
import tkinter.messagebox as Messagebox
import tkinter.simpledialog as Simpledialog
import csv, os, shutil, subprocess
from pathlib import Path

ROOT_FLD = Path("D:\\Python")

class MyTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENV_LIST = sorted((ROOT_FLD / "Venv").iterdir())
        self.APP_LIST = {"Python": "PYTHON.EXE", 
                         "Jupyter": "JUPYTER-LAB.EXE",
                         "Marimo": "MARIMO.EXE",
                         "IDLE": "IDLE.EXE"}
        self.FLD_LIST = get_favorites(ROOT_FLD / "Scripts/notebook_favs.csv")

        self.setup_window()
        self.add_widgets()
        self.populate_widgets()

    def setup_window(self):
        self.title("Python Interactive Starter")
        self.geometry("600x400")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def add_widgets(self):
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(row=99, columnspan=3, sticky="ESW", padx=5, pady=5)

        # add labels and lists
        self.lbl_env = ttk.Label(self, text="Environment")
        self.lbl_env.grid(row=1, column=1, padx=2, sticky="w")
        self.lst_env = ttk.Treeview(self, show="tree")
        self.lst_env.grid(row=2, column=1, padx=2, sticky="new")

        self.lbl_fld = ttk.Label(self, text="Directory")
        self.lbl_fld.grid(row=1, column=2, padx=2, sticky="w")
        self.lst_fld = ttk.Treeview(self, show="tree")
        self.lst_fld.grid(row=2, column=2, padx=2, sticky="new")

        self.lbl_app = ttk.Label(self, text="Application")
        self.lbl_app.grid(row=1, column=3, padx=2, sticky="w")
        self.lst_app = ttk.Treeview(self, show="tree")
        self.lst_app.grid(row=2, column=3, padx=2, sticky="new")

        # add the ok and cancel buttons
        self.btn_cancel = ttk.Button(self.btn_frame, text="Cancel")
        self.btn_cancel.pack(side=tk.RIGHT)
        self.btn_ok = ttk.Button(self.btn_frame, text="OK")
        self.btn_ok.pack(side=tk.RIGHT)

    def populate_widgets(self):
        for env in self.ENV_LIST:
            self.lst_env.insert("", tk.END, text=env.name)
        for fld in self.FLD_LIST:
            self.lst_fld.insert("", tk.END, text=fld)
        for app in self.APP_LIST:
            self.lst_app.insert("", tk.END, text=app)

def main():
    app = MyTk()
    app.mainloop()

def get_favorites(filename="notebook_favs.csv"):
    with open(filename, 'r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        favs = {data["title"]:data for data in reader}
    for data in favs.values():
        data["usage"] = int(data["usage"])
    # sort the favorites
    titles = list(favs.keys())
    titles.sort(reverse=True, key=lambda title: favs[title]["usage"])
    return favs    


if __name__ == "__main__":
    main()
    # print(get_favorites())